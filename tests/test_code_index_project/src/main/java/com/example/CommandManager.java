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
import java.net.*;
import java.nio.file.*;

/**
 * 命令模式实现
 * 将请求封装为对象，支持撤销、重做、队列等操作
 */
public class CommandManager {

    // 单例模式
    private static volatile CommandManager instance;
    private static final Object LOCK = new Object();

    private final Map<String, CommandFactory> commandFactories;
    private final Deque<Command> commandHistory;
    private final Deque<Command> undoHistory;
    private final ExecutorService executor;
    private final Map<String, Command> activeCommands;

    private CommandManager() {
        this.commandFactories = new ConcurrentHashMap<>();
        this.commandHistory = new ConcurrentLinkedDeque<>();
        this.undoHistory = new ConcurrentLinkedDeque<>();
        this.executor = Executors.newCachedThreadPool();
        this.activeCommands = new ConcurrentHashMap<>();
        initializeDefaultCommands();
    }

    public static CommandManager getInstance() {
        if (instance == null) {
            synchronized (LOCK) {
                if (instance == null) {
                    instance = new CommandManager();
                }
            }
        }
        return instance;
    }

    /**
     * 初始化默认命令
     */
    private void initializeDefaultCommands() {
        // 文件操作命令
        registerCommand("file_create", new FileCreateCommandFactory());
        registerCommand("file_delete", new FileDeleteCommandFactory());
        registerCommand("file_copy", new FileCopyCommandFactory());
        registerCommand("file_move", new FileMoveCommandFactory());

        // 数据操作命令
        registerCommand("data_insert", new DataInsertCommandFactory());
        registerCommand("data_update", new DataUpdateCommandFactory());
        registerCommand("data_delete", new DataDeleteCommandFactory());
        registerCommand("data_query", new DataQueryCommandFactory());

        // 用户操作命令
        registerCommand("user_create", new UserCreateCommandFactory());
        registerCommand("user_update", new UserUpdateCommandFactory());
        registerCommand("user_delete", new UserDeleteCommandFactory());
        registerCommand("user_login", new UserLoginCommandFactory());

        // 系统操作命令
        registerCommand("system_backup", new SystemBackupCommandFactory());
        registerCommand("system_restore", new SystemRestoreCommandFactory());
        registerCommand("system_shutdown", new SystemShutdownCommandFactory());
        registerCommand("system_restart", new SystemRestartCommandFactory());

        // 网络操作命令
        registerCommand("network_connect", new NetworkConnectCommandFactory());
        registerCommand("network_disconnect", new NetworkDisconnectCommandFactory());
        registerCommand("network_send", new NetworkSendCommandFactory());
        registerCommand("network_receive", new NetworkReceiveCommandFactory());

        // 复合命令
        registerCommand("composite", new CompositeCommandFactory());
    }

    /**
     * 注册命令工厂
     */
    public void registerCommand(String commandType, CommandFactory factory) {
        commandFactories.put(commandType, factory);
    }

    /**
     * 创建命令
     */
    public Command createCommand(String commandType, Object... params) {
        CommandFactory factory = commandFactories.get(commandType);
        if (factory == null) {
            throw new IllegalArgumentException("Command type not found: " + commandType);
        }
        return factory.create(params);
    }

    /**
     * 执行命令
     */
    public Object executeCommand(String commandType, Object... params) {
        Command command = createCommand(commandType, params);
        return executeCommand(command);
    }

    /**
     * 执行命令对象
     */
    public Object executeCommand(Command command) {
        try {
            Object result = command.execute();
            if (command.isUndoable()) {
                commandHistory.push(command);
                undoHistory.clear(); // 执行新命令时清空重做历史
            }
            return result;
        } catch (Exception e) {
            System.err.println("Command execution failed: " + e.getMessage());
            throw new RuntimeException("Command execution failed", e);
        }
    }

    /**
     * 撤销最后一个命令
     */
    public void undo() {
        if (!commandHistory.isEmpty()) {
            Command command = commandHistory.pop();
            try {
                command.undo();
                undoHistory.push(command);
                System.out.println("Command undone: " + command.getDescription());
            } catch (Exception e) {
                System.err.println("Undo failed: " + e.getMessage());
                // 如果撤销失败，将命令重新放回历史记录
                commandHistory.push(command);
            }
        } else {
            System.out.println("No commands to undo");
        }
    }

    /**
     * 重做最后一个撤销的命令
     */
    public void redo() {
        if (!undoHistory.isEmpty()) {
            Command command = undoHistory.pop();
            try {
                command.execute();
                commandHistory.push(command);
                System.out.println("Command redone: " + command.getDescription());
            } catch (Exception e) {
                System.err.println("Redo failed: " + e.getMessage());
                // 如果重做失败，将命令重新放回撤销历史
                undoHistory.push(command);
            }
        } else {
            System.out.println("No commands to redo");
        }
    }

    /**
     * 异步执行命令
     */
    public CompletableFuture<Object> executeAsync(String commandType, Object... params) {
        return CompletableFuture.supplyAsync(() -> executeCommand(commandType, params), executor);
    }

    /**
     * 批量执行命令
     */
    public List<Object> executeBatch(List<String> commandTypes, List<Object[]> paramsList) {
        List<Object> results = new ArrayList<>();
        for (int i = 0; i < commandTypes.size(); i++) {
            String commandType = commandTypes.get(i);
            Object[] params = i < paramsList.size() ? paramsList.get(i) : new Object[0];
            results.add(executeCommand(commandType, params));
        }
        return results;
    }

    /**
     * 获取命令历史
     */
    public List<String> getCommandHistory() {
        return commandHistory.stream()
                .map(Command::getDescription)
                .collect(Collectors.toList());
    }

    /**
     * 清空命令历史
     */
    public void clearHistory() {
        commandHistory.clear();
        undoHistory.clear();
    }

    /**
     * 获取活跃命令
     */
    public Map<String, Command> getActiveCommands() {
        return new HashMap<>(activeCommands);
    }

    // 命令接口
    public interface Command {
        Object execute() throws Exception;
        void undo() throws Exception;
        boolean isUndoable();
        String getDescription();
        String getType();
    }

    // 命令工厂接口
    public interface CommandFactory {
        Command create(Object... params);
    }

    // 文件创建命令
    public static class FileCreateCommandFactory implements CommandFactory {
        @Override
        public Command create(Object... params) {
            String filePath = (String) params[0];
            String content = params.length > 1 ? (String) params[1] : "";
            return new FileCreateCommand(filePath, content);
        }
    }

    public static class FileCreateCommand implements Command {
        private final String filePath;
        private final String content;
        private boolean executed = false;

        public FileCreateCommand(String filePath, String content) {
            this.filePath = filePath;
            this.content = content;
        }

        @Override
        public Object execute() throws Exception {
            File file = new File(filePath);
            if (file.exists()) {
                throw new IOException("File already exists: " + filePath);
            }

            try (FileWriter writer = new FileWriter(file)) {
                writer.write(content);
            }

            executed = true;
            System.out.println("File created: " + filePath);
            return filePath;
        }

        @Override
        public void undo() throws Exception {
            if (executed) {
                Files.deleteIfExists(Paths.get(filePath));
                executed = false;
                System.out.println("File creation undone: " + filePath);
            }
        }

        @Override
        public boolean isUndoable() {
            return true;
        }

        @Override
        public String getDescription() {
            return "Create file: " + filePath;
        }

        @Override
        public String getType() {
            return "file_create";
        }
    }

    // 文件删除命令
    public static class FileDeleteCommandFactory implements CommandFactory {
        @Override
        public Command create(Object... params) {
            String filePath = (String) params[0];
            return new FileDeleteCommand(filePath);
        }
    }

    public static class FileDeleteCommand implements Command {
        private final String filePath;
        private String backupContent;
        private boolean executed = false;

        public FileDeleteCommand(String filePath) {
            this.filePath = filePath;
        }

        @Override
        public Object execute() throws Exception {
            Path path = Paths.get(filePath);
            if (!Files.exists(path)) {
                throw new IOException("File does not exist: " + filePath);
            }

            // 备份文件内容
            backupContent = Files.readString(path);
            Files.delete(path);

            executed = true;
            System.out.println("File deleted: " + filePath);
            return filePath;
        }

        @Override
        public void undo() throws Exception {
            if (executed && backupContent != null) {
                try (FileWriter writer = new FileWriter(filePath)) {
                    writer.write(backupContent);
                }
                executed = false;
                System.out.println("File deletion undone: " + filePath);
            }
        }

        @Override
        public boolean isUndoable() {
            return true;
        }

        @Override
        public String getDescription() {
            return "Delete file: " + filePath;
        }

        @Override
        public String getType() {
            return "file_delete";
        }
    }

    // 文件复制命令
    public static class FileCopyCommandFactory implements CommandFactory {
        @Override
        public Command create(Object... params) {
            String sourcePath = (String) params[0];
            String destPath = (String) params[1];
            return new FileCopyCommand(sourcePath, destPath);
        }
    }

    public static class FileCopyCommand implements Command {
        private final String sourcePath;
        private final String destPath;
        private boolean executed = false;

        public FileCopyCommand(String sourcePath, String destPath) {
            this.sourcePath = sourcePath;
            this.destPath = destPath;
        }

        @Override
        public Object execute() throws Exception {
            Path source = Paths.get(sourcePath);
            Path dest = Paths.get(destPath);

            if (!Files.exists(source)) {
                throw new IOException("Source file does not exist: " + sourcePath);
            }

            Files.copy(source, dest, java.nio.file.StandardCopyOption.REPLACE_EXISTING);

            executed = true;
            System.out.println("File copied from " + sourcePath + " to " + destPath);
            return destPath;
        }

        @Override
        public void undo() throws Exception {
            if (executed) {
                Files.deleteIfExists(Paths.get(destPath));
                executed = false;
                System.out.println("File copy undone: " + destPath);
            }
        }

        @Override
        public boolean isUndoable() {
            return true;
        }

        @Override
        public String getDescription() {
            return "Copy file from " + sourcePath + " to " + destPath;
        }

        @Override
        public String getType() {
            return "file_copy";
        }
    }

    // 文件移动命令
    public static class FileMoveCommandFactory implements CommandFactory {
        @Override
        public Command create(Object... params) {
            String sourcePath = (String) params[0];
            String destPath = (String) params[1];
            return new FileMoveCommand(sourcePath, destPath);
        }
    }

    public static class FileMoveCommand implements Command {
        private final String sourcePath;
        private final String destPath;
        private boolean executed = false;

        public FileMoveCommand(String sourcePath, String destPath) {
            this.sourcePath = sourcePath;
            this.destPath = destPath;
        }

        @Override
        public Object execute() throws Exception {
            Path source = Paths.get(sourcePath);
            Path dest = Paths.get(destPath);

            if (!Files.exists(source)) {
                throw new IOException("Source file does not exist: " + sourcePath);
            }

            Files.move(source, dest, java.nio.file.StandardCopyOption.REPLACE_EXISTING);

            executed = true;
            System.out.println("File moved from " + sourcePath + " to " + destPath);
            return destPath;
        }

        @Override
        public void undo() throws Exception {
            if (executed) {
                Files.move(Paths.get(destPath), Paths.get(sourcePath),
                          java.nio.file.StandardCopyOption.REPLACE_EXISTING);
                executed = false;
                System.out.println("File move undone: " + sourcePath);
            }
        }

        @Override
        public boolean isUndoable() {
            return true;
        }

        @Override
        public String getDescription() {
            return "Move file from " + sourcePath + " to " + destPath;
        }

        @Override
        public String getType() {
            return "file_move";
        }
    }

    // 数据插入命令
    public static class DataInsertCommandFactory implements CommandFactory {
        @Override
        public Command create(Object... params) {
            String tableName = (String) params[0];
            Map<String, Object> data = (Map<String, Object>) params[1];
            return new DataInsertCommand(tableName, data);
        }
    }

    public static class DataInsertCommand implements Command {
        private final String tableName;
        private final Map<String, Object> data;
        private Long generatedId;
        private boolean executed = false;

        public DataInsertCommand(String tableName, Map<String, Object> data) {
            this.tableName = tableName;
            this.data = new HashMap<>(data);
        }

        @Override
        public Object execute() throws Exception {
            // 模拟数据库插入
            generatedId = System.currentTimeMillis(); // 模拟生成的ID
            System.out.println("Data inserted into " + tableName + " with ID: " + generatedId);
            executed = true;
            return generatedId;
        }

        @Override
        public void undo() throws Exception {
            if (executed && generatedId != null) {
                // 模拟删除插入的数据
                System.out.println("Data insertion undone for ID: " + generatedId);
                executed = false;
            }
        }

        @Override
        public boolean isUndoable() {
            return true;
        }

        @Override
        public String getDescription() {
            return "Insert data into " + tableName;
        }

        @Override
        public String getType() {
            return "data_insert";
        }
    }

    // 数据更新命令
    public static class DataUpdateCommandFactory implements CommandFactory {
        @Override
        public Command create(Object... params) {
            String tableName = (String) params[0];
            Long id = (Long) params[1];
            Map<String, Object> newData = (Map<String, Object>) params[2];
            return new DataUpdateCommand(tableName, id, newData);
        }
    }

    public static class DataUpdateCommand implements Command {
        private final String tableName;
        private final Long id;
        private final Map<String, Object> newData;
        private Map<String, Object> oldData;
        private boolean executed = false;

        public DataUpdateCommand(String tableName, Long id, Map<String, Object> newData) {
            this.tableName = tableName;
            this.id = id;
            this.newData = new HashMap<>(newData);
        }

        @Override
        public Object execute() throws Exception {
            // 模拟获取旧数据
            oldData = Map.of("name", "Old Name", "value", 100); // 模拟旧数据

            // 模拟更新
            System.out.println("Data updated in " + tableName + " for ID: " + id);
            executed = true;
            return id;
        }

        @Override
        public void undo() throws Exception {
            if (executed && oldData != null) {
                // 模拟恢复旧数据
                System.out.println("Data update undone for ID: " + id);
                executed = false;
            }
        }

        @Override
        public boolean isUndoable() {
            return true;
        }

        @Override
        public String getDescription() {
            return "Update data in " + tableName + " for ID: " + id;
        }

        @Override
        public String getType() {
            return "data_update";
        }
    }

    // 数据删除命令
    public static class DataDeleteCommandFactory implements CommandFactory {
        @Override
        public Command create(Object... params) {
            String tableName = (String) params[0];
            Long id = (Long) params[1];
            return new DataDeleteCommand(tableName, id);
        }
    }

    public static class DataDeleteCommand implements Command {
        private final String tableName;
        private final Long id;
        private Map<String, Object> deletedData;
        private boolean executed = false;

        public DataDeleteCommand(String tableName, Long id) {
            this.tableName = tableName;
            this.id = id;
        }

        @Override
        public Object execute() throws Exception {
            // 模拟获取要删除的数据
            deletedData = Map.of("id", id, "name", "Test Item", "value", 200);

            // 模拟删除
            System.out.println("Data deleted from " + tableName + " for ID: " + id);
            executed = true;
            return id;
        }

        @Override
        public void undo() throws Exception {
            if (executed && deletedData != null) {
                // 模拟恢复删除的数据
                System.out.println("Data deletion undone for ID: " + id);
                executed = false;
            }
        }

        @Override
        public boolean isUndoable() {
            return true;
        }

        @Override
        public String getDescription() {
            return "Delete data from " + tableName + " for ID: " + id;
        }

        @Override
        public String getType() {
            return "data_delete";
        }
    }

    // 数据查询命令
    public static class DataQueryCommandFactory implements CommandFactory {
        @Override
        public Command create(Object... params) {
            String tableName = (String) params[0];
            String query = (String) params[1];
            return new DataQueryCommand(tableName, query);
        }
    }

    public static class DataQueryCommand implements Command {
        private final String tableName;
        private final String query;
        private List<Map<String, Object>> results;

        public DataQueryCommand(String tableName, String query) {
            this.tableName = tableName;
            this.query = query;
        }

        @Override
        public Object execute() throws Exception {
            // 模拟查询执行
            results = Arrays.asList(
                Map.of("id", 1L, "name", "Item 1", "value", 100),
                Map.of("id", 2L, "name", "Item 2", "value", 200)
            );

            System.out.println("Query executed on " + tableName + ": " + query);
            return results;
        }

        @Override
        public void undo() throws Exception {
            // 查询通常不可撤销
            throw new UnsupportedOperationException("Query commands cannot be undone");
        }

        @Override
        public boolean isUndoable() {
            return false;
        }

        @Override
        public String getDescription() {
            return "Query data from " + tableName + ": " + query;
        }

        @Override
        public String getType() {
            return "data_query";
        }
    }

    // 用户创建命令
    public static class UserCreateCommandFactory implements CommandFactory {
        @Override
        public Command create(Object... params) {
            String username = (String) params[0];
            String email = (String) params[1];
            return new UserCreateCommand(username, email);
        }
    }

    public static class UserUpdateCommandFactory implements CommandFactory {
        @Override
        public Command create(Object... params) {
            Long userId = (Long) params[0];
            Map<String, Object> updates = (Map<String, Object>) params[1];
            return new UserUpdateCommand(userId, updates);
        }
    }

    public static class UserDeleteCommandFactory implements CommandFactory {
        @Override
        public Command create(Object... params) {
            Long userId = (Long) params[0];
            return new UserDeleteCommand(userId);
        }
    }

    public static class UserCreateCommand implements Command {
        private final String username;
        private final String email;
        private Long userId;
        private boolean executed = false;

        public UserCreateCommand(String username, String email) {
            this.username = username;
            this.email = email;
        }

        @Override
        public Object execute() throws Exception {
            // 模拟用户创建
            userId = System.currentTimeMillis();
            System.out.println("User created: " + username + " (" + email + ") with ID: " + userId);
            executed = true;
            return userId;
        }

        @Override
        public void undo() throws Exception {
            if (executed && userId != null) {
                // 模拟用户删除
                System.out.println("User creation undone for ID: " + userId);
                executed = false;
            }
        }

        @Override
        public boolean isUndoable() {
            return true;
        }

        @Override
        public String getDescription() {
            return "Create user: " + username;
        }

        @Override
        public String getType() {
            return "user_create";
        }
    }

    public static class UserUpdateCommand implements Command {
        private final Long userId;
        private final Map<String, Object> updates;
        private Map<String, Object> oldData;
        private boolean executed = false;

        public UserUpdateCommand(Long userId, Map<String, Object> updates) {
            this.userId = userId;
            this.updates = new HashMap<>(updates);
        }

        @Override
        public Object execute() throws Exception {
            // 模拟获取旧数据
            oldData = Map.of("username", "olduser", "email", "old@example.com");
            System.out.println("User updated: ID " + userId + " with " + updates);
            executed = true;
            return userId;
        }

        @Override
        public void undo() throws Exception {
            if (executed && oldData != null) {
                System.out.println("User update undone for ID: " + userId);
                executed = false;
            }
        }

        @Override
        public boolean isUndoable() {
            return true;
        }

        @Override
        public String getDescription() {
            return "Update user: " + userId;
        }

        @Override
        public String getType() {
            return "user_update";
        }
    }

    public static class UserDeleteCommand implements Command {
        private final Long userId;
        private Map<String, Object> deletedData;
        private boolean executed = false;

        public UserDeleteCommand(Long userId) {
            this.userId = userId;
        }

        @Override
        public Object execute() throws Exception {
            // 模拟获取要删除的用户数据
            deletedData = Map.of("id", userId, "username", "testuser", "email", "test@example.com");
            System.out.println("User deleted: ID " + userId);
            executed = true;
            return userId;
        }

        @Override
        public void undo() throws Exception {
            if (executed && deletedData != null) {
                System.out.println("User deletion undone for ID: " + userId);
                executed = false;
            }
        }

        @Override
        public boolean isUndoable() {
            return true;
        }

        @Override
        public String getDescription() {
            return "Delete user: " + userId;
        }

        @Override
        public String getType() {
            return "user_delete";
        }
    }

    // 用户登录命令
    public static class UserLoginCommandFactory implements CommandFactory {
        @Override
        public Command create(Object... params) {
            String username = (String) params[0];
            String password = (String) params[1];
            return new UserLoginCommand(username, password);
        }
    }

    public static class UserLoginCommand implements Command {
        private final String username;
        private final String password;
        private String sessionToken;
        private boolean executed = false;

        public UserLoginCommand(String username, String password) {
            this.username = username;
            this.password = password;
        }

        @Override
        public Object execute() throws Exception {
            // 模拟用户登录
            if ("admin".equals(username) && "password".equals(password)) {
                sessionToken = UUID.randomUUID().toString();
                System.out.println("User logged in: " + username + ", Session: " + sessionToken);
                executed = true;
                return sessionToken;
            } else {
                throw new SecurityException("Invalid credentials");
            }
        }

        @Override
        public void undo() throws Exception {
            if (executed && sessionToken != null) {
                // 模拟登出
                System.out.println("User login undone for session: " + sessionToken);
                executed = false;
            }
        }

        @Override
        public boolean isUndoable() {
            return true;
        }

        @Override
        public String getDescription() {
            return "Login user: " + username;
        }

        @Override
        public String getType() {
            return "user_login";
        }
    }

    // 系统备份命令
    public static class SystemBackupCommandFactory implements CommandFactory {
        @Override
        public Command create(Object... params) {
            String sourceDir = (String) params[0];
            String backupDir = (String) params[1];
            return new SystemBackupCommand(sourceDir, backupDir);
        }
    }

    public static class SystemRestoreCommandFactory implements CommandFactory {
        @Override
        public Command create(Object... params) {
            String backupId = (String) params[0];
            String targetDir = (String) params[1];
            return new SystemRestoreCommand(backupId, targetDir);
        }
    }

    public static class SystemShutdownCommandFactory implements CommandFactory {
        @Override
        public Command create(Object... params) {
            boolean force = params.length > 0 ? (Boolean) params[0] : false;
            return new SystemShutdownCommand(force);
        }
    }

    public static class SystemRestartCommandFactory implements CommandFactory {
        @Override
        public Command create(Object... params) {
            boolean force = params.length > 0 ? (Boolean) params[0] : false;
            return new SystemRestartCommand(force);
        }
    }

    public static class SystemBackupCommand implements Command {
        private final String sourceDir;
        private final String backupDir;
        private String backupId;
        private boolean executed = false;

        public SystemBackupCommand(String sourceDir, String backupDir) {
            this.sourceDir = sourceDir;
            this.backupDir = backupDir;
        }

        @Override
        public Object execute() throws Exception {
            // 模拟系统备份
            backupId = "backup_" + System.currentTimeMillis();
            System.out.println("System backup created: " + backupId + " from " + sourceDir + " to " + backupDir);
            executed = true;
            return backupId;
        }

        @Override
        public void undo() throws Exception {
            if (executed && backupId != null) {
                // 模拟删除备份
                System.out.println("System backup undone: " + backupId);
                executed = false;
            }
        }

        @Override
        public boolean isUndoable() {
            return true;
        }

        @Override
        public String getDescription() {
            return "Create system backup from " + sourceDir + " to " + backupDir;
        }

        @Override
        public String getType() {
            return "system_backup";
        }
    }

    public static class SystemRestoreCommand implements Command {
        private final String backupId;
        private final String targetDir;
        private boolean executed = false;

        public SystemRestoreCommand(String backupId, String targetDir) {
            this.backupId = backupId;
            this.targetDir = targetDir;
        }

        @Override
        public Object execute() throws Exception {
            System.out.println("System restore initiated: " + backupId + " to " + targetDir);
            executed = true;
            return backupId;
        }

        @Override
        public void undo() throws Exception {
            if (executed) {
                System.out.println("System restore undone: " + backupId);
                executed = false;
            }
        }

        @Override
        public boolean isUndoable() {
            return true;
        }

        @Override
        public String getDescription() {
            return "Restore system from backup: " + backupId;
        }

        @Override
        public String getType() {
            return "system_restore";
        }
    }

    public static class SystemShutdownCommand implements Command {
        private final boolean force;
        private boolean executed = false;

        public SystemShutdownCommand(boolean force) {
            this.force = force;
        }

        @Override
        public Object execute() throws Exception {
            System.out.println("System shutdown initiated" + (force ? " (forced)" : ""));
            executed = true;
            return "shutdown_initiated";
        }

        @Override
        public void undo() throws Exception {
            if (executed) {
                System.out.println("System shutdown cancelled");
                executed = false;
            }
        }

        @Override
        public boolean isUndoable() {
            return true;
        }

        @Override
        public String getDescription() {
            return "Shutdown system" + (force ? " (forced)" : "");
        }

        @Override
        public String getType() {
            return "system_shutdown";
        }
    }

    public static class SystemRestartCommand implements Command {
        private final boolean force;
        private boolean executed = false;

        public SystemRestartCommand(boolean force) {
            this.force = force;
        }

        @Override
        public Object execute() throws Exception {
            System.out.println("System restart initiated" + (force ? " (forced)" : ""));
            executed = true;
            return "restart_initiated";
        }

        @Override
        public void undo() throws Exception {
            if (executed) {
                System.out.println("System restart cancelled");
                executed = false;
            }
        }

        @Override
        public boolean isUndoable() {
            return true;
        }

        @Override
        public String getDescription() {
            return "Restart system" + (force ? " (forced)" : "");
        }

        @Override
        public String getType() {
            return "system_restart";
        }
    }

    // 网络连接命令
    public static class NetworkConnectCommandFactory implements CommandFactory {
        @Override
        public Command create(Object... params) {
            String host = (String) params[0];
            int port = (Integer) params[1];
            return new NetworkConnectCommand(host, port);
        }
    }

    public static class NetworkDisconnectCommandFactory implements CommandFactory {
        @Override
        public Command create(Object... params) {
            String connectionId = (String) params[0];
            return new NetworkDisconnectCommand(connectionId);
        }
    }

    public static class NetworkSendCommandFactory implements CommandFactory {
        @Override
        public Command create(Object... params) {
            String connectionId = (String) params[0];
            byte[] data = (byte[]) params[1];
            return new NetworkSendCommand(connectionId, data);
        }
    }

    public static class NetworkReceiveCommandFactory implements CommandFactory {
        @Override
        public Command create(Object... params) {
            String connectionId = (String) params[0];
            int bufferSize = params.length > 1 ? (Integer) params[1] : 1024;
            return new NetworkReceiveCommand(connectionId, bufferSize);
        }
    }

    public static class NetworkConnectCommand implements Command {
        private final String host;
        private final int port;
        private Socket socket;
        private boolean executed = false;

        public NetworkConnectCommand(String host, int port) {
            this.host = host;
            this.port = port;
        }

        @Override
        public Object execute() throws Exception {
            // 模拟网络连接
            socket = new Socket(); // 这里不会实际连接，只是创建对象
            System.out.println("Network connection established to " + host + ":" + port);
            executed = true;
            return socket;
        }

        @Override
        public void undo() throws Exception {
            if (executed && socket != null) {
                // 模拟断开连接
                socket.close();
                System.out.println("Network connection closed for " + host + ":" + port);
                executed = false;
            }
        }

        @Override
        public boolean isUndoable() {
            return true;
        }

        @Override
        public String getDescription() {
            return "Connect to network host: " + host + ":" + port;
        }

        @Override
        public String getType() {
            return "network_connect";
        }
    }

    public static class NetworkDisconnectCommand implements Command {
        private final String connectionId;
        private boolean executed = false;

        public NetworkDisconnectCommand(String connectionId) {
            this.connectionId = connectionId;
        }

        @Override
        public Object execute() throws Exception {
            System.out.println("Network connection closed: " + connectionId);
            executed = true;
            return connectionId;
        }

        @Override
        public void undo() throws Exception {
            if (executed) {
                System.out.println("Network disconnection undone: " + connectionId);
                executed = false;
            }
        }

        @Override
        public boolean isUndoable() {
            return true;
        }

        @Override
        public String getDescription() {
            return "Disconnect network connection: " + connectionId;
        }

        @Override
        public String getType() {
            return "network_disconnect";
        }
    }

    public static class NetworkSendCommand implements Command {
        private final String connectionId;
        private final byte[] data;
        private boolean executed = false;

        public NetworkSendCommand(String connectionId, byte[] data) {
            this.connectionId = connectionId;
            this.data = data.clone();
        }

        @Override
        public Object execute() throws Exception {
            System.out.println("Data sent over connection " + connectionId + ": " + data.length + " bytes");
            executed = true;
            return data.length;
        }

        @Override
        public void undo() throws Exception {
            if (executed) {
                System.out.println("Data send undone for connection: " + connectionId);
                executed = false;
            }
        }

        @Override
        public boolean isUndoable() {
            return true;
        }

        @Override
        public String getDescription() {
            return "Send data over network connection: " + connectionId;
        }

        @Override
        public String getType() {
            return "network_send";
        }
    }

    public static class NetworkReceiveCommand implements Command {
        private final String connectionId;
        private final int bufferSize;
        private byte[] receivedData;
        private boolean executed = false;

        public NetworkReceiveCommand(String connectionId, int bufferSize) {
            this.connectionId = connectionId;
            this.bufferSize = bufferSize;
        }

        @Override
        public Object execute() throws Exception {
            // 模拟接收数据
            receivedData = new byte[Math.min(bufferSize, 100)]; // 模拟接收到一些数据
            for (int i = 0; i < receivedData.length; i++) {
                receivedData[i] = (byte) (i % 256);
            }
            System.out.println("Data received from connection " + connectionId + ": " + receivedData.length + " bytes");
            executed = true;
            return receivedData;
        }

        @Override
        public void undo() throws Exception {
            if (executed) {
                System.out.println("Data receive undone for connection: " + connectionId);
                executed = false;
            }
        }

        @Override
        public boolean isUndoable() {
            return true;
        }

        @Override
        public String getDescription() {
            return "Receive data from network connection: " + connectionId;
        }

        @Override
        public String getType() {
            return "network_receive";
        }
    }

    // 复合命令 - 组合多个命令
    public static class CompositeCommandFactory implements CommandFactory {
        @Override
        public Command create(Object... params) {
            @SuppressWarnings("unchecked")
            List<Command> commands = (List<Command>) params[0];
            return new CompositeCommand(commands);
        }
    }

    public static class CompositeCommand implements Command {
        private final List<Command> commands;
        private boolean executed = false;

        public CompositeCommand(List<Command> commands) {
            this.commands = new ArrayList<>(commands);
        }

        @Override
        public Object execute() throws Exception {
            List<Object> results = new ArrayList<>();
            Exception lastException = null;

            for (Command command : commands) {
                try {
                    results.add(command.execute());
                } catch (Exception e) {
                    lastException = e;
                    break;
                }
            }

            if (lastException != null) {
                // 如果有命令失败，撤销已执行的命令
                for (int i = results.size() - 1; i >= 0; i--) {
                    try {
                        commands.get(i).undo();
                    } catch (Exception undoException) {
                        System.err.println("Failed to undo command: " + undoException.getMessage());
                    }
                }
                throw lastException;
            }

            executed = true;
            return results;
        }

        @Override
        public void undo() throws Exception {
            if (executed) {
                // 逆序撤销命令
                for (int i = commands.size() - 1; i >= 0; i--) {
                    commands.get(i).undo();
                }
                executed = false;
            }
        }

        @Override
        public boolean isUndoable() {
            return commands.stream().allMatch(Command::isUndoable);
        }

        @Override
        public String getDescription() {
            return "Execute composite command with " + commands.size() + " sub-commands";
        }

        @Override
        public String getType() {
            return "composite";
        }
    }

    // 命令队列 - 支持异步命令执行
    public static class CommandQueue {
        private final BlockingQueue<Command> queue = new LinkedBlockingQueue<>();
        private final ExecutorService executor = Executors.newSingleThreadExecutor();
        private volatile boolean running = true;

        public CommandQueue() {
            executor.submit(this::processCommands);
        }

        public void enqueue(Command command) {
            try {
                queue.put(command);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }

        private void processCommands() {
            while (running) {
                try {
                    Command command = queue.take();
                    command.execute();
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                    break;
                } catch (Exception e) {
                    System.err.println("Command execution failed in queue: " + e.getMessage());
                }
            }
        }

        public void shutdown() {
            running = false;
            executor.shutdown();
            try {
                if (!executor.awaitTermination(5, TimeUnit.SECONDS)) {
                    executor.shutdownNow();
                }
            } catch (InterruptedException e) {
                executor.shutdownNow();
                Thread.currentThread().interrupt();
            }
        }

        public int getQueueSize() {
            return queue.size();
        }
    }
}