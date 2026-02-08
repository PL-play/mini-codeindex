# Q5

**Question**: 项目中有哪些设计模式示例？各自对应的类或文件在哪里？

**Answer**:

项目中采用了多种经典的设计模式，主要集中在 Java 的管理类架构和 Python 的插件式/策略化实现中。以下是详细的设计模式示例及其对应的类与文件位置：

### 1. 创建型模式 (Creational Patterns)

*   **单例模式 (Singleton)**
    *   **说明**：用于确保管理类在全局只有一个实例，并提供线程安全的访问。
    *   **对应类/文件**：
        *   `DecoratorManager`: [src/main/java/com/example/DecoratorManager.java:17-23]
        *   `FactoryManager`: [src/main/java/com/example/FactoryManager.java:12-15]
        *   `StrategyManager`: [src/main/java/com/example/StrategyManager.java:15-19]
        *   `AdapterManager`: [src/main/java/com/example/AdapterManager.java:22-26]
*   **工厂模式 (Factory)**
    *   **说明**：通过工厂接口动态创建对象，解耦了对象的创建与使用。
    *   **对应类/文件**：
        *   `ObjectFactory` 接口及其实现类（如 `UserFactory`）: [src/main/java/com/example/FactoryManager.java:121-137]
        *   `DecoratorFactory` 接口及其实现类（如 `LoggingDecoratorFactory`）: [src/main/java/com/example/DecoratorManager.java:144-153]
*   **建造者模式 (Builder)**
    *   **说明**：用于构建复杂的 `User` 实体对象。
    *   **对应类/文件**：
        *   `User.Builder`: [src/main/java/com/example/FactoryManager.java:137] (在 `UserFactory` 中调用)

### 2. 结构型模式 (Structural Patterns)

*   **装饰器模式 (Decorator)**
    *   **说明**：动态地给对象添加额外的职责（如日志、缓存、加密等）。
    *   **对应类/文件**：
        *   `Decorator` 接口及其实现类（如 `LoggingDecorator`, `CachingDecorator`）: [src/main/java/com/example/DecoratorManager.java:138-197]
        *   Python 原生装饰器（用于缓存和认证）: [src/authentication.py:21]
*   **适配器模式 (Adapter)**
    *   **说明**：将不兼容的接口转换为客户端期望的接口。
    *   **对应类/文件**：
        *   `Adapter` 接口及其实现类（如 `DatabaseAdapter`, `PaymentAdapter`）: [src/main/java/com/example/AdapterManager.java:22-55]

### 3. 行为型模式 (Behavioral Patterns)

*   **策略模式 (Strategy)**
    *   **说明**：定义一系列算法，并将每一个算法封装起来，使它们可以相互替换。
    *   **对应类/文件**：
        *   Java 实现：`Strategy` 接口及其实现类（如 `SortingStrategyFactory` 中的排序算法）: [src/main/java/com/example/StrategyManager.java:158-164]
        *   Python 实现：`ConfigProvider` (配置源策略), `DatabaseManager` (数据库后端策略), `NotificationProvider` (通知渠道策略): [src/main/python/config.py:28-34], [src/main/python/database.py:52-63], [src/main/python/notification.py:74-80]
*   **观察者模式 (Observer)**
    *   **说明**：定义对象间的一对多依赖，当一个对象状态改变时，所有依赖者都会收到通知。
    *   **对应类/文件**：
        *   `Subject` 和 `Observer` 接口: [src/main/java/com/example/ObserverManager.java:176-185]
        *   `EventSystem` (事件驱动架构): [src/main/java/com/example/EventSystem.java:13-22]
*   **命令模式 (Command)**
    *   **说明**：将请求封装为对象，支持撤销/重做和异步执行。
    *   **对应类/文件**：
        *   `CommandManager` 及其内部的 `Command` 历史管理: [src/main/java/com/example/CommandManager.java:19-160]
*   **模板方法模式 (Template Method)**
    *   **说明**：在父类中定义算法骨架，将具体步骤延迟到子类中实现。
    *   **对应类/文件**：
        *   `DatabaseManager.transaction` (定义了事务处理的通用流程): [src/main/python/database.py:91-98]

### 总结映射表

| 设计模式 | 主要文件位置 | 核心类/接口 |
| :--- | :--- | :--- |
| **Singleton** | `FactoryManager.java`, `StrategyManager.java` | `getInstance()` 方法 |
| **Factory** | `FactoryManager.java`, `DecoratorManager.java` | `ObjectFactory`, `DecoratorFactory` |
| **Strategy** | `StrategyManager.java`, `config.py`, `database.py` | `Strategy`, `ConfigProvider`, `DatabaseManager` |
| **Observer** | `ObserverManager.java`, `EventSystem.java` | `Subject`, `Observer`, `EventListener` |
| **Decorator** | `DecoratorManager.java`, `authentication.py` | `Decorator`, `@lru_cache` |
| **Adapter** | `AdapterManager.java` | `Adapter`, `DatabaseAdapter` |
| **Command** | `CommandManager.java` | `Command`, `commandHistory` |
| **Builder** | `User.java` (由 `FactoryManager` 调用) | `User.Builder` |
