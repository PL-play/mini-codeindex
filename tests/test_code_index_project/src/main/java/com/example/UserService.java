package com.example;

import java.util.*;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.locks.ReadWriteLock;
import java.util.concurrent.locks.ReentrantReadWriteLock;
import java.util.stream.Collectors;
import java.util.function.Predicate;
import java.util.function.Function;
import java.util.function.Consumer;
import java.time.LocalDateTime;
import java.time.temporal.ChronoUnit;

/**
 * 用户服务类，提供用户管理的功能
 * 支持并发操作、缓存、审计日志等高级功能
 */
public class UserService {
    private final Map<String, User> users;
    private final ReadWriteLock lock;
    private final Map<String, User> userCache;
    private final List<UserServiceListener> listeners;
    private final AuditLogger auditLogger;
    private final UserValidator validator;
    private final UserStatistics statistics;

    // 常量
    private static final int MAX_CACHE_SIZE = 1000;
    private static final long CACHE_EXPIRY_MINUTES = 30;

    // 枚举
    public enum OperationType {
        CREATE, READ, UPDATE, DELETE, SEARCH
    }

    // 内部类
    public static class UserStatistics {
        private int totalUsers;
        private int activeUsers;
        private Map<String, Integer> departmentCounts;
        private Map<String, Integer> skillCounts;
        private double averageAge;
        private LocalDateTime lastUpdated;

        public UserStatistics() {
            this.departmentCounts = new HashMap<>();
            this.skillCounts = new HashMap<>();
            this.lastUpdated = LocalDateTime.now();
        }

        public synchronized void update(List<User> users) {
            this.totalUsers = users.size();
            this.activeUsers = (int) users.stream()
                    .filter(user -> !user.getRoles().contains("inactive"))
                    .count();

            this.departmentCounts = users.stream()
                    .collect(Collectors.groupingBy(
                            User::getDepartment,
                            Collectors.summingInt(user -> 1)
                    ));

            this.skillCounts = users.stream()
                    .flatMap(user -> user.getSkills().stream())
                    .collect(Collectors.groupingBy(
                            skill -> skill,
                            Collectors.summingInt(skill -> 1)
                    ));

            this.averageAge = users.stream()
                    .mapToInt(User::getAge)
                    .average()
                    .orElse(0.0);

            this.lastUpdated = LocalDateTime.now();
        }

        // Getters
        public int getTotalUsers() { return totalUsers; }
        public int getActiveUsers() { return activeUsers; }
        public Map<String, Integer> getDepartmentCounts() { return new HashMap<>(departmentCounts); }
        public Map<String, Integer> getSkillCounts() { return new HashMap<>(skillCounts); }
        public double getAverageAge() { return averageAge; }
        public LocalDateTime getLastUpdated() { return lastUpdated; }
    }

    public static class AuditLogger {
        private final List<AuditEntry> auditLog;

        public AuditLogger() {
            this.auditLog = new ArrayList<>();
        }

        public void log(OperationType operation, String userId, String details) {
            AuditEntry entry = new AuditEntry(operation, userId, details, LocalDateTime.now());
            synchronized (auditLog) {
                auditLog.add(entry);
                // 保持日志大小
                if (auditLog.size() > 10000) {
                    auditLog.remove(0);
                }
            }
        }

        public List<AuditEntry> getRecentEntries(int limit) {
            synchronized (auditLog) {
                int size = auditLog.size();
                int start = Math.max(0, size - limit);
                return new ArrayList<>(auditLog.subList(start, size));
            }
        }

        public List<AuditEntry> getEntriesByUser(String userId) {
            synchronized (auditLog) {
                return auditLog.stream()
                        .filter(entry -> userId.equals(entry.getUserId()))
                        .collect(Collectors.toList());
            }
        }
    }

    public static class AuditEntry {
        private final OperationType operation;
        private final String userId;
        private final String details;
        private final LocalDateTime timestamp;

        public AuditEntry(OperationType operation, String userId, String details, LocalDateTime timestamp) {
            this.operation = operation;
            this.userId = userId;
            this.details = details;
            this.timestamp = timestamp;
        }

        // Getters
        public OperationType getOperation() { return operation; }
        public String getUserId() { return userId; }
        public String getDetails() { return details; }
        public LocalDateTime getTimestamp() { return timestamp; }
    }

    public interface UserServiceListener {
        void onUserCreated(User user);
        void onUserUpdated(User user);
        void onUserDeleted(String userId);
    }

    public static class UserValidator {
        public void validateUser(User user) throws User.ValidationException {
            if (user == null) {
                throw new User.ValidationException("User cannot be null");
            }
            user.validate();
        }

        public void validateUserId(String userId) throws User.ValidationException {
            if (userId == null || userId.trim().isEmpty()) {
                throw new User.ValidationException("User ID cannot be null or empty");
            }
        }
    }

    public static class ValidationException extends Exception {
        public ValidationException(String message) {
            super(message);
        }
    }

    // 构造函数
    public UserService() {
        this.users = new ConcurrentHashMap<>();
        this.lock = new ReentrantReadWriteLock();
        this.userCache = new ConcurrentHashMap<>();
        this.listeners = new ArrayList<>();
        this.auditLogger = new AuditLogger();
        this.validator = new UserValidator();
        this.statistics = new UserStatistics();
    }

    // 核心CRUD方法
    public User createUser(User user) throws User.ValidationException, DuplicateUserException {
        validator.validateUser(user);
        validator.validateUserId(user.getId());

        lock.writeLock().lock();
        try {
            if (users.containsKey(user.getId())) {
                throw new DuplicateUserException("User with ID " + user.getId() + " already exists");
            }

            users.put(user.getId(), user);
            userCache.put(user.getId(), user);
            updateStatistics();

            auditLogger.log(OperationType.CREATE, user.getId(), "User created");
            notifyListeners(user1 -> user1.onUserCreated(user));

            return user;
        } finally {
            lock.writeLock().unlock();
        }
    }

    public User getUserById(String userId) throws User.ValidationException, UserNotFoundException {
        validator.validateUserId(userId);

        // 先检查缓存
        User cachedUser = userCache.get(userId);
        if (cachedUser != null) {
            auditLogger.log(OperationType.READ, userId, "User retrieved from cache");
            return cachedUser;
        }

        lock.readLock().lock();
        try {
            User user = users.get(userId);
            if (user == null) {
                throw new UserNotFoundException("User with ID " + userId + " not found");
            }

            // 更新缓存
            userCache.put(userId, user);
            auditLogger.log(OperationType.READ, userId, "User retrieved from storage");

            return user;
        } finally {
            lock.readLock().unlock();
        }
    }

    public User updateUser(User updatedUser) throws User.ValidationException, UserNotFoundException {
        validator.validateUser(updatedUser);
        validator.validateUserId(updatedUser.getId());

        lock.writeLock().lock();
        try {
            User existingUser = users.get(updatedUser.getId());
            if (existingUser == null) {
                throw new UserNotFoundException("User with ID " + updatedUser.getId() + " not found");
            }

            users.put(updatedUser.getId(), updatedUser);
            userCache.put(updatedUser.getId(), updatedUser);
            updateStatistics();

            auditLogger.log(OperationType.UPDATE, updatedUser.getId(), "User updated");
            notifyListeners(user -> user.onUserUpdated(updatedUser));

            return updatedUser;
        } finally {
            lock.writeLock().unlock();
        }
    }

    public boolean deleteUser(String userId) throws User.ValidationException {
        validator.validateUserId(userId);

        lock.writeLock().lock();
        try {
            User removedUser = users.remove(userId);
            if (removedUser != null) {
                userCache.remove(userId);
                updateStatistics();

                auditLogger.log(OperationType.DELETE, userId, "User deleted");
                notifyListeners(user -> user.onUserDeleted(userId));

                return true;
            }
            return false;
        } finally {
            lock.writeLock().unlock();
        }
    }

    // 高级查询方法
    public List<User> findUsers(Predicate<User> predicate) {
        lock.readLock().lock();
        try {
            return users.values().stream()
                    .filter(predicate)
                    .collect(Collectors.toList());
        } finally {
            lock.readLock().unlock();
        }
    }

    public List<User> findUsersByDepartment(String department) {
        return findUsers(user -> department.equals(user.getDepartment()));
    }

    public List<User> findUsersBySkill(String skill) {
        return findUsers(user -> user.hasSkill(skill));
    }

    public List<User> findUsersByAgeRange(int minAge, int maxAge) {
        return findUsers(user -> user.getAge() >= minAge && user.getAge() <= maxAge);
    }

    public List<User> searchUsers(String query) {
        String lowerQuery = query.toLowerCase();
        return findUsers(user ->
            user.getName().toLowerCase().contains(lowerQuery) ||
            user.getEmail().toLowerCase().contains(lowerQuery) ||
            user.getSkills().stream().anyMatch(skill -> skill.toLowerCase().contains(lowerQuery))
        );
    }

    public Map<String, List<User>> groupUsersByDepartment() {
        lock.readLock().lock();
        try {
            return users.values().stream()
                    .collect(Collectors.groupingBy(User::getDepartment));
        } finally {
            lock.readLock().unlock();
        }
    }

    public Map<String, Long> getSkillDistribution() {
        lock.readLock().lock();
        try {
            return users.values().stream()
                    .flatMap(user -> user.getSkills().stream())
                    .collect(Collectors.groupingBy(
                            skill -> skill,
                            Collectors.counting()
                    ));
        } finally {
            lock.readLock().unlock();
        }
    }

    // 批量操作
    public List<User> createUsers(List<User> userList) throws User.ValidationException {
        List<User> createdUsers = new ArrayList<>();
        List<Exception> errors = new ArrayList<>();

        for (User user : userList) {
            try {
                createdUsers.add(createUser(user));
            } catch (Exception e) {
                errors.add(e);
            }
        }

        if (!errors.isEmpty()) {
            throw new User.ValidationException("Batch creation failed: " + errors.size() + " errors occurred");
        }

        return createdUsers;
    }

    public List<User> getAllUsers() {
        lock.readLock().lock();
        try {
            return new ArrayList<>(users.values());
        } finally {
            lock.readLock().unlock();
        }
    }

    public int getUserCount() {
        return users.size();
    }

    // 缓存管理
    public void clearCache() {
        userCache.clear();
    }

    public void evictCache(String userId) {
        userCache.remove(userId);
    }

    // 监听器管理
    public void addListener(UserServiceListener listener) {
        synchronized (listeners) {
            listeners.add(listener);
        }
    }

    public void removeListener(UserServiceListener listener) {
        synchronized (listeners) {
            listeners.remove(listener);
        }
    }

    private void notifyListeners(Consumer<UserServiceListener> action) {
        List<UserServiceListener> currentListeners;
        synchronized (listeners) {
            currentListeners = new ArrayList<>(listeners);
        }

        for (UserServiceListener listener : currentListeners) {
            try {
                action.accept(listener);
            } catch (Exception e) {
                // 记录错误但不中断
                System.err.println("Listener notification failed: " + e.getMessage());
            }
        }
    }

    // 统计更新
    private void updateStatistics() {
        statistics.update(getAllUsers());
    }

    // Getters
    public UserStatistics getStatistics() {
        return statistics;
    }

    public AuditLogger getAuditLogger() {
        return auditLogger;
    }

    // 异常类
    public static class DuplicateUserException extends Exception {
        public DuplicateUserException(String message) {
            super(message);
        }
    }

    public static class UserNotFoundException extends Exception {
        public UserNotFoundException(String message) {
            super(message);
        }
    }

    // 高级功能
    public List<User> getUsersWithComplexQuery(Map<String, Object> criteria) {
        Predicate<User> predicate = user -> {
            for (Map.Entry<String, Object> entry : criteria.entrySet()) {
                String key = entry.getKey();
                Object value = entry.getValue();

                switch (key) {
                    case "department":
                        if (!value.equals(user.getDepartment())) return false;
                        break;
                    case "minAge":
                        if (user.getAge() < (Integer) value) return false;
                        break;
                    case "maxAge":
                        if (user.getAge() > (Integer) value) return false;
                        break;
                    case "hasSkill":
                        if (!user.hasSkill((String) value)) return false;
                        break;
                    case "nameContains":
                        if (!user.getName().toLowerCase().contains(((String) value).toLowerCase())) return false;
                        break;
                }
            }
            return true;
        };

        return findUsers(predicate);
    }

    public void bulkUpdateSkills(String department, String oldSkill, String newSkill) {
        List<User> usersToUpdate = findUsersByDepartment(department);

        for (User user : usersToUpdate) {
            if (user.hasSkill(oldSkill)) {
                user.removeSkill(oldSkill);
                user.addSkill(newSkill);
                try {
                    updateUser(user);
                } catch (Exception e) {
                    System.err.println("Failed to update user " + user.getId() + ": " + e.getMessage());
                }
            }
        }
    }

    public Map<String, Object> generateReport() {
        Map<String, Object> report = new HashMap<>();
        report.put("totalUsers", getUserCount());
        report.put("statistics", statistics);
        report.put("departmentDistribution", groupUsersByDepartment());
        report.put("skillDistribution", getSkillDistribution());
        report.put("recentAuditEntries", auditLogger.getRecentEntries(10));
        report.put("generatedAt", LocalDateTime.now());

        return report;
    }

    // 主方法，用于测试
    public static void main(String[] args) {
        UserService service = new UserService();

        try {
            // 创建用户
            User user1 = new User.Builder()
                    .id("1")
                    .name("Alice Johnson")
                    .email("alice@example.com")
                    .age(28)
                    .department("engineering")
                    .skill("java")
                    .skill("python")
                    .build();

            User user2 = new User.Builder()
                    .id("2")
                    .name("Bob Smith")
                    .email("bob@example.com")
                    .age(35)
                    .department("marketing")
                    .skill("marketing")
                    .skill("analytics")
                    .build();

            // 添加用户
            service.createUser(user1);
            service.createUser(user2);

            // 查询用户
            User foundUser = service.getUserById("1");
            if (foundUser != null) {
                System.out.println("Found user: " + foundUser);
            }

            // 搜索用户
            List<User> engineers = service.findUsersByDepartment("engineering");
            System.out.println("Engineers: " + engineers);

            // 生成报告
            Map<String, Object> report = service.generateReport();
            System.out.println("Report: " + report);

        } catch (Exception e) {
            System.err.println("Error: " + e.getMessage());
        }
    }
}