package com.example;

import java.util.*;
import java.util.function.*;
import java.util.stream.*;
import java.time.*;
import java.time.format.*;
import java.time.temporal.*;
import java.math.*;
import java.math.RoundingMode;
import java.util.concurrent.*;
import java.util.concurrent.atomic.*;
import java.util.regex.*;
import java.io.*;

/**
 * 高级工具类集合
 * 包含各种实用工具函数和辅助类
 */
public class AdvancedUtils {

    // 时间处理工具
    public static class TimeUtils {
        private static final DateTimeFormatter ISO_FORMATTER =
            DateTimeFormatter.ofPattern("yyyy-MM-dd'T'HH:mm:ss.SSS'Z'");

        public static String formatTimestamp(LocalDateTime timestamp) {
            return timestamp.atZone(ZoneId.systemDefault()).format(ISO_FORMATTER);
        }

        public static LocalDateTime parseTimestamp(String timestamp) {
            return LocalDateTime.parse(timestamp, ISO_FORMATTER);
        }

        public static long calculateDuration(LocalDateTime start, LocalDateTime end) {
            return Duration.between(start, end).toMillis();
        }

        public static String formatDuration(long milliseconds) {
            Duration duration = Duration.ofMillis(milliseconds);
            long hours = duration.toHours();
            long minutes = duration.toMinutes() % 60;
            long seconds = duration.getSeconds() % 60;
            long millis = duration.toMillis() % 1000;

            return String.format("%02d:%02d:%02d.%03d", hours, minutes, seconds, millis);
        }

        public static LocalDateTime getBusinessDay(LocalDateTime dateTime, int offset) {
            LocalDateTime result = dateTime;
            int days = Math.abs(offset);
            int direction = offset > 0 ? 1 : -1;

            for (int i = 0; i < days; i++) {
                result = result.plusDays(direction);
                while (isWeekend(result.toLocalDate())) {
                    result = result.plusDays(direction);
                }
            }

            return result;
        }

        private static boolean isWeekend(LocalDate date) {
            DayOfWeek day = date.getDayOfWeek();
            return day == DayOfWeek.SATURDAY || day == DayOfWeek.SUNDAY;
        }

        public static List<LocalDate> getBusinessDays(LocalDate start, LocalDate end) {
            List<LocalDate> businessDays = new ArrayList<>();
            LocalDate current = start;

            while (!current.isAfter(end)) {
                if (!isWeekend(current)) {
                    businessDays.add(current);
                }
                current = current.plusDays(1);
            }

            return businessDays;
        }
    }

    // 字符串处理工具
    public static class StringUtils {
        private static final Pattern EMAIL_PATTERN =
            Pattern.compile("^[A-Za-z0-9+_.-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$");

        private static final Pattern PHONE_PATTERN =
            Pattern.compile("^\\+?[1-9]\\d{1,14}$");

        public static boolean isNullOrEmpty(String str) {
            return str == null || str.trim().isEmpty();
        }

        public static boolean isNotNullOrEmpty(String str) {
            return !isNullOrEmpty(str);
        }

        public static String capitalize(String str) {
            if (isNullOrEmpty(str)) return str;
            return str.substring(0, 1).toUpperCase() + str.substring(1).toLowerCase();
        }

        public static String camelCase(String str) {
            if (isNullOrEmpty(str)) return str;
            String[] parts = str.split("[\\s_-]+");
            return Arrays.stream(parts)
                .filter(StringUtils::isNotNullOrEmpty)
                .map(StringUtils::capitalize)
                .collect(Collectors.joining());
        }

        public static String snakeCase(String str) {
            if (isNullOrEmpty(str)) return str;
            return str.replaceAll("([a-z])([A-Z])", "$1_$2")
                     .replaceAll("[\\s-]+", "_")
                     .toLowerCase();
        }

        public static String kebabCase(String str) {
            if (isNullOrEmpty(str)) return str;
            return snakeCase(str).replace("_", "-");
        }

        public static boolean isValidEmail(String email) {
            return isNotNullOrEmpty(email) && EMAIL_PATTERN.matcher(email).matches();
        }

        public static boolean isValidPhone(String phone) {
            return isNotNullOrEmpty(phone) && PHONE_PATTERN.matcher(phone).matches();
        }

        public static String maskSensitiveData(String data, int visibleChars) {
            if (isNullOrEmpty(data) || data.length() <= visibleChars) return data;
            int maskLength = data.length() - visibleChars;
            String visible = data.substring(0, visibleChars / 2) +
                           "*".repeat(maskLength) +
                           data.substring(data.length() - visibleChars / 2);
            return visible;
        }

        public static String generateSlug(String text) {
            if (isNullOrEmpty(text)) return "";
            return text.toLowerCase()
                      .replaceAll("[^a-z0-9\\s-]", "")
                      .replaceAll("\\s+", "-")
                      .replaceAll("-+", "-")
                      .replaceAll("^-|-$", "");
        }

        public static double calculateSimilarity(String str1, String str2) {
            if (str1 == null || str2 == null) return 0.0;
            if (str1.equals(str2)) return 1.0;

            int len1 = str1.length();
            int len2 = str2.length();
            if (len1 == 0 || len2 == 0) return 0.0;

            int maxLen = Math.max(len1, len2);
            int distance = levenshteinDistance(str1, str2);
            return 1.0 - (double) distance / maxLen;
        }

        private static int levenshteinDistance(String str1, String str2) {
            int[][] dp = new int[str1.length() + 1][str2.length() + 1];

            for (int i = 0; i <= str1.length(); i++) {
                dp[i][0] = i;
            }
            for (int j = 0; j <= str2.length(); j++) {
                dp[0][j] = j;
            }

            for (int i = 1; i <= str1.length(); i++) {
                for (int j = 1; j <= str2.length(); j++) {
                    int cost = str1.charAt(i - 1) == str2.charAt(j - 1) ? 0 : 1;
                    dp[i][j] = Math.min(
                        Math.min(dp[i - 1][j] + 1, dp[i][j - 1] + 1),
                        dp[i - 1][j - 1] + cost
                    );
                }
            }

            return dp[str1.length()][str2.length()];
        }
    }

    // 数学计算工具
    public static class MathUtils {
        private static final BigDecimal HUNDRED = new BigDecimal("100");

        public static BigDecimal calculatePercentage(BigDecimal value, BigDecimal total) {
            if (total.compareTo(BigDecimal.ZERO) == 0) return BigDecimal.ZERO;
            return value.divide(total, 4, RoundingMode.HALF_UP)
                       .multiply(HUNDRED);
        }

        public static BigDecimal calculateCompoundInterest(BigDecimal principal,
                                                         BigDecimal rate,
                                                         int periods) {
            BigDecimal factor = BigDecimal.ONE.add(rate.divide(HUNDRED, 6, RoundingMode.HALF_UP));
            return principal.multiply(factor.pow(periods));
        }

        public static BigDecimal calculateStandardDeviation(List<BigDecimal> values) {
            if (values.isEmpty()) return BigDecimal.ZERO;

            BigDecimal mean = values.stream()
                .reduce(BigDecimal.ZERO, BigDecimal::add)
                .divide(new BigDecimal(values.size()), 6, RoundingMode.HALF_UP);

            BigDecimal variance = values.stream()
                .map(v -> v.subtract(mean).pow(2))
                .reduce(BigDecimal.ZERO, BigDecimal::add)
                .divide(new BigDecimal(values.size()), 6, RoundingMode.HALF_UP);

            return BigDecimal.valueOf(Math.sqrt(variance.doubleValue()));
        }

        public static BigDecimal calculateMovingAverage(List<BigDecimal> values, int windowSize) {
            if (values.size() < windowSize) return BigDecimal.ZERO;

            return values.subList(values.size() - windowSize, values.size())
                .stream()
                .reduce(BigDecimal.ZERO, BigDecimal::add)
                .divide(new BigDecimal(windowSize), 2, RoundingMode.HALF_UP);
        }

        public static List<BigDecimal> generateFibonacciSequence(int count) {
            List<BigDecimal> sequence = new ArrayList<>();
            if (count >= 1) sequence.add(BigDecimal.ONE);
            if (count >= 2) sequence.add(BigDecimal.ONE);

            for (int i = 2; i < count; i++) {
                BigDecimal next = sequence.get(i - 1).add(sequence.get(i - 2));
                sequence.add(next);
            }

            return sequence;
        }

        public static boolean isPrime(int number) {
            if (number <= 1) return false;
            if (number <= 3) return true;
            if (number % 2 == 0 || number % 3 == 0) return false;

            for (int i = 5; i * i <= number; i += 6) {
                if (number % i == 0 || number % (i + 2) == 0) return false;
            }

            return true;
        }

        public static List<Integer> getPrimeFactors(int number) {
            List<Integer> factors = new ArrayList<>();
            if (number <= 1) return factors;

            // Check for 2
            while (number % 2 == 0) {
                factors.add(2);
                number /= 2;
            }

            // Check for odd factors
            for (int i = 3; i * i <= number; i += 2) {
                while (number % i == 0) {
                    factors.add(i);
                    number /= i;
                }
            }

            // If number is a prime number greater than 2
            if (number > 2) {
                factors.add(number);
            }

            return factors;
        }
    }

    // 集合操作工具
    public static class CollectionUtils {
        public static <T> List<T> distinct(List<T> list) {
            return list.stream().distinct().collect(Collectors.toList());
        }

        public static <T> List<T> intersection(List<T> list1, List<T> list2) {
            Set<T> set1 = new HashSet<>(list1);
            return list2.stream()
                       .filter(set1::contains)
                       .collect(Collectors.toList());
        }

        public static <T> List<T> union(List<T> list1, List<T> list2) {
            Set<T> result = new HashSet<>(list1);
            result.addAll(list2);
            return new ArrayList<>(result);
        }

        public static <T> List<T> difference(List<T> list1, List<T> list2) {
            Set<T> set2 = new HashSet<>(list2);
            return list1.stream()
                       .filter(item -> !set2.contains(item))
                       .collect(Collectors.toList());
        }

        public static <T, K> Map<K, List<T>> groupBy(List<T> list, Function<T, K> keyExtractor) {
            return list.stream().collect(Collectors.groupingBy(keyExtractor));
        }

        public static <T, K, V> Map<K, V> toMap(List<T> list,
                                              Function<T, K> keyExtractor,
                                              Function<T, V> valueExtractor) {
            return list.stream().collect(Collectors.toMap(keyExtractor, valueExtractor));
        }

        public static <T> List<T> filter(List<T> list, Predicate<T> predicate) {
            return list.stream().filter(predicate).collect(Collectors.toList());
        }

        public static <T, R> List<R> map(List<T> list, Function<T, R> mapper) {
            return list.stream().map(mapper).collect(Collectors.toList());
        }

        public static <T> Optional<T> findFirst(List<T> list, Predicate<T> predicate) {
            return list.stream().filter(predicate).findFirst();
        }

        public static <T> boolean anyMatch(List<T> list, Predicate<T> predicate) {
            return list.stream().anyMatch(predicate);
        }

        public static <T> boolean allMatch(List<T> list, Predicate<T> predicate) {
            return list.stream().allMatch(predicate);
        }

        public static <T> boolean noneMatch(List<T> list, Predicate<T> predicate) {
            return list.stream().noneMatch(predicate);
        }

        public static <T extends Comparable<T>> List<T> sort(List<T> list) {
            return list.stream().sorted().collect(Collectors.toList());
        }

        public static <T> List<T> sort(List<T> list, Comparator<T> comparator) {
            return list.stream().sorted(comparator).collect(Collectors.toList());
        }

        public static <T> List<T> reverse(List<T> list) {
            List<T> reversed = new ArrayList<>(list);
            Collections.reverse(reversed);
            return reversed;
        }

        public static <T> List<List<T>> partition(List<T> list, int size) {
            List<List<T>> partitions = new ArrayList<>();
            for (int i = 0; i < list.size(); i += size) {
                partitions.add(list.subList(i, Math.min(i + size, list.size())));
            }
            return partitions;
        }

        public static <T> T getRandomElement(List<T> list) {
            if (list.isEmpty()) return null;
            return list.get(ThreadLocalRandom.current().nextInt(list.size()));
        }

        public static <T> List<T> shuffle(List<T> list) {
            List<T> shuffled = new ArrayList<>(list);
            Collections.shuffle(shuffled);
            return shuffled;
        }
    }

    // 验证工具
    public static class ValidationUtils {
        public static ValidationResult validateEmail(String email) {
            if (StringUtils.isNullOrEmpty(email)) {
                return new ValidationResult(false, "Email is required");
            }
            if (!StringUtils.isValidEmail(email)) {
                return new ValidationResult(false, "Invalid email format");
            }
            return new ValidationResult(true, null);
        }

        public static ValidationResult validatePhone(String phone) {
            if (StringUtils.isNullOrEmpty(phone)) {
                return new ValidationResult(false, "Phone is required");
            }
            if (!StringUtils.isValidPhone(phone)) {
                return new ValidationResult(false, "Invalid phone format");
            }
            return new ValidationResult(true, null);
        }

        public static ValidationResult validatePassword(String password) {
            if (StringUtils.isNullOrEmpty(password)) {
                return new ValidationResult(false, "Password is required");
            }
            if (password.length() < 8) {
                return new ValidationResult(false, "Password must be at least 8 characters");
            }
            if (!password.matches(".*[A-Z].*")) {
                return new ValidationResult(false, "Password must contain uppercase letter");
            }
            if (!password.matches(".*[a-z].*")) {
                return new ValidationResult(false, "Password must contain lowercase letter");
            }
            if (!password.matches(".*\\d.*")) {
                return new ValidationResult(false, "Password must contain digit");
            }
            return new ValidationResult(true, null);
        }

        public static ValidationResult validateRange(double value, double min, double max) {
            if (value < min) {
                return new ValidationResult(false, String.format("Value must be >= %.2f", min));
            }
            if (value > max) {
                return new ValidationResult(false, String.format("Value must be <= %.2f", max));
            }
            return new ValidationResult(true, null);
        }

        public static ValidationResult validateLength(String text, int minLength, int maxLength) {
            if (text == null) {
                return new ValidationResult(false, "Text cannot be null");
            }
            if (text.length() < minLength) {
                return new ValidationResult(false,
                    String.format("Text must be at least %d characters", minLength));
            }
            if (text.length() > maxLength) {
                return new ValidationResult(false,
                    String.format("Text must be at most %d characters", maxLength));
            }
            return new ValidationResult(true, null);
        }

        public static ValidationResult validateNotNull(Object obj, String fieldName) {
            if (obj == null) {
                return new ValidationResult(false, fieldName + " cannot be null");
            }
            return new ValidationResult(true, null);
        }

        public static ValidationResult validateNotEmpty(Collection<?> collection, String fieldName) {
            if (collection == null) {
                return new ValidationResult(false, fieldName + " cannot be null");
            }
            if (collection.isEmpty()) {
                return new ValidationResult(false, fieldName + " cannot be empty");
            }
            return new ValidationResult(true, null);
        }

        public static class ValidationResult {
            public final boolean valid;
            public final String errorMessage;

            public ValidationResult(boolean valid, String errorMessage) {
                this.valid = valid;
                this.errorMessage = errorMessage;
            }

            public boolean isValid() {
                return valid;
            }

            public String getErrorMessage() {
                return errorMessage;
            }
        }
    }

    // 并发工具
    public static class ConcurrencyUtils {
        private static final ScheduledExecutorService DEFAULT_EXECUTOR =
            Executors.newScheduledThreadPool(4, r -> {
                Thread t = new Thread(r);
                t.setDaemon(true);
                return t;
            });

        public static <T> CompletableFuture<T> async(Supplier<T> supplier) {
            return CompletableFuture.supplyAsync(supplier, DEFAULT_EXECUTOR);
        }

        public static <T> CompletableFuture<T> async(Supplier<T> supplier, Executor executor) {
            return CompletableFuture.supplyAsync(supplier, executor);
        }

        public static CompletableFuture<Void> async(Runnable runnable) {
            return CompletableFuture.runAsync(runnable, DEFAULT_EXECUTOR);
        }

        public static CompletableFuture<Void> async(Runnable runnable, Executor executor) {
            return CompletableFuture.runAsync(runnable, executor);
        }

        public static <T> CompletableFuture<List<T>> allOf(List<CompletableFuture<T>> futures) {
            return CompletableFuture.allOf(futures.toArray(new CompletableFuture[0]))
                .thenApply(v -> futures.stream()
                    .map(CompletableFuture::join)
                    .collect(Collectors.toList()));
        }

        public static <T> CompletableFuture<T> anyOf(List<CompletableFuture<T>> futures) {
            return CompletableFuture.anyOf(futures.toArray(new CompletableFuture[0]))
                .thenApply(result -> (T) result);
        }

        public static <T> CompletableFuture<T> withTimeout(CompletableFuture<T> future,
                                                          long timeout, TimeUnit unit) {
            CompletableFuture<T> timeoutFuture = new CompletableFuture<>();
            DEFAULT_EXECUTOR.schedule(new Runnable() {
                @Override
                public void run() {
                    if (!future.isDone()) {
                        timeoutFuture.completeExceptionally(new TimeoutException());
                    }
                }
            }, timeout, unit);
            return future.applyToEither(timeoutFuture, Function.identity());
        }

        public static <T> CompletableFuture<T> retry(Supplier<CompletableFuture<T>> operation,
                                                    int maxRetries, long delayMillis) {
            return operation.get().exceptionally(e -> {
                if (maxRetries > 0) {
                    try {
                        Thread.sleep(delayMillis);
                    } catch (InterruptedException ie) {
                        Thread.currentThread().interrupt();
                        throw new RuntimeException(ie);
                    }
                    return retry(operation, maxRetries - 1, delayMillis * 2).join();
                }
                throw new RuntimeException(e);
            });
        }

        public static class CircuitBreaker {
            private final int failureThreshold;
            private final long timeoutMillis;
            private final AtomicInteger failureCount = new AtomicInteger(0);
            private final AtomicLong lastFailureTime = new AtomicLong(0);
            private volatile boolean open = false;

            public CircuitBreaker(int failureThreshold, long timeoutMillis) {
                this.failureThreshold = failureThreshold;
                this.timeoutMillis = timeoutMillis;
            }

            public <T> T execute(Supplier<T> operation) throws Exception {
                if (open) {
                    if (System.currentTimeMillis() - lastFailureTime.get() > timeoutMillis) {
                        open = false;
                        failureCount.set(0);
                    } else {
                        throw new RuntimeException("Circuit breaker is open");
                    }
                }

                try {
                    T result = operation.get();
                    failureCount.set(0);
                    return result;
                } catch (Exception e) {
                    if (failureCount.incrementAndGet() >= failureThreshold) {
                        open = true;
                        lastFailureTime.set(System.currentTimeMillis());
                    }
                    throw e;
                }
            }
        }

        public static class RateLimiter {
            private final int permitsPerSecond;
            private final AtomicLong nextAvailableTime = new AtomicLong(0);

            public RateLimiter(int permitsPerSecond) {
                this.permitsPerSecond = permitsPerSecond;
            }

            public boolean tryAcquire() {
                long now = System.nanoTime();
                long nextTime = nextAvailableTime.get();

                if (now >= nextTime) {
                    long interval = 1_000_000_000L / permitsPerSecond;
                    return nextAvailableTime.compareAndSet(nextTime, now + interval);
                }

                return false;
            }

            public void acquire() throws InterruptedException {
                long now = System.nanoTime();
                long nextTime = nextAvailableTime.get();

                if (now < nextTime) {
                    long sleepTime = (nextTime - now) / 1_000_000;
                    Thread.sleep(sleepTime);
                }

                long interval = 1_000_000_000L / permitsPerSecond;
                nextAvailableTime.addAndGet(interval);
            }
        }
    }

    // 文件操作工具
    public static class FileUtils {
        public static String readFile(String filePath) throws IOException {
            return new String(java.nio.file.Files.readAllBytes(java.nio.file.Paths.get(filePath)));
        }

        public static void writeFile(String filePath, String content) throws IOException {
            java.nio.file.Files.write(java.nio.file.Paths.get(filePath), content.getBytes());
        }

        public static void appendFile(String filePath, String content) throws IOException {
            java.nio.file.Files.write(java.nio.file.Paths.get(filePath),
                content.getBytes(), java.nio.file.StandardOpenOption.APPEND);
        }

        public static boolean fileExists(String filePath) {
            return java.nio.file.Files.exists(java.nio.file.Paths.get(filePath));
        }

        public static long getFileSize(String filePath) throws IOException {
            return java.nio.file.Files.size(java.nio.file.Paths.get(filePath));
        }

        public static String getFileExtension(String fileName) {
            int lastDotIndex = fileName.lastIndexOf('.');
            return lastDotIndex > 0 ? fileName.substring(lastDotIndex + 1) : "";
        }

        public static String getFileNameWithoutExtension(String fileName) {
            int lastDotIndex = fileName.lastIndexOf('.');
            return lastDotIndex > 0 ? fileName.substring(0, lastDotIndex) : fileName;
        }

        public static List<String> listFiles(String directory) throws IOException {
            return java.nio.file.Files.list(java.nio.file.Paths.get(directory))
                .map(path -> path.toString())
                .collect(Collectors.toList());
        }

        public static List<String> listFilesRecursive(String directory) throws IOException {
            return java.nio.file.Files.walk(java.nio.file.Paths.get(directory))
                .filter(java.nio.file.Files::isRegularFile)
                .map(path -> path.toString())
                .collect(Collectors.toList());
        }

        public static void createDirectory(String directory) throws IOException {
            java.nio.file.Files.createDirectories(java.nio.file.Paths.get(directory));
        }

        public static void deleteFile(String filePath) throws IOException {
            java.nio.file.Files.delete(java.nio.file.Paths.get(filePath));
        }

        public static void copyFile(String source, String destination) throws IOException {
            java.nio.file.Files.copy(java.nio.file.Paths.get(source),
                java.nio.file.Paths.get(destination),
                java.nio.file.StandardCopyOption.REPLACE_EXISTING);
        }

        public static void moveFile(String source, String destination) throws IOException {
            java.nio.file.Files.move(java.nio.file.Paths.get(source),
                java.nio.file.Paths.get(destination),
                java.nio.file.StandardCopyOption.REPLACE_EXISTING);
        }
    }

    // 加密工具
    public static class CryptoUtils {
        private static final String ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";

        public static String caesarEncrypt(String text, int shift) {
            StringBuilder result = new StringBuilder();
            for (char c : text.toUpperCase().toCharArray()) {
                if (Character.isLetter(c)) {
                    int index = ALPHABET.indexOf(c);
                    int newIndex = (index + shift) % ALPHABET.length();
                    result.append(ALPHABET.charAt(newIndex));
                } else {
                    result.append(c);
                }
            }
            return result.toString();
        }

        public static String caesarDecrypt(String text, int shift) {
            return caesarEncrypt(text, -shift);
        }

        public static String generateChecksum(String data) {
            int checksum = 0;
            for (char c : data.toCharArray()) {
                checksum = (checksum + c) % 256;
            }
            return String.format("%02X", checksum);
        }

        public static boolean verifyChecksum(String data, String expectedChecksum) {
            String actualChecksum = generateChecksum(data);
            return actualChecksum.equalsIgnoreCase(expectedChecksum);
        }

        public static String base64Encode(String text) {
            return java.util.Base64.getEncoder().encodeToString(text.getBytes());
        }

        public static String base64Decode(String encoded) {
            return new String(java.util.Base64.getDecoder().decode(encoded));
        }

        public static String rot13(String text) {
            return caesarEncrypt(text, 13);
        }
    }

    // 网络工具
    public static class NetworkUtils {
        public static boolean isValidIPAddress(String ip) {
            String pattern = "^((25[0-5]|(2[0-4]|1\\d|[1-9]|)\\d)\\.?\\b){4}$";
            return ip.matches(pattern);
        }

        public static boolean isValidPort(int port) {
            return port >= 1 && port <= 65535;
        }

        public static String getLocalIPAddress() {
            try {
                return java.net.InetAddress.getLocalHost().getHostAddress();
            } catch (Exception e) {
                return "127.0.0.1";
            }
        }

        public static String getHostname() {
            try {
                return java.net.InetAddress.getLocalHost().getHostName();
            } catch (Exception e) {
                return "localhost";
            }
        }

        public static boolean isReachable(String host, int timeout) {
            try {
                return java.net.InetAddress.getByName(host).isReachable(timeout);
            } catch (Exception e) {
                return false;
            }
        }

        public static String formatUrl(String protocol, String host, int port, String path) {
            return String.format("%s://%s:%d%s", protocol, host, port,
                path.startsWith("/") ? path : "/" + path);
        }

        public static Map<String, String> parseQueryString(String queryString) {
            Map<String, String> params = new HashMap<>();
            if (StringUtils.isNullOrEmpty(queryString)) return params;

            String[] pairs = queryString.split("&");
            for (String pair : pairs) {
                String[] keyValue = pair.split("=", 2);
                if (keyValue.length == 2) {
                    params.put(java.net.URLDecoder.decode(keyValue[0]),
                             java.net.URLDecoder.decode(keyValue[1]));
                }
            }
            return params;
        }

        public static String buildQueryString(Map<String, String> params) {
            return params.entrySet().stream()
                .map(entry -> java.net.URLEncoder.encode(entry.getKey()) + "=" +
                             java.net.URLEncoder.encode(entry.getValue()))
                .collect(Collectors.joining("&"));
        }
    }
}