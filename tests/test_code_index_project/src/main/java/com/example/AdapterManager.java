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
import java.sql.*;
import java.net.*;
import java.net.http.*;
import java.nio.file.*;
import javax.net.ssl.*;

/**
 * 适配器模式实现
 * 将不兼容的接口转换为兼容接口的适配器集合
 */
public class AdapterManager {

    // 单例模式
    private static volatile AdapterManager instance;
    private static final Object LOCK = new Object();

    private final Map<String, AdapterFactory> adapterFactories;
    private final Map<String, Adapter<?, ?>> activeAdapters;

    private AdapterManager() {
        this.adapterFactories = new ConcurrentHashMap<>();
        this.activeAdapters = new ConcurrentHashMap<>();
        initializeDefaultAdapters();
    }

    public static AdapterManager getInstance() {
        if (instance == null) {
            synchronized (LOCK) {
                if (instance == null) {
                    instance = new AdapterManager();
                }
            }
        }
        return instance;
    }

    /**
     * 初始化默认适配器
     */
    private void initializeDefaultAdapters() {
        // 数据库适配器
        registerAdapter("database", new DatabaseAdapterFactory());

        // HTTP客户端适配器
        registerAdapter("http", new HttpAdapterFactory());

        // 文件系统适配器
        registerAdapter("filesystem", new FileSystemAdapterFactory());

        // 缓存适配器
        registerAdapter("cache", new CacheAdapterFactory());

        // 消息队列适配器
        registerAdapter("message_queue", new MessageQueueAdapterFactory());

        // 支付网关适配器
        registerAdapter("payment", new PaymentAdapterFactory());

        // 邮件服务适配器
        registerAdapter("email", new EmailAdapterFactory());

        // 存储适配器
        registerAdapter("storage", new StorageAdapterFactory());

        // 认证适配器
        registerAdapter("authentication", new AuthenticationAdapterFactory());

        // 日志适配器
        registerAdapter("logging", new LoggingAdapterFactory());
    }

    /**
     * 注册适配器工厂
     */
    public void registerAdapter(String adapterType, AdapterFactory factory) {
        adapterFactories.put(adapterType, factory);
    }

    /**
     * 创建适配器
     */
    @SuppressWarnings("unchecked")
    public <T, U> Adapter<T, U> createAdapter(String adapterType, Object... params) {
        AdapterFactory factory = adapterFactories.get(adapterType);
        if (factory == null) {
            throw new IllegalArgumentException("Adapter type not found: " + adapterType);
        }
        return (Adapter<T, U>) factory.create(params);
    }

    /**
     * 适配对象
     */
    public <T, U> U adapt(String adapterType, T source, Object... params) {
        Adapter<T, U> adapter = createAdapter(adapterType, params);
        return adapter.adapt(source);
    }

    /**
     * 获取活跃适配器
     */
    public Map<String, Adapter<?, ?>> getActiveAdapters() {
        return new HashMap<>(activeAdapters);
    }

    // 适配器接口
    public interface Adapter<T, U> {
        U adapt(T source);
        String getType();
    }

    // 适配器工厂接口
    public interface AdapterFactory {
        Adapter<?, ?> create(Object... params);
    }

    // 数据库适配器
    public static class DatabaseAdapterFactory implements AdapterFactory {
        @Override
        public Adapter<?, ?> create(Object... params) {
            String dbType = params.length > 0 ? (String) params[0] : "postgresql";
            return new DatabaseAdapter(dbType);
        }
    }

    public static class DatabaseAdapter implements Adapter<Map<String, Object>, ResultSet> {
        private final String dbType;

        public DatabaseAdapter(String dbType) {
            this.dbType = dbType;
        }

        @Override
        public ResultSet adapt(Map<String, Object> queryParams) {
            // 模拟数据库查询适配
            System.out.println("Adapting query for " + dbType + " database");
            // 这里应该返回实际的ResultSet，但为了演示，我们返回null
            return null;
        }

        @Override
        public String getType() {
            return "database";
        }
    }

    // HTTP客户端适配器
    public static class HttpAdapterFactory implements AdapterFactory {
        @Override
        public Adapter<?, ?> create(Object... params) {
            String clientType = params.length > 0 ? (String) params[0] : "apache";
            return new HttpAdapter(clientType);
        }
    }

    public static class HttpAdapter implements Adapter<Map<String, Object>, HttpResponse<String>> {
        private final String clientType;

        public HttpAdapter(String clientType) {
            this.clientType = clientType;
        }

        @Override
        public HttpResponse<String> adapt(Map<String, Object> requestParams) {
            System.out.println("Adapting HTTP request using " + clientType + " client");
            // 模拟HTTP响应
            return new HttpResponse<String>() {
                @Override
                public int statusCode() { return 200; }
                @Override
                public HttpRequest request() { return null; }
                @Override
                public Optional<HttpResponse<String>> previousResponse() { return Optional.empty(); }
                @Override
                public HttpHeaders headers() { return HttpHeaders.of(Map.of(), (a, b) -> true); }
                @Override
                public String body() { return "{\"status\":\"success\"}"; }
                @Override
                public Optional<SSLSession> sslSession() { return Optional.empty(); }
                @Override
                public URI uri() { return URI.create("http://example.com"); }
                @Override
                public HttpClient.Version version() { return HttpClient.Version.HTTP_1_1; }
            };
        }

        @Override
        public String getType() {
            return "http";
        }
    }

    // 文件系统适配器
    public static class FileSystemAdapterFactory implements AdapterFactory {
        @Override
        public Adapter<?, ?> create(Object... params) {
            String fsType = params.length > 0 ? (String) params[0] : "local";
            return new FileSystemAdapter(fsType);
        }
    }

    public static class FileSystemAdapter implements Adapter<Path, InputStream> {
        private final String fsType;

        public FileSystemAdapter(String fsType) {
            this.fsType = fsType;
        }

        @Override
        public InputStream adapt(Path filePath) {
            System.out.println("Adapting file access for " + fsType + " filesystem");
            try {
                return Files.newInputStream(filePath);
            } catch (IOException e) {
                throw new RuntimeException("Failed to adapt file access", e);
            }
        }

        @Override
        public String getType() {
            return "filesystem";
        }
    }

    // 缓存适配器
    public static class CacheAdapterFactory implements AdapterFactory {
        @Override
        public Adapter<?, ?> create(Object... params) {
            String cacheType = params.length > 0 ? (String) params[0] : "redis";
            return new CacheAdapter(cacheType);
        }
    }

    public static class CacheAdapter implements Adapter<String, Object> {
        private final String cacheType;
        private final Map<String, Object> localCache = new ConcurrentHashMap<>();

        public CacheAdapter(String cacheType) {
            this.cacheType = cacheType;
        }

        @Override
        public Object adapt(String key) {
            System.out.println("Adapting cache access for " + cacheType);
            // 模拟缓存适配
            return localCache.get(key);
        }

        public void put(String key, Object value) {
            localCache.put(key, value);
        }

        @Override
        public String getType() {
            return "cache";
        }
    }

    // 消息队列适配器
    public static class MessageQueueAdapterFactory implements AdapterFactory {
        @Override
        public Adapter<?, ?> create(Object... params) {
            String mqType = params.length > 0 ? (String) params[0] : "rabbitmq";
            return new MessageQueueAdapter(mqType);
        }
    }

    public static class MessageQueueAdapter implements Adapter<Map<String, Object>, Boolean> {
        private final String mqType;
        private final BlockingQueue<Map<String, Object>> messageQueue = new LinkedBlockingQueue<>();

        public MessageQueueAdapter(String mqType) {
            this.mqType = mqType;
        }

        @Override
        public Boolean adapt(Map<String, Object> message) {
            System.out.println("Adapting message for " + mqType + " queue");
            try {
                messageQueue.put(message);
                return true;
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                return false;
            }
        }

        public Map<String, Object> receive() throws InterruptedException {
            return messageQueue.take();
        }

        @Override
        public String getType() {
            return "message_queue";
        }
    }

    // 支付网关适配器
    public static class PaymentAdapterFactory implements AdapterFactory {
        @Override
        public Adapter<?, ?> create(Object... params) {
            String gatewayType = params.length > 0 ? (String) params[0] : "stripe";
            return new PaymentAdapter(gatewayType);
        }
    }

    public static class PaymentAdapter implements Adapter<Map<String, Object>, Map<String, Object>> {
        private final String gatewayType;

        public PaymentAdapter(String gatewayType) {
            this.gatewayType = gatewayType;
        }

        @Override
        public Map<String, Object> adapt(Map<String, Object> paymentRequest) {
            System.out.println("Adapting payment request for " + gatewayType + " gateway");

            // 模拟支付处理
            Map<String, Object> response = new HashMap<>();
            response.put("status", "success");
            response.put("transaction_id", UUID.randomUUID().toString());
            response.put("gateway", gatewayType);
            response.put("amount", paymentRequest.get("amount"));
            response.put("currency", paymentRequest.get("currency"));

            return response;
        }

        @Override
        public String getType() {
            return "payment";
        }
    }

    // 邮件服务适配器
    public static class EmailAdapterFactory implements AdapterFactory {
        @Override
        public Adapter<?, ?> create(Object... params) {
            String emailType = params.length > 0 ? (String) params[0] : "smtp";
            return new EmailAdapter(emailType);
        }
    }

    public static class EmailAdapter implements Adapter<Map<String, Object>, Boolean> {
        private final String emailType;

        public EmailAdapter(String emailType) {
            this.emailType = emailType;
        }

        @Override
        public Boolean adapt(Map<String, Object> emailRequest) {
            System.out.println("Adapting email sending for " + emailType + " service");

            String to = (String) emailRequest.get("to");
            String subject = (String) emailRequest.get("subject");
            String body = (String) emailRequest.get("body");

            System.out.println("Sending email to: " + to);
            System.out.println("Subject: " + subject);
            System.out.println("Body: " + body.substring(0, Math.min(50, body.length())) + "...");

            // 模拟邮件发送
            return true;
        }

        @Override
        public String getType() {
            return "email";
        }
    }

    // 存储适配器
    public static class StorageAdapterFactory implements AdapterFactory {
        @Override
        public Adapter<?, ?> create(Object... params) {
            String storageType = params.length > 0 ? (String) params[0] : "s3";
            return new StorageAdapter(storageType);
        }
    }

    public static class StorageAdapter implements Adapter<byte[], String> {
        private final String storageType;
        private final Map<String, byte[]> storage = new ConcurrentHashMap<>();

        public StorageAdapter(String storageType) {
            this.storageType = storageType;
        }

        @Override
        public String adapt(byte[] data) {
            System.out.println("Adapting data storage for " + storageType);

            String key = UUID.randomUUID().toString();
            storage.put(key, data);

            return key;
        }

        public byte[] retrieve(String key) {
            return storage.get(key);
        }

        @Override
        public String getType() {
            return "storage";
        }
    }

    // 认证适配器
    public static class AuthenticationAdapterFactory implements AdapterFactory {
        @Override
        public Adapter<?, ?> create(Object... params) {
            String authType = params.length > 0 ? (String) params[0] : "oauth2";
            return new AuthenticationAdapter(authType);
        }
    }

    public static class AuthenticationAdapter implements Adapter<Map<String, Object>, Map<String, Object>> {
        private final String authType;

        public AuthenticationAdapter(String authType) {
            this.authType = authType;
        }

        @Override
        public Map<String, Object> adapt(Map<String, Object> authRequest) {
            System.out.println("Adapting authentication for " + authType);

            String username = (String) authRequest.get("username");
            String password = (String) authRequest.get("password");

            // 模拟认证
            Map<String, Object> response = new HashMap<>();
            if ("admin".equals(username) && "password".equals(password)) {
                response.put("authenticated", true);
                response.put("token", UUID.randomUUID().toString());
                response.put("user_id", "12345");
                response.put("roles", Arrays.asList("admin", "user"));
            } else {
                response.put("authenticated", false);
                response.put("error", "Invalid credentials");
            }

            return response;
        }

        @Override
        public String getType() {
            return "authentication";
        }
    }

    // 日志适配器
    public static class LoggingAdapterFactory implements AdapterFactory {
        @Override
        public Adapter<?, ?> create(Object... params) {
            String logType = params.length > 0 ? (String) params[0] : "log4j";
            return new LoggingAdapter(logType);
        }
    }

    public static class LoggingAdapter implements Adapter<Map<String, Object>, Void> {
        private final String logType;

        public LoggingAdapter(String logType) {
            this.logType = logType;
        }

        @Override
        public Void adapt(Map<String, Object> logEntry) {
            System.out.println("Adapting log entry for " + logType + " logger");

            String level = (String) logEntry.get("level");
            String message = (String) logEntry.get("message");
            String logger = (String) logEntry.getOrDefault("logger", "default");

            String formattedMessage = String.format("[%s] %s - %s: %s",
                Instant.now(),
                level.toUpperCase(),
                logger,
                message
            );

            System.out.println(formattedMessage);

            return null;
        }

        @Override
        public String getType() {
            return "logging";
        }
    }

    // 复合适配器 - 组合多个适配器
    public static class CompositeAdapter<T, U> implements Adapter<T, U> {
        private final List<Adapter<?, ?>> adapters;

        @SafeVarargs
        public CompositeAdapter(Adapter<? super T, ?>... adapters) {
            this.adapters = Arrays.asList(adapters);
        }

        @Override
        @SuppressWarnings("unchecked")
        public U adapt(T source) {
            Object result = source;
            for (Adapter adapter : adapters) {
                result = adapter.adapt(result);
            }
            return (U) result;
        }

        @Override
        public String getType() {
            return "composite";
        }
    }

    // 适配器链构建器
    public static class AdapterChainBuilder {
        private final List<AdapterFactory> factories = new ArrayList<>();
        private final List<Object[]> paramsList = new ArrayList<>();

        public AdapterChainBuilder addAdapter(String adapterType, Object... params) {
            AdapterFactory factory = AdapterManager.getInstance().adapterFactories.get(adapterType);
            if (factory != null) {
                factories.add(factory);
                paramsList.add(params);
            }
            return this;
        }

        public <T, U> Adapter<T, U> build() {
            List<Adapter<?, ?>> adapters = new ArrayList<>();
            for (int i = 0; i < factories.size(); i++) {
                adapters.add(factories.get(i).create(paramsList.get(i)));
            }
            return new CompositeAdapter<>(adapters.toArray(new Adapter[0]));
        }
    }

    // 静态方法用于创建适配器链
    public static <T, U> Adapter<T, U> createAdapterChain(String... adapterTypes) {
        AdapterChainBuilder builder = new AdapterChainBuilder();
        for (String type : adapterTypes) {
            builder.addAdapter(type);
        }
        return builder.build();
    }
}