package com.example;

import java.util.*;
import java.util.function.*;
import java.util.concurrent.*;
import java.util.stream.*;
import java.io.*;
import java.time.*;
import java.time.temporal.*;
import java.math.*;
import java.math.RoundingMode;

/**
 * 观察者模式实现
 * 定义对象间的一种一对多的依赖关系，当一个对象的状态发生改变时，所有依赖于它的对象都得到通知并被自动更新
 */
public class ObserverManager {

    // 单例模式
    private static volatile ObserverManager instance;
    private static final Object LOCK = new Object();

    private final Map<String, Subject> subjects;
    private final Map<String, List<Observer>> observers;
    private final ExecutorService notificationExecutor;
    private final Map<String, NotificationStrategy> notificationStrategies;

    private ObserverManager() {
        this.subjects = new ConcurrentHashMap<>();
        this.observers = new ConcurrentHashMap<>();
        this.notificationExecutor = Executors.newCachedThreadPool();
        this.notificationStrategies = new ConcurrentHashMap<>();
        initializeDefaultSubjects();
        initializeNotificationStrategies();
    }

    public static ObserverManager getInstance() {
        if (instance == null) {
            synchronized (LOCK) {
                if (instance == null) {
                    instance = new ObserverManager();
                }
            }
        }
        return instance;
    }

    /**
     * 初始化默认主题
     */
    private void initializeDefaultSubjects() {
        // 用户相关主题
        createSubject("user_login");
        createSubject("user_logout");
        createSubject("user_registration");
        createSubject("user_profile_update");

        // 系统相关主题
        createSubject("system_startup");
        createSubject("system_shutdown");
        createSubject("system_error");
        createSubject("system_maintenance");

        // 数据相关主题
        createSubject("data_created");
        createSubject("data_updated");
        createSubject("data_deleted");
        createSubject("data_backup");

        // 业务相关主题
        createSubject("order_created");
        createSubject("order_cancelled");
        createSubject("payment_received");
        createSubject("inventory_low");

        // 监控相关主题
        createSubject("performance_alert");
        createSubject("security_alert");
        createSubject("health_check");
        createSubject("resource_usage");
    }

    /**
     * 初始化通知策略
     */
    private void initializeNotificationStrategies() {
        registerNotificationStrategy("immediate", new ImmediateNotificationStrategy());
        registerNotificationStrategy("async", new AsyncNotificationStrategy());
        registerNotificationStrategy("batched", new BatchedNotificationStrategy());
        registerNotificationStrategy("filtered", new FilteredNotificationStrategy());
        registerNotificationStrategy("prioritized", new PrioritizedNotificationStrategy());
    }

    /**
     * 创建主题
     */
    public Subject createSubject(String subjectName) {
        Subject subject = new ConcreteSubject(subjectName);
        subjects.put(subjectName, subject);
        observers.put(subjectName, new CopyOnWriteArrayList<>());
        return subject;
    }

    /**
     * 获取主题
     */
    public Subject getSubject(String subjectName) {
        return subjects.get(subjectName);
    }

    /**
     * 注册观察者
     */
    public void registerObserver(String subjectName, Observer observer) {
        List<Observer> subjectObservers = observers.get(subjectName);
        if (subjectObservers != null) {
            subjectObservers.add(observer);
        }
    }

    /**
     * 注销观察者
     */
    public void unregisterObserver(String subjectName, Observer observer) {
        List<Observer> subjectObservers = observers.get(subjectName);
        if (subjectObservers != null) {
            subjectObservers.remove(observer);
        }
    }

    /**
     * 通知观察者
     */
    public void notifyObservers(String subjectName, Object data) {
        Subject subject = subjects.get(subjectName);
        if (subject != null) {
            subject.notifyObservers(data);
        }
    }

    /**
     * 注册通知策略
     */
    public void registerNotificationStrategy(String strategyName, NotificationStrategy strategy) {
        notificationStrategies.put(strategyName, strategy);
    }

    /**
     * 使用特定策略通知观察者
     */
    public void notifyWithStrategy(String subjectName, String strategyName, Object data) {
        NotificationStrategy strategy = notificationStrategies.get(strategyName);
        if (strategy != null) {
            strategy.notify(subjectName, data);
        } else {
            notifyObservers(subjectName, data);
        }
    }

    /**
     * 获取主题列表
     */
    public Set<String> getSubjectNames() {
        return new HashSet<>(subjects.keySet());
    }

    /**
     * 获取观察者数量
     */
    public int getObserverCount(String subjectName) {
        List<Observer> subjectObservers = observers.get(subjectName);
        return subjectObservers != null ? subjectObservers.size() : 0;
    }

    // 主题接口
    public interface Subject {
        void registerObserver(Observer observer);
        void unregisterObserver(Observer observer);
        void notifyObservers(Object data);
        String getName();
    }

    // 观察者接口
    public interface Observer {
        void update(String subjectName, Object data);
        String getName();
        int getPriority();
    }

    // 通知策略接口
    public interface NotificationStrategy {
        void notify(String subjectName, Object data);
        String getName();
    }

    // 具体主题实现
    public class ConcreteSubject implements Subject {
        private final String name;

        public ConcreteSubject(String name) {
            this.name = name;
        }

        @Override
        public void registerObserver(Observer observer) {
            ObserverManager.this.registerObserver(name, observer);
        }

        @Override
        public void unregisterObserver(Observer observer) {
            ObserverManager.this.unregisterObserver(name, observer);
        }

        @Override
        public void notifyObservers(Object data) {
            List<Observer> subjectObservers = observers.get(name);
            if (subjectObservers != null) {
                // 按优先级排序
                List<Observer> sortedObservers = subjectObservers.stream()
                    .sorted(Comparator.comparingInt(Observer::getPriority).reversed())
                    .collect(Collectors.toList());

                for (Observer observer : sortedObservers) {
                    try {
                        observer.update(name, data);
                    } catch (Exception e) {
                        System.err.println("Observer update failed: " + observer.getName() + " - " + e.getMessage());
                    }
                }
            }
        }

        @Override
        public String getName() {
            return name;
        }
    }

    // 立即通知策略
    public class ImmediateNotificationStrategy implements NotificationStrategy {
        @Override
        public void notify(String subjectName, Object data) {
            ObserverManager.this.notifyObservers(subjectName, data);
        }

        @Override
        public String getName() {
            return "immediate";
        }
    }

    // 异步通知策略
    public class AsyncNotificationStrategy implements NotificationStrategy {
        @Override
        public void notify(String subjectName, Object data) {
            notificationExecutor.submit(() -> {
                ObserverManager.this.notifyObservers(subjectName, data);
            });
        }

        @Override
        public String getName() {
            return "async";
        }
    }

    // 批处理通知策略
    public class BatchedNotificationStrategy implements NotificationStrategy {
        private final Map<String, List<Object>> batchBuffer = new ConcurrentHashMap<>();
        private final ScheduledExecutorService batchScheduler = Executors.newScheduledThreadPool(1);

        public BatchedNotificationStrategy() {
            // 每5秒处理一次批处理
            batchScheduler.scheduleAtFixedRate(this::processBatches, 5, 5, TimeUnit.SECONDS);
        }

        @Override
        public void notify(String subjectName, Object data) {
            batchBuffer.computeIfAbsent(subjectName, k -> new ArrayList<>()).add(data);
        }

        private void processBatches() {
            Map<String, List<Object>> batchesToProcess = new HashMap<>(batchBuffer);
            batchBuffer.clear();

            for (Map.Entry<String, List<Object>> entry : batchesToProcess.entrySet()) {
                String subjectName = entry.getKey();
                List<Object> batchData = entry.getValue();

                notificationExecutor.submit(() -> {
                    ObserverManager.this.notifyObservers(subjectName, batchData);
                });
            }
        }

        @Override
        public String getName() {
            return "batched";
        }
    }

    // 过滤通知策略
    public class FilteredNotificationStrategy implements NotificationStrategy {
        private final Map<String, Predicate<Object>> filters = new ConcurrentHashMap<>();

        public void addFilter(String subjectName, Predicate<Object> filter) {
            filters.put(subjectName, filter);
        }

        @Override
        public void notify(String subjectName, Object data) {
            Predicate<Object> filter = filters.get(subjectName);
            if (filter == null || filter.test(data)) {
                ObserverManager.this.notifyObservers(subjectName, data);
            }
        }

        @Override
        public String getName() {
            return "filtered";
        }
    }

    // 优先级通知策略
    public class PrioritizedNotificationStrategy implements NotificationStrategy {
        private final Map<String, PriorityQueue<NotificationTask>> priorityQueues = new ConcurrentHashMap<>();

        @Override
        public void notify(String subjectName, Object data) {
            PriorityQueue<NotificationTask> queue = priorityQueues.computeIfAbsent(subjectName,
                k -> new PriorityQueue<>(Comparator.comparingInt(NotificationTask::getPriority).reversed()));

            queue.add(new NotificationTask(data, 1)); // 默认优先级为1

            // 异步处理队列
            notificationExecutor.submit(() -> processPriorityQueue(subjectName));
        }

        private void processPriorityQueue(String subjectName) {
            PriorityQueue<NotificationTask> queue = priorityQueues.get(subjectName);
            if (queue != null) {
                NotificationTask task = queue.poll();
                if (task != null) {
                    ObserverManager.this.notifyObservers(subjectName, task.getData());
                }
            }
        }

        @Override
        public String getName() {
            return "prioritized";
        }

        private class NotificationTask {
            private final Object data;
            private final int priority;

            public NotificationTask(Object data, int priority) {
                this.data = data;
                this.priority = priority;
            }

            public Object getData() { return data; }
            public int getPriority() { return priority; }
        }
    }

    // 具体观察者实现
    public static abstract class AbstractObserver implements Observer {
        protected final String name;
        protected final int priority;

        public AbstractObserver(String name, int priority) {
            this.name = name;
            this.priority = priority;
        }

        @Override
        public String getName() {
            return name;
        }

        @Override
        public int getPriority() {
            return priority;
        }

        @Override
        public abstract void update(String subjectName, Object data);
    }

    // 日志观察者
    public static class LoggingObserver extends AbstractObserver {
        public LoggingObserver(String name, int priority) {
            super(name, priority);
        }

        @Override
        public void update(String subjectName, Object data) {
            System.out.println("[" + Instant.now() + "] " + name + " received update for " +
                             subjectName + ": " + data);
        }
    }

    // 邮件通知观察者
    public static class EmailNotificationObserver extends AbstractObserver {
        private final String emailAddress;

        public EmailNotificationObserver(String name, String emailAddress, int priority) {
            super(name, priority);
            this.emailAddress = emailAddress;
        }

        @Override
        public void update(String subjectName, Object data) {
            System.out.println("Sending email notification to " + emailAddress +
                             " for subject: " + subjectName + ", data: " + data);
            // 这里可以集成实际的邮件发送服务
        }
    }

    // 数据库记录观察者
    public static class DatabaseLoggingObserver extends AbstractObserver {
        public DatabaseLoggingObserver(String name, int priority) {
            super(name, priority);
        }

        @Override
        public void update(String subjectName, Object data) {
            System.out.println("Logging to database: subject=" + subjectName +
                             ", data=" + data + ", timestamp=" + Instant.now());
            // 这里可以集成实际的数据库操作
        }
    }

    // 性能监控观察者
    public static class PerformanceMonitoringObserver extends AbstractObserver {
        private final Map<String, Long> eventCounts = new ConcurrentHashMap<>();
        private final Map<String, Long> lastEventTimes = new ConcurrentHashMap<>();

        public PerformanceMonitoringObserver(String name, int priority) {
            super(name, priority);
        }

        @Override
        public void update(String subjectName, Object data) {
            long currentTime = System.currentTimeMillis();

            // 更新事件计数
            eventCounts.merge(subjectName, 1L, Long::sum);

            // 计算事件频率
            Long lastTime = lastEventTimes.get(subjectName);
            if (lastTime != null) {
                long timeDiff = currentTime - lastTime;
                double frequency = 1000.0 / timeDiff; // 每秒事件数
                System.out.println("Performance monitor: " + subjectName +
                                 " event frequency: " + String.format("%.2f", frequency) + " events/sec");
            }

            lastEventTimes.put(subjectName, currentTime);

            // 性能分析
            analyzePerformance(subjectName);
        }

        private void analyzePerformance(String subjectName) {
            Long count = eventCounts.get(subjectName);
            if (count != null && count > 100) {
                System.out.println("Performance alert: High frequency of " + subjectName +
                                 " events (" + count + " total)");
            }
        }

        public Map<String, Long> getEventCounts() {
            return new HashMap<>(eventCounts);
        }
    }

    // 安全监控观察者
    public static class SecurityMonitoringObserver extends AbstractObserver {
        private final Set<String> suspiciousPatterns = Set.of("error", "failed", "unauthorized", "breach");

        public SecurityMonitoringObserver(String name, int priority) {
            super(name, priority);
        }

        @Override
        public void update(String subjectName, Object data) {
            String dataString = data.toString().toLowerCase();

            boolean isSuspicious = suspiciousPatterns.stream()
                .anyMatch(pattern -> dataString.contains(pattern));

            if (isSuspicious) {
                System.out.println("SECURITY ALERT: Suspicious activity detected in " +
                                 subjectName + ": " + data);
                // 这里可以触发安全响应措施
                triggerSecurityResponse(subjectName, data);
            }
        }

        private void triggerSecurityResponse(String subjectName, Object data) {
            System.out.println("Security response triggered for: " + subjectName);
            // 可以发送警报、记录日志、暂时禁用功能等
        }
    }

    // 缓存失效观察者
    public static class CacheInvalidationObserver extends AbstractObserver {
        private final Set<String> cacheKeys = ConcurrentHashMap.newKeySet();

        public CacheInvalidationObserver(String name, int priority) {
            super(name, priority);
        }

        @Override
        public void update(String subjectName, Object data) {
            if (subjectName.contains("update") || subjectName.contains("delete")) {
                // 假设数据对象有ID字段
                String cacheKey = generateCacheKey(subjectName, data);
                cacheKeys.add(cacheKey);

                System.out.println("Invalidating cache for key: " + cacheKey);
                // 这里可以集成实际的缓存失效逻辑
            }
        }

        private String generateCacheKey(String subjectName, Object data) {
            // 简单的缓存键生成逻辑
            return subjectName + ":" + Objects.hashCode(data);
        }

        public Set<String> getInvalidatedKeys() {
            return new HashSet<>(cacheKeys);
        }
    }

    // 业务规则观察者
    public static class BusinessRuleObserver extends AbstractObserver {
        private final Map<String, Consumer<Object>> businessRules = new HashMap<>();

        public BusinessRuleObserver(String name, int priority) {
            super(name, priority);
            initializeBusinessRules();
        }

        private void initializeBusinessRules() {
            // 示例业务规则
            businessRules.put("order_created", this::handleOrderCreated);
            businessRules.put("payment_received", this::handlePaymentReceived);
            businessRules.put("inventory_low", this::handleInventoryLow);
        }

        @Override
        public void update(String subjectName, Object data) {
            Consumer<Object> rule = businessRules.get(subjectName);
            if (rule != null) {
                rule.accept(data);
            }
        }

        private void handleOrderCreated(Object data) {
            System.out.println("Business rule: Processing order creation - " + data);
            // 订单创建后的业务逻辑
        }

        private void handlePaymentReceived(Object data) {
            System.out.println("Business rule: Processing payment - " + data);
            // 支付成功后的业务逻辑
        }

        private void handleInventoryLow(Object data) {
            System.out.println("Business rule: Inventory low alert - " + data);
            // 库存不足时的业务逻辑
        }
    }

    // 观察者工厂
    public static class ObserverFactory {
        public static Observer createLoggingObserver(String name, int priority) {
            return new LoggingObserver(name, priority);
        }

        public static Observer createEmailObserver(String name, String email, int priority) {
            return new EmailNotificationObserver(name, email, priority);
        }

        public static Observer createDatabaseObserver(String name, int priority) {
            return new DatabaseLoggingObserver(name, priority);
        }

        public static Observer createPerformanceObserver(String name, int priority) {
            return new PerformanceMonitoringObserver(name, priority);
        }

        public static Observer createSecurityObserver(String name, int priority) {
            return new SecurityMonitoringObserver(name, priority);
        }

        public static Observer createCacheObserver(String name, int priority) {
            return new CacheInvalidationObserver(name, priority);
        }

        public static Observer createBusinessRuleObserver(String name, int priority) {
            return new BusinessRuleObserver(name, priority);
        }
    }

    // 观察者组 - 管理一组相关的观察者
    public static class ObserverGroup {
        private final String groupName;
        private final List<Observer> observers = new CopyOnWriteArrayList<>();

        public ObserverGroup(String groupName) {
            this.groupName = groupName;
        }

        public void addObserver(Observer observer) {
            observers.add(observer);
        }

        public void removeObserver(Observer observer) {
            observers.remove(observer);
        }

        public void registerToSubject(String subjectName) {
            ObserverManager manager = ObserverManager.getInstance();
            for (Observer observer : observers) {
                manager.registerObserver(subjectName, observer);
            }
        }

        public void unregisterFromSubject(String subjectName) {
            ObserverManager manager = ObserverManager.getInstance();
            for (Observer observer : observers) {
                manager.unregisterObserver(subjectName, observer);
            }
        }

        public List<Observer> getObservers() {
            return new ArrayList<>(observers);
        }

        public String getGroupName() {
            return groupName;
        }
    }
}