package com.example;

import java.util.*;
import java.util.function.*;
import java.math.*;
import java.time.*;
import java.time.temporal.*;
import java.util.concurrent.*;
import java.util.stream.*;

/**
 * 策略模式实现
 * 各种算法和业务逻辑的策略集合
 */
public class StrategyManager {

    // 单例模式
    private static volatile StrategyManager instance;
    private static final Object LOCK = new Object();

    private final Map<String, StrategyFactory> strategyFactories;
    private final Map<String, Object> strategyCache;
    private final Map<String, StrategySelector> selectors;

    private StrategyManager() {
        this.strategyFactories = new ConcurrentHashMap<>();
        this.strategyCache = new ConcurrentHashMap<>();
        this.selectors = new ConcurrentHashMap<>();
        initializeDefaultStrategies();
    }

    public static StrategyManager getInstance() {
        if (instance == null) {
            synchronized (LOCK) {
                if (instance == null) {
                    instance = new StrategyManager();
                }
            }
        }
        return instance;
    }

    /**
     * 初始化默认策略
     */
    private void initializeDefaultStrategies() {
        // 排序策略
        registerStrategy("sorting", new SortingStrategyFactory());

        // 搜索策略
        registerStrategy("searching", new SearchingStrategyFactory());

        // 缓存策略
        registerStrategy("caching", new CachingStrategyFactory());

        // 通知策略
        registerStrategy("notification", new NotificationStrategyFactory());

        // 验证策略
        registerStrategy("validation", new ValidationStrategyFactory());

        // 定价策略
        registerStrategy("pricing", new PricingStrategyFactory());

        // 折扣策略
        registerStrategy("discount", new DiscountStrategyFactory());

        // 支付策略
        registerStrategy("payment", new PaymentStrategyFactory());

        // 报告策略
        registerStrategy("reporting", new ReportingStrategyFactory());

        // 压缩策略
        registerStrategy("compression", new CompressionStrategyFactory());
    }

    /**
     * 注册策略工厂
     */
    public void registerStrategy(String strategyType, StrategyFactory factory) {
        strategyFactories.put(strategyType, factory);
    }

    /**
     * 获取策略
     */
    @SuppressWarnings("unchecked")
    public <T> T getStrategy(String strategyType, String strategyName, Object... params) {
        String cacheKey = strategyType + ":" + strategyName + ":" + Arrays.toString(params);
        return (T) strategyCache.computeIfAbsent(cacheKey, key -> {
            StrategyFactory factory = strategyFactories.get(strategyType);
            if (factory == null) {
                throw new IllegalArgumentException("Strategy type not found: " + strategyType);
            }
            return factory.create(strategyName, params);
        });
    }

    /**
     * 注册策略选择器
     */
    public void registerSelector(String strategyType, StrategySelector selector) {
        selectors.put(strategyType, selector);
    }

    /**
     * 选择并获取策略
     */
    public <T> T selectStrategy(String strategyType, Map<String, Object> context) {
        StrategySelector selector = selectors.get(strategyType);
        if (selector == null) {
            throw new IllegalArgumentException("Strategy selector not found: " + strategyType);
        }

        String selectedStrategy = selector.select(context);
        return getStrategy(strategyType, selectedStrategy);
    }

    /**
     * 执行策略
     */
    public <T, R> R executeStrategy(String strategyType, String strategyName,
                                   T input, Object... params) {
        Strategy<T, R> strategy = getStrategy(strategyType, strategyName, params);
        return strategy.execute(input);
    }

    /**
     * 批量执行策略
     */
    public <T, R> List<R> executeStrategies(String strategyType, List<String> strategyNames,
                                          T input, Object... params) {
        return strategyNames.stream()
            .<R>map(name -> executeStrategy(strategyType, name, input, params))
            .collect(Collectors.toList());
    }

    /**
     * 链式执行策略
     */
    public <T, R> R executeStrategyChain(String strategyType, List<String> strategyNames,
                                       T input, Object... params) {
        Object result = input;
        for (String strategyName : strategyNames) {
            @SuppressWarnings("unchecked")
            Strategy<Object, Object> strategy = getStrategy(strategyType, strategyName, params);
            result = strategy.execute(result);
        }
        @SuppressWarnings("unchecked")
        R finalResult = (R) result;
        return finalResult;
    }

    // 策略接口
    public interface Strategy<T, R> {
        R execute(T input);
    }

    // 策略工厂接口
    public interface StrategyFactory {
        Object create(String strategyName, Object... params);
    }

    // 策略选择器接口
    public interface StrategySelector {
        String select(Map<String, Object> context);
    }

    // 排序策略
    public static class SortingStrategyFactory implements StrategyFactory {
        @Override
        public Object create(String strategyName, Object... params) {
            switch (strategyName) {
                case "bubble":
                    return (Strategy<List<Integer>, List<Integer>>) this::bubbleSort;
                case "quick":
                    return (Strategy<List<Integer>, List<Integer>>) this::quickSort;
                case "merge":
                    return (Strategy<List<Integer>, List<Integer>>) this::mergeSort;
                case "insertion":
                    return (Strategy<List<Integer>, List<Integer>>) this::insertionSort;
                default:
                    throw new IllegalArgumentException("Unknown sorting strategy: " + strategyName);
            }
        }

        private List<Integer> bubbleSort(List<Integer> list) {
            List<Integer> sorted = new ArrayList<>(list);
            for (int i = 0; i < sorted.size() - 1; i++) {
                for (int j = 0; j < sorted.size() - i - 1; j++) {
                    if (sorted.get(j) > sorted.get(j + 1)) {
                        Collections.swap(sorted, j, j + 1);
                    }
                }
            }
            return sorted;
        }

        private List<Integer> quickSort(List<Integer> list) {
            if (list.size() <= 1) return new ArrayList<>(list);

            int pivot = list.get(list.size() / 2);
            List<Integer> left = list.stream().filter(x -> x < pivot).collect(Collectors.toList());
            List<Integer> middle = list.stream().filter(x -> x == pivot).collect(Collectors.toList());
            List<Integer> right = list.stream().filter(x -> x > pivot).collect(Collectors.toList());

            List<Integer> result = new ArrayList<>();
            result.addAll(quickSort(left));
            result.addAll(middle);
            result.addAll(quickSort(right));
            return result;
        }

        private List<Integer> mergeSort(List<Integer> list) {
            if (list.size() <= 1) return new ArrayList<>(list);

            int mid = list.size() / 2;
            List<Integer> left = mergeSort(list.subList(0, mid));
            List<Integer> right = mergeSort(list.subList(mid, list.size()));

            return merge(left, right);
        }

        private List<Integer> merge(List<Integer> left, List<Integer> right) {
            List<Integer> result = new ArrayList<>();
            int i = 0, j = 0;

            while (i < left.size() && j < right.size()) {
                if (left.get(i) <= right.get(j)) {
                    result.add(left.get(i++));
                } else {
                    result.add(right.get(j++));
                }
            }

            result.addAll(left.subList(i, left.size()));
            result.addAll(right.subList(j, right.size()));
            return result;
        }

        private List<Integer> insertionSort(List<Integer> list) {
            List<Integer> sorted = new ArrayList<>(list);
            for (int i = 1; i < sorted.size(); i++) {
                int key = sorted.get(i);
                int j = i - 1;
                while (j >= 0 && sorted.get(j) > key) {
                    sorted.set(j + 1, sorted.get(j));
                    j--;
                }
                sorted.set(j + 1, key);
            }
            return sorted;
        }
    }

    // 搜索策略
    public static class SearchingStrategyFactory implements StrategyFactory {
        @Override
        public Object create(String strategyName, Object... params) {
            switch (strategyName) {
                case "linear":
                    return (Strategy<SearchInput, Integer>) this::linearSearch;
                case "binary":
                    return (Strategy<SearchInput, Integer>) this::binarySearch;
                case "interpolation":
                    return (Strategy<SearchInput, Integer>) this::interpolationSearch;
                default:
                    throw new IllegalArgumentException("Unknown searching strategy: " + strategyName);
            }
        }

        private Integer linearSearch(SearchInput input) {
            for (int i = 0; i < input.array.length; i++) {
                if (input.array[i] == input.target) {
                    return i;
                }
            }
            return -1;
        }

        private Integer binarySearch(SearchInput input) {
            int left = 0;
            int right = input.array.length - 1;

            while (left <= right) {
                int mid = left + (right - left) / 2;
                if (input.array[mid] == input.target) {
                    return mid;
                } else if (input.array[mid] < input.target) {
                    left = mid + 1;
                } else {
                    right = mid - 1;
                }
            }
            return -1;
        }

        private Integer interpolationSearch(SearchInput input) {
            int low = 0;
            int high = input.array.length - 1;

            while (low <= high && input.target >= input.array[low] &&
                   input.target <= input.array[high]) {
                if (low == high) {
                    if (input.array[low] == input.target) return low;
                    return -1;
                }

                int pos = low + (((high - low) / (input.array[high] - input.array[low])) *
                                (input.target - input.array[low]));

                if (input.array[pos] == input.target) {
                    return pos;
                } else if (input.array[pos] < input.target) {
                    low = pos + 1;
                } else {
                    high = pos - 1;
                }
            }
            return -1;
        }
    }

    // 缓存策略
    public static class CachingStrategyFactory implements StrategyFactory {
        @Override
        public Object create(String strategyName, Object... params) {
            switch (strategyName) {
                case "lru":
                    return new LRUCacheStrategy();
                case "lfu":
                    return new LFUCacheStrategy();
                case "fifo":
                    return new FIFOCacheStrategy();
                default:
                    throw new IllegalArgumentException("Unknown caching strategy: " + strategyName);
            }
        }
    }

    // 通知策略
    public static class NotificationStrategyFactory implements StrategyFactory {
        @Override
        public Object create(String strategyName, Object... params) {
            switch (strategyName) {
                case "email":
                    return (Strategy<NotificationData, Boolean>) data -> {
                        System.out.println("Sending email notification: " + data.message);
                        return true;
                    };
                case "sms":
                    return (Strategy<NotificationData, Boolean>) data -> {
                        System.out.println("Sending SMS notification: " + data.message);
                        return true;
                    };
                case "push":
                    return (Strategy<NotificationData, Boolean>) data -> {
                        System.out.println("Sending push notification: " + data.message);
                        return true;
                    };
                default:
                    throw new IllegalArgumentException("Unknown notification strategy: " + strategyName);
            }
        }
    }

    // 验证策略
    public static class ValidationStrategyFactory implements StrategyFactory {
        @Override
        public Object create(String strategyName, Object... params) {
            switch (strategyName) {
                case "email":
                    return (Strategy<String, Boolean>) email ->
                        email.matches("^[A-Za-z0-9+_.-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$");
                case "phone":
                    return (Strategy<String, Boolean>) phone ->
                        phone.matches("^\\+?[1-9]\\d{1,14}$");
                case "password":
                    return (Strategy<String, Boolean>) password ->
                        password.length() >= 8 &&
                        password.matches(".*[A-Z].*") &&
                        password.matches(".*[a-z].*") &&
                        password.matches(".*\\d.*");
                default:
                    throw new IllegalArgumentException("Unknown validation strategy: " + strategyName);
            }
        }
    }

    // 定价策略
    public static class PricingStrategyFactory implements StrategyFactory {
        @Override
        public Object create(String strategyName, Object... params) {
            switch (strategyName) {
                case "fixed":
                    return (Strategy<BigDecimal, BigDecimal>) price -> price;
                case "discount":
                    BigDecimal discountRate = params.length > 0 ?
                        (BigDecimal) params[0] : new BigDecimal("0.1");
                    return (Strategy<BigDecimal, BigDecimal>) price ->
                        price.subtract(price.multiply(discountRate));
                case "premium":
                    BigDecimal premiumRate = params.length > 0 ?
                        (BigDecimal) params[0] : new BigDecimal("0.2");
                    return (Strategy<BigDecimal, BigDecimal>) price ->
                        price.add(price.multiply(premiumRate));
                default:
                    throw new IllegalArgumentException("Unknown pricing strategy: " + strategyName);
            }
        }
    }

    // 折扣策略
    public static class DiscountStrategyFactory implements StrategyFactory {
        @Override
        public Object create(String strategyName, Object... params) {
            switch (strategyName) {
                case "percentage":
                    BigDecimal percentage = params.length > 0 ?
                        (BigDecimal) params[0] : new BigDecimal("10");
                    return (Strategy<BigDecimal, BigDecimal>) price ->
                        price.subtract(price.multiply(percentage.divide(new BigDecimal("100"))));
                case "fixed":
                    BigDecimal fixedAmount = params.length > 0 ?
                        (BigDecimal) params[0] : new BigDecimal("5");
                    return (Strategy<BigDecimal, BigDecimal>) price ->
                        price.subtract(fixedAmount).max(BigDecimal.ZERO);
                case "bulk":
                    return (Strategy<BulkDiscountInput, BigDecimal>) input -> {
                        BigDecimal discount = BigDecimal.ZERO;
                        if (input.quantity >= 10) discount = new BigDecimal("0.1");
                        if (input.quantity >= 50) discount = new BigDecimal("0.2");
                        if (input.quantity >= 100) discount = new BigDecimal("0.3");
                        return input.unitPrice.multiply(new BigDecimal(input.quantity))
                            .multiply(BigDecimal.ONE.subtract(discount));
                    };
                default:
                    throw new IllegalArgumentException("Unknown discount strategy: " + strategyName);
            }
        }
    }

    // 支付策略
    public static class PaymentStrategyFactory implements StrategyFactory {
        @Override
        public Object create(String strategyName, Object... params) {
            switch (strategyName) {
                case "credit_card":
                    return (Strategy<PaymentData, PaymentResult>) data -> {
                        // 模拟信用卡支付
                        boolean success = data.amount.compareTo(new BigDecimal("10000")) <= 0;
                        return new PaymentResult(success, success ? "Payment approved" : "Payment declined");
                    };
                case "paypal":
                    return (Strategy<PaymentData, PaymentResult>) data -> {
                        // 模拟PayPal支付
                        boolean success = data.amount.compareTo(new BigDecimal("5000")) <= 0;
                        return new PaymentResult(success, success ? "PayPal payment successful" : "PayPal payment failed");
                    };
                case "bank_transfer":
                    return (Strategy<PaymentData, PaymentResult>) data -> {
                        // 模拟银行转账
                        return new PaymentResult(true, "Bank transfer initiated");
                    };
                default:
                    throw new IllegalArgumentException("Unknown payment strategy: " + strategyName);
            }
        }
    }

    // 报告策略
    public static class ReportingStrategyFactory implements StrategyFactory {
        @Override
        public Object create(String strategyName, Object... params) {
            switch (strategyName) {
                case "summary":
                    return (Strategy<List<Map<String, Object>>, String>) data -> {
                        StringBuilder report = new StringBuilder();
                        report.append("Summary Report\n");
                        report.append("Total Records: ").append(data.size()).append("\n");
                        // 更多摘要逻辑...
                        return report.toString();
                    };
                case "detailed":
                    return (Strategy<List<Map<String, Object>>, String>) data -> {
                        StringBuilder report = new StringBuilder();
                        report.append("Detailed Report\n");
                        for (Map<String, Object> record : data) {
                            report.append("Record: ").append(record).append("\n");
                        }
                        return report.toString();
                    };
                case "chart":
                    return (Strategy<List<Map<String, Object>>, String>) data -> {
                        // 模拟图表生成
                        return "Chart data would be generated here";
                    };
                default:
                    throw new IllegalArgumentException("Unknown reporting strategy: " + strategyName);
            }
        }
    }

    // 压缩策略
    public static class CompressionStrategyFactory implements StrategyFactory {
        @Override
        public Object create(String strategyName, Object... params) {
            switch (strategyName) {
                case "gzip":
                    return (Strategy<byte[], byte[]>) data -> {
                        // 模拟GZIP压缩
                        return ("COMPRESSED:" + new String(data)).getBytes();
                    };
                case "deflate":
                    return (Strategy<byte[], byte[]>) data -> {
                        // 模拟DEFLATE压缩
                        return ("DEFLATED:" + new String(data)).getBytes();
                    };
                case "lz4":
                    return (Strategy<byte[], byte[]>) data -> {
                        // 模拟LZ4压缩
                        return ("LZ4:" + new String(data)).getBytes();
                    };
                default:
                    throw new IllegalArgumentException("Unknown compression strategy: " + strategyName);
            }
        }
    }

    // 缓存策略实现
    public interface CacheStrategy extends Strategy<Object, Object> {
        boolean contains(Object key);
        void put(Object key, Object value);
        Object get(Object key);
        void remove(Object key);
        void clear();
        int size();
    }

    public static class LRUCacheStrategy implements CacheStrategy {
        private final LinkedHashMap<Object, Object> cache;
        private final int capacity;

        public LRUCacheStrategy(int capacity) {
            this.capacity = capacity;
            this.cache = new LinkedHashMap<Object, Object>(capacity, 0.75f, true) {
                @Override
                protected boolean removeEldestEntry(Map.Entry<Object, Object> eldest) {
                    return size() > capacity;
                }
            };
        }

        public LRUCacheStrategy() {
            this(100);
        }

        @Override
        public Object execute(Object input) {
            return get(input);
        }

        @Override
        public boolean contains(Object key) {
            return cache.containsKey(key);
        }

        @Override
        public void put(Object key, Object value) {
            cache.put(key, value);
        }

        @Override
        public Object get(Object key) {
            return cache.get(key);
        }

        @Override
        public void remove(Object key) {
            cache.remove(key);
        }

        @Override
        public void clear() {
            cache.clear();
        }

        @Override
        public int size() {
            return cache.size();
        }
    }

    public static class LFUCacheStrategy implements CacheStrategy {
        private final Map<Object, Object> cache;
        private final Map<Object, Integer> frequency;
        private final int capacity;

        public LFUCacheStrategy(int capacity) {
            this.capacity = capacity;
            this.cache = new HashMap<>();
            this.frequency = new HashMap<>();
        }

        public LFUCacheStrategy() {
            this(100);
        }

        @Override
        public Object execute(Object input) {
            return get(input);
        }

        @Override
        public boolean contains(Object key) {
            return cache.containsKey(key);
        }

        @Override
        public void put(Object key, Object value) {
            if (cache.size() >= capacity && !cache.containsKey(key)) {
                // 移除访问频率最低的项目
                Object leastFrequent = frequency.entrySet().stream()
                    .min(Map.Entry.comparingByValue())
                    .map(Map.Entry::getKey)
                    .orElse(null);
                if (leastFrequent != null) {
                    cache.remove(leastFrequent);
                    frequency.remove(leastFrequent);
                }
            }
            cache.put(key, value);
            frequency.put(key, frequency.getOrDefault(key, 0) + 1);
        }

        @Override
        public Object get(Object key) {
            if (cache.containsKey(key)) {
                frequency.put(key, frequency.get(key) + 1);
                return cache.get(key);
            }
            return null;
        }

        @Override
        public void remove(Object key) {
            cache.remove(key);
            frequency.remove(key);
        }

        @Override
        public void clear() {
            cache.clear();
            frequency.clear();
        }

        @Override
        public int size() {
            return cache.size();
        }
    }

    public static class FIFOCacheStrategy implements CacheStrategy {
        private final Map<Object, Object> cache;
        private final Deque<Object> order;
        private final int capacity;

        public FIFOCacheStrategy(int capacity) {
            this.capacity = capacity;
            this.cache = new HashMap<>();
            this.order = new LinkedList<>();
        }

        public FIFOCacheStrategy() {
            this(100);
        }

        @Override
        public Object execute(Object input) {
            return get(input);
        }

        @Override
        public boolean contains(Object key) {
            return cache.containsKey(key);
        }

        @Override
        public void put(Object key, Object value) {
            if (!cache.containsKey(key)) {
                if (cache.size() >= capacity) {
                    Object oldest = order.removeFirst();
                    cache.remove(oldest);
                }
                order.addLast(key);
            }
            cache.put(key, value);
        }

        @Override
        public Object get(Object key) {
            return cache.get(key);
        }

        @Override
        public void remove(Object key) {
            cache.remove(key);
            order.remove(key);
        }

        @Override
        public void clear() {
            cache.clear();
            order.clear();
        }

        @Override
        public int size() {
            return cache.size();
        }
    }

    // 数据类
    public static class SearchInput {
        public final int[] array;
        public final int target;

        public SearchInput(int[] array, int target) {
            this.array = array;
            this.target = target;
        }
    }

    public static class NotificationData {
        public final String recipient;
        public final String message;
        public final String type;

        public NotificationData(String recipient, String message, String type) {
            this.recipient = recipient;
            this.message = message;
            this.type = type;
        }
    }

    public static class BulkDiscountInput {
        public final BigDecimal unitPrice;
        public final int quantity;

        public BulkDiscountInput(BigDecimal unitPrice, int quantity) {
            this.unitPrice = unitPrice;
            this.quantity = quantity;
        }
    }

    public static class PaymentData {
        public final BigDecimal amount;
        public final String currency;
        public final String method;

        public PaymentData(BigDecimal amount, String currency, String method) {
            this.amount = amount;
            this.currency = currency;
            this.method = method;
        }
    }

    public static class PaymentResult {
        public final boolean success;
        public final String message;

        public PaymentResult(boolean success, String message) {
            this.success = success;
            this.message = message;
        }
    }
}