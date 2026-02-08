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
 * 装饰器模式实现
 * 为对象动态添加功能和行为的装饰器集合
 */
public class DecoratorManager {

    // 单例模式
    private static volatile DecoratorManager instance;
    private static final Object LOCK = new Object();

    private final Map<String, DecoratorFactory> decoratorFactories;
    private final Map<String, List<Decorator<?>>> activeDecorators;

    private DecoratorManager() {
        this.decoratorFactories = new ConcurrentHashMap<>();
        this.activeDecorators = new ConcurrentHashMap<>();
        initializeDefaultDecorators();
    }

    public static DecoratorManager getInstance() {
        if (instance == null) {
            synchronized (LOCK) {
                if (instance == null) {
                    instance = new DecoratorManager();
                }
            }
        }
        return instance;
    }

    /**
     * 初始化默认装饰器
     */
    private void initializeDefaultDecorators() {
        // 日志装饰器
        registerDecorator("logging", new LoggingDecoratorFactory());

        // 缓存装饰器
        registerDecorator("caching", new CachingDecoratorFactory());

        // 验证装饰器
        registerDecorator("validation", new ValidationDecoratorFactory());

        // 性能监控装饰器
        registerDecorator("performance", new PerformanceDecoratorFactory());

        // 安全装饰器
        registerDecorator("security", new SecurityDecoratorFactory());

        // 重试装饰器
        registerDecorator("retry", new RetryDecoratorFactory());

        // 事务装饰器
        registerDecorator("transaction", new TransactionDecoratorFactory());

        // 异步装饰器
        registerDecorator("async", new AsyncDecoratorFactory());

        // 压缩装饰器
        registerDecorator("compression", new CompressionDecoratorFactory());

        // 加密装饰器
        registerDecorator("encryption", new EncryptionDecoratorFactory());
    }

    /**
     * 注册装饰器工厂
     */
    public void registerDecorator(String decoratorType, DecoratorFactory factory) {
        decoratorFactories.put(decoratorType, factory);
    }

    /**
     * 创建装饰器
     */
    @SuppressWarnings("unchecked")
    public <T> Decorator<T> createDecorator(String decoratorType, Object... params) {
        DecoratorFactory factory = decoratorFactories.get(decoratorType);
        if (factory == null) {
            throw new IllegalArgumentException("Decorator type not found: " + decoratorType);
        }
        return (Decorator<T>) factory.create(params);
    }

    /**
     * 装饰对象
     */
    public <T> T decorate(String decoratorType, T target, Object... params) {
        Decorator<T> decorator = createDecorator(decoratorType, params);
        return decorator.decorate(target);
    }

    /**
     * 多重装饰对象
     */
    public <T> T decorateMultiple(T target, String... decoratorTypes) {
        T result = target;
        for (String decoratorType : decoratorTypes) {
            result = decorate(decoratorType, result);
        }
        return result;
    }

    /**
     * 应用装饰器链
     */
    public <T> T applyDecoratorChain(T target, List<String> decoratorTypes,
                                    List<Object[]> paramsList) {
        T result = target;
        for (int i = 0; i < decoratorTypes.size(); i++) {
            String decoratorType = decoratorTypes.get(i);
            Object[] params = i < paramsList.size() ? paramsList.get(i) : new Object[0];
            result = decorate(decoratorType, result, params);
        }
        return result;
    }

    /**
     * 获取活跃装饰器
     */
    public List<Decorator<?>> getActiveDecorators(String decoratorType) {
        return activeDecorators.getOrDefault(decoratorType, new ArrayList<>());
    }

    // 装饰器接口
    public interface Decorator<T> {
        T decorate(T target);
        String getType();
    }

    // 装饰器工厂接口
    public interface DecoratorFactory {
        Decorator<?> create(Object... params);
    }

    // 日志装饰器
    public static class LoggingDecoratorFactory implements DecoratorFactory {
        @Override
        public Decorator<?> create(Object... params) {
            String loggerName = params.length > 0 ? (String) params[0] : "Decorator";
            return new LoggingDecorator(loggerName);
        }
    }

    public static class LoggingDecorator<T> implements Decorator<T> {
        private final String loggerName;

        public LoggingDecorator(String loggerName) {
            this.loggerName = loggerName;
        }

        @Override
        public T decorate(T target) {
            if (target instanceof Function) {
                @SuppressWarnings("unchecked")
                Function<Object, Object> function = (Function<Object, Object>) target;
                Function<Object, Object> decoratedFunction = input -> {
                    System.out.println("[" + loggerName + "] Input: " + input);
                    Object result = function.apply(input);
                    System.out.println("[" + loggerName + "] Output: " + result);
                    return result;
                };
                @SuppressWarnings("unchecked")
                T result = (T) decoratedFunction;
                return result;
            }
            return target;
        }

        @Override
        public String getType() {
            return "logging";
        }
    }

    // 缓存装饰器
    public static class CachingDecoratorFactory implements DecoratorFactory {
        @Override
        public Decorator<?> create(Object... params) {
            int capacity = params.length > 0 ? (Integer) params[0] : 100;
            return new CachingDecorator(capacity);
        }
    }

    public static class CachingDecorator<T> implements Decorator<T> {
        private final Map<Object, Object> cache;
        private final int capacity;

        public CachingDecorator(int capacity) {
            this.capacity = capacity;
            this.cache = new LinkedHashMap<Object, Object>(capacity, 0.75f, true) {
                @Override
                protected boolean removeEldestEntry(Map.Entry<Object, Object> eldest) {
                    return size() > capacity;
                }
            };
        }

        @Override
        public T decorate(T target) {
            if (target instanceof Function) {
                @SuppressWarnings("unchecked")
                Function<Object, Object> function = (Function<Object, Object>) target;
                Function<Object, Object> decoratedFunction = input -> {
                    if (cache.containsKey(input)) {
                        System.out.println("Cache hit for input: " + input);
                        return cache.get(input);
                    }
                    Object result = function.apply(input);
                    cache.put(input, result);
                    System.out.println("Cache miss, computed result for input: " + input);
                    return result;
                };
                @SuppressWarnings("unchecked")
                T result = (T) decoratedFunction;
                return result;
            }
            return target;
        }

        @Override
        public String getType() {
            return "caching";
        }

        public void clearCache() {
            cache.clear();
        }

        public int getCacheSize() {
            return cache.size();
        }
    }

    // 验证装饰器
    public static class ValidationDecoratorFactory implements DecoratorFactory {
        @Override
        public Decorator<?> create(Object... params) {
            Predicate<Object> validator = params.length > 0 ?
                (Predicate<Object>) params[0] : Objects::nonNull;
            return new ValidationDecorator(validator);
        }
    }

    public static class ValidationDecorator<T> implements Decorator<T> {
        private final Predicate<Object> validator;

        public ValidationDecorator(Predicate<Object> validator) {
            this.validator = validator;
        }

        @Override
        public T decorate(T target) {
            if (target instanceof Function) {
                @SuppressWarnings("unchecked")
                Function<Object, Object> function = (Function<Object, Object>) target;
                Function<Object, Object> decoratedFunction = input -> {
                    if (!validator.test(input)) {
                        throw new IllegalArgumentException("Input validation failed: " + input);
                    }
                    return function.apply(input);
                };
                @SuppressWarnings("unchecked")
                T result = (T) decoratedFunction;
                return result;
            }
            return target;
        }

        @Override
        public String getType() {
            return "validation";
        }
    }

    // 性能监控装饰器
    public static class PerformanceDecoratorFactory implements DecoratorFactory {
        @Override
        public Decorator<?> create(Object... params) {
            String metricName = params.length > 0 ? (String) params[0] : "operation";
            return new PerformanceDecorator(metricName);
        }
    }

    public static class PerformanceDecorator<T> implements Decorator<T> {
        private final String metricName;

        public PerformanceDecorator(String metricName) {
            this.metricName = metricName;
        }

        @Override
        public T decorate(T target) {
            if (target instanceof Function) {
                @SuppressWarnings("unchecked")
                Function<Object, Object> function = (Function<Object, Object>) target;
                Function<Object, Object> decoratedFunction = input -> {
                    long startTime = System.nanoTime();
                    try {
                        Object result = function.apply(input);
                        long endTime = System.nanoTime();
                        long duration = (endTime - startTime) / 1_000_000; // 转换为毫秒
                        System.out.println("[" + metricName + "] Execution time: " + duration + "ms");
                        return result;
                    } catch (Exception e) {
                        long endTime = System.nanoTime();
                        long duration = (endTime - startTime) / 1_000_000;
                        System.out.println("[" + metricName + "] Failed after: " + duration + "ms");
                        throw e;
                    }
                };
                @SuppressWarnings("unchecked")
                T result = (T) decoratedFunction;
                return result;
            }
            return target;
        }

        @Override
        public String getType() {
            return "performance";
        }
    }

    // 安全装饰器
    public static class SecurityDecoratorFactory implements DecoratorFactory {
        @Override
        public Decorator<?> create(Object... params) {
            String requiredRole = params.length > 0 ? (String) params[0] : "user";
            return new SecurityDecorator(requiredRole);
        }
    }

    public static class SecurityDecorator<T> implements Decorator<T> {
        private final String requiredRole;

        public SecurityDecorator(String requiredRole) {
            this.requiredRole = requiredRole;
        }

        @Override
        public T decorate(T target) {
            if (target instanceof Function) {
                @SuppressWarnings("unchecked")
                Function<Object, Object> function = (Function<Object, Object>) target;
                Function<Object, Object> decoratedFunction = input -> {
                    // 模拟权限检查
                    String userRole = getCurrentUserRole();
                    if (!hasPermission(userRole, requiredRole)) {
                        throw new SecurityException("Access denied. Required role: " + requiredRole +
                                                  ", User role: " + userRole);
                    }
                    return function.apply(input);
                };
                @SuppressWarnings("unchecked")
                T result = (T) decoratedFunction;
                return result;
            }
            return target;
        }

        @Override
        public String getType() {
            return "security";
        }

        private String getCurrentUserRole() {
            // 模拟获取当前用户角色
            return "admin"; // 为了演示，假设用户是管理员
        }

        private boolean hasPermission(String userRole, String requiredRole) {
            // 简单的角色层次检查
            Map<String, Integer> roleHierarchy = Map.of(
                "guest", 0,
                "user", 1,
                "moderator", 2,
                "admin", 3,
                "superadmin", 4
            );

            Integer userLevel = roleHierarchy.getOrDefault(userRole, 0);
            Integer requiredLevel = roleHierarchy.getOrDefault(requiredRole, 0);

            return userLevel >= requiredLevel;
        }
    }

    // 重试装饰器
    public static class RetryDecoratorFactory implements DecoratorFactory {
        @Override
        public Decorator<?> create(Object... params) {
            int maxRetries = params.length > 0 ? (Integer) params[0] : 3;
            long delayMillis = params.length > 1 ? (Long) params[1] : 1000L;
            return new RetryDecorator(maxRetries, delayMillis);
        }
    }

    public static class RetryDecorator<T> implements Decorator<T> {
        private final int maxRetries;
        private final long delayMillis;

        public RetryDecorator(int maxRetries, long delayMillis) {
            this.maxRetries = maxRetries;
            this.delayMillis = delayMillis;
        }

        @Override
        public T decorate(T target) {
            if (target instanceof Function) {
                @SuppressWarnings("unchecked")
                Function<Object, Object> function = (Function<Object, Object>) target;
                Function<Object, Object> decoratedFunction = input -> {
                    Exception lastException = null;
                    for (int attempt = 0; attempt <= maxRetries; attempt++) {
                        try {
                            return function.apply(input);
                        } catch (Exception e) {
                            lastException = e;
                            if (attempt < maxRetries) {
                                System.out.println("Attempt " + (attempt + 1) + " failed, retrying...");
                                try {
                                    Thread.sleep(delayMillis);
                                } catch (InterruptedException ie) {
                                    Thread.currentThread().interrupt();
                                    throw new RuntimeException(ie);
                                }
                            }
                        }
                    }
                    throw new RuntimeException("Operation failed after " + (maxRetries + 1) + " attempts",
                                             lastException);
                };
                @SuppressWarnings("unchecked")
                T result = (T) decoratedFunction;
                return result;
            }
            return target;
        }

        @Override
        public String getType() {
            return "retry";
        }
    }

    // 事务装饰器
    public static class TransactionDecoratorFactory implements DecoratorFactory {
        @Override
        public Decorator<?> create(Object... params) {
            return new TransactionDecorator();
        }
    }

    public static class TransactionDecorator<T> implements Decorator<T> {
        @Override
        public T decorate(T target) {
            if (target instanceof Function) {
                @SuppressWarnings("unchecked")
                Function<Object, Object> function = (Function<Object, Object>) target;
                Function<Object, Object> decoratedFunction = input -> {
                    System.out.println("Starting transaction...");
                    try {
                        Object result = function.apply(input);
                        System.out.println("Committing transaction...");
                        return result;
                    } catch (Exception e) {
                        System.out.println("Rolling back transaction...");
                        throw e;
                    }
                };
                @SuppressWarnings("unchecked")
                T result = (T) decoratedFunction;
                return result;
            }
            return target;
        }

        @Override
        public String getType() {
            return "transaction";
        }
    }

    // 异步装饰器
    public static class AsyncDecoratorFactory implements DecoratorFactory {
        @Override
        public Decorator<?> create(Object... params) {
            Executor executor = params.length > 0 ?
                (Executor) params[0] : Executors.newCachedThreadPool();
            return new AsyncDecorator(executor);
        }
    }

    public static class AsyncDecorator<T> implements Decorator<T> {
        private final Executor executor;

        public AsyncDecorator(Executor executor) {
            this.executor = executor;
        }

        @Override
        public T decorate(T target) {
            if (target instanceof Function) {
                @SuppressWarnings("unchecked")
                Function<Object, Object> function = (Function<Object, Object>) target;
                Function<Object, Object> decoratedFunction = input -> {
                    CompletableFuture<Object> future = new CompletableFuture<>();
                    executor.execute(() -> {
                        try {
                            Object result = function.apply(input);
                            future.complete(result);
                        } catch (Exception e) {
                            future.completeExceptionally(e);
                        }
                    });
                    return future;
                };
                @SuppressWarnings("unchecked")
                T result = (T) decoratedFunction;
                return result;
            }
            return target;
        }

        @Override
        public String getType() {
            return "async";
        }
    }

    // 压缩装饰器
    public static class CompressionDecoratorFactory implements DecoratorFactory {
        @Override
        public Decorator<?> create(Object... params) {
            String algorithm = params.length > 0 ? (String) params[0] : "gzip";
            return new CompressionDecorator(algorithm);
        }
    }

    public static class CompressionDecorator<T> implements Decorator<T> {
        private final String algorithm;

        public CompressionDecorator(String algorithm) {
            this.algorithm = algorithm;
        }

        @Override
        public T decorate(T target) {
            if (target instanceof Function) {
                @SuppressWarnings("unchecked")
                Function<Object, Object> function = (Function<Object, Object>) target;
                Function<Object, Object> decoratedFunction = input -> {
                    if (input instanceof String) {
                        String data = (String) input;
                        String compressed = algorithm.toUpperCase() + ":" + data;
                        System.out.println("Compressing data with " + algorithm);
                        Object result = function.apply(compressed);
                        System.out.println("Decompressing result");
                        return result;
                    }
                    return function.apply(input);
                };
                @SuppressWarnings("unchecked")
                T result = (T) decoratedFunction;
                return result;
            }
            return target;
        }

        @Override
        public String getType() {
            return "compression";
        }
    }

    // 加密装饰器
    public static class EncryptionDecoratorFactory implements DecoratorFactory {
        @Override
        public Decorator<?> create(Object... params) {
            String key = params.length > 0 ? (String) params[0] : "default_key";
            return new EncryptionDecorator(key);
        }
    }

    public static class EncryptionDecorator<T> implements Decorator<T> {
        private final String key;

        public EncryptionDecorator(String key) {
            this.key = key;
        }

        @Override
        public T decorate(T target) {
            if (target instanceof Function) {
                @SuppressWarnings("unchecked")
                Function<Object, Object> function = (Function<Object, Object>) target;
                Function<Object, Object> decoratedFunction = input -> {
                    if (input instanceof String) {
                        String data = (String) input;
                        String encrypted = encrypt(data, key);
                        System.out.println("Encrypting data");
                        Object result = function.apply(encrypted);
                        String decrypted = decrypt(result.toString(), key);
                        System.out.println("Decrypting result");
                        return decrypted;
                    }
                    return function.apply(input);
                };
                @SuppressWarnings("unchecked")
                T result = (T) decoratedFunction;
                return result;
            }
            return target;
        }

        @Override
        public String getType() {
            return "encryption";
        }

        private String encrypt(String data, String key) {
            // 简单的凯撒密码加密（仅用于演示）
            int shift = key.length() % 26;
            StringBuilder result = new StringBuilder();
            for (char c : data.toUpperCase().toCharArray()) {
                if (Character.isLetter(c)) {
                    char encrypted = (char) ((c - 'A' + shift) % 26 + 'A');
                    result.append(encrypted);
                } else {
                    result.append(c);
                }
            }
            return "ENC:" + result.toString();
        }

        private String decrypt(String encryptedData, String key) {
            if (!encryptedData.startsWith("ENC:")) {
                return encryptedData;
            }
            String data = encryptedData.substring(4);
            int shift = key.length() % 26;
            StringBuilder result = new StringBuilder();
            for (char c : data.toCharArray()) {
                if (Character.isLetter(c)) {
                    char decrypted = (char) ((c - 'A' - shift + 26) % 26 + 'A');
                    result.append(decrypted);
                } else {
                    result.append(c);
                }
            }
            return result.toString();
        }
    }
}