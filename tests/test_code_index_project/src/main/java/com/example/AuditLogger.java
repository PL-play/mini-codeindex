package com.example;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.*;
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicLong;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 * 审计日志记录器
 * 负责记录系统操作的审计日志
 */
public class AuditLogger {
    private static final Logger logger = Logger.getLogger(AuditLogger.class.getName());
    private static final DateTimeFormatter TIMESTAMP_FORMAT =
        DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss.SSS");

    private final BlockingQueue<AuditEvent> eventQueue;
    private final ExecutorService executorService;
    private final Map<String, AuditHandler> handlers;
    private final AtomicLong eventCounter;
    private final Map<String, AuditStatistics> statistics;
    private volatile boolean running;

    // 审计事件类型
    public enum AuditEventType {
        USER_LOGIN("USER_LOGIN"),
        USER_LOGOUT("USER_LOGOUT"),
        USER_CREATE("USER_CREATE"),
        USER_UPDATE("USER_UPDATE"),
        USER_DELETE("USER_DELETE"),
        PERMISSION_CHANGE("PERMISSION_CHANGE"),
        DATA_ACCESS("DATA_ACCESS"),
        DATA_MODIFY("DATA_MODIFY"),
        SYSTEM_CONFIG_CHANGE("SYSTEM_CONFIG_CHANGE"),
        SECURITY_VIOLATION("SECURITY_VIOLATION"),
        API_ACCESS("API_ACCESS"),
        BATCH_OPERATION("BATCH_OPERATION");

        private final String code;

        AuditEventType(String code) {
            this.code = code;
        }

        public String getCode() {
            return code;
        }
    }

    // 审计严重性级别
    public enum AuditSeverity {
        LOW, MEDIUM, HIGH, CRITICAL
    }

    public AuditLogger() {
        this.eventQueue = new LinkedBlockingQueue<>(10000);
        this.executorService = Executors.newFixedThreadPool(3);
        this.handlers = new ConcurrentHashMap<>();
        this.eventCounter = new AtomicLong(0);
        this.statistics = new ConcurrentHashMap<>();
        this.running = false;

        initializeDefaultHandlers();
        startProcessing();
    }

    /**
     * 初始化默认处理器
     */
    private void initializeDefaultHandlers() {
        // 控制台处理器
        addHandler("console", new ConsoleAuditHandler());

        // 文件处理器
        addHandler("file", new FileAuditHandler());

        // 数据库处理器
        addHandler("database", new DatabaseAuditHandler());
    }

    /**
     * 启动事件处理
     */
    private void startProcessing() {
        running = true;
        for (int i = 0; i < 3; i++) {
            executorService.submit(this::processEvents);
        }
    }

    /**
     * 停止审计日志记录器
     */
    public void shutdown() {
        running = false;
        executorService.shutdown();
        try {
            if (!executorService.awaitTermination(30, TimeUnit.SECONDS)) {
                executorService.shutdownNow();
            }
        } catch (InterruptedException e) {
            executorService.shutdownNow();
            Thread.currentThread().interrupt();
        }
    }

    /**
     * 记录审计事件
     */
    public void log(AuditEvent event) {
        if (!running) {
            logger.warning("AuditLogger is not running, event discarded: " + event);
            return;
        }

        try {
            boolean added = eventQueue.offer(event, 5, TimeUnit.SECONDS);
            if (!added) {
                logger.severe("Audit event queue is full, event discarded: " + event);
            } else {
                eventCounter.incrementAndGet();
                updateStatistics(event);
            }
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            logger.severe("Interrupted while adding audit event to queue: " + event);
        }
    }

    /**
     * 记录审计事件（便捷方法）
     */
    public void log(String userId, AuditEventType eventType, String resource,
                   String action, AuditSeverity severity, String details) {
        AuditEvent event = new AuditEvent(
            UUID.randomUUID().toString(),
            LocalDateTime.now(),
            userId,
            eventType,
            resource,
            action,
            severity,
            details,
            getCurrentContext()
        );
        log(event);
    }

    /**
     * 记录用户登录事件
     */
    public void logUserLogin(String userId, String ipAddress, boolean success) {
        String details = String.format("Login attempt from IP: %s, Success: %s", ipAddress, success);
        log(userId, AuditEventType.USER_LOGIN, "authentication", "login",
            success ? AuditSeverity.LOW : AuditSeverity.MEDIUM, details);
    }

    /**
     * 记录用户注销事件
     */
    public void logUserLogout(String userId) {
        log(userId, AuditEventType.USER_LOGOUT, "authentication", "logout",
            AuditSeverity.LOW, "User logged out");
    }

    /**
     * 记录用户创建事件
     */
    public void logUserCreate(String userId, String createdUserId) {
        String details = String.format("Created user: %s", createdUserId);
        log(userId, AuditEventType.USER_CREATE, "user_management", "create_user",
            AuditSeverity.MEDIUM, details);
    }

    /**
     * 记录用户更新事件
     */
    public void logUserUpdate(String userId, String updatedUserId, String changes) {
        String details = String.format("Updated user: %s, Changes: %s", updatedUserId, changes);
        log(userId, AuditEventType.USER_UPDATE, "user_management", "update_user",
            AuditSeverity.MEDIUM, details);
    }

    /**
     * 记录用户删除事件
     */
    public void logUserDelete(String userId, String deletedUserId) {
        String details = String.format("Deleted user: %s", deletedUserId);
        log(userId, AuditEventType.USER_DELETE, "user_management", "delete_user",
            AuditSeverity.HIGH, details);
    }

    /**
     * 记录权限变更事件
     */
    public void logPermissionChange(String userId, String targetUserId, String permission,
                                   String action, String reason) {
        String details = String.format("Permission change for user %s: %s %s, Reason: %s",
                                     targetUserId, action, permission, reason);
        log(userId, AuditEventType.PERMISSION_CHANGE, "permission_management",
            "change_permission", AuditSeverity.HIGH, details);
    }

    /**
     * 记录数据访问事件
     */
    public void logDataAccess(String userId, String tableName, String operation,
                             String recordId, int recordCount) {
        String details = String.format("Data access: %s on %s, Record ID: %s, Count: %d",
                                     operation, tableName, recordId, recordCount);
        AuditSeverity severity = "DELETE".equals(operation) ? AuditSeverity.HIGH : AuditSeverity.LOW;
        log(userId, AuditEventType.DATA_ACCESS, "data_access", operation.toLowerCase(),
            severity, details);
    }

    /**
     * 记录安全违规事件
     */
    public void logSecurityViolation(String userId, String violationType, String details,
                                    String ipAddress) {
        String fullDetails = String.format("Security violation: %s, Details: %s, IP: %s",
                                         violationType, details, ipAddress);
        log(userId, AuditEventType.SECURITY_VIOLATION, "security", "violation",
            AuditSeverity.CRITICAL, fullDetails);
    }

    /**
     * 记录API访问事件
     */
    public void logApiAccess(String userId, String endpoint, String method, int statusCode,
                            long responseTime, String ipAddress) {
        String details = String.format("API access: %s %s, Status: %d, Response time: %dms, IP: %s",
                                     method, endpoint, statusCode, responseTime, ipAddress);
        AuditSeverity severity = statusCode >= 400 ? AuditSeverity.MEDIUM : AuditSeverity.LOW;
        log(userId, AuditEventType.API_ACCESS, "api", "access", severity, details);
    }

    /**
     * 记录批量操作事件
     */
    public void logBatchOperation(String userId, String operationType, int itemCount,
                                 boolean success, String details) {
        String fullDetails = String.format("Batch operation: %s, Items: %d, Success: %s, Details: %s",
                                         operationType, itemCount, success, details);
        AuditSeverity severity = success ? AuditSeverity.MEDIUM : AuditSeverity.HIGH;
        log(userId, AuditEventType.BATCH_OPERATION, "batch_operation", operationType.toLowerCase(),
            severity, fullDetails);
    }

    /**
     * 添加审计处理器
     */
    public void addHandler(String name, AuditHandler handler) {
        handlers.put(name, handler);
    }

    /**
     * 移除审计处理器
     */
    public void removeHandler(String name) {
        handlers.remove(name);
    }

    /**
     * 获取审计处理器
     */
    public AuditHandler getHandler(String name) {
        return handlers.get(name);
    }

    /**
     * 获取统计信息
     */
    public AuditStatistics getStatistics(String eventType) {
        return statistics.get(eventType);
    }

    /**
     * 获取所有统计信息
     */
    public Map<String, AuditStatistics> getAllStatistics() {
        return new HashMap<>(statistics);
    }

    /**
     * 获取事件计数器
     */
    public long getEventCount() {
        return eventCounter.get();
    }

    /**
     * 重置统计信息
     */
    public void resetStatistics() {
        statistics.clear();
    }

    /**
     * 处理审计事件
     */
    private void processEvents() {
        while (running || !eventQueue.isEmpty()) {
            try {
                AuditEvent event = eventQueue.poll(1, TimeUnit.SECONDS);
                if (event != null) {
                    processEvent(event);
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                break;
            } catch (Exception e) {
                logger.log(Level.SEVERE, "Error processing audit event", e);
            }
        }
    }

    /**
     * 处理单个审计事件
     */
    private void processEvent(AuditEvent event) {
        for (AuditHandler handler : handlers.values()) {
            try {
                handler.handle(event);
            } catch (Exception e) {
                logger.log(Level.SEVERE, "Error in audit handler: " + handler.getClass().getName(), e);
            }
        }
    }

    /**
     * 更新统计信息
     */
    private void updateStatistics(AuditEvent event) {
        String key = event.eventType.getCode();
        statistics.computeIfAbsent(key, k -> new AuditStatistics()).increment(event.severity);
    }

    /**
     * 获取当前上下文信息
     */
    private Map<String, String> getCurrentContext() {
        Map<String, String> context = new HashMap<>();
        context.put("thread", Thread.currentThread().getName());
        context.put("timestamp", LocalDateTime.now().format(TIMESTAMP_FORMAT));
        // 这里可以添加更多上下文信息，如会话ID、请求ID等
        return context;
    }

    /**
     * 审计事件类
     */
    public static class AuditEvent {
        public final String id;
        public final LocalDateTime timestamp;
        public final String userId;
        public final AuditEventType eventType;
        public final String resource;
        public final String action;
        public final AuditSeverity severity;
        public final String details;
        public final Map<String, String> context;

        public AuditEvent(String id, LocalDateTime timestamp, String userId,
                         AuditEventType eventType, String resource, String action,
                         AuditSeverity severity, String details, Map<String, String> context) {
            this.id = id;
            this.timestamp = timestamp;
            this.userId = userId;
            this.eventType = eventType;
            this.resource = resource;
            this.action = action;
            this.severity = severity;
            this.details = details;
            this.context = new HashMap<>(context);
        }

        @Override
        public String toString() {
            return String.format("[%s] %s - %s: %s (%s)",
                               timestamp.format(TIMESTAMP_FORMAT),
                               userId, eventType.getCode(), action, details);
        }
    }

    /**
     * 审计处理器接口
     */
    public interface AuditHandler {
        void handle(AuditEvent event) throws Exception;
    }

    /**
     * 控制台审计处理器
     */
    public static class ConsoleAuditHandler implements AuditHandler {
        @Override
        public void handle(AuditEvent event) {
            System.out.println("[AUDIT] " + event.toString());
        }
    }

    /**
     * 文件审计处理器
     */
    public static class FileAuditHandler implements AuditHandler {
        private static final String LOG_FILE = "audit.log";

        @Override
        public void handle(AuditEvent event) throws Exception {
            // 简化实现：实际应该使用适当的文件写入逻辑
            String logEntry = event.timestamp.format(TIMESTAMP_FORMAT) + " | " +
                            event.userId + " | " + event.eventType.getCode() + " | " +
                            event.resource + " | " + event.action + " | " +
                            event.severity + " | " + event.details + "\n";

            // 这里应该写入文件
            System.out.println("Writing to audit.log: " + logEntry.trim());
        }
    }

    /**
     * 数据库审计处理器
     */
    public static class DatabaseAuditHandler implements AuditHandler {
        @Override
        public void handle(AuditEvent event) throws Exception {
            // 简化实现：实际应该将事件插入数据库
            System.out.println("Inserting audit event into database: " + event.id);
        }
    }

    /**
     * 审计统计信息
     */
    public static class AuditStatistics {
        private final Map<AuditSeverity, AtomicLong> severityCounts = new ConcurrentHashMap<>();
        private final AtomicLong totalCount = new AtomicLong(0);

        public void increment(AuditSeverity severity) {
            severityCounts.computeIfAbsent(severity, k -> new AtomicLong(0)).incrementAndGet();
            totalCount.incrementAndGet();
        }

        public long getCount(AuditSeverity severity) {
            return severityCounts.getOrDefault(severity, new AtomicLong(0)).get();
        }

        public long getTotalCount() {
            return totalCount.get();
        }

        public Map<AuditSeverity, Long> getAllCounts() {
            Map<AuditSeverity, Long> counts = new HashMap<>();
            for (Map.Entry<AuditSeverity, AtomicLong> entry : severityCounts.entrySet()) {
                counts.put(entry.getKey(), entry.getValue().get());
            }
            return counts;
        }
    }
}