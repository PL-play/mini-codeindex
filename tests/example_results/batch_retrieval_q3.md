# Q3

**Question**: Java 侧的用户管理功能涉及哪些核心类，它们之间是什么关系？

**Answer**:

Java 侧的用户管理功能并非基于 Spring Boot 等标准 Web 框架，而是采用了一种基于**命令模式（Command Pattern）**和**核心服务层**的自定义架构。

以下是该功能涉及的核心类及其关系分析：

### 1. 核心实体与数据模型
*   **`User`**: 核心数据模型，包含用户基本信息（ID、姓名、邮箱、年龄、部门）、权限角色（Roles）、技能列表（Skills）以及元数据（Metadata）。[User:src/main/java/com/example/User.java:14-28]
*   **`User.UserStatus`**: 枚举类，定义了用户的状态，如 `ACTIVE`（活跃）、`INACTIVE`（非活跃）、`SUSPENDED`（停用）等。[User:src/main/java/com/example/User.java:36-38]

### 2. 业务逻辑与服务层
*   **`UserService`**: 用户管理的核心服务类。它负责处理用户数据的持久化逻辑、验证和审计。
    *   **存储机制**：使用 `ConcurrentHashMap` 进行内存级存储，并配合 `ReadWriteLock` 确保并发安全。[UserService:src/main/java/com/example/UserService.java:18-22]
    *   **内部组件**：集成 `AuditLogger`（审计日志）、`UserValidator`（数据验证）和 `UserStatistics`（统计分析）。[UserService:src/main/java/com/example/UserService.java:23-25]
*   **`PermissionManager`**: 独立于 `UserService`，专门负责用户权限和角色的校验与分配。

### 3. 功能入口：命令模式实现
该项目通过 `CommandManager` 将用户操作封装为可执行的命令对象，这是外部调用用户管理功能的主要入口：
*   **`CommandManager`**: 维护命令工厂的注册表，负责创建和执行用户相关的指令。[CommandManager:src/main/java/com/example/CommandManager.java:71-74]
*   **具体命令类**：
    *   `UserCreateCommand`: 处理用户创建。
    *   `UserUpdateCommand`: 处理信息更新。
    *   `UserDeleteCommand`: 处理用户删除。
    *   `UserLoginCommand`: 处理登录逻辑。

### 4. 核心类之间的关系
1.  **组合关系 (Composition)**：`UserService` 组合了 `UserValidator` 和 `AuditLogger`，在执行增删改查操作前先通过验证器校验，操作后由审计日志记录。
2.  **工厂模式 (Factory Pattern)**：`CommandManager` 通过各种 `CommandFactory`（如 `UserCreateCommandFactory`）动态生成具体的命令实例。
3.  **依赖关系 (Dependency)**：
    *   `Command` 对象在执行时会调用 `UserService` 提供的底层方法。
    *   `AdapterManager$AuthenticationAdapter` 作为适配器，将底层的认证逻辑（可能涉及 Python 侧的 `authentication.py`）与 Java 侧的服务进行对接。

### 总结
Java 侧的用户管理是一个高度解耦的系统，通过 **Command -> Service -> Entity** 的链路运行。它不依赖外部数据库框架（如 JPA/Hibernate），而是通过 `UserService` 在内存中管理 `User` 实体，并利用命令模式实现了操作的可追溯性和统一触发机制。
