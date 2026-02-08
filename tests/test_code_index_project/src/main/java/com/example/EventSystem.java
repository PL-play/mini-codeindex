package com.example;

import java.util.*;
import java.util.concurrent.*;
import java.util.concurrent.atomic.*;
import java.util.function.*;
import java.util.stream.*;

/**
 * 观察者模式实现
 * 事件驱动的系统架构
 */
public class EventSystem {

    // 单例模式
    private static volatile EventSystem instance;
    private static final Object LOCK = new Object();

    private final Map<String, List<EventListener<?>>> listeners;
    private final Map<String, EventQueue> eventQueues;
    private final ExecutorService executorService;
    private final Map<String, EventFilter> filters;
    private final Map<String, EventTransformer> transformers;

    private EventSystem() {
        this.listeners = new ConcurrentHashMap<>();
        this.eventQueues = new ConcurrentHashMap<>();
        this.executorService = Executors.newFixedThreadPool(10);
        this.filters = new ConcurrentHashMap<>();
        this.transformers = new ConcurrentHashMap<>();

        initializeDefaultEvents();
        startEventProcessor();
    }

    public static EventSystem getInstance() {
        if (instance == null) {
            synchronized (LOCK) {
                if (instance == null) {
                    instance = new EventSystem();
                }
            }
        }
        return instance;
    }

    /**
     * 初始化默认事件
     */
    private void initializeDefaultEvents() {
        // 用户相关事件
        registerEventType("user.created");
        registerEventType("user.updated");
        registerEventType("user.deleted");
        registerEventType("user.login");
        registerEventType("user.logout");

        // 系统事件
        registerEventType("system.startup");
        registerEventType("system.shutdown");
        registerEventType("system.error");

        // 数据事件
        registerEventType("data.processed");
        registerEventType("data.exported");
        registerEventType("data.imported");

        // 安全事件
        registerEventType("security.violation");
        registerEventType("security.login_failure");
        registerEventType("security.permission_denied");

        // 业务事件
        registerEventType("business.transaction_completed");
        registerEventType("business.report_generated");
        registerEventType("business.notification_sent");
    }

    /**
     * 注册事件类型
     */
    public void registerEventType(String eventType) {
        listeners.putIfAbsent(eventType, new CopyOnWriteArrayList<>());
        eventQueues.putIfAbsent(eventType, new EventQueue(eventType));
    }

    /**
     * 添加事件监听器
     */
    public <T> void addListener(String eventType, EventListener<T> listener) {
        listeners.computeIfAbsent(eventType, k -> new CopyOnWriteArrayList<>()).add(listener);
    }

    /**
     * 移除事件监听器
     */
    public <T> void removeListener(String eventType, EventListener<T> listener) {
        List<EventListener<?>> eventListeners = listeners.get(eventType);
        if (eventListeners != null) {
            eventListeners.remove(listener);
        }
    }

    /**
     * 发布事件
     */
    public <T> void publishEvent(String eventType, T data) {
        publishEvent(eventType, data, null);
    }

    /**
     * 发布事件（带上下文）
     */
    public <T> void publishEvent(String eventType, T data, Map<String, Object> context) {
        Event<T> event = new Event<>(eventType, data, context);

        // 应用过滤器
        EventFilter filter = filters.get(eventType);
        if (filter != null && !filter.accept(event)) {
            return;
        }

        // 应用转换器
        EventTransformer transformer = transformers.get(eventType);
        if (transformer != null) {
            event = transformer.transform(event);
        }

        // 添加到队列
        EventQueue queue = eventQueues.get(eventType);
        if (queue != null) {
            queue.add(event);
        }
    }

    /**
     * 同步发布事件
     */
    public <T> void publishEventSync(String eventType, T data) {
        publishEventSync(eventType, data, null);
    }

    /**
     * 同步发布事件（带上下文）
     */
    public <T> void publishEventSync(String eventType, T data, Map<String, Object> context) {
        Event<T> event = new Event<>(eventType, data, context);

        // 应用过滤器和转换器
        EventFilter filter = filters.get(eventType);
        if (filter != null && !filter.accept(event)) {
            return;
        }

        EventTransformer transformer = transformers.get(eventType);
        if (transformer != null) {
            event = transformer.transform(event);
        }

        // 直接通知监听器
        notifyListeners(event);
    }

    /**
     * 添加事件过滤器
     */
    public void addFilter(String eventType, EventFilter filter) {
        filters.put(eventType, filter);
    }

    /**
     * 添加事件转换器
     */
    public void addTransformer(String eventType, EventTransformer transformer) {
        transformers.put(eventType, transformer);
    }

    /**
     * 获取事件统计
     */
    public EventStatistics getStatistics(String eventType) {
        EventQueue queue = eventQueues.get(eventType);
        return queue != null ? queue.getStatistics() : new EventStatistics();
    }

    /**
     * 关闭事件系统
     */
    public void shutdown() {
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
     * 启动事件处理器
     */
    private void startEventProcessor() {
        executorService.submit(this::processEvents);
    }

    /**
     * 处理事件队列
     */
    private void processEvents() {
        while (!Thread.currentThread().isInterrupted()) {
            try {
                // 处理所有事件队列
                for (EventQueue queue : eventQueues.values()) {
                    Event<?> event = queue.poll();
                    if (event != null) {
                        notifyListeners(event);
                    }
                }

                // 短暂休眠避免CPU占用过高
                Thread.sleep(10);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                break;
            } catch (Exception e) {
                // 记录错误但继续处理
                System.err.println("Error processing events: " + e.getMessage());
            }
        }
    }

    /**
     * 通知监听器
     */
    @SuppressWarnings("unchecked")
    private <T> void notifyListeners(Event<T> event) {
        List<EventListener<?>> eventListeners = listeners.get(event.eventType);
        if (eventListeners != null) {
            for (EventListener<?> listener : eventListeners) {
                try {
                    executorService.submit(() -> {
                        try {
                            ((EventListener<T>) listener).onEvent(event);
                        } catch (Exception e) {
                            System.err.println("Error in event listener: " + e.getMessage());
                        }
                    });
                } catch (RejectedExecutionException e) {
                    // 线程池已关闭
                    break;
                }
            }
        }
    }

    // 事件类
    public static class Event<T> {
        public final String eventType;
        public final T data;
        public final Map<String, Object> context;
        public final long timestamp;
        public final String eventId;

        public Event(String eventType, T data, Map<String, Object> context) {
            this.eventType = eventType;
            this.data = data;
            this.context = context != null ? new HashMap<>(context) : new HashMap<>();
            this.timestamp = System.currentTimeMillis();
            this.eventId = UUID.randomUUID().toString();
        }

        @Override
        public String toString() {
            return String.format("Event{id='%s', type='%s', timestamp=%d}",
                               eventId, eventType, timestamp);
        }
    }

    // 事件监听器接口
    @FunctionalInterface
    public interface EventListener<T> {
        void onEvent(Event<T> event);
    }

    // 事件过滤器接口
    @FunctionalInterface
    public interface EventFilter {
        boolean accept(Event<?> event);
    }

    // 事件转换器接口
    @FunctionalInterface
    public interface EventTransformer {
        <T> Event<T> transform(Event<T> event);
    }

    // 事件队列
    private static class EventQueue {
        private final String eventType;
        private final BlockingQueue<Event<?>> queue;
        private final AtomicLong processedCount;
        private final AtomicLong errorCount;
        private final AtomicLong totalProcessingTime;

        public EventQueue(String eventType) {
            this.eventType = eventType;
            this.queue = new LinkedBlockingQueue<>(10000);
            this.processedCount = new AtomicLong(0);
            this.errorCount = new AtomicLong(0);
            this.totalProcessingTime = new AtomicLong(0);
        }

        public void add(Event<?> event) {
            if (!queue.offer(event)) {
                System.err.println("Event queue full for type: " + eventType);
            }
        }

        public Event<?> poll() {
            return queue.poll();
        }

        public EventStatistics getStatistics() {
            return new EventStatistics(
                processedCount.get(),
                errorCount.get(),
                queue.size(),
                totalProcessingTime.get() / Math.max(processedCount.get(), 1)
            );
        }
    }

    // 事件统计
    public static class EventStatistics {
        public final long processedCount;
        public final long errorCount;
        public final int queueSize;
        public final long averageProcessingTime;

        public EventStatistics() {
            this(0, 0, 0, 0);
        }

        public EventStatistics(long processedCount, long errorCount,
                             int queueSize, long averageProcessingTime) {
            this.processedCount = processedCount;
            this.errorCount = errorCount;
            this.queueSize = queueSize;
            this.averageProcessingTime = averageProcessingTime;
        }
    }

    // 预定义的事件监听器
    public static class LoggingEventListener implements EventListener<Object> {
        private final String loggerName;

        public LoggingEventListener(String loggerName) {
            this.loggerName = loggerName;
        }

        @Override
        public void onEvent(Event<Object> event) {
            System.out.println(String.format("[%s] Event: %s - %s",
                                           loggerName, event.eventType, event.data));
        }
    }

    public static class MetricsEventListener implements EventListener<Object> {
        private final Map<String, AtomicLong> metrics;

        public MetricsEventListener() {
            this.metrics = new ConcurrentHashMap<>();
        }

        @Override
        public void onEvent(Event<Object> event) {
            metrics.computeIfAbsent(event.eventType, k -> new AtomicLong(0)).incrementAndGet();
        }

        public long getMetric(String eventType) {
            return metrics.getOrDefault(eventType, new AtomicLong(0)).get();
        }
    }

    public static class ConditionalEventListener<T> implements EventListener<T> {
        private final Predicate<Event<T>> condition;
        private final Consumer<Event<T>> action;

        public ConditionalEventListener(Predicate<Event<T>> condition, Consumer<Event<T>> action) {
            this.condition = condition;
            this.action = action;
        }

        @Override
        public void onEvent(Event<T> event) {
            if (condition.test(event)) {
                action.accept(event);
            }
        }
    }

    // 事件过滤器实现
    public static class TypeBasedEventFilter implements EventFilter {
        private final Set<String> allowedTypes;

        public TypeBasedEventFilter(String... allowedTypes) {
            this.allowedTypes = new HashSet<>(Arrays.asList(allowedTypes));
        }

        @Override
        public boolean accept(Event<?> event) {
            return allowedTypes.contains(event.eventType);
        }
    }

    public static class ContextBasedEventFilter implements EventFilter {
        private final String key;
        private final Object expectedValue;

        public ContextBasedEventFilter(String key, Object expectedValue) {
            this.key = key;
            this.expectedValue = expectedValue;
        }

        @Override
        public boolean accept(Event<?> event) {
            return Objects.equals(event.context.get(key), expectedValue);
        }
    }

    // 事件转换器实现
    public static class DataTransformingEventTransformer implements EventTransformer {
        private final Function<Object, Object> transformer;

        public DataTransformingEventTransformer(Function<Object, Object> transformer) {
            this.transformer = transformer;
        }

        @Override
        @SuppressWarnings("unchecked")
        public <T> Event<T> transform(Event<T> event) {
            T transformedData = (T) transformer.apply(event.data);
            return new Event<>(event.eventType, transformedData, event.context);
        }
    }

    public static class ContextEnrichingEventTransformer implements EventTransformer {
        private final Map<String, Object> additionalContext;

        public ContextEnrichingEventTransformer(Map<String, Object> additionalContext) {
            this.additionalContext = additionalContext;
        }

        @Override
        @SuppressWarnings("unchecked")
        public <T> Event<T> transform(Event<T> event) {
            Map<String, Object> enrichedContext = new HashMap<>(event.context);
            enrichedContext.putAll(additionalContext);
            return new Event<>(event.eventType, event.data, enrichedContext);
        }
    }
}