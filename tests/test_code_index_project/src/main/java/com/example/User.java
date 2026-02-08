package com.example;

import java.util.*;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.regex.Pattern;
import java.util.regex.Matcher;
import java.util.stream.Collectors;

/**
 * 用户实体类
 * 包含用户的基本信息、技能、偏好设置等
 */
public class User {
    private String id;
    private String name;
    private String email;
    private int age;
    private String department;
    private List<String> skills;
    private Map<String, Object> metadata;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
    private UserPreferences preferences;
    private List<UserActivity> activities;
    private Set<String> roles;
    private Map<String, String> customFields;

    // 常量
    public static final int MIN_AGE = 0;
    public static final int MAX_AGE = 150;
    public static final Pattern EMAIL_PATTERN = Pattern.compile("^[A-Za-z0-9+_.-]+@[A-Za-z0-9.-]+$");

    // 枚举
    public enum UserStatus {
        ACTIVE, INACTIVE, SUSPENDED, DELETED
    }

    public enum Department {
        ENGINEERING, MARKETING, SALES, HR, FINANCE, OPERATIONS
    }

    // 内部类
    public static class UserPreferences {
        private boolean emailNotifications;
        private String theme;
        private String language;
        private Map<String, Object> settings;

        public UserPreferences() {
            this.emailNotifications = true;
            this.theme = "light";
            this.language = "en";
            this.settings = new HashMap<>();
        }

        // Getters and setters
        public boolean isEmailNotifications() { return emailNotifications; }
        public void setEmailNotifications(boolean emailNotifications) { this.emailNotifications = emailNotifications; }

        public String getTheme() { return theme; }
        public void setTheme(String theme) { this.theme = theme; }

        public String getLanguage() { return language; }
        public void setLanguage(String language) { this.language = language; }

        public Map<String, Object> getSettings() { return settings; }
        public void setSettings(Map<String, Object> settings) { this.settings = settings; }

        @Override
        public String toString() {
            return "UserPreferences{" +
                    "emailNotifications=" + emailNotifications +
                    ", theme='" + theme + '\'' +
                    ", language='" + language + '\'' +
                    ", settings=" + settings +
                    '}';
        }
    }

    public static class UserActivity {
        private String activityId;
        private String activityType;
        private LocalDateTime timestamp;
        private String description;
        private Map<String, Object> details;

        public UserActivity(String activityId, String activityType, String description) {
            this.activityId = activityId;
            this.activityType = activityType;
            this.timestamp = LocalDateTime.now();
            this.description = description;
            this.details = new HashMap<>();
        }

        // Getters and setters
        public String getActivityId() { return activityId; }
        public void setActivityId(String activityId) { this.activityId = activityId; }

        public String getActivityType() { return activityType; }
        public void setActivityType(String activityType) { this.activityType = activityType; }

        public LocalDateTime getTimestamp() { return timestamp; }
        public void setTimestamp(LocalDateTime timestamp) { this.timestamp = timestamp; }

        public String getDescription() { return description; }
        public void setDescription(String description) { this.description = description; }

        public Map<String, Object> getDetails() { return details; }
        public void setDetails(Map<String, Object> details) { this.details = details; }
    }

    // 构造函数
    public User() {
        this.skills = new ArrayList<>();
        this.metadata = new HashMap<>();
        this.createdAt = LocalDateTime.now();
        this.updatedAt = LocalDateTime.now();
        this.preferences = new UserPreferences();
        this.activities = new ArrayList<>();
        this.roles = new HashSet<>();
        this.customFields = new HashMap<>();
    }

    public User(String id, String name, String email) {
        this();
        this.id = id;
        this.name = name;
        this.email = email;
    }

    public User(String id, String name, String email, int age, String department) {
        this(id, name, email);
        this.age = age;
        this.department = department;
    }

    // 验证方法
    public boolean validate() throws ValidationException {
        List<String> errors = new ArrayList<>();

        if (id == null || id.trim().isEmpty()) {
            errors.add("ID cannot be null or empty");
        }

        if (name == null || name.trim().isEmpty()) {
            errors.add("Name cannot be null or empty");
        }

        if (email == null || !EMAIL_PATTERN.matcher(email).matches()) {
            errors.add("Invalid email format");
        }

        if (age < MIN_AGE || age > MAX_AGE) {
            errors.add("Age must be between " + MIN_AGE + " and " + MAX_AGE);
        }

        if (!errors.isEmpty()) {
            throw new ValidationException("Validation failed: " + String.join(", ", errors));
        }

        return true;
    }

    // 业务方法
    public void addSkill(String skill) {
        if (skill != null && !skill.trim().isEmpty() && !skills.contains(skill)) {
            skills.add(skill);
            updateTimestamp();
            logActivity("SKILL_ADDED", "Added skill: " + skill);
        }
    }

    public void removeSkill(String skill) {
        if (skills.remove(skill)) {
            updateTimestamp();
            logActivity("SKILL_REMOVED", "Removed skill: " + skill);
        }
    }

    public boolean hasSkill(String skill) {
        return skills.contains(skill);
    }

    public List<String> getSkillsByPrefix(String prefix) {
        return skills.stream()
                .filter(skill -> skill.toLowerCase().startsWith(prefix.toLowerCase()))
                .collect(Collectors.toList());
    }

    public void addRole(String role) {
        if (role != null && !role.trim().isEmpty()) {
            roles.add(role);
            updateTimestamp();
            logActivity("ROLE_ADDED", "Added role: " + role);
        }
    }

    public void removeRole(String role) {
        if (roles.remove(role)) {
            updateTimestamp();
            logActivity("ROLE_REMOVED", "Removed role: " + role);
        }
    }

    public boolean hasRole(String role) {
        return roles.contains(role);
    }

    public void setCustomField(String key, String value) {
        customFields.put(key, value);
        updateTimestamp();
    }

    public String getCustomField(String key) {
        return customFields.get(key);
    }

    public void logActivity(String activityType, String description) {
        UserActivity activity = new UserActivity(
                UUID.randomUUID().toString(),
                activityType,
                description
        );
        activities.add(activity);
    }

    public List<UserActivity> getRecentActivities(int limit) {
        return activities.stream()
                .sorted((a, b) -> b.getTimestamp().compareTo(a.getTimestamp()))
                .limit(limit)
                .collect(Collectors.toList());
    }

    public Map<String, Long> getActivitySummary() {
        return activities.stream()
                .collect(Collectors.groupingBy(
                        UserActivity::getActivityType,
                        Collectors.counting()
                ));
    }

    public void updateTimestamp() {
        this.updatedAt = LocalDateTime.now();
    }

    // 静态方法
    public static User createFromMap(Map<String, Object> data) throws ValidationException {
        User user = new User();
        user.setId((String) data.get("id"));
        user.setName((String) data.get("name"));
        user.setEmail((String) data.get("email"));
        user.setAge(data.get("age") != null ? (Integer) data.get("age") : 0);
        user.setDepartment((String) data.get("department"));

        @SuppressWarnings("unchecked")
        List<String> skills = (List<String>) data.get("skills");
        if (skills != null) {
            user.setSkills(new ArrayList<>(skills));
        }

        user.validate();
        return user;
    }

    public static List<User> filterByDepartment(List<User> users, String department) {
        return users.stream()
                .filter(user -> department.equals(user.getDepartment()))
                .collect(Collectors.toList());
    }

    public static List<User> filterBySkill(List<User> users, String skill) {
        return users.stream()
                .filter(user -> user.hasSkill(skill))
                .collect(Collectors.toList());
    }

    public static Map<String, List<User>> groupByDepartment(List<User> users) {
        return users.stream()
                .collect(Collectors.groupingBy(User::getDepartment));
    }

    public static double calculateAverageAge(List<User> users) {
        return users.stream()
                .mapToInt(User::getAge)
                .average()
                .orElse(0.0);
    }

    // Getters and setters
    public String getId() { return id; }
    public void setId(String id) { this.id = id; }

    public String getName() { return name; }
    public void setName(String name) { this.name = name; }

    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }

    public int getAge() { return age; }
    public void setAge(int age) { this.age = age; }

    public String getDepartment() { return department; }
    public void setDepartment(String department) { this.department = department; }

    public List<String> getSkills() { return new ArrayList<>(skills); }
    public void setSkills(List<String> skills) { this.skills = skills != null ? new ArrayList<>(skills) : new ArrayList<>(); }

    public Map<String, Object> getMetadata() { return new HashMap<>(metadata); }
    public void setMetadata(Map<String, Object> metadata) { this.metadata = metadata != null ? new HashMap<>(metadata) : new HashMap<>(); }

    public LocalDateTime getCreatedAt() { return createdAt; }
    public void setCreatedAt(LocalDateTime createdAt) { this.createdAt = createdAt; }

    public LocalDateTime getUpdatedAt() { return updatedAt; }
    public void setUpdatedAt(LocalDateTime updatedAt) { this.updatedAt = updatedAt; }

    public UserPreferences getPreferences() { return preferences; }
    public void setPreferences(UserPreferences preferences) { this.preferences = preferences; }

    public List<UserActivity> getActivities() { return new ArrayList<>(activities); }
    public void setActivities(List<UserActivity> activities) { this.activities = activities != null ? new ArrayList<>(activities) : new ArrayList<>(); }

    public Set<String> getRoles() { return new HashSet<>(roles); }
    public void setRoles(Set<String> roles) { this.roles = roles != null ? new HashSet<>(roles) : new HashSet<>(); }

    public Map<String, String> getCustomFields() { return new HashMap<>(customFields); }
    public void setCustomFields(Map<String, String> customFields) { this.customFields = customFields != null ? new HashMap<>(customFields) : new HashMap<>(); }

    @Override
    public String toString() {
        return "User{" +
                "id='" + id + '\'' +
                ", name='" + name + '\'' +
                ", email='" + email + '\'' +
                ", age=" + age +
                ", department='" + department + '\'' +
                ", skills=" + skills +
                ", roles=" + roles +
                ", createdAt=" + createdAt +
                ", updatedAt=" + updatedAt +
                '}';
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        User user = (User) o;
        return Objects.equals(id, user.id);
    }

    @Override
    public int hashCode() {
        return Objects.hash(id);
    }

    // 自定义异常
    public static class ValidationException extends Exception {
        public ValidationException(String message) {
            super(message);
        }
    }

    // Builder pattern
    public static class Builder {
        private String id;
        private String name;
        private String email;
        private int age;
        private String department;
        private List<String> skills = new ArrayList<>();
        private Map<String, Object> metadata = new HashMap<>();

        public Builder id(String id) {
            this.id = id;
            return this;
        }

        public Builder name(String name) {
            this.name = name;
            return this;
        }

        public Builder email(String email) {
            this.email = email;
            return this;
        }

        public Builder age(int age) {
            this.age = age;
            return this;
        }

        public Builder department(String department) {
            this.department = department;
            return this;
        }

        public Builder skill(String skill) {
            this.skills.add(skill);
            return this;
        }

        public Builder skills(List<String> skills) {
            this.skills.addAll(skills);
            return this;
        }

        public Builder metadata(String key, Object value) {
            this.metadata.put(key, value);
            return this;
        }

        public User build() throws ValidationException {
            User user = new User(id, name, email, age, department);
            user.setSkills(skills);
            user.setMetadata(metadata);
            user.validate();
            return user;
        }
    }
}