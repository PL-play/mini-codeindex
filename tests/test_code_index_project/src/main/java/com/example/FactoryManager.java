package com.example;

import java.util.*;
import java.util.function.*;
import java.util.concurrent.*;
import java.util.stream.*;

/**
 * 工厂模式实现
 * 负责创建各种对象和服务
 */
public class FactoryManager {

    // 单例模式实现
    private static volatile FactoryManager instance;
    private static final Object LOCK = new Object();

    private final Map<String, ObjectFactory<?>> factories;
    private final Map<String, ServiceRegistry> serviceRegistries;
    private final Map<String, Object> singletonInstances;

    private FactoryManager() {
        this.factories = new ConcurrentHashMap<>();
        this.serviceRegistries = new ConcurrentHashMap<>();
        this.singletonInstances = new ConcurrentHashMap<>();
        initializeDefaultFactories();
    }

    public static FactoryManager getInstance() {
        if (instance == null) {
            synchronized (LOCK) {
                if (instance == null) {
                    instance = new FactoryManager();
                }
            }
        }
        return instance;
    }

    /**
     * 初始化默认工厂
     */
    private void initializeDefaultFactories() {
        // 用户相关工厂
        registerFactory("user", new UserFactory());
        registerFactory("userService", new UserServiceFactory());
        registerFactory("permissionManager", new PermissionManagerFactory());

        // 数据处理工厂
        registerFactory("dataProcessor", new DataProcessorFactory());
        registerFactory("reportGenerator", new ReportGeneratorFactory());

        // 工具类工厂
        registerFactory("auditLogger", new AuditLoggerFactory());
        registerFactory("cacheManager", new CacheManagerFactory());
        registerFactory("notificationService", new NotificationServiceFactory());

        // 服务注册表
        registerServiceRegistry("database", new DatabaseServiceRegistry());
        registerServiceRegistry("api", new ApiServiceRegistry());
        registerServiceRegistry("cache", new CacheServiceRegistry());
    }

    /**
     * 注册工厂
     */
    public <T> void registerFactory(String name, ObjectFactory<T> factory) {
        factories.put(name, factory);
    }

    /**
     * 获取工厂创建的对象
     */
    @SuppressWarnings("unchecked")
    public <T> T create(String name, Object... args) {
        ObjectFactory<T> factory = (ObjectFactory<T>) factories.get(name);
        if (factory == null) {
            throw new IllegalArgumentException("Factory not found: " + name);
        }
        return factory.create(args);
    }

    /**
     * 获取单例实例
     */
    @SuppressWarnings("unchecked")
    public <T> T getSingleton(String name, Object... args) {
        return (T) singletonInstances.computeIfAbsent(name, key -> create(key, args));
    }

    /**
     * 注册服务注册表
     */
    public void registerServiceRegistry(String name, ServiceRegistry registry) {
        serviceRegistries.put(name, registry);
    }

    /**
     * 获取服务
     */
    public <T> T getService(String registryName, String serviceName) {
        ServiceRegistry registry = serviceRegistries.get(registryName);
        if (registry == null) {
            throw new IllegalArgumentException("Service registry not found: " + registryName);
        }
        return registry.getService(serviceName);
    }

    /**
     * 注册服务
     */
    public void registerService(String registryName, String serviceName, Object service) {
        ServiceRegistry registry = serviceRegistries.get(registryName);
        if (registry == null) {
            throw new IllegalArgumentException("Service registry not found: " + registryName);
        }
        registry.registerService(serviceName, service);
    }

    // 工厂接口
    public interface ObjectFactory<T> {
        T create(Object... args);
    }

    // 服务注册表接口
    public interface ServiceRegistry {
        <T> T getService(String name);
        void registerService(String name, Object service);
    }

    // 具体工厂实现
    public static class UserFactory implements ObjectFactory<User> {
        @Override
        public User create(Object... args) {
            try {
                if (args.length == 0) {
                    return new User.Builder()
                        .id("default")
                        .name("default")
                        .email("default@example.com")
                        .build();
                }

                String userId = (String) args[0];
                String username = (String) args[1];
                String email = (String) args[2];

                return new User.Builder()
                    .id(userId)
                    .name(username)
                    .email(email)
                    .build();
            } catch (User.ValidationException e) {
                throw new RuntimeException("Failed to create user: " + e.getMessage(), e);
            }
        }
    }

    public static class UserServiceFactory implements ObjectFactory<UserService> {
        @Override
        public UserService create(Object... args) {
            UserService userService = new UserService();
            // 配置服务
            if (args.length > 0 && args[0] instanceof Map) {
                @SuppressWarnings("unchecked")
                Map<String, Object> config = (Map<String, Object>) args[0];
                configureUserService(userService, config);
            }
            return userService;
        }

        private void configureUserService(UserService service, Map<String, Object> config) {
            // 配置逻辑
            Boolean enableCache = (Boolean) config.get("enableCache");
            if (enableCache != null && enableCache) {
                // 启用缓存
            }

            Integer maxRetries = (Integer) config.get("maxRetries");
            if (maxRetries != null) {
                // 设置重试次数
            }
        }
    }

    public static class PermissionManagerFactory implements ObjectFactory<PermissionManager> {
        @Override
        public PermissionManager create(Object... args) {
            PermissionManager manager = new PermissionManager();

            // 初始化默认权限
            manager.assignRole("admin", PermissionManager.ROLE_ADMIN);
            manager.assignRole("user", PermissionManager.ROLE_USER);

            return manager;
        }
    }

    public static class DataProcessorFactory implements ObjectFactory<DataProcessor> {
        @Override
        public DataProcessor create(Object... args) {
            return new DataProcessor();
        }
    }

    public static class ReportGeneratorFactory implements ObjectFactory<ReportGenerator> {
        @Override
        public ReportGenerator create(Object... args) {
            ReportGenerator.ReportDataProvider dataProvider = null;
            if (args.length > 0 && args[0] instanceof ReportGenerator.ReportDataProvider) {
                dataProvider = (ReportGenerator.ReportDataProvider) args[0];
            }

            if (dataProvider == null) {
                dataProvider = new DefaultReportDataProvider();
            }

            return new ReportGenerator(dataProvider);
        }
    }

    public static class AuditLoggerFactory implements ObjectFactory<AuditLogger> {
        @Override
        public AuditLogger create(Object... args) {
            return new AuditLogger();
        }
    }

    public static class CacheManagerFactory implements ObjectFactory<CacheManager> {
        @Override
        public CacheManager create(Object... args) {
            return new CacheManager();
        }
    }

    public static class NotificationServiceFactory implements ObjectFactory<NotificationService> {
        @Override
        public NotificationService create(Object... args) {
            return new NotificationService();
        }
    }

    // 服务注册表实现
    public static class DatabaseServiceRegistry implements ServiceRegistry {
        private final Map<String, Object> services = new ConcurrentHashMap<>();

        @Override
        @SuppressWarnings("unchecked")
        public <T> T getService(String name) {
            return (T) services.get(name);
        }

        @Override
        public void registerService(String name, Object service) {
            services.put(name, service);
        }
    }

    public static class ApiServiceRegistry implements ServiceRegistry {
        private final Map<String, Object> services = new ConcurrentHashMap<>();

        @Override
        @SuppressWarnings("unchecked")
        public <T> T getService(String name) {
            return (T) services.get(name);
        }

        @Override
        public void registerService(String name, Object service) {
            services.put(name, service);
        }
    }

    public static class CacheServiceRegistry implements ServiceRegistry {
        private final Map<String, Object> services = new ConcurrentHashMap<>();

        @Override
        @SuppressWarnings("unchecked")
        public <T> T getService(String name) {
            return (T) services.get(name);
        }

        @Override
        public void registerService(String name, Object service) {
            services.put(name, service);
        }
    }

    // 默认报告数据提供者
    public static class DefaultReportDataProvider implements ReportGenerator.ReportDataProvider {
        @Override
        public List<ReportGenerator.UserActivityData> getUserActivities(java.time.LocalDate startDate,
                                                      java.time.LocalDate endDate,
                                                      String department) {
            // 返回模拟数据
            return Arrays.asList(
                new ReportGenerator.UserActivityData("user1", 10, java.time.LocalDateTime.now(), 3600000, 50),
                new ReportGenerator.UserActivityData("user2", 8, java.time.LocalDateTime.now().minusHours(1), 2800000, 40)
            );
        }

        @Override
        public List<ReportGenerator.PerformanceMetric> getPerformanceMetrics(String metricType,
                                                           java.time.LocalDateTime startTime,
                                                           java.time.LocalDateTime endTime) {
            return Arrays.asList(
                new ReportGenerator.PerformanceMetric("cpu_usage", 75.5, java.time.LocalDateTime.now()),
                new ReportGenerator.PerformanceMetric("memory_usage", 60.2, java.time.LocalDateTime.now().minusMinutes(5))
            );
        }

        @Override
        public List<ReportGenerator.FinancialData> getFinancialData(java.time.LocalDate startDate,
                                                  java.time.LocalDate endDate) {
            return Arrays.asList(
                new ReportGenerator.FinancialData("2024-01", new java.math.BigDecimal("10000.00"),
                                new java.math.BigDecimal("8000.00"),
                                new java.math.BigDecimal("2000.00"), 15.5)
            );
        }

        @Override
        public List<ReportGenerator.AuditEventData> getAuditEvents(java.time.LocalDateTime startTime,
                                                 java.time.LocalDateTime endTime,
                                                 String userId, String eventType) {
            return Arrays.asList(
                new ReportGenerator.AuditEventData(java.time.LocalDateTime.now(), "user1", "LOGIN",
                                 "authentication", "User logged in")
            );
        }

        @Override
        public List<ReportGenerator.DepartmentData> getDepartmentData() {
            return Arrays.asList(
                new ReportGenerator.DepartmentData("Engineering", 25, "High", 85.5, 2),
                new ReportGenerator.DepartmentData("Sales", 15, "Medium", 78.2, 1)
            );
        }
    }
}