# Q4

**Question**: Python 侧的数据处理流程是什么，入口脚本和关键依赖文件有哪些？

**Answer**:

Python 侧的数据处理流程是一个典型的 **ETL（提取、转换、加载）** 架构，主要通过 `DataProcessor` 类进行核心逻辑的调度。以下是详细的流程分析、入口脚本及关键依赖文件：

### 1. 数据处理流程 (Data Processing Flow)
Python 侧的数据处理遵循 **“加载 -> 转换（流水线+增强）-> 分析 -> 保存”** 的模式：

1.  **数据摄取 (Ingestion)**：
    *   从本地文件系统读取 JSON 或 CSV 格式的原始数据 [src/main/python/data_processor.py:188]。
    *   通过 `APIClient` 从外部 REST 接口同步用户数据，支持 HMAC 和 Bearer 认证 [src/main/python/api_client.py:84]。
    *   通过 `DatabaseManager` 从 SQLite、PostgreSQL 或 MySQL 数据库中提取数据 [src/main/python/database.py:52]。
2.  **数据转换流水线 (Transformation Pipeline)**：
    *   系统采用插件化设计，通过 `DataTransformer` 基类实现多个转换器：
        *   `EmailNormalizer`：标准化邮箱格式。
        *   `AgeCategorizer`：根据年龄段进行分类（如 minor, adult 等）。
        *   `SkillAnalyzer`：分析用户技能标签（如是否包含 Python/Java）。
    *   **逻辑增强**：在基础转换后，系统会自动执行复杂计算（如年龄平方、开方）、文本分析（域名提取、技能多样性评分）以及统计特征工程（Z-Score 计算、分组统计） [src/main/python/data_processor.py:214-221]。
3.  **数据持久化与输出 (Persistence & Output)**：
    *   **文件存储**：将处理后的 DataFrame 保存为 CSV 或 JSON 文件 [src/main/python/data_processor.py:324]。
    *   **数据库更新**：通过 SQL 执行器将结果回写至关系型数据库。
    *   **外部通知**：处理完成后，可通过 `NotificationService` 发送 SMTP 邮件或推送通知 [src/main/python/notification.py:88]。

### 2. 入口脚本 (Entry Points)
项目没有统一的 CLI 框架，而是依赖于脚本级的 `main` 块执行：

*   **核心处理入口**：`src/main/python/data_processor.py`
    这是数据处理的主程序，包含了同步、异步（`process_async`）和并行（`process_parallel`）三种处理模式的调用示例 [src/main/python/data_processor.py:663]。
*   **功能演示入口**：
    *   `src/caching.py`：用于演示或测试缓存机制的入口 [src/caching.py:916]。
    *   `src/authentication.py`：用于演示身份验证逻辑的入口 [src/authentication.py:699]。

### 3. 关键依赖文件 (Key Dependencies)
项目通过标准的依赖清单管理外部库：

*   **`requirements.txt` (Python 核心依赖)**：
    *   `pandas` (2.1.4)：用于核心数据清洗、转换和 DataFrame 操作。
    *   `numpy` (1.24.3)：用于数值计算和统计特征生成。
    *   `requests` (2.31.0)：用于 API 客户端的网络请求。
*   **`pom.xml` (Java 侧相关依赖)**：
    *   `gson` (2.10.1)：由于项目是多语言环境，Java 侧使用 Gson 处理与 Python 侧交互的 JSON 数据 [pom.xml:18-22]。
*   **内部核心模块**：
    *   `config.py`：管理环境变量和 YAML/JSON 配置加载。
    *   `database.py`：封装了多种 SQL 数据库的连接池和事务管理逻辑。
    *   `api_client.py`：集成了重试机制（backoff）和速率限制（RateLimiter）的 API 调用封装。
