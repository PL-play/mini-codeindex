package com.example;

import java.io.*;
import java.math.BigDecimal;
import java.math.RoundingMode;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.*;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.function.Function;
import java.util.stream.Collectors;

/**
 * 报告生成器
 * 负责生成各种业务报告和统计报表
 */
public class ReportGenerator {
    private static final DateTimeFormatter DATE_FORMAT = DateTimeFormatter.ofPattern("yyyy-MM-dd");
    private static final DateTimeFormatter DATETIME_FORMAT =
        DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");

    private final ExecutorService executorService;
    private final Map<String, ReportTemplate> templates;
    private final ReportDataProvider dataProvider;
    private final ReportCache cache;

    // 报告类型枚举
    public enum ReportType {
        USER_ACTIVITY("USER_ACTIVITY"),
        SYSTEM_PERFORMANCE("SYSTEM_PERFORMANCE"),
        FINANCIAL_SUMMARY("FINANCIAL_SUMMARY"),
        AUDIT_TRAIL("AUDIT_TRAIL"),
        DEPARTMENT_ANALYSIS("DEPARTMENT_ANALYSIS"),
        SECURITY_REPORT("SECURITY_REPORT"),
        API_USAGE("API_USAGE"),
        CUSTOM("CUSTOM");

        private final String code;

        ReportType(String code) {
            this.code = code;
        }

        public String getCode() {
            return code;
        }
    }

    // 输出格式枚举
    public enum OutputFormat {
        PDF, HTML, CSV, JSON, XML, EXCEL
    }

    public ReportGenerator(ReportDataProvider dataProvider) {
        this.executorService = Executors.newFixedThreadPool(4);
        this.templates = new HashMap<>();
        this.dataProvider = dataProvider;
        this.cache = new ReportCache();

        initializeTemplates();
    }

    /**
     * 初始化报告模板
     */
    private void initializeTemplates() {
        // 用户活动报告模板
        templates.put("user_activity", new ReportTemplate(
            "User Activity Report",
            ReportType.USER_ACTIVITY,
            Arrays.asList("userId", "loginCount", "lastLogin", "totalTime", "actions"),
            this::generateUserActivityReport
        ));

        // 系统性能报告模板
        templates.put("system_performance", new ReportTemplate(
            "System Performance Report",
            ReportType.SYSTEM_PERFORMANCE,
            Arrays.asList("metric", "value", "timestamp", "threshold", "status"),
            this::generateSystemPerformanceReport
        ));

        // 财务摘要报告模板
        templates.put("financial_summary", new ReportTemplate(
            "Financial Summary Report",
            ReportType.FINANCIAL_SUMMARY,
            Arrays.asList("period", "revenue", "expenses", "profit", "growth"),
            this::generateFinancialSummaryReport
        ));

        // 审计跟踪报告模板
        templates.put("audit_trail", new ReportTemplate(
            "Audit Trail Report",
            ReportType.AUDIT_TRAIL,
            Arrays.asList("timestamp", "userId", "action", "resource", "details"),
            this::generateAuditTrailReport
        ));

        // 部门分析报告模板
        templates.put("department_analysis", new ReportTemplate(
            "Department Analysis Report",
            ReportType.DEPARTMENT_ANALYSIS,
            Arrays.asList("department", "userCount", "activityLevel", "performance", "issues"),
            this::generateDepartmentAnalysisReport
        ));
    }

    /**
     * 生成报告
     */
    public CompletableFuture<ReportResult> generateReport(String templateName,
                                                        Map<String, Object> parameters,
                                                        OutputFormat format) {
        return CompletableFuture.supplyAsync(() -> {
            try {
                ReportTemplate template = templates.get(templateName);
                if (template == null) {
                    throw new IllegalArgumentException("Unknown template: " + templateName);
                }

                // 检查缓存
                String cacheKey = generateCacheKey(templateName, parameters, format);
                ReportResult cached = cache.get(cacheKey);
                if (cached != null && !isExpired(cached)) {
                    return cached;
                }

                // 生成报告数据
                List<Map<String, Object>> data = template.generator.generate(parameters);

                // 格式化输出
                String content = formatReport(data, format, template);

                // 创建结果
                ReportResult result = new ReportResult(
                    UUID.randomUUID().toString(),
                    template.title,
                    LocalDateTime.now(),
                    content,
                    format,
                    data.size()
                );

                // 缓存结果
                cache.put(cacheKey, result);

                return result;

            } catch (Exception e) {
                throw new RuntimeException("Failed to generate report: " + templateName, e);
            }
        }, executorService);
    }

    /**
     * 生成用户活动报告
     */
    private List<Map<String, Object>> generateUserActivityReport(Map<String, Object> parameters) {
        LocalDate startDate = (LocalDate) parameters.getOrDefault("startDate", LocalDate.now().minusDays(30));
        LocalDate endDate = (LocalDate) parameters.getOrDefault("endDate", LocalDate.now());
        String department = (String) parameters.get("department");

        List<Map<String, Object>> data = new ArrayList<>();

        // 从数据提供者获取用户活动数据
        List<UserActivityData> activities = dataProvider.getUserActivities(startDate, endDate, department);

        for (UserActivityData activity : activities) {
            Map<String, Object> row = new HashMap<>();
            row.put("userId", activity.userId);
            row.put("loginCount", activity.loginCount);
            row.put("lastLogin", activity.lastLogin != null ?
                activity.lastLogin.format(DATETIME_FORMAT) : "Never");
            row.put("totalTime", formatDuration(activity.totalTimeMinutes));
            row.put("actions", activity.actionCount);
            data.add(row);
        }

        return data;
    }

    /**
     * 生成系统性能报告
     */
    private List<Map<String, Object>> generateSystemPerformanceReport(Map<String, Object> parameters) {
        LocalDateTime startTime = (LocalDateTime) parameters.getOrDefault("startTime",
            LocalDateTime.now().minusHours(24));
        LocalDateTime endTime = (LocalDateTime) parameters.getOrDefault("endTime", LocalDateTime.now());

        List<Map<String, Object>> data = new ArrayList<>();

        // CPU 使用率
        List<PerformanceMetric> cpuMetrics = dataProvider.getPerformanceMetrics("cpu_usage", startTime, endTime);
        for (PerformanceMetric metric : cpuMetrics) {
            Map<String, Object> row = new HashMap<>();
            row.put("metric", "CPU Usage");
            row.put("value", String.format("%.2f%%", metric.value));
            row.put("timestamp", metric.timestamp.format(DATETIME_FORMAT));
            row.put("threshold", "80.00%");
            row.put("status", metric.value > 80 ? "CRITICAL" : metric.value > 60 ? "WARNING" : "NORMAL");
            data.add(row);
        }

        // 内存使用率
        List<PerformanceMetric> memoryMetrics = dataProvider.getPerformanceMetrics("memory_usage", startTime, endTime);
        for (PerformanceMetric metric : memoryMetrics) {
            Map<String, Object> row = new HashMap<>();
            row.put("metric", "Memory Usage");
            row.put("value", String.format("%.2f%%", metric.value));
            row.put("timestamp", metric.timestamp.format(DATETIME_FORMAT));
            row.put("threshold", "85.00%");
            row.put("status", metric.value > 85 ? "CRITICAL" : metric.value > 70 ? "WARNING" : "NORMAL");
            data.add(row);
        }

        // 磁盘使用率
        List<PerformanceMetric> diskMetrics = dataProvider.getPerformanceMetrics("disk_usage", startTime, endTime);
        for (PerformanceMetric metric : diskMetrics) {
            Map<String, Object> row = new HashMap<>();
            row.put("metric", "Disk Usage");
            row.put("value", String.format("%.2f%%", metric.value));
            row.put("timestamp", metric.timestamp.format(DATETIME_FORMAT));
            row.put("threshold", "90.00%");
            row.put("status", metric.value > 90 ? "CRITICAL" : metric.value > 75 ? "WARNING" : "NORMAL");
            data.add(row);
        }

        return data;
    }

    /**
     * 生成财务摘要报告
     */
    private List<Map<String, Object>> generateFinancialSummaryReport(Map<String, Object> parameters) {
        LocalDate startDate = (LocalDate) parameters.getOrDefault("startDate", LocalDate.now().minusMonths(1));
        LocalDate endDate = (LocalDate) parameters.getOrDefault("endDate", LocalDate.now());

        List<Map<String, Object>> data = new ArrayList<>();

        // 获取财务数据
        List<FinancialData> financialData = dataProvider.getFinancialData(startDate, endDate);

        for (FinancialData fd : financialData) {
            Map<String, Object> row = new HashMap<>();
            row.put("period", fd.period);
            row.put("revenue", formatCurrency(fd.revenue));
            row.put("expenses", formatCurrency(fd.expenses));
            row.put("profit", formatCurrency(fd.profit));
            row.put("growth", String.format("%.2f%%", fd.growthRate));
            data.add(row);
        }

        return data;
    }

    /**
     * 生成审计跟踪报告
     */
    private List<Map<String, Object>> generateAuditTrailReport(Map<String, Object> parameters) {
        LocalDateTime startTime = (LocalDateTime) parameters.getOrDefault("startTime",
            LocalDateTime.now().minusDays(7));
        LocalDateTime endTime = (LocalDateTime) parameters.getOrDefault("endTime", LocalDateTime.now());
        String userId = (String) parameters.get("userId");
        String eventType = (String) parameters.get("eventType");

        List<Map<String, Object>> data = new ArrayList<>();

        // 获取审计事件
        List<AuditEventData> events = dataProvider.getAuditEvents(startTime, endTime, userId, eventType);

        for (AuditEventData event : events) {
            Map<String, Object> row = new HashMap<>();
            row.put("timestamp", event.timestamp.format(DATETIME_FORMAT));
            row.put("userId", event.userId);
            row.put("action", event.action);
            row.put("resource", event.resource);
            row.put("details", event.details);
            data.add(row);
        }

        return data;
    }

    /**
     * 生成部门分析报告
     */
    private List<Map<String, Object>> generateDepartmentAnalysisReport(Map<String, Object> parameters) {
        List<Map<String, Object>> data = new ArrayList<>();

        // 获取部门数据
        List<DepartmentData> departments = dataProvider.getDepartmentData();

        for (DepartmentData dept : departments) {
            Map<String, Object> row = new HashMap<>();
            row.put("department", dept.name);
            row.put("userCount", dept.userCount);
            row.put("activityLevel", dept.activityLevel);
            row.put("performance", String.format("%.2f%%", dept.performanceScore));
            row.put("issues", dept.openIssues);
            data.add(row);
        }

        return data;
    }

    /**
     * 格式化报告
     */
    private String formatReport(List<Map<String, Object>> data, OutputFormat format,
                               ReportTemplate template) throws IOException {
        switch (format) {
            case CSV:
                return formatAsCSV(data, template);
            case JSON:
                return formatAsJSON(data);
            case HTML:
                return formatAsHTML(data, template);
            case XML:
                return formatAsXML(data, template);
            case PDF:
                return formatAsPDF(data, template);
            case EXCEL:
                return formatAsExcel(data, template);
            default:
                throw new IllegalArgumentException("Unsupported format: " + format);
        }
    }

    /**
     * 格式化为CSV
     */
    private String formatAsCSV(List<Map<String, Object>> data, ReportTemplate template) {
        StringBuilder csv = new StringBuilder();

        // 标题行
        csv.append(String.join(",", template.columns)).append("\n");

        // 数据行
        for (Map<String, Object> row : data) {
            List<String> values = template.columns.stream()
                .map(col -> String.valueOf(row.getOrDefault(col, "")))
                .collect(Collectors.toList());
            csv.append(String.join(",", values)).append("\n");
        }

        return csv.toString();
    }

    /**
     * 格式化为JSON
     */
    private String formatAsJSON(List<Map<String, Object>> data) {
        // 简化实现
        StringBuilder json = new StringBuilder();
        json.append("[\n");
        for (int i = 0; i < data.size(); i++) {
            json.append("  ").append(mapToJsonString(data.get(i)));
            if (i < data.size() - 1) {
                json.append(",");
            }
            json.append("\n");
        }
        json.append("]");
        return json.toString();
    }

    /**
     * 格式化为HTML
     */
    private String formatAsHTML(List<Map<String, Object>> data, ReportTemplate template) {
        StringBuilder html = new StringBuilder();
        html.append("<html><head><title>").append(template.title).append("</title>");
        html.append("<style>table {border-collapse: collapse;} th, td {border: 1px solid #ddd; padding: 8px;}</style>");
        html.append("</head><body>");
        html.append("<h1>").append(template.title).append("</h1>");
        html.append("<table><thead><tr>");

        for (String column : template.columns) {
            html.append("<th>").append(column).append("</th>");
        }
        html.append("</tr></thead><tbody>");

        for (Map<String, Object> row : data) {
            html.append("<tr>");
            for (String column : template.columns) {
                html.append("<td>").append(row.getOrDefault(column, "")).append("</td>");
            }
            html.append("</tr>");
        }

        html.append("</tbody></table></body></html>");
        return html.toString();
    }

    /**
     * 格式化为XML
     */
    private String formatAsXML(List<Map<String, Object>> data, ReportTemplate template) {
        StringBuilder xml = new StringBuilder();
        xml.append("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n");
        xml.append("<report>\n");
        xml.append("  <title>").append(template.title).append("</title>\n");
        xml.append("  <generated>").append(LocalDateTime.now().format(DATETIME_FORMAT)).append("</generated>\n");
        xml.append("  <data>\n");

        for (Map<String, Object> row : data) {
            xml.append("    <row>\n");
            for (String column : template.columns) {
                xml.append("      <").append(column).append(">")
                   .append(row.getOrDefault(column, "")).append("</").append(column).append(">\n");
            }
            xml.append("    </row>\n");
        }

        xml.append("  </data>\n</report>");
        return xml.toString();
    }

    /**
     * 格式化为PDF（简化实现）
     */
    private String formatAsPDF(List<Map<String, Object>> data, ReportTemplate template) {
        // 实际实现需要PDF库，这里返回HTML格式作为替代
        return formatAsHTML(data, template);
    }

    /**
     * 格式化为Excel（简化实现）
     */
    private String formatAsExcel(List<Map<String, Object>> data, ReportTemplate template) {
        // 实际实现需要Excel库，这里返回CSV格式作为替代
        return formatAsCSV(data, template);
    }

    /**
     * 保存报告到文件
     */
    public void saveReportToFile(ReportResult report, String filePath) throws IOException {
        Path path = Paths.get(filePath);
        Files.createDirectories(path.getParent());
        Files.write(path, report.content.getBytes());
    }

    /**
     * 关闭报告生成器
     */
    public void shutdown() {
        executorService.shutdown();
        cache.clear();
    }

    // 辅助方法
    private String generateCacheKey(String templateName, Map<String, Object> parameters, OutputFormat format) {
        String params = parameters.entrySet().stream()
            .sorted(Map.Entry.comparingByKey())
            .map(e -> e.getKey() + "=" + e.getValue())
            .collect(Collectors.joining("&"));
        return templateName + "|" + params + "|" + format;
    }

    private boolean isExpired(ReportResult result) {
        // 缓存5分钟
        return result.generatedTime.isBefore(LocalDateTime.now().minusMinutes(5));
    }

    private String formatDuration(long minutes) {
        long hours = minutes / 60;
        long mins = minutes % 60;
        return String.format("%dh %dm", hours, mins);
    }

    private String formatCurrency(BigDecimal amount) {
        return "$" + amount.setScale(2, RoundingMode.HALF_UP).toString();
    }

    private String mapToJsonString(Map<String, Object> map) {
        return "{" + map.entrySet().stream()
            .map(e -> "\"" + e.getKey() + "\":\"" + e.getValue() + "\"")
            .collect(Collectors.joining(",")) + "}";
    }

    // 数据类
    public static class ReportTemplate {
        public final String title;
        public final ReportType type;
        public final List<String> columns;
        public final ReportDataGenerator generator;

        public ReportTemplate(String title, ReportType type, List<String> columns,
                            ReportDataGenerator generator) {
            this.title = title;
            this.type = type;
            this.columns = columns;
            this.generator = generator;
        }
    }

    public static class ReportResult {
        public final String id;
        public final String title;
        public final LocalDateTime generatedTime;
        public final String content;
        public final OutputFormat format;
        public final int recordCount;

        public ReportResult(String id, String title, LocalDateTime generatedTime,
                          String content, OutputFormat format, int recordCount) {
            this.id = id;
            this.title = title;
            this.generatedTime = generatedTime;
            this.content = content;
            this.format = format;
            this.recordCount = recordCount;
        }
    }

    // 数据提供者接口
    public interface ReportDataProvider {
        List<UserActivityData> getUserActivities(LocalDate startDate, LocalDate endDate, String department);
        List<PerformanceMetric> getPerformanceMetrics(String metricType, LocalDateTime startTime, LocalDateTime endTime);
        List<FinancialData> getFinancialData(LocalDate startDate, LocalDate endDate);
        List<AuditEventData> getAuditEvents(LocalDateTime startTime, LocalDateTime endTime, String userId, String eventType);
        List<DepartmentData> getDepartmentData();
    }

    // 数据生成器接口
    public interface ReportDataGenerator {
        List<Map<String, Object>> generate(Map<String, Object> parameters);
    }

    // 数据传输对象
    public static class UserActivityData {
        public final String userId;
        public final int loginCount;
        public final LocalDateTime lastLogin;
        public final long totalTimeMinutes;
        public final int actionCount;

        public UserActivityData(String userId, int loginCount, LocalDateTime lastLogin,
                              long totalTimeMinutes, int actionCount) {
            this.userId = userId;
            this.loginCount = loginCount;
            this.lastLogin = lastLogin;
            this.totalTimeMinutes = totalTimeMinutes;
            this.actionCount = actionCount;
        }
    }

    public static class PerformanceMetric {
        public final String metricType;
        public final double value;
        public final LocalDateTime timestamp;

        public PerformanceMetric(String metricType, double value, LocalDateTime timestamp) {
            this.metricType = metricType;
            this.value = value;
            this.timestamp = timestamp;
        }
    }

    public static class FinancialData {
        public final String period;
        public final BigDecimal revenue;
        public final BigDecimal expenses;
        public final BigDecimal profit;
        public final double growthRate;

        public FinancialData(String period, BigDecimal revenue, BigDecimal expenses,
                           BigDecimal profit, double growthRate) {
            this.period = period;
            this.revenue = revenue;
            this.expenses = expenses;
            this.profit = profit;
            this.growthRate = growthRate;
        }
    }

    public static class AuditEventData {
        public final LocalDateTime timestamp;
        public final String userId;
        public final String action;
        public final String resource;
        public final String details;

        public AuditEventData(LocalDateTime timestamp, String userId, String action,
                            String resource, String details) {
            this.timestamp = timestamp;
            this.userId = userId;
            this.action = action;
            this.resource = resource;
            this.details = details;
        }
    }

    public static class DepartmentData {
        public final String name;
        public final int userCount;
        public final String activityLevel;
        public final double performanceScore;
        public final int openIssues;

        public DepartmentData(String name, int userCount, String activityLevel,
                            double performanceScore, int openIssues) {
            this.name = name;
            this.userCount = userCount;
            this.activityLevel = activityLevel;
            this.performanceScore = performanceScore;
            this.openIssues = openIssues;
        }
    }

    /**
     * 报告缓存
     */
    private static class ReportCache {
        private final Map<String, ReportResult> cache = new ConcurrentHashMap<>();

        public void put(String key, ReportResult result) {
            cache.put(key, result);
        }

        public ReportResult get(String key) {
            return cache.get(key);
        }

        public void clear() {
            cache.clear();
        }
    }
}