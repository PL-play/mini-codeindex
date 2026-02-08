# Subtask Debug Report

**Title**: Synthesize module relationships
**Instruction**: Determine if and how the Java and Python components interact (e.g., via APIs, shared data, or subprocess calls) to provide a holistic view.

## Tool Calls
### Think Reflection
Reflection recorded: I need to determine how the Java and Python components interact in this project. I'll start by exploring the directory structure to identify the Java and Python modules and then search for common interaction patterns like subprocess calls, API endpoints (HTTP/gRPC), or shared files.

Plan:
1. Use tree_summary_tool to see the project structure.
2. Use language_stats_tool to confirm the presence of Java and Python files.
3. Search for interaction keywords:
    - Python calling Java: "subprocess", "Popen", "os.system", "py4j", "jpype".
    - Java calling Python: "ProcessBuilder", "Runtime.getRuntime().exec", "Jython".
    - Shared communication: "localhost", "port", "http", "socket", "json", "grpc", "thrift".
    - Shared data: "csv", "json", "database", "sql".

### Call 1
```json
{
  "tool": "tree_summary_tool",
  "args": {
    "root_dir": "/home/ran/Documents/work/VectorCode/mini_code_index/test_code_index_project"
  },
  "result": {
    "tree": {
      "name": "test_code_index_project",
      "path": "test_code_index_project",
      "type": "dir",
      "children": [
        {
          "name": "src",
          "path": "src",
          "type": "dir",
          "children": [
            {
              "name": "main",
              "path": "src/main",
              "type": "dir",
              "children": [
                {
                  "name": "java",
                  "path": "src/main/java",
                  "type": "dir",
                  "children": [
                    {
                      "name": "com",
                      "path": "src/main/java/com",
                      "type": "dir",
                      "children": []
                    }
                  ]
                },
                {
                  "name": "python",
                  "path": "src/main/python",
                  "type": "dir",
                  "children": [
                    {
                      "name": "api_client.py",
                      "path": "src/main/python/api_client.py",
                      "type": "file"
                    },
                    {
                      "name": "config.py",
                      "path": "src/main/python/config.py",
                      "type": "file"
                    },
                    {
                      "name": "data_processor.py",
                      "path": "src/main/python/data_processor.py",
                      "type": "file"
                    },
                    {
                      "name": "database.py",
                      "path": "src/main/python/database.py",
                      "type": "file"
                    },
                    {
                      "name": "notification.py",
                      "path": "src/main/python/notification.py",
                      "type": "file"
                    }
                  ]
                }
              ]
            },
            {
              "name": "authentication.py",
              "path": "src/authentication.py",
              "type": "file"
            },
            {
              "name": "caching.py",
              "path": "src/caching.py",
              "type": "file"
            }
          ]
        },
        {
          "name": "target",
          "path": "target",
          "type": "dir",
          "children": [
            {
              "name": "classes",
              "path": "target/classes",
              "type": "dir",
              "children": [
                {
                  "name": "com",
                  "path": "target/classes/com",
                  "type": "dir",
                  "children": [
                    {
                      "name": "example",
                      "path": "target/classes/com/example",
                      "type": "dir",
                      "children": []
                    }
                  ]
                }
              ]
            },
            {
              "name": "generated-sources",
              "path": "target/generated-sources",
              "type": "dir",
              "children": [
                {
                  "name": "annotations",
                  "path": "target/generated-sources/annotations",
                  "type": "dir",
                  "children": []
                }
              ]
            },
            {
              "name": "maven-status",
              "path": "target/maven-status",
              "type": "dir",
              "children": [
                {
                  "name": "maven-compiler-plugin",
                  "path": "target/maven-status/maven-compiler-plugin",
                  "type": "dir",
                  "children": [
                    {
                      "name": "compile",
                      "path": "target/maven-status/maven-compiler-plugin/compile",
                      "type": "dir",
                      "children": []
                    }
                  ]
                }
              ]
            },
            {
              "name": "test-classes",
              "path": "target/test-classes",
              "type": "dir",
              "children": []
            }
          ]
        },
        {
          "name": "pom.xml",
          "path": "pom.xml",
          "type": "file"
        },
        {
          "name": "README.md",
          "path": "README.md",
          "type": "file"
        },
        {
          "name": "requirements.txt",
          "path": "requirements.txt",
          "type": "file"
        }
      ]
    }
  },
  "tool_iter": 1,
  "call_index": 1
}
```

### Call 2
```json
{
  "tool": "language_stats_tool",
  "args": {
    "root_dir": "/home/ran/Documents/work/VectorCode/mini_code_index/test_code_index_project"
  },
  "result": [
    {
      "ext": ".class",
      "files": 230,
      "lines": 12467
    },
    {
      "ext": ".java",
      "files": 16,
      "lines": 8237
    },
    {
      "ext": ".lst",
      "files": 2,
      "lines": 247
    },
    {
      "ext": ".md",
      "files": 1,
      "lines": 28
    },
    {
      "ext": ".py",
      "files": 7,
      "lines": 4488
    },
    {
      "ext": ".txt",
      "files": 1,
      "lines": 3
    },
    {
      "ext": ".xml",
      "files": 1,
      "lines": 24
    }
  ],
  "tool_iter": 1,
  "call_index": 2
}
```

### Think Reflection
Reflection recorded: The project has both Java and Python components.
Java is located in `src/main/java/com/...` and Python is in `src/main/python/` and `src/`.
There is a `pom.xml` (Maven) and `requirements.txt` (Python).

I'll look for interaction points:
1. `src/main/python/api_client.py` suggests Python might be calling an API (possibly Java's).
2. `src/main/python/database.py` suggests shared data via a database.
3. I'll search for "ProcessBuilder" or "exec" in Java files to see if it calls Python.
4. I'll search for "requests" or "http" in Python files.
5. I'll search for "localhost" or port numbers in both.

Let's start by listing the Java files to get a better idea of the package structure.

### Call 3
```json
{
  "tool": "path_glob_tool",
  "args": {
    "pattern": "src/main/java/**/*.java",
    "root_dir": "/home/ran/Documents/work/VectorCode/mini_code_index/test_code_index_project"
  },
  "result": [
    {
      "path": "src/main/java/com/example/DecoratorManager.java"
    },
    {
      "path": "src/main/java/com/example/FactoryManager.java"
    },
    {
      "path": "src/main/java/com/example/CommandManager.java"
    },
    {
      "path": "src/main/java/com/example/UserService.java"
    },
    {
      "path": "src/main/java/com/example/ReportGenerator.java"
    },
    {
      "path": "src/main/java/com/example/EventSystem.java"
    },
    {
      "path": "src/main/java/com/example/StrategyManager.java"
    },
    {
      "path": "src/main/java/com/example/AdapterManager.java"
    },
    {
      "path": "src/main/java/com/example/AdvancedUtils.java"
    },
    {
      "path": "src/main/java/com/example/AuditLogger.java"
    },
    {
      "path": "src/main/java/com/example/ObserverManager.java"
    },
    {
      "path": "src/main/java/com/example/DataProcessor.java"
    },
    {
      "path": "src/main/java/com/example/PermissionManager.java"
    },
    {
      "path": "src/main/java/com/example/NotificationService.java"
    },
    {
      "path": "src/main/java/com/example/User.java"
    },
    {
      "path": "src/main/java/com/example/CacheManager.java"
    }
  ],
  "tool_iter": 3,
  "call_index": 1
}
```

### Call 4
```json
{
  "tool": "text_search_tool",
  "args": {
    "root_dir": "/home/ran/Documents/work/VectorCode/mini_code_index/test_code_index_project",
    "query": "ProcessBuilder|Runtime\\.getRuntime\\(\\)\\.exec|subprocess|requests|http|localhost|port"
  },
  "result": [],
  "tool_iter": 3,
  "call_index": 2
}
```

### Think Reflection
Reflection recorded: The previous search for "ProcessBuilder|Runtime\.getRuntime\(\)\.exec|subprocess|requests|http|localhost|port" returned no results, which is unexpected given the file names like `api_client.py`. It's possible the search was too restrictive or the interaction is different.

Let's try:
1. Reading `src/main/python/api_client.py` to see what it connects to.
2. Reading `src/main/python/database.py` to see if it shares a database with Java.
3. Searching for "python" in Java files and "java" in Python files.
4. Checking `pom.xml` for any web framework (like Spring Boot) that might expose an API.
5. Checking `requirements.txt` for any libraries like `requests`, `flask`, `fastapi`, or `py4j`.

### Call 5
```json
{
  "tool": "read_file_range_tool",
  "args": {
    "start_line": 1,
    "path": "/home/ran/Documents/work/VectorCode/mini_code_index/test_code_index_project/src/main/python/api_client.py",
    "end_line": 50
  },
  "result": {
    "content": "#!/usr/bin/env python3\n\"\"\"\nAPI 客户端模块\n提供外部 API 集成功能\n\"\"\"\n\nimport requests\nimport aiohttp\nimport asyncio\nfrom typing import Dict, Any, List, Optional, Union\nimport json\nimport logging\nfrom dataclasses import dataclass\nimport time\nfrom functools import wraps\nimport jwt\nimport hashlib\nimport hmac\nimport base64\nfrom urllib.parse import urlencode\nimport threading\nfrom concurrent.futures import ThreadPoolExecutor\nimport backoff\n\nlogger = logging.getLogger(__name__)\n\n\n@dataclass\nclass APIConfig:\n    \"\"\"API 配置\"\"\"\n    base_url: str\n    api_key: Optional[str] = None\n    api_secret: Optional[str] = None\n    timeout: int = 30\n    retries: int = 3\n    rate_limit: int = 100  # requests per minute\n    auth_type: str = \"bearer\"  # bearer, basic, api_key, hmac\n\n\n@dataclass\nclass APIResponse:\n    \"\"\"API 响应\"\"\"\n    status_code: int\n    data: Any\n    headers: Dict[str, str]\n    success: bool\n    error_message: Optional[str] = None\n    request_time: float = 0.0\n\n"
  },
  "tool_iter": 5,
  "call_index": 1
}
```

### Call 6
```json
{
  "tool": "read_file_range_tool",
  "args": {
    "end_line": 50,
    "path": "/home/ran/Documents/work/VectorCode/mini_code_index/test_code_index_project/src/main/python/database.py",
    "start_line": 1
  },
  "result": {
    "content": "#!/usr/bin/env python3\n\"\"\"\n数据库管理模块\n提供数据库连接、查询、事务管理等功能\n\"\"\"\n\nimport sqlite3\nimport psycopg2\nimport mysql.connector\nfrom typing import List, Dict, Any, Optional, Union\nfrom contextlib import contextmanager\nfrom dataclasses import dataclass\nimport logging\nimport time\nimport json\nfrom abc import ABC, abstractmethod\nfrom enum import Enum\n\nlogger = logging.getLogger(__name__)\n\n\nclass DatabaseType(Enum):\n    SQLITE = \"sqlite\"\n    POSTGRESQL = \"postgresql\"\n    MYSQL = \"mysql\"\n\n\n@dataclass\nclass DatabaseConfig:\n    \"\"\"数据库配置\"\"\"\n    db_type: DatabaseType\n    host: str = \"localhost\"\n    port: Optional[int] = None\n    database: str = \"\"\n    username: str = \"\"\n    password: str = \"\"\n    connection_pool_size: int = 10\n    connection_timeout: int = 30\n    max_retries: int = 3\n\n\nclass DatabaseConnectionError(Exception):\n    \"\"\"数据库连接异常\"\"\"\n    pass\n\n\nclass DatabaseQueryError(Exception):\n    \"\"\"数据库查询异常\"\"\"\n    pass\n"
  },
  "tool_iter": 5,
  "call_index": 2
}
```

### Call 7
```json
{
  "tool": "read_file_range_tool",
  "args": {
    "end_line": 50,
    "path": "/home/ran/Documents/work/VectorCode/mini_code_index/test_code_index_project/pom.xml",
    "start_line": 1
  },
  "result": {
    "content": "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<project xmlns=\"http://maven.apache.org/POM/4.0.0\"\n         xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n         xsi:schemaLocation=\"http://maven.apache.org/POM/4.0.0\n         http://maven.apache.org/xsd/maven-4.0.0.xsd\">\n    <modelVersion>4.0.0</modelVersion>\n\n    <groupId>com.example</groupId>\n    <artifactId>test-code-index</artifactId>\n    <version>1.0-SNAPSHOT</version>\n\n    <properties>\n        <maven.compiler.source>11</maven.compiler.source>\n        <maven.compiler.target>11</maven.compiler.target>\n    </properties>\n\n    <dependencies>\n        <dependency>\n            <groupId>com.google.code.gson</groupId>\n            <artifactId>gson</artifactId>\n            <version>2.10.1</version>\n        </dependency>\n    </dependencies>\n</project>"
  },
  "tool_iter": 5,
  "call_index": 3
}
```

### Call 8
```json
{
  "tool": "read_file_range_tool",
  "args": {
    "path": "/home/ran/Documents/work/VectorCode/mini_code_index/test_code_index_project/requirements.txt",
    "end_line": 10,
    "start_line": 1
  },
  "result": {
    "content": "requests==2.31.0\npandas==2.1.4\nnumpy==1.24.3"
  },
  "tool_iter": 5,
  "call_index": 4
}
```

### Think Reflection
Reflection recorded: The `api_client.py` uses `requests` and `aiohttp`, and `database.py` supports SQLite, PostgreSQL, and MySQL. `pom.xml` only has `gson` as a dependency, which is for JSON processing.

I still haven't found a direct link between Java and Python.
Let's look for:
1. Any configuration files (like `.env`, `config.yaml`, `application.properties`) that might define shared ports or database names.
2. Search for "python" in the whole project.
3. Search for "java" in the whole project.
4. Check `src/main/python/config.py`.
5. Check `src/main/java/com/example/DataProcessor.java` and `src/main/python/data_processor.py` to see if they perform complementary tasks or share logic.
6. Check `src/main/java/com/example/NotificationService.java` and `src/main/python/notification.py`.

The search for "requests" failed earlier, but `api_client.py` clearly imports it. This might be because I used a regex with `|` and maybe the tool didn't handle it as expected or I made a mistake. I'll try searching for "requests" alone.

### Call 9
```json
{
  "tool": "text_search_tool",
  "args": {
    "root_dir": "/home/ran/Documents/work/VectorCode/mini_code_index/test_code_index_project",
    "query": "requests"
  },
  "result": [
    {
      "path": "requirements.txt",
      "line": 1,
      "col": 1,
      "snippet": "requests==2.31.0",
      "context_before": "",
      "context_after": "pandas==2.1.4\nnumpy==1.24.3"
    },
    {
      "path": "src/caching.py",
      "line": 113,
      "col": 15,
      "snippet": "total_requests = self.hits + self.misses",
      "context_before": "    def update_hit_rate(self):\n        \"\"\"Update hit rate calculation.\"\"\"",
      "context_after": "        self.hit_rate = self.hits / total_requests if total_requests > 0 else 0.0\n"
    },
    {
      "path": "src/caching.py",
      "line": 114,
      "col": 43,
      "snippet": "self.hit_rate = self.hits / total_requests if total_requests > 0 else 0.0",
      "context_before": "        \"\"\"Update hit rate calculation.\"\"\"\n        total_requests = self.hits + self.misses",
      "context_after": "\n    def reset(self):"
    },
    {
      "path": "src/caching.py",
      "line": 114,
      "col": 61,
      "snippet": "self.hit_rate = self.hits / total_requests if total_requests > 0 else 0.0",
      "context_before": "        \"\"\"Update hit rate calculation.\"\"\"\n        total_requests = self.hits + self.misses",
      "context_after": "\n    def reset(self):"
    },
    {
      "path": "src/main/python/api_client.py",
      "line": 7,
      "col": 8,
      "snippet": "import requests",
      "context_before": "\"\"\"\n",
      "context_after": "import aiohttp\nimport asyncio"
    },
    {
      "path": "src/main/python/api_client.py",
      "line": 36,
      "col": 30,
      "snippet": "rate_limit: int = 100  # requests per minute",
      "context_before": "    timeout: int = 30\n    retries: int = 3",
      "context_after": "    auth_type: str = \"bearer\"  # bearer, basic, api_key, hmac\n"
    },
    {
      "path": "src/main/python/api_client.py",
      "line": 62,
      "col": 24,
      "snippet": "def __init__(self, requests_per_minute: int):",
      "context_before": "    \"\"\"速率限制器\"\"\"\n",
      "context_after": "        self.requests_per_minute = requests_per_minute\n        self.requests = []"
    },
    {
      "path": "src/main/python/api_client.py",
      "line": 63,
      "col": 14,
      "snippet": "self.requests_per_minute = requests_per_minute",
      "context_before": "\n    def __init__(self, requests_per_minute: int):",
      "context_after": "        self.requests = []\n        self.lock = threading.Lock()"
    },
    {
      "path": "src/main/python/api_client.py",
      "line": 63,
      "col": 36,
      "snippet": "self.requests_per_minute = requests_per_minute",
      "context_before": "\n    def __init__(self, requests_per_minute: int):",
      "context_after": "        self.requests = []\n        self.lock = threading.Lock()"
    },
    {
      "path": "src/main/python/api_client.py",
      "line": 64,
      "col": 14,
      "snippet": "self.requests = []",
      "context_before": "    def __init__(self, requests_per_minute: int):\n        self.requests_per_minute = requests_per_minute",
      "context_after": "        self.lock = threading.Lock()\n"
    },
    {
      "path": "src/main/python/api_client.py",
      "line": 72,
      "col": 18,
      "snippet": "self.requests = [req_time for req_time in self.requests if now - req_time < 60]",
      "context_before": "            now = time.time()\n            # 移除一分钟前的请求",
      "context_after": "\n            if len(self.requests) >= self.requests_per_minute:"
    },
    {
      "path": "src/main/python/api_client.py",
      "line": 72,
      "col": 60,
      "snippet": "self.requests = [req_time for req_time in self.requests if now - req_time < 60]",
      "context_before": "            now = time.time()\n            # 移除一分钟前的请求",
      "context_after": "\n            if len(self.requests) >= self.requests_per_minute:"
    },
    {
      "path": "src/main/python/api_client.py",
      "line": 74,
      "col": 25,
      "snippet": "if len(self.requests) >= self.requests_per_minute:",
      "context_before": "            self.requests = [req_time for req_time in self.requests if now - req_time < 60]\n",
      "context_after": "                # 计算需要等待的时间\n                oldest_request = min(self.requests)"
    },
    {
      "path": "src/main/python/api_client.py",
      "line": 74,
      "col": 43,
      "snippet": "if len(self.requests) >= self.requests_per_minute:",
      "context_before": "            self.requests = [req_time for req_time in self.requests if now - req_time < 60]\n",
      "context_after": "                # 计算需要等待的时间\n                oldest_request = min(self.requests)"
    },
    {
      "path": "src/main/python/api_client.py",
      "line": 76,
      "col": 43,
      "snippet": "oldest_request = min(self.requests)",
      "context_before": "            if len(self.requests) >= self.requests_per_minute:\n                # 计算需要等待的时间",
      "context_after": "                wait_time = 60 - (now - oldest_request)\n                if wait_time > 0:"
    },
    {
      "path": "src/main/python/api_client.py",
      "line": 81,
      "col": 18,
      "snippet": "self.requests.append(now)",
      "context_before": "                    time.sleep(wait_time)\n",
      "context_after": "\n"
    },
    {
      "path": "src/main/python/api_client.py",
      "line": 89,
      "col": 24,
      "snippet": "self.session = requests.Session()",
      "context_before": "    def __init__(self, config: APIConfig):\n        self.config = config",
      "context_after": "        self.rate_limiter = RateLimiter(config.rate_limit)\n        self._setup_auth()"
    },
    {
      "path": "src/main/python/api_client.py",
      "line": 98,
      "col": 20,
      "snippet": "auth = requests.auth.HTTPBasicAuth(self.config.api_key, self.config.api_secret)",
      "context_before": "            self.session.headers.update({\"Authorization\": f\"Bearer {self.config.api_key}\"})\n        elif self.config.auth_type == \"basic\" and self.config.api_key and self.config.api_secret:",
      "context_after": "            self.session.auth = auth\n        elif self.config.auth_type == \"api_key\" and self.config.api_key:"
    },
    {
      "path": "src/main/python/api_client.py",
      "line": 120,
      "col": 42,
      "snippet": "@backoff.on_exception(backoff.expo, (requests.RequestException, APIError), max_tries=3)",
      "context_before": "        return base64.b64encode(signature).decode()\n",
      "context_after": "    def _make_request(self, method: str, endpoint: str, **kwargs) -> APIResponse:\n        \"\"\"发起请求\"\"\""
    },
    {
      "path": "src/main/python/api_client.py",
      "line": 172,
      "col": 16,
      "snippet": "except requests.RequestException as e:",
      "context_before": "            )\n",
      "context_after": "            request_time = time.time() - start_time\n            return APIResponse("
    },
    {
      "path": "src/main/python/config.py",
      "line": 229,
      "col": 16,
      "snippet": "rate_limit_requests: int = 100",
      "context_before": "    base_url: str = \"http://localhost:8000\"\n    api_key: str = \"\"",
      "context_after": "    rate_limit_window_seconds: int = 60\n    enable_cors: bool = True"
    }
  ],
  "tool_iter": 7,
  "call_index": 1
}
```

### Call 10
```json
{
  "tool": "text_search_tool",
  "args": {
    "root_dir": "/home/ran/Documents/work/VectorCode/mini_code_index/test_code_index_project",
    "query": "python"
  },
  "result": [
    {
      "path": "README.md",
      "line": 8,
      "col": 13,
      "snippet": "- `src/main/python/` - Python 脚本",
      "context_before": "\n- `src/main/java/com/example/` - Java 源代码",
      "context_after": "- `pom.xml` - Maven 配置（Java）\n- `requirements.txt` - Python 依赖"
    },
    {
      "path": "README.md",
      "line": 27,
      "col": 1,
      "snippet": "python src/main/python/data_processor.py",
      "context_before": "### Python\n```bash",
      "context_after": "```"
    },
    {
      "path": "README.md",
      "line": 27,
      "col": 17,
      "snippet": "python src/main/python/data_processor.py",
      "context_before": "### Python\n```bash",
      "context_after": "```"
    },
    {
      "path": "target/classes/com/example/UserService.class",
      "line": 217,
      "col": 8,
      "snippet": "\u0000\u0001\b\u0001\u0001\u0000\u0006python",
      "context_before": "\u0000\u0001\b\u0001\u0001\u0000\u0004java\n\u0001\u0001",
      "context_after": "\u0001\u0001\n\u0001\u0001\u0001\u0000\u0005build\u0001\u0000\u0014()Lcom/example/User;\b\u0001\u0001\u0000\u00012\b\u0001\u0001\u0000\tBob Smith\b\u0001\u0001\u0000\u000fbob@example.com\b\u0001\u0001\u0000\tmarketing\b\u0001\u0001\u0000\tanalytics"
    },
    {
      "path": "src/main/java/com/example/UserService.java",
      "line": 503,
      "col": 29,
      "snippet": ".skill(\"python\")",
      "context_before": "                    .department(\"engineering\")\n                    .skill(\"java\")",
      "context_after": "                    .build();\n"
    },
    {
      "path": "src/main/python/api_client.py",
      "line": 1,
      "col": 16,
      "snippet": "#!/usr/bin/env python3",
      "context_before": "",
      "context_after": "\"\"\"\nAPI 客户端模块"
    },
    {
      "path": "src/main/python/config.py",
      "line": 1,
      "col": 16,
      "snippet": "#!/usr/bin/env python3",
      "context_before": "",
      "context_after": "\"\"\"\n配置模块"
    },
    {
      "path": "src/main/python/data_processor.py",
      "line": 1,
      "col": 16,
      "snippet": "#!/usr/bin/env python3",
      "context_before": "",
      "context_after": "\"\"\"\n数据处理脚本"
    },
    {
      "path": "src/main/python/data_processor.py",
      "line": 148,
      "col": 19,
      "snippet": "data['has_python'] = data['skills'].apply(lambda x: 'python' in [s.lower() for s in x])",
      "context_before": "        data = data.copy()\n        data['skill_count'] = data['skills'].apply(len)",
      "context_after": "        data['has_java'] = data['skills'].apply(lambda x: 'java' in [s.lower() for s in x])\n        return data"
    },
    {
      "path": "src/main/python/data_processor.py",
      "line": 148,
      "col": 62,
      "snippet": "data['has_python'] = data['skills'].apply(lambda x: 'python' in [s.lower() for s in x])",
      "context_before": "        data = data.copy()\n        data['skill_count'] = data['skills'].apply(len)",
      "context_after": "        data['has_java'] = data['skills'].apply(lambda x: 'java' in [s.lower() for s in x])\n        return data"
    },
    {
      "path": "src/main/python/data_processor.py",
      "line": 286,
      "col": 46,
      "snippet": "lambda x: any(skill.lower() in ['python', 'java', 'javascript', 'c++', 'sql'] for skill in x)",
      "context_before": "        df['skill_diversity'] = df['skills'].apply(lambda x: len(set(x)) / len(x) if x else 0)\n        df['has_technical_skills'] = df['skills'].apply(",
      "context_after": "        )\n"
    },
    {
      "path": "src/main/python/data_processor.py",
      "line": 614,
      "col": 128,
      "snippet": "{\"id\": \"1\", \"name\": \"Alice Johnson\", \"email\": \"alice@example.com\", \"age\": 28, \"department\": \"engineering\", \"skills\": [\"python\", \"java\", \"sql\"]},",
      "context_before": "    # 示例数据\n    sample_data = [",
      "context_after": "        {\"id\": \"2\", \"name\": \"Bob Smith\", \"email\": \"bob@example.com\", \"age\": 35, \"department\": \"marketing\", \"skills\": [\"marketing\", \"analytics\"]},\n        {\"id\": \"3\", \"name\": \"Charlie Brown\", \"email\": \"charlie@test.com\", \"age\": 42, \"department\": \"engineering\", \"skills\": [\"c++\", \"python\", \"machine learning\"]},"
    },
    {
      "path": "src/main/python/data_processor.py",
      "line": 616,
      "col": 134,
      "snippet": "{\"id\": \"3\", \"name\": \"Charlie Brown\", \"email\": \"charlie@test.com\", \"age\": 42, \"department\": \"engineering\", \"skills\": [\"c++\", \"python\", \"machine learning\"]},",
      "context_before": "        {\"id\": \"1\", \"name\": \"Alice Johnson\", \"email\": \"alice@example.com\", \"age\": 28, \"department\": \"engineering\", \"skills\": [\"python\", \"java\", \"sql\"]},\n        {\"id\": \"2\", \"name\": \"Bob Smith\", \"email\": \"bob@example.com\", \"age\": 35, \"department\": \"marketing\", \"skills\": [\"marketing\", \"analytics\"]},",
      "context_after": "        {\"id\": \"4\", \"name\": \"Diana Prince\", \"email\": \"diana@wonder.com\", \"age\": 30, \"department\": \"hr\", \"skills\": [\"communication\", \"leadership\"]},\n        {\"id\": \"5\", \"name\": \"Eve Adams\", \"email\": \"eve@secure.org\", \"age\": 26, \"department\": \"security\", \"skills\": [\"cryptography\", \"python\", \"networking\"]},"
    },
    {
      "path": "src/main/python/data_processor.py",
      "line": 618,
      "col": 134,
      "snippet": "{\"id\": \"5\", \"name\": \"Eve Adams\", \"email\": \"eve@secure.org\", \"age\": 26, \"department\": \"security\", \"skills\": [\"cryptography\", \"python\", \"networking\"]},",
      "context_before": "        {\"id\": \"3\", \"name\": \"Charlie Brown\", \"email\": \"charlie@test.com\", \"age\": 42, \"department\": \"engineering\", \"skills\": [\"c++\", \"python\", \"machine learning\"]},\n        {\"id\": \"4\", \"name\": \"Diana Prince\", \"email\": \"diana@wonder.com\", \"age\": 30, \"department\": \"hr\", \"skills\": [\"communication\", \"leadership\"]},",
      "context_after": "        {\"id\": \"6\", \"name\": \"Frank Miller\", \"email\": \"frank@art.com\", \"age\": 55, \"department\": \"design\", \"skills\": [\"photoshop\", \"illustrator\", \"creativity\"]},\n        {\"id\": \"7\", \"name\": \"Grace Hopper\", \"email\": \"grace@tech.com\", \"age\": 85, \"department\": \"engineering\", \"skills\": [\"cobol\", \"fortran\", \"compilers\"]},"
    },
    {
      "path": "src/main/python/data_processor.py",
      "line": 622,
      "col": 142,
      "snippet": "{\"id\": \"9\", \"name\": \"Ivy League\", \"email\": \"ivy@univ.edu\", \"age\": 22, \"department\": \"education\", \"skills\": [\"teaching\", \"research\", \"python\"]},",
      "context_before": "        {\"id\": \"7\", \"name\": \"Grace Hopper\", \"email\": \"grace@tech.com\", \"age\": 85, \"department\": \"engineering\", \"skills\": [\"cobol\", \"fortran\", \"compilers\"]},\n        {\"id\": \"8\", \"name\": \"Henry Ford\", \"email\": \"henry@auto.com\", \"age\": 78, \"department\": \"manufacturing\", \"skills\": [\"engineering\", \"business\", \"innovation\"]},",
      "context_after": "        {\"id\": \"10\", \"name\": \"Jack Sparrow\", \"email\": \"jack@pirate.com\", \"age\": 45, \"department\": \"adventure\", \"skills\": [\"sailing\", \"swordsmanship\", \"treasure hunting\"]}\n    ]"
    },
    {
      "path": "src/main/python/database.py",
      "line": 1,
      "col": 16,
      "snippet": "#!/usr/bin/env python3",
      "context_before": "",
      "context_after": "\"\"\"\n数据库管理模块"
    },
    {
      "path": "src/main/python/notification.py",
      "line": 1,
      "col": 16,
      "snippet": "#!/usr/bin/env python3",
      "context_before": "",
      "context_after": "\"\"\"\n通知模块"
    }
  ],
  "tool_iter": 7,
  "call_index": 2
}
```

### Call 11
```json
{
  "tool": "text_search_tool",
  "args": {
    "query": "java",
    "root_dir": "/home/ran/Documents/work/VectorCode/mini_code_index/test_code_index_project"
  },
  "result": [
    {
      "path": "README.md",
      "line": 7,
      "col": 13,
      "snippet": "- `src/main/java/com/example/` - Java 源代码",
      "context_before": "## 项目结构\n",
      "context_after": "- `src/main/python/` - Python 脚本\n- `pom.xml` - Maven 配置（Java）"
    },
    {
      "path": "README.md",
      "line": 22,
      "col": 10,
      "snippet": "mvn exec:java -Dexec.mainClass=\"com.example.UserService\"",
      "context_before": "```bash\nmvn compile",
      "context_after": "```\n"
    },
    {
      "path": "target/classes/com/example/AdapterManager$AdapterFactory.class",
      "line": 1,
      "col": 60,
      "snippet": "\u0000\u0000\u00007\u0000\u0013\u0007\u0000\u0002\u0001\u0000)com/example/AdapterManager$AdapterFactory\u0007\u0000\u0004\u0001\u0000\u0010java/lang/Object\u0001\u0000\u0006create\u0001\u00009([Ljava/lang/Object;)Lcom/example/AdapterManager$Adapter;\u0001\u0000\tSignature\u0001\u0000=([Ljava/lang/Object;)Lcom/example/AdapterManager$Adapter<**>;\u0001\u0000",
      "context_before": "",
      "context_after": "SourceFile\u0001\u0000\u0013AdapterManager.java\u0001\u0000\nInnerClasses\u0007\u0000"
    },
    {
      "path": "target/classes/com/example/AdapterManager$AdapterFactory.class",
      "line": 1,
      "col": 91,
      "snippet": "\u0000\u0000\u00007\u0000\u0013\u0007\u0000\u0002\u0001\u0000)com/example/AdapterManager$AdapterFactory\u0007\u0000\u0004\u0001\u0000\u0010java/lang/Object\u0001\u0000\u0006create\u0001\u00009([Ljava/lang/Object;)Lcom/example/AdapterManager$Adapter;\u0001\u0000\tSignature\u0001\u0000=([Ljava/lang/Object;)Lcom/example/AdapterManager$Adapter<**>;\u0001\u0000",
      "context_before": "",
      "context_after": "SourceFile\u0001\u0000\u0013AdapterManager.java\u0001\u0000\nInnerClasses\u0007\u0000"
    },
    {
      "path": "target/classes/com/example/AdapterManager$AdapterFactory.class",
      "line": 1,
      "col": 163,
      "snippet": "\u0000\u0000\u00007\u0000\u0013\u0007\u0000\u0002\u0001\u0000)com/example/AdapterManager$AdapterFactory\u0007\u0000\u0004\u0001\u0000\u0010java/lang/Object\u0001\u0000\u0006create\u0001\u00009([Ljava/lang/Object;)Lcom/example/AdapterManager$Adapter;\u0001\u0000\tSignature\u0001\u0000=([Ljava/lang/Object;)Lcom/example/AdapterManager$Adapter<**>;\u0001\u0000",
      "context_before": "",
      "context_after": "SourceFile\u0001\u0000\u0013AdapterManager.java\u0001\u0000\nInnerClasses\u0007\u0000"
    },
    {
      "path": "target/classes/com/example/AdapterManager$AdapterFactory.class",
      "line": 2,
      "col": 29,
      "snippet": "SourceFile\u0001\u0000\u0013AdapterManager.java\u0001\u0000",
      "context_before": "\u0000\u0000\u00007\u0000\u0013\u0007\u0000\u0002\u0001\u0000)com/example/AdapterManager$AdapterFactory\u0007\u0000\u0004\u0001\u0000\u0010java/lang/Object\u0001\u0000\u0006create\u0001\u00009([Ljava/lang/Object;)Lcom/example/AdapterManager$Adapter;\u0001\u0000\tSignature\u0001\u0000=([Ljava/lang/Object;)Lcom/example/AdapterManager$Adapter<**>;\u0001\u0000",
      "context_after": "InnerClasses\u0007\u0000\n\u0001\u0000\"com/example/AdapterManager$Adapter\u0007\u0000\u000f\u0001\u0000\u001acom/example/AdapterManager\u0001\u0000\u0007Adapter\u0001\u0000\u000eAdapterFactory\u0001\u0000\bNestHost\u0006\u0001\u0000\u0001\u0000\u0003\u0000\u0000\u0000\u0000\u0000\u0001\u0004\u0000\u0005\u0000\u0006\u0000\u0001\u0000\u0007\u0000\u0000\u0000\u0002\u0000\b\u0000\u0003\u0000\t\u0000\u0000\u0000\u0002\u0000"
    },
    {
      "path": "target/classes/com/example/EventSystem$Event.class",
      "line": 2,
      "col": 36,
      "snippet": "com/example/EventSystem$Event\u0007\u0000\u0004\u0001\u0000\u0010java/lang/Object\u0001\u0000\teventType\u0001\u0000\u0012Ljava/lang/String;\u0001\u0000\u0004data\u0001\u0000\u0012Ljava/lang/Object;\u0001\u0000\tSignature\u0001\u0000\u0003TT;\u0001\u0000\u0007context\u0001\u0000\u000fLjava/util/Map;\u0001\u00005Ljava/util/Map<Ljava/lang/String;Ljava/lang/Object;>;\u0001\u0000\ttimestamp\u0001\u0000\u0001J\u0001\u0000\u0007eventId\u0001\u0000\u0006<init>\u0001\u00006(Ljava/lang/String;Ljava/lang/Object;Ljava/util/Map;)V\u0001\u0000M(Ljava/lang/String;TT;Ljava/util/Map<Ljava/lang/String;Ljava/lang/Object;>;)V\u0001\u0000\u0004Code",
      "context_before": "\u0000\u0000\u00007\u0000W\u0007\u0000\u0002\u0001\u0000",
      "context_after": "\u0000\u0003\u0000\u0016\n\u0000\u0011\u0000\u0017\u0001\u0000\u0003()V\t\u0000\u0001\u0000\u0019"
    },
    {
      "path": "target/classes/com/example/EventSystem$Event.class",
      "line": 2,
      "col": 68,
      "snippet": "com/example/EventSystem$Event\u0007\u0000\u0004\u0001\u0000\u0010java/lang/Object\u0001\u0000\teventType\u0001\u0000\u0012Ljava/lang/String;\u0001\u0000\u0004data\u0001\u0000\u0012Ljava/lang/Object;\u0001\u0000\tSignature\u0001\u0000\u0003TT;\u0001\u0000\u0007context\u0001\u0000\u000fLjava/util/Map;\u0001\u00005Ljava/util/Map<Ljava/lang/String;Ljava/lang/Object;>;\u0001\u0000\ttimestamp\u0001\u0000\u0001J\u0001\u0000\u0007eventId\u0001\u0000\u0006<init>\u0001\u00006(Ljava/lang/String;Ljava/lang/Object;Ljava/util/Map;)V\u0001\u0000M(Ljava/lang/String;TT;Ljava/util/Map<Ljava/lang/String;Ljava/lang/Object;>;)V\u0001\u0000\u0004Code",
      "context_before": "\u0000\u0000\u00007\u0000W\u0007\u0000\u0002\u0001\u0000",
      "context_after": "\u0000\u0003\u0000\u0016\n\u0000\u0011\u0000\u0017\u0001\u0000\u0003()V\t\u0000\u0001\u0000\u0019"
    },
    {
      "path": "target/classes/com/example/EventSystem$Event.class",
      "line": 2,
      "col": 96,
      "snippet": "com/example/EventSystem$Event\u0007\u0000\u0004\u0001\u0000\u0010java/lang/Object\u0001\u0000\teventType\u0001\u0000\u0012Ljava/lang/String;\u0001\u0000\u0004data\u0001\u0000\u0012Ljava/lang/Object;\u0001\u0000\tSignature\u0001\u0000\u0003TT;\u0001\u0000\u0007context\u0001\u0000\u000fLjava/util/Map;\u0001\u00005Ljava/util/Map<Ljava/lang/String;Ljava/lang/Object;>;\u0001\u0000\ttimestamp\u0001\u0000\u0001J\u0001\u0000\u0007eventId\u0001\u0000\u0006<init>\u0001\u00006(Ljava/lang/String;Ljava/lang/Object;Ljava/util/Map;)V\u0001\u0000M(Ljava/lang/String;TT;Ljava/util/Map<Ljava/lang/String;Ljava/lang/Object;>;)V\u0001\u0000\u0004Code",
      "context_before": "\u0000\u0000\u00007\u0000W\u0007\u0000\u0002\u0001\u0000",
      "context_after": "\u0000\u0003\u0000\u0016\n\u0000\u0011\u0000\u0017\u0001\u0000\u0003()V\t\u0000\u0001\u0000\u0019"
    },
    {
      "path": "target/classes/com/example/EventSystem$Event.class",
      "line": 2,
      "col": 145,
      "snippet": "com/example/EventSystem$Event\u0007\u0000\u0004\u0001\u0000\u0010java/lang/Object\u0001\u0000\teventType\u0001\u0000\u0012Ljava/lang/String;\u0001\u0000\u0004data\u0001\u0000\u0012Ljava/lang/Object;\u0001\u0000\tSignature\u0001\u0000\u0003TT;\u0001\u0000\u0007context\u0001\u0000\u000fLjava/util/Map;\u0001\u00005Ljava/util/Map<Ljava/lang/String;Ljava/lang/Object;>;\u0001\u0000\ttimestamp\u0001\u0000\u0001J\u0001\u0000\u0007eventId\u0001\u0000\u0006<init>\u0001\u00006(Ljava/lang/String;Ljava/lang/Object;Ljava/util/Map;)V\u0001\u0000M(Ljava/lang/String;TT;Ljava/util/Map<Ljava/lang/String;Ljava/lang/Object;>;)V\u0001\u0000\u0004Code",
      "context_before": "\u0000\u0000\u00007\u0000W\u0007\u0000\u0002\u0001\u0000",
      "context_after": "\u0000\u0003\u0000\u0016\n\u0000\u0011\u0000\u0017\u0001\u0000\u0003()V\t\u0000\u0001\u0000\u0019"
    },
    {
      "path": "target/classes/com/example/EventSystem$Event.class",
      "line": 2,
      "col": 163,
      "snippet": "com/example/EventSystem$Event\u0007\u0000\u0004\u0001\u0000\u0010java/lang/Object\u0001\u0000\teventType\u0001\u0000\u0012Ljava/lang/String;\u0001\u0000\u0004data\u0001\u0000\u0012Ljava/lang/Object;\u0001\u0000\tSignature\u0001\u0000\u0003TT;\u0001\u0000\u0007context\u0001\u0000\u000fLjava/util/Map;\u0001\u00005Ljava/util/Map<Ljava/lang/String;Ljava/lang/Object;>;\u0001\u0000\ttimestamp\u0001\u0000\u0001J\u0001\u0000\u0007eventId\u0001\u0000\u0006<init>\u0001\u00006(Ljava/lang/String;Ljava/lang/Object;Ljava/util/Map;)V\u0001\u0000M(Ljava/lang/String;TT;Ljava/util/Map<Ljava/lang/String;Ljava/lang/Object;>;)V\u0001\u0000\u0004Code",
      "context_before": "\u0000\u0000\u00007\u0000W\u0007\u0000\u0002\u0001\u0000",
      "context_after": "\u0000\u0003\u0000\u0016\n\u0000\u0011\u0000\u0017\u0001\u0000\u0003()V\t\u0000\u0001\u0000\u0019"
    },
    {
      "path": "target/classes/com/example/EventSystem$Event.class",
      "line": 2,
      "col": 178,
      "snippet": "com/example/EventSystem$Event\u0007\u0000\u0004\u0001\u0000\u0010java/lang/Object\u0001\u0000\teventType\u0001\u0000\u0012Ljava/lang/String;\u0001\u0000\u0004data\u0001\u0000\u0012Ljava/lang/Object;\u0001\u0000\tSignature\u0001\u0000\u0003TT;\u0001\u0000\u0007context\u0001\u0000\u000fLjava/util/Map;\u0001\u00005Ljava/util/Map<Ljava/lang/String;Ljava/lang/Object;>;\u0001\u0000\ttimestamp\u0001\u0000\u0001J\u0001\u0000\u0007eventId\u0001\u0000\u0006<init>\u0001\u00006(Ljava/lang/String;Ljava/lang/Object;Ljava/util/Map;)V\u0001\u0000M(Ljava/lang/String;TT;Ljava/util/Map<Ljava/lang/String;Ljava/lang/Object;>;)V\u0001\u0000\u0004Code",
      "context_before": "\u0000\u0000\u00007\u0000W\u0007\u0000\u0002\u0001\u0000",
      "context_after": "\u0000\u0003\u0000\u0016\n\u0000\u0011\u0000\u0017\u0001\u0000\u0003()V\t\u0000\u0001\u0000\u0019"
    },
    {
      "path": "target/classes/com/example/EventSystem$Event.class",
      "line": 2,
      "col": 196,
      "snippet": "com/example/EventSystem$Event\u0007\u0000\u0004\u0001\u0000\u0010java/lang/Object\u0001\u0000\teventType\u0001\u0000\u0012Ljava/lang/String;\u0001\u0000\u0004data\u0001\u0000\u0012Ljava/lang/Object;\u0001\u0000\tSignature\u0001\u0000\u0003TT;\u0001\u0000\u0007context\u0001\u0000\u000fLjava/util/Map;\u0001\u00005Ljava/util/Map<Ljava/lang/String;Ljava/lang/Object;>;\u0001\u0000\ttimestamp\u0001\u0000\u0001J\u0001\u0000\u0007eventId\u0001\u0000\u0006<init>\u0001\u00006(Ljava/lang/String;Ljava/lang/Object;Ljava/util/Map;)V\u0001\u0000M(Ljava/lang/String;TT;Ljava/util/Map<Ljava/lang/String;Ljava/lang/Object;>;)V\u0001\u0000\u0004Code",
      "context_before": "\u0000\u0000\u00007\u0000W\u0007\u0000\u0002\u0001\u0000",
      "context_after": "\u0000\u0003\u0000\u0016\n\u0000\u0011\u0000\u0017\u0001\u0000\u0003()V\t\u0000\u0001\u0000\u0019"
    },
    {
      "path": "target/classes/com/example/EventSystem$Event.class",
      "line": 2,
      "col": 255,
      "snippet": "com/example/EventSystem$Event\u0007\u0000\u0004\u0001\u0000\u0010java/lang/Object\u0001\u0000\teventType\u0001\u0000\u0012Ljava/lang/String;\u0001\u0000\u0004data\u0001\u0000\u0012Ljava/lang/Object;\u0001\u0000\tSignature\u0001\u0000\u0003TT;\u0001\u0000\u0007context\u0001\u0000\u000fLjava/util/Map;\u0001\u00005Ljava/util/Map<Ljava/lang/String;Ljava/lang/Object;>;\u0001\u0000\ttimestamp\u0001\u0000\u0001J\u0001\u0000\u0007eventId\u0001\u0000\u0006<init>\u0001\u00006(Ljava/lang/String;Ljava/lang/Object;Ljava/util/Map;)V\u0001\u0000M(Ljava/lang/String;TT;Ljava/util/Map<Ljava/lang/String;Ljava/lang/Object;>;)V\u0001\u0000\u0004Code",
      "context_before": "\u0000\u0000\u00007\u0000W\u0007\u0000\u0002\u0001\u0000",
      "context_after": "\u0000\u0003\u0000\u0016\n\u0000\u0011\u0000\u0017\u0001\u0000\u0003()V\t\u0000\u0001\u0000\u0019"
    },
    {
      "path": "target/classes/com/example/EventSystem$Event.class",
      "line": 2,
      "col": 273,
      "snippet": "com/example/EventSystem$Event\u0007\u0000\u0004\u0001\u0000\u0010java/lang/Object\u0001\u0000\teventType\u0001\u0000\u0012Ljava/lang/String;\u0001\u0000\u0004data\u0001\u0000\u0012Ljava/lang/Object;\u0001\u0000\tSignature\u0001\u0000\u0003TT;\u0001\u0000\u0007context\u0001\u0000\u000fLjava/util/Map;\u0001\u00005Ljava/util/Map<Ljava/lang/String;Ljava/lang/Object;>;\u0001\u0000\ttimestamp\u0001\u0000\u0001J\u0001\u0000\u0007eventId\u0001\u0000\u0006<init>\u0001\u00006(Ljava/lang/String;Ljava/lang/Object;Ljava/util/Map;)V\u0001\u0000M(Ljava/lang/String;TT;Ljava/util/Map<Ljava/lang/String;Ljava/lang/Object;>;)V\u0001\u0000\u0004Code",
      "context_before": "\u0000\u0000\u00007\u0000W\u0007\u0000\u0002\u0001\u0000",
      "context_after": "\u0000\u0003\u0000\u0016\n\u0000\u0011\u0000\u0017\u0001\u0000\u0003()V\t\u0000\u0001\u0000\u0019"
    },
    {
      "path": "target/classes/com/example/EventSystem$Event.class",
      "line": 2,
      "col": 291,
      "snippet": "com/example/EventSystem$Event\u0007\u0000\u0004\u0001\u0000\u0010java/lang/Object\u0001\u0000\teventType\u0001\u0000\u0012Ljava/lang/String;\u0001\u0000\u0004data\u0001\u0000\u0012Ljava/lang/Object;\u0001\u0000\tSignature\u0001\u0000\u0003TT;\u0001\u0000\u0007context\u0001\u0000\u000fLjava/util/Map;\u0001\u00005Ljava/util/Map<Ljava/lang/String;Ljava/lang/Object;>;\u0001\u0000\ttimestamp\u0001\u0000\u0001J\u0001\u0000\u0007eventId\u0001\u0000\u0006<init>\u0001\u00006(Ljava/lang/String;Ljava/lang/Object;Ljava/util/Map;)V\u0001\u0000M(Ljava/lang/String;TT;Ljava/util/Map<Ljava/lang/String;Ljava/lang/Object;>;)V\u0001\u0000\u0004Code",
      "context_before": "\u0000\u0000\u00007\u0000W\u0007\u0000\u0002\u0001\u0000",
      "context_after": "\u0000\u0003\u0000\u0016\n\u0000\u0011\u0000\u0017\u0001\u0000\u0003()V\t\u0000\u0001\u0000\u0019"
    },
    {
      "path": "target/classes/com/example/EventSystem$Event.class",
      "line": 2,
      "col": 312,
      "snippet": "com/example/EventSystem$Event\u0007\u0000\u0004\u0001\u0000\u0010java/lang/Object\u0001\u0000\teventType\u0001\u0000\u0012Ljava/lang/String;\u0001\u0000\u0004data\u0001\u0000\u0012Ljava/lang/Object;\u0001\u0000\tSignature\u0001\u0000\u0003TT;\u0001\u0000\u0007context\u0001\u0000\u000fLjava/util/Map;\u0001\u00005Ljava/util/Map<Ljava/lang/String;Ljava/lang/Object;>;\u0001\u0000\ttimestamp\u0001\u0000\u0001J\u0001\u0000\u0007eventId\u0001\u0000\u0006<init>\u0001\u00006(Ljava/lang/String;Ljava/lang/Object;Ljava/util/Map;)V\u0001\u0000M(Ljava/lang/String;TT;Ljava/util/Map<Ljava/lang/String;Ljava/lang/Object;>;)V\u0001\u0000\u0004Code",
      "context_before": "\u0000\u0000\u00007\u0000W\u0007\u0000\u0002\u0001\u0000",
      "context_after": "\u0000\u0003\u0000\u0016\n\u0000\u0011\u0000\u0017\u0001\u0000\u0003()V\t\u0000\u0001\u0000\u0019"
    },
    {
      "path": "target/classes/com/example/EventSystem$Event.class",
      "line": 2,
      "col": 333,
      "snippet": "com/example/EventSystem$Event\u0007\u0000\u0004\u0001\u0000\u0010java/lang/Object\u0001\u0000\teventType\u0001\u0000\u0012Ljava/lang/String;\u0001\u0000\u0004data\u0001\u0000\u0012Ljava/lang/Object;\u0001\u0000\tSignature\u0001\u0000\u0003TT;\u0001\u0000\u0007context\u0001\u0000\u000fLjava/util/Map;\u0001\u00005Ljava/util/Map<Ljava/lang/String;Ljava/lang/Object;>;\u0001\u0000\ttimestamp\u0001\u0000\u0001J\u0001\u0000\u0007eventId\u0001\u0000\u0006<init>\u0001\u00006(Ljava/lang/String;Ljava/lang/Object;Ljava/util/Map;)V\u0001\u0000M(Ljava/lang/String;TT;Ljava/util/Map<Ljava/lang/String;Ljava/lang/Object;>;)V\u0001\u0000\u0004Code",
      "context_before": "\u0000\u0000\u00007\u0000W\u0007\u0000\u0002\u0001\u0000",
      "context_after": "\u0000\u0003\u0000\u0016\n\u0000\u0011\u0000\u0017\u0001\u0000\u0003()V\t\u0000\u0001\u0000\u0019"
    },
    {
      "path": "target/classes/com/example/EventSystem$Event.class",
      "line": 2,
      "col": 348,
      "snippet": "com/example/EventSystem$Event\u0007\u0000\u0004\u0001\u0000\u0010java/lang/Object\u0001\u0000\teventType\u0001\u0000\u0012Ljava/lang/String;\u0001\u0000\u0004data\u0001\u0000\u0012Ljava/lang/Object;\u0001\u0000\tSignature\u0001\u0000\u0003TT;\u0001\u0000\u0007context\u0001\u0000\u000fLjava/util/Map;\u0001\u00005Ljava/util/Map<Ljava/lang/String;Ljava/lang/Object;>;\u0001\u0000\ttimestamp\u0001\u0000\u0001J\u0001\u0000\u0007eventId\u0001\u0000\u0006<init>\u0001\u00006(Ljava/lang/String;Ljava/lang/Object;Ljava/util/Map;)V\u0001\u0000M(Ljava/lang/String;TT;Ljava/util/Map<Ljava/lang/String;Ljava/lang/Object;>;)V\u0001\u0000\u0004Code",
      "context_before": "\u0000\u0000\u00007\u0000W\u0007\u0000\u0002\u0001\u0000",
      "context_after": "\u0000\u0003\u0000\u0016\n\u0000\u0011\u0000\u0017\u0001\u0000\u0003()V\t\u0000\u0001\u0000\u0019"
    },
    {
      "path": "target/classes/com/example/EventSystem$Event.class",
      "line": 2,
      "col": 366,
      "snippet": "com/example/EventSystem$Event\u0007\u0000\u0004\u0001\u0000\u0010java/lang/Object\u0001\u0000\teventType\u0001\u0000\u0012Ljava/lang/String;\u0001\u0000\u0004data\u0001\u0000\u0012Ljava/lang/Object;\u0001\u0000\tSignature\u0001\u0000\u0003TT;\u0001\u0000\u0007context\u0001\u0000\u000fLjava/util/Map;\u0001\u00005Ljava/util/Map<Ljava/lang/String;Ljava/lang/Object;>;\u0001\u0000\ttimestamp\u0001\u0000\u0001J\u0001\u0000\u0007eventId\u0001\u0000\u0006<init>\u0001\u00006(Ljava/lang/String;Ljava/lang/Object;Ljava/util/Map;)V\u0001\u0000M(Ljava/lang/String;TT;Ljava/util/Map<Ljava/lang/String;Ljava/lang/Object;>;)V\u0001\u0000\u0004Code",
      "context_before": "\u0000\u0000\u00007\u0000W\u0007\u0000\u0002\u0001\u0000",
      "context_after": "\u0000\u0003\u0000\u0016\n\u0000\u0011\u0000\u0017\u0001\u0000\u0003()V\t\u0000\u0001\u0000\u0019"
    },
    {
      "path": "target/classes/com/example/EventSystem$Event.class",
      "line": 7,
      "col": 4,
      "snippet": "\u0001\u0000\u0011java/util/HashMap",
      "context_before": "\u0000\u0005\u0000\u0006\t\u0000\u0001\u0000\u001b\n\u0000\u0007\u0000\b\u0007\u0000",
      "context_after": "\u0000\n\u0000\u001f"
    },
    {
      "path": "target/classes/com/example/EventSystem$Event.class",
      "line": 10,
      "col": 10,
      "snippet": "\u0000\u0011\u0000 \u0001\u0000\u0012(Ljava/util/Map;)V",
      "context_before": "\u0000\n\u0000\u001f",
      "context_after": "\u0000\n\u0000\u0016\t\u0000\u0001\u0000#"
    },
    {
      "path": "target/classes/com/example/EventSystem$Event.class",
      "line": 16,
      "col": 11,
      "snippet": "\u0000%\u0000'\u0007\u0000&\u0001\u0000\u0010java/lang/System",
      "context_before": "\u0000\n",
      "context_after": "\u0000(\u0000)\u0001\u0000\u0011currentTimeMillis\u0001\u0000\u0003()J\t\u0000\u0001\u0000+\n\u0000\u000e\u0000\u000f"
    },
    {
      "path": "target/classes/com/example/EventSystem$Event.class",
      "line": 19,
      "col": 11,
      "snippet": "\u0000-\u0000/\u0007\u0000.\u0001\u0000\u000ejava/util/UUID",
      "context_before": "\u0000(\u0000)\u0001\u0000\u0011currentTimeMillis\u0001\u0000\u0003()J\t\u0000\u0001\u0000+\n\u0000\u000e\u0000\u000f",
      "context_after": "\u00000\u00001\u0001\u0000\nrandomUUID\u0001\u0000\u0012()Ljava/util/UUID;"
    },
    {
      "path": "target/classes/com/example/EventSystem$Event.class",
      "line": 21,
      "col": 17,
      "snippet": "randomUUID\u0001\u0000\u0012()Ljava/util/UUID;",
      "context_before": "\u0000-\u0000/\u0007\u0000.\u0001\u0000\u000ejava/util/UUID\n\u00000\u00001\u0001\u0000",
      "context_after": "\u0000-\u00003\n\u00004\u00005\u0001\u0000\btoString\u0001\u0000\u0014()Ljava/lang/String;\t\u0000\u0001\u00007"
    },
    {
      "path": "target/classes/com/example/EventSystem$Event.class",
      "line": 23,
      "col": 22,
      "snippet": "\u00004\u00005\u0001\u0000\btoString\u0001\u0000\u0014()Ljava/lang/String;\t\u0000\u0001\u00007",
      "context_before": "randomUUID\u0001\u0000\u0012()Ljava/util/UUID;\n\u0000-\u00003",
      "context_after": "\u0000\u0010\u0000\u0006\u0001\u0000\u000fLineNumberTable\u0001\u0000\u0012LocalVariableTable\u0001\u0000\u0004this\u0001\u0000\u001fLcom/example/EventSystem$Event;\u0001\u0000\u0016LocalVariableTypeTable\u0001\u0000$Lcom/example/EventSystem$Event<TT;>;\u0001\u0000\nStackMapTable\u0007\u0000@\u0001\u0000\u0010java/lang/String\u0007\u0000B\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/EventSystem$Event.class",
      "line": 25,
      "col": 20,
      "snippet": "StackMapTable\u0007\u0000@\u0001\u0000\u0010java/lang/String\u0007\u0000B\u0001\u0000",
      "context_before": "\u00004\u00005\u0001\u0000\btoString\u0001\u0000\u0014()Ljava/lang/String;\t\u0000\u0001\u00007\n\u0000\u0010\u0000\u0006\u0001\u0000\u000fLineNumberTable\u0001\u0000\u0012LocalVariableTable\u0001\u0000\u0004this\u0001\u0000\u001fLcom/example/EventSystem$Event;\u0001\u0000\u0016LocalVariableTypeTable\u0001\u0000$Lcom/example/EventSystem$Event<TT;>;\u0001\u0000",
      "context_after": "java/util/Map\b\u0000D\u0001\u0000'Event{id='%s', type='%s', timestamp=%d}\n\u0000F\u0000H\u0007\u0000G\u0001\u0000\u000ejava/lang/Long"
    },
    {
      "path": "target/classes/com/example/EventSystem$Event.class",
      "line": 26,
      "col": 1,
      "snippet": "java/util/Map\b\u0000D\u0001\u0000'Event{id='%s', type='%s', timestamp=%d}",
      "context_before": "\u0000\u0010\u0000\u0006\u0001\u0000\u000fLineNumberTable\u0001\u0000\u0012LocalVariableTable\u0001\u0000\u0004this\u0001\u0000\u001fLcom/example/EventSystem$Event;\u0001\u0000\u0016LocalVariableTypeTable\u0001\u0000$Lcom/example/EventSystem$Event<TT;>;\u0001\u0000\nStackMapTable\u0007\u0000@\u0001\u0000\u0010java/lang/String\u0007\u0000B\u0001\u0000",
      "context_after": "\u0000F\u0000H\u0007\u0000G\u0001\u0000\u000ejava/lang/Long\n\u0000I\u0000J\u0001\u0000\u0007valueOf\u0001\u0000\u0013(J)Ljava/lang/Long;"
    },
    {
      "path": "target/classes/com/example/EventSystem$Event.class",
      "line": 27,
      "col": 11,
      "snippet": "\u0000F\u0000H\u0007\u0000G\u0001\u0000\u000ejava/lang/Long",
      "context_before": "StackMapTable\u0007\u0000@\u0001\u0000\u0010java/lang/String\u0007\u0000B\u0001\u0000\njava/util/Map\b\u0000D\u0001\u0000'Event{id='%s', type='%s', timestamp=%d}",
      "context_after": "\u0000I\u0000J\u0001\u0000\u0007valueOf\u0001\u0000\u0013(J)Ljava/lang/Long;\n\u0000?\u0000L"
    },
    {
      "path": "target/classes/com/example/EventSystem$Event.class",
      "line": 28,
      "col": 22,
      "snippet": "\u0000I\u0000J\u0001\u0000\u0007valueOf\u0001\u0000\u0013(J)Ljava/lang/Long;",
      "context_before": "java/util/Map\b\u0000D\u0001\u0000'Event{id='%s', type='%s', timestamp=%d}\n\u0000F\u0000H\u0007\u0000G\u0001\u0000\u000ejava/lang/Long",
      "context_after": "\u0000?\u0000L\n\u0000M\u0000N\u0001\u0000\u0006format\u0001\u00009(Ljava/lang/String;[Ljava/lang/Object;)Ljava/lang/String;\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/EventSystem$Event.class",
      "line": 30,
      "col": 19,
      "snippet": "\u0000M\u0000N\u0001\u0000\u0006format\u0001\u00009(Ljava/lang/String;[Ljava/lang/Object;)Ljava/lang/String;\u0001\u0000",
      "context_before": "\u0000I\u0000J\u0001\u0000\u0007valueOf\u0001\u0000\u0013(J)Ljava/lang/Long;\n\u0000?\u0000L",
      "context_after": "SourceFile\u0001\u0000\u0010EventSystem.java\u0001\u0000(<T:Ljava/lang/Object;>Ljava/lang/Object;\u0001\u0000\nInnerClasses\u0007\u0000T\u0001\u0000\u0017com/example/EventSystem\u0001\u0000\u0005Event\u0001\u0000\bNestHost\u0000!\u0000\u0001\u0000\u0003\u0000\u0000\u0000\u0005\u0000\u0011\u0000\u0005\u0000\u0006\u0000\u0000\u0000\u0011\u0000\u0007\u0000\b\u0000\u0001\u0000\t\u0000\u0000\u0000\u0002\u0000"
    },
    {
      "path": "target/classes/com/example/EventSystem$Event.class",
      "line": 30,
      "col": 38,
      "snippet": "\u0000M\u0000N\u0001\u0000\u0006format\u0001\u00009(Ljava/lang/String;[Ljava/lang/Object;)Ljava/lang/String;\u0001\u0000",
      "context_before": "\u0000I\u0000J\u0001\u0000\u0007valueOf\u0001\u0000\u0013(J)Ljava/lang/Long;\n\u0000?\u0000L",
      "context_after": "SourceFile\u0001\u0000\u0010EventSystem.java\u0001\u0000(<T:Ljava/lang/Object;>Ljava/lang/Object;\u0001\u0000\nInnerClasses\u0007\u0000T\u0001\u0000\u0017com/example/EventSystem\u0001\u0000\u0005Event\u0001\u0000\bNestHost\u0000!\u0000\u0001\u0000\u0003\u0000\u0000\u0000\u0005\u0000\u0011\u0000\u0005\u0000\u0006\u0000\u0000\u0000\u0011\u0000\u0007\u0000\b\u0000\u0001\u0000\t\u0000\u0000\u0000\u0002\u0000"
    },
    {
      "path": "target/classes/com/example/EventSystem$Event.class",
      "line": 30,
      "col": 57,
      "snippet": "\u0000M\u0000N\u0001\u0000\u0006format\u0001\u00009(Ljava/lang/String;[Ljava/lang/Object;)Ljava/lang/String;\u0001\u0000",
      "context_before": "\u0000I\u0000J\u0001\u0000\u0007valueOf\u0001\u0000\u0013(J)Ljava/lang/Long;\n\u0000?\u0000L",
      "context_after": "SourceFile\u0001\u0000\u0010EventSystem.java\u0001\u0000(<T:Ljava/lang/Object;>Ljava/lang/Object;\u0001\u0000\nInnerClasses\u0007\u0000T\u0001\u0000\u0017com/example/EventSystem\u0001\u0000\u0005Event\u0001\u0000\bNestHost\u0000!\u0000\u0001\u0000\u0003\u0000\u0000\u0000\u0005\u0000\u0011\u0000\u0005\u0000\u0006\u0000\u0000\u0000\u0011\u0000\u0007\u0000\b\u0000\u0001\u0000\t\u0000\u0000\u0000\u0002\u0000"
    },
    {
      "path": "target/classes/com/example/EventSystem$Event.class",
      "line": 31,
      "col": 26,
      "snippet": "SourceFile\u0001\u0000\u0010EventSystem.java\u0001\u0000(<T:Ljava/lang/Object;>Ljava/lang/Object;\u0001\u0000",
      "context_before": "\u0000?\u0000L\n\u0000M\u0000N\u0001\u0000\u0006format\u0001\u00009(Ljava/lang/String;[Ljava/lang/Object;)Ljava/lang/String;\u0001\u0000",
      "context_after": "InnerClasses\u0007\u0000T\u0001\u0000\u0017com/example/EventSystem\u0001\u0000\u0005Event\u0001\u0000\bNestHost\u0000!\u0000\u0001\u0000\u0003\u0000\u0000\u0000\u0005\u0000\u0011\u0000\u0005\u0000\u0006\u0000\u0000\u0000\u0011\u0000\u0007\u0000\b\u0000\u0001\u0000\t\u0000\u0000\u0000\u0002\u0000\n\u0000\u0011\u0000"
    },
    {
      "path": "target/classes/com/example/EventSystem$Event.class",
      "line": 31,
      "col": 37,
      "snippet": "SourceFile\u0001\u0000\u0010EventSystem.java\u0001\u0000(<T:Ljava/lang/Object;>Ljava/lang/Object;\u0001\u0000",
      "context_before": "\u0000?\u0000L\n\u0000M\u0000N\u0001\u0000\u0006format\u0001\u00009(Ljava/lang/String;[Ljava/lang/Object;)Ljava/lang/String;\u0001\u0000",
      "context_after": "InnerClasses\u0007\u0000T\u0001\u0000\u0017com/example/EventSystem\u0001\u0000\u0005Event\u0001\u0000\bNestHost\u0000!\u0000\u0001\u0000\u0003\u0000\u0000\u0000\u0005\u0000\u0011\u0000\u0005\u0000\u0006\u0000\u0000\u0000\u0011\u0000\u0007\u0000\b\u0000\u0001\u0000\t\u0000\u0000\u0000\u0002\u0000\n\u0000\u0011\u0000"
    },
    {
      "path": "target/classes/com/example/EventSystem$Event.class",
      "line": 31,
      "col": 56,
      "snippet": "SourceFile\u0001\u0000\u0010EventSystem.java\u0001\u0000(<T:Ljava/lang/Object;>Ljava/lang/Object;\u0001\u0000",
      "context_before": "\u0000?\u0000L\n\u0000M\u0000N\u0001\u0000\u0006format\u0001\u00009(Ljava/lang/String;[Ljava/lang/Object;)Ljava/lang/String;\u0001\u0000",
      "context_after": "InnerClasses\u0007\u0000T\u0001\u0000\u0017com/example/EventSystem\u0001\u0000\u0005Event\u0001\u0000\bNestHost\u0000!\u0000\u0001\u0000\u0003\u0000\u0000\u0000\u0005\u0000\u0011\u0000\u0005\u0000\u0006\u0000\u0000\u0000\u0011\u0000\u0007\u0000\b\u0000\u0001\u0000\t\u0000\u0000\u0000\u0002\u0000\n\u0000\u0011\u0000"
    },
    {
      "path": "target/classes/com/example/PermissionManager$PermissionEffect.class",
      "line": 1,
      "col": 65,
      "snippet": "\u0000\u0000\u00007\u00007\u0007\u0000\u0002\u0001\u0000.com/example/PermissionManager$PermissionEffect\u0007\u0000\u0004\u0001\u0000\u000ejava/lang/Enum\u0001\u0000\u0005ALLOW\u0001\u00000Lcom/example/PermissionManager$PermissionEffect;\u0001\u0000\u0004DENY\u0001\u0000\u0007NEUTRAL\u0001\u0000",
      "context_before": "",
      "context_after": "ENUM$VALUES\u0001\u00001[Lcom/example/PermissionManager$PermissionEffect;\u0001\u0000\b<clinit>\u0001\u0000\u0003()V\u0001\u0000\u0004Code\b\u0000\u0005\n\u0000\u0001\u0000\u0010"
    },
    {
      "path": "target/classes/com/example/PermissionManager$PermissionEffect.class",
      "line": 4,
      "col": 19,
      "snippet": "\u0000\u0011\u0000\u0012\u0001\u0000\u0006<init>\u0001\u0000\u0016(Ljava/lang/String;I)V\t\u0000\u0001\u0000\u0014",
      "context_before": "ENUM$VALUES\u0001\u00001[Lcom/example/PermissionManager$PermissionEffect;\u0001\u0000\b<clinit>\u0001\u0000\u0003()V\u0001\u0000\u0004Code\b\u0000\u0005\n\u0000\u0001\u0000\u0010",
      "context_after": "\u0000\u0005\u0000\u0006\b\u0000\u0007\t\u0000\u0001\u0000\u0017\n\u0000\u0007\u0000\u0006\b\u0000\b\t\u0000\u0001\u0000\u001a"
    },
    {
      "path": "target/classes/com/example/PermissionManager$PermissionEffect.class",
      "line": 12,
      "col": 11,
      "snippet": "\u0000$\u0000&\u0007\u0000%\u0001\u0000\u0010java/lang/System",
      "context_before": "\u0001\u0000\u000fLineNumberTable\u0001\u0000\u0012LocalVariableTable\n\u0000\u0003\u0000\u0010\u0001\u0000\u0004this\u0001\u0000\u0006values\u0001\u00003()[Lcom/example/PermissionManager$PermissionEffect;",
      "context_after": "\u0000'\u0000(\u0001\u0000\tarraycopy\u0001\u0000*(Ljava/lang/Object;ILjava/lang/Object;II)V\u0001\u0000\u0007valueOf\u0001\u0000D(Ljava/lang/String;)Lcom/example/PermissionManager$PermissionEffect;\n\u0000\u0003\u0000,"
    },
    {
      "path": "target/classes/com/example/PermissionManager$PermissionEffect.class",
      "line": 13,
      "col": 22,
      "snippet": "\u0000'\u0000(\u0001\u0000\tarraycopy\u0001\u0000*(Ljava/lang/Object;ILjava/lang/Object;II)V\u0001\u0000\u0007valueOf\u0001\u0000D(Ljava/lang/String;)Lcom/example/PermissionManager$PermissionEffect;",
      "context_before": "\u0000\u0003\u0000\u0010\u0001\u0000\u0004this\u0001\u0000\u0006values\u0001\u00003()[Lcom/example/PermissionManager$PermissionEffect;\n\u0000$\u0000&\u0007\u0000%\u0001\u0000\u0010java/lang/System",
      "context_after": "\u0000\u0003\u0000,\n\u0000)\u0000-\u0001\u00005(Ljava/lang/Class;Ljava/lang/String;)Ljava/lang/Enum;\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/PermissionManager$PermissionEffect.class",
      "line": 13,
      "col": 41,
      "snippet": "\u0000'\u0000(\u0001\u0000\tarraycopy\u0001\u0000*(Ljava/lang/Object;ILjava/lang/Object;II)V\u0001\u0000\u0007valueOf\u0001\u0000D(Ljava/lang/String;)Lcom/example/PermissionManager$PermissionEffect;",
      "context_before": "\u0000\u0003\u0000\u0010\u0001\u0000\u0004this\u0001\u0000\u0006values\u0001\u00003()[Lcom/example/PermissionManager$PermissionEffect;\n\u0000$\u0000&\u0007\u0000%\u0001\u0000\u0010java/lang/System",
      "context_after": "\u0000\u0003\u0000,\n\u0000)\u0000-\u0001\u00005(Ljava/lang/Class;Ljava/lang/String;)Ljava/lang/Enum;\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/PermissionManager$PermissionEffect.class",
      "line": 13,
      "col": 77,
      "snippet": "\u0000'\u0000(\u0001\u0000\tarraycopy\u0001\u0000*(Ljava/lang/Object;ILjava/lang/Object;II)V\u0001\u0000\u0007valueOf\u0001\u0000D(Ljava/lang/String;)Lcom/example/PermissionManager$PermissionEffect;",
      "context_before": "\u0000\u0003\u0000\u0010\u0001\u0000\u0004this\u0001\u0000\u0006values\u0001\u00003()[Lcom/example/PermissionManager$PermissionEffect;\n\u0000$\u0000&\u0007\u0000%\u0001\u0000\u0010java/lang/System",
      "context_after": "\u0000\u0003\u0000,\n\u0000)\u0000-\u0001\u00005(Ljava/lang/Class;Ljava/lang/String;)Ljava/lang/Enum;\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/PermissionManager$PermissionEffect.class",
      "line": 15,
      "col": 10,
      "snippet": "\u0000)\u0000-\u0001\u00005(Ljava/lang/Class;Ljava/lang/String;)Ljava/lang/Enum;\u0001\u0000",
      "context_before": "\u0000'\u0000(\u0001\u0000\tarraycopy\u0001\u0000*(Ljava/lang/Object;ILjava/lang/Object;II)V\u0001\u0000\u0007valueOf\u0001\u0000D(Ljava/lang/String;)Lcom/example/PermissionManager$PermissionEffect;\n\u0000\u0003\u0000,",
      "context_after": "SourceFile\u0001\u0000\u0016PermissionManager.java\u0001\u0000\tSignature\u0001\u0000BLjava/lang/Enum<Lcom/example/PermissionManager$PermissionEffect;>;\u0001\u0000\nInnerClasses\u0007\u00004\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/PermissionManager$PermissionEffect.class",
      "line": 15,
      "col": 27,
      "snippet": "\u0000)\u0000-\u0001\u00005(Ljava/lang/Class;Ljava/lang/String;)Ljava/lang/Enum;\u0001\u0000",
      "context_before": "\u0000'\u0000(\u0001\u0000\tarraycopy\u0001\u0000*(Ljava/lang/Object;ILjava/lang/Object;II)V\u0001\u0000\u0007valueOf\u0001\u0000D(Ljava/lang/String;)Lcom/example/PermissionManager$PermissionEffect;\n\u0000\u0003\u0000,",
      "context_after": "SourceFile\u0001\u0000\u0016PermissionManager.java\u0001\u0000\tSignature\u0001\u0000BLjava/lang/Enum<Lcom/example/PermissionManager$PermissionEffect;>;\u0001\u0000\nInnerClasses\u0007\u00004\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/PermissionManager$PermissionEffect.class",
      "line": 15,
      "col": 46,
      "snippet": "\u0000)\u0000-\u0001\u00005(Ljava/lang/Class;Ljava/lang/String;)Ljava/lang/Enum;\u0001\u0000",
      "context_before": "\u0000'\u0000(\u0001\u0000\tarraycopy\u0001\u0000*(Ljava/lang/Object;ILjava/lang/Object;II)V\u0001\u0000\u0007valueOf\u0001\u0000D(Ljava/lang/String;)Lcom/example/PermissionManager$PermissionEffect;\n\u0000\u0003\u0000,",
      "context_after": "SourceFile\u0001\u0000\u0016PermissionManager.java\u0001\u0000\tSignature\u0001\u0000BLjava/lang/Enum<Lcom/example/PermissionManager$PermissionEffect;>;\u0001\u0000\nInnerClasses\u0007\u00004\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/PermissionManager$PermissionEffect.class",
      "line": 16,
      "col": 32,
      "snippet": "SourceFile\u0001\u0000\u0016PermissionManager.java\u0001\u0000\tSignature\u0001\u0000BLjava/lang/Enum<Lcom/example/PermissionManager$PermissionEffect;>;\u0001\u0000",
      "context_before": "\u0000\u0003\u0000,\n\u0000)\u0000-\u0001\u00005(Ljava/lang/Class;Ljava/lang/String;)Ljava/lang/Enum;\u0001\u0000",
      "context_after": "InnerClasses\u0007\u00004\u0001\u0000\ncom/example/PermissionManager\u0001\u0000\u0010PermissionEffect\u0001\u0000\bNestHost@1\u0000\u0001\u0000\u0003\u0000\u0000\u0000\u0004@\u0019\u0000\u0005\u0000\u0006\u0000\u0000@\u0019\u0000\u0007\u0000\u0006\u0000\u0000@\u0019\u0000\b\u0000\u0006\u0000\u0000\u0010\u001a\u0000\t\u0000"
    },
    {
      "path": "target/classes/com/example/PermissionManager$PermissionEffect.class",
      "line": 16,
      "col": 52,
      "snippet": "SourceFile\u0001\u0000\u0016PermissionManager.java\u0001\u0000\tSignature\u0001\u0000BLjava/lang/Enum<Lcom/example/PermissionManager$PermissionEffect;>;\u0001\u0000",
      "context_before": "\u0000\u0003\u0000,\n\u0000)\u0000-\u0001\u00005(Ljava/lang/Class;Ljava/lang/String;)Ljava/lang/Enum;\u0001\u0000",
      "context_after": "InnerClasses\u0007\u00004\u0001\u0000\ncom/example/PermissionManager\u0001\u0000\u0010PermissionEffect\u0001\u0000\bNestHost@1\u0000\u0001\u0000\u0003\u0000\u0000\u0000\u0004@\u0019\u0000\u0005\u0000\u0006\u0000\u0000@\u0019\u0000\u0007\u0000\u0006\u0000\u0000@\u0019\u0000\b\u0000\u0006\u0000\u0000\u0010\u001a\u0000\t\u0000"
    },
    {
      "path": "target/classes/com/example/UserService$AuditLogger.class",
      "line": 1,
      "col": 53,
      "snippet": "\u0000\u0000\u00007\u0000\u0007\u0000\u0002\u0001\u0000#com/example/UserService$AuditLogger\u0007\u0000\u0004\u0001\u0000\u0010java/lang/Object\u0001\u0000\bauditLog\u0001\u0000\u0010Ljava/util/List;\u0001\u0000\tSignature\u0001\u00006Ljava/util/List<Lcom/example/UserService$AuditEntry;>;\u0001\u0000\u0006<init>\u0001\u0000\u0003()V\u0001\u0000\u0004Code",
      "context_before": "",
      "context_after": "\u0000\u0003\u0000\n"
    },
    {
      "path": "target/classes/com/example/UserService$AuditLogger.class",
      "line": 1,
      "col": 84,
      "snippet": "\u0000\u0000\u00007\u0000\u0007\u0000\u0002\u0001\u0000#com/example/UserService$AuditLogger\u0007\u0000\u0004\u0001\u0000\u0010java/lang/Object\u0001\u0000\bauditLog\u0001\u0000\u0010Ljava/util/List;\u0001\u0000\tSignature\u0001\u00006Ljava/util/List<Lcom/example/UserService$AuditEntry;>;\u0001\u0000\u0006<init>\u0001\u0000\u0003()V\u0001\u0000\u0004Code",
      "context_before": "",
      "context_after": "\u0000\u0003\u0000\n"
    },
    {
      "path": "target/classes/com/example/UserService$AuditLogger.class",
      "line": 1,
      "col": 115,
      "snippet": "\u0000\u0000\u00007\u0000\u0007\u0000\u0002\u0001\u0000#com/example/UserService$AuditLogger\u0007\u0000\u0004\u0001\u0000\u0010java/lang/Object\u0001\u0000\bauditLog\u0001\u0000\u0010Ljava/util/List;\u0001\u0000\tSignature\u0001\u00006Ljava/util/List<Lcom/example/UserService$AuditEntry;>;\u0001\u0000\u0006<init>\u0001\u0000\u0003()V\u0001\u0000\u0004Code",
      "context_before": "",
      "context_after": "\u0000\u0003\u0000\n"
    },
    {
      "path": "target/classes/com/example/UserService$AuditLogger.class",
      "line": 5,
      "col": 7,
      "snippet": "\u0007\u0000\u000f\u0001\u0000\u0013java/util/ArrayList",
      "context_before": "\n\u0000\t\u0000",
      "context_after": "\u0000\u000e\u0000\n\t\u0000\u0001\u0000\u0012"
    },
    {
      "path": "target/classes/com/example/UserService$AuditLogger.class",
      "line": 8,
      "col": 141,
      "snippet": "\u0000\u0005\u0000\u0006\u0001\u0000\u000fLineNumberTable\u0001\u0000\u0012LocalVariableTable\u0001\u0000\u0004this\u0001\u0000%Lcom/example/UserService$AuditLogger;\u0001\u0000\u0003log\u0001\u0000N(Lcom/example/UserService$OperationType;Ljava/lang/String;Ljava/lang/String;)V\u0007\u0000\u001a\u0001\u0000\"com/example/UserService$AuditEntry",
      "context_before": "\u0000\u000e\u0000\n\t\u0000\u0001\u0000\u0012",
      "context_after": "\u0000\n\u0000"
    },
    {
      "path": "target/classes/com/example/UserService$AuditLogger.class",
      "line": 8,
      "col": 159,
      "snippet": "\u0000\u0005\u0000\u0006\u0001\u0000\u000fLineNumberTable\u0001\u0000\u0012LocalVariableTable\u0001\u0000\u0004this\u0001\u0000%Lcom/example/UserService$AuditLogger;\u0001\u0000\u0003log\u0001\u0000N(Lcom/example/UserService$OperationType;Ljava/lang/String;Ljava/lang/String;)V\u0007\u0000\u001a\u0001\u0000\"com/example/UserService$AuditEntry",
      "context_before": "\u0000\u000e\u0000\n\t\u0000\u0001\u0000\u0012",
      "context_after": "\u0000\n\u0000"
    },
    {
      "path": "target/classes/com/example/UserService$AuditLogger.class",
      "line": 12,
      "col": 4,
      "snippet": "\u0001\u0000\u0017java/time/LocalDateTime",
      "context_before": "\u0000\n\u0007\u0000",
      "context_after": "\u0000\u001f\u0000 \u0001\u0000\u0003now\u0001\u0000\u001b()Ljava/time/LocalDateTime;\n\u0000\u0019\u0000\""
    },
    {
      "path": "target/classes/com/example/UserService$AuditLogger.class",
      "line": 13,
      "col": 17,
      "snippet": "\u0000\u001f\u0000 \u0001\u0000\u0003now\u0001\u0000\u001b()Ljava/time/LocalDateTime;",
      "context_before": "\u0007\u0000\n\u0001\u0000\u0017java/time/LocalDateTime",
      "context_after": "\u0000\u0019\u0000\"\n\u0000\t\u0000#\u0001\u0000g(Lcom/example/UserService$OperationType;Ljava/lang/String;Ljava/lang/String;Ljava/time/LocalDateTime;)V"
    },
    {
      "path": "target/classes/com/example/UserService$AuditLogger.class",
      "line": 15,
      "col": 49,
      "snippet": "\u0000\t\u0000#\u0001\u0000g(Lcom/example/UserService$OperationType;Ljava/lang/String;Ljava/lang/String;Ljava/time/LocalDateTime;)V",
      "context_before": "\u0000\u001f\u0000 \u0001\u0000\u0003now\u0001\u0000\u001b()Ljava/time/LocalDateTime;\n\u0000\u0019\u0000\"",
      "context_after": "\u0000%\u0000'\u0007\u0000&\u0001\u0000\u000ejava/util/List\n\u0000(\u0000)\u0001\u0000\u0003add\u0001\u0000\u0015(Ljava/lang/Object;)Z"
    },
    {
      "path": "target/classes/com/example/UserService$AuditLogger.class",
      "line": 15,
      "col": 67,
      "snippet": "\u0000\t\u0000#\u0001\u0000g(Lcom/example/UserService$OperationType;Ljava/lang/String;Ljava/lang/String;Ljava/time/LocalDateTime;)V",
      "context_before": "\u0000\u001f\u0000 \u0001\u0000\u0003now\u0001\u0000\u001b()Ljava/time/LocalDateTime;\n\u0000\u0019\u0000\"",
      "context_after": "\u0000%\u0000'\u0007\u0000&\u0001\u0000\u000ejava/util/List\n\u0000(\u0000)\u0001\u0000\u0003add\u0001\u0000\u0015(Ljava/lang/Object;)Z"
    },
    {
      "path": "target/classes/com/example/UserService$AuditLogger.class",
      "line": 15,
      "col": 85,
      "snippet": "\u0000\t\u0000#\u0001\u0000g(Lcom/example/UserService$OperationType;Ljava/lang/String;Ljava/lang/String;Ljava/time/LocalDateTime;)V",
      "context_before": "\u0000\u001f\u0000 \u0001\u0000\u0003now\u0001\u0000\u001b()Ljava/time/LocalDateTime;\n\u0000\u0019\u0000\"",
      "context_after": "\u0000%\u0000'\u0007\u0000&\u0001\u0000\u000ejava/util/List\n\u0000(\u0000)\u0001\u0000\u0003add\u0001\u0000\u0015(Ljava/lang/Object;)Z"
    },
    {
      "path": "target/classes/com/example/UserService$AuditLogger.class",
      "line": 16,
      "col": 11,
      "snippet": "\u0000%\u0000'\u0007\u0000&\u0001\u0000\u000ejava/util/List",
      "context_before": "\u0000\u0019\u0000\"\n\u0000\t\u0000#\u0001\u0000g(Lcom/example/UserService$OperationType;Ljava/lang/String;Ljava/lang/String;Ljava/time/LocalDateTime;)V",
      "context_after": "\u0000(\u0000)\u0001\u0000\u0003add\u0001\u0000\u0015(Ljava/lang/Object;)Z\n\u0000%\u0000+"
    },
    {
      "path": "target/classes/com/example/UserService$AuditLogger.class",
      "line": 17,
      "col": 16,
      "snippet": "\u0000(\u0000)\u0001\u0000\u0003add\u0001\u0000\u0015(Ljava/lang/Object;)Z",
      "context_before": "\u0000\t\u0000#\u0001\u0000g(Lcom/example/UserService$OperationType;Ljava/lang/String;Ljava/lang/String;Ljava/time/LocalDateTime;)V\n\u0000%\u0000'\u0007\u0000&\u0001\u0000\u000ejava/util/List",
      "context_after": "\u0000%\u0000+\n\u0000,\u0000-\u0001\u0000\u0004size\u0001\u0000\u0003()I"
    },
    {
      "path": "target/classes/com/example/UserService$AuditLogger.class",
      "line": 21,
      "col": 21,
      "snippet": "\u00000\u00001\u0001\u0000\u0006remove\u0001\u0000\u0015(I)Ljava/lang/Object;\u0001\u0000\toperation\u0001\u0000'Lcom/example/UserService$OperationType;\u0001\u0000\u0006userId\u0001\u0000\u0012Ljava/lang/String;\u0001\u0000\u0007details\u0001\u0000\u0005entry\u0001\u0000$Lcom/example/UserService$AuditEntry;\u0001\u0000",
      "context_before": "\u0000,\u0000-\u0001\u0000\u0004size\u0001\u0000\u0003()I\n\u0000%\u0000/",
      "context_after": "StackMapTable\u0007\u0000;\u0001\u0000\u0013java/lang/Throwable\u0001\u0000\u0010getRecentEntries\u0001\u0000\u0013(I)Ljava/util/List;\u0001\u00009(I)Ljava/util/List<Lcom/example/UserService$AuditEntry;>;\n\u0000@\u0000B\u0007\u0000A\u0001\u0000\u000ejava/lang/Math"
    },
    {
      "path": "target/classes/com/example/UserService$AuditLogger.class",
      "line": 21,
      "col": 105,
      "snippet": "\u00000\u00001\u0001\u0000\u0006remove\u0001\u0000\u0015(I)Ljava/lang/Object;\u0001\u0000\toperation\u0001\u0000'Lcom/example/UserService$OperationType;\u0001\u0000\u0006userId\u0001\u0000\u0012Ljava/lang/String;\u0001\u0000\u0007details\u0001\u0000\u0005entry\u0001\u0000$Lcom/example/UserService$AuditEntry;\u0001\u0000",
      "context_before": "\u0000,\u0000-\u0001\u0000\u0004size\u0001\u0000\u0003()I\n\u0000%\u0000/",
      "context_after": "StackMapTable\u0007\u0000;\u0001\u0000\u0013java/lang/Throwable\u0001\u0000\u0010getRecentEntries\u0001\u0000\u0013(I)Ljava/util/List;\u0001\u00009(I)Ljava/util/List<Lcom/example/UserService$AuditEntry;>;\n\u0000@\u0000B\u0007\u0000A\u0001\u0000\u000ejava/lang/Math"
    },
    {
      "path": "target/classes/com/example/UserService$AuditLogger.class",
      "line": 22,
      "col": 20,
      "snippet": "StackMapTable\u0007\u0000;\u0001\u0000\u0013java/lang/Throwable\u0001\u0000\u0010getRecentEntries\u0001\u0000\u0013(I)Ljava/util/List;\u0001\u00009(I)Ljava/util/List<Lcom/example/UserService$AuditEntry;>;",
      "context_before": "\u0000%\u0000/\n\u00000\u00001\u0001\u0000\u0006remove\u0001\u0000\u0015(I)Ljava/lang/Object;\u0001\u0000\toperation\u0001\u0000'Lcom/example/UserService$OperationType;\u0001\u0000\u0006userId\u0001\u0000\u0012Ljava/lang/String;\u0001\u0000\u0007details\u0001\u0000\u0005entry\u0001\u0000$Lcom/example/UserService$AuditEntry;\u0001\u0000",
      "context_after": "\u0000@\u0000B\u0007\u0000A\u0001\u0000\u000ejava/lang/Math\n\u0000C\u0000D\u0001\u0000\u0003max\u0001\u0000\u0005(II)I"
    },
    {
      "path": "target/classes/com/example/UserService$AuditLogger.class",
      "line": 22,
      "col": 65,
      "snippet": "StackMapTable\u0007\u0000;\u0001\u0000\u0013java/lang/Throwable\u0001\u0000\u0010getRecentEntries\u0001\u0000\u0013(I)Ljava/util/List;\u0001\u00009(I)Ljava/util/List<Lcom/example/UserService$AuditEntry;>;",
      "context_before": "\u0000%\u0000/\n\u00000\u00001\u0001\u0000\u0006remove\u0001\u0000\u0015(I)Ljava/lang/Object;\u0001\u0000\toperation\u0001\u0000'Lcom/example/UserService$OperationType;\u0001\u0000\u0006userId\u0001\u0000\u0012Ljava/lang/String;\u0001\u0000\u0007details\u0001\u0000\u0005entry\u0001\u0000$Lcom/example/UserService$AuditEntry;\u0001\u0000",
      "context_after": "\u0000@\u0000B\u0007\u0000A\u0001\u0000\u000ejava/lang/Math\n\u0000C\u0000D\u0001\u0000\u0003max\u0001\u0000\u0005(II)I"
    },
    {
      "path": "target/classes/com/example/UserService$AuditLogger.class",
      "line": 22,
      "col": 87,
      "snippet": "StackMapTable\u0007\u0000;\u0001\u0000\u0013java/lang/Throwable\u0001\u0000\u0010getRecentEntries\u0001\u0000\u0013(I)Ljava/util/List;\u0001\u00009(I)Ljava/util/List<Lcom/example/UserService$AuditEntry;>;",
      "context_before": "\u0000%\u0000/\n\u00000\u00001\u0001\u0000\u0006remove\u0001\u0000\u0015(I)Ljava/lang/Object;\u0001\u0000\toperation\u0001\u0000'Lcom/example/UserService$OperationType;\u0001\u0000\u0006userId\u0001\u0000\u0012Ljava/lang/String;\u0001\u0000\u0007details\u0001\u0000\u0005entry\u0001\u0000$Lcom/example/UserService$AuditEntry;\u0001\u0000",
      "context_after": "\u0000@\u0000B\u0007\u0000A\u0001\u0000\u000ejava/lang/Math\n\u0000C\u0000D\u0001\u0000\u0003max\u0001\u0000\u0005(II)I"
    },
    {
      "path": "target/classes/com/example/UserService$AuditLogger.class",
      "line": 23,
      "col": 11,
      "snippet": "\u0000@\u0000B\u0007\u0000A\u0001\u0000\u000ejava/lang/Math",
      "context_before": "\u00000\u00001\u0001\u0000\u0006remove\u0001\u0000\u0015(I)Ljava/lang/Object;\u0001\u0000\toperation\u0001\u0000'Lcom/example/UserService$OperationType;\u0001\u0000\u0006userId\u0001\u0000\u0012Ljava/lang/String;\u0001\u0000\u0007details\u0001\u0000\u0005entry\u0001\u0000$Lcom/example/UserService$AuditEntry;\u0001\u0000\nStackMapTable\u0007\u0000;\u0001\u0000\u0013java/lang/Throwable\u0001\u0000\u0010getRecentEntries\u0001\u0000\u0013(I)Ljava/util/List;\u0001\u00009(I)Ljava/util/List<Lcom/example/UserService$AuditEntry;>;",
      "context_after": "\u0000C\u0000D\u0001\u0000\u0003max\u0001\u0000\u0005(II)I\n\u0000%\u0000F"
    },
    {
      "path": "target/classes/com/example/UserService$AuditLogger.class",
      "line": 26,
      "col": 23,
      "snippet": "\u0000G\u0000H\u0001\u0000\u0007subList\u0001\u0000\u0014(II)Ljava/util/List;",
      "context_before": "\u0000C\u0000D\u0001\u0000\u0003max\u0001\u0000\u0005(II)I\n\u0000%\u0000F",
      "context_after": "\u0000\u000e\u0000J\n\u0000\t\u0000K\u0001\u0000\u0019(Ljava/util/Collection;)V\u0001\u0000\u0005limit\u0001\u0000\u0001I\u0001\u0000\u0005start\u0001\u0000\u0010getEntriesByUser\u0001\u0000$(Ljava/lang/String;)Ljava/util/List;\u0001\u0000J(Ljava/lang/String;)Ljava/util/List<Lcom/example/UserService$AuditEntry;>;"
    },
    {
      "path": "target/classes/com/example/UserService$AuditLogger.class",
      "line": 28,
      "col": 10,
      "snippet": "\u0000\t\u0000K\u0001\u0000\u0019(Ljava/util/Collection;)V\u0001\u0000\u0005limit\u0001\u0000\u0001I\u0001\u0000\u0005start\u0001\u0000\u0010getEntriesByUser\u0001\u0000$(Ljava/lang/String;)Ljava/util/List;\u0001\u0000J(Ljava/lang/String;)Ljava/util/List<Lcom/example/UserService$AuditEntry;>;",
      "context_before": "\u0000G\u0000H\u0001\u0000\u0007subList\u0001\u0000\u0014(II)Ljava/util/List;\n\u0000\u000e\u0000J",
      "context_after": "\u0000%\u0000S\n\u0000T\u0000U\u0001\u0000\u0006stream\u0001\u0000\u001b()Ljava/util/stream/Stream;\u0012\u0000\u0000\u0000W"
    },
    {
      "path": "target/classes/com/example/UserService$AuditLogger.class",
      "line": 28,
      "col": 77,
      "snippet": "\u0000\t\u0000K\u0001\u0000\u0019(Ljava/util/Collection;)V\u0001\u0000\u0005limit\u0001\u0000\u0001I\u0001\u0000\u0005start\u0001\u0000\u0010getEntriesByUser\u0001\u0000$(Ljava/lang/String;)Ljava/util/List;\u0001\u0000J(Ljava/lang/String;)Ljava/util/List<Lcom/example/UserService$AuditEntry;>;",
      "context_before": "\u0000G\u0000H\u0001\u0000\u0007subList\u0001\u0000\u0014(II)Ljava/util/List;\n\u0000\u000e\u0000J",
      "context_after": "\u0000%\u0000S\n\u0000T\u0000U\u0001\u0000\u0006stream\u0001\u0000\u001b()Ljava/util/stream/Stream;\u0012\u0000\u0000\u0000W"
    },
    {
      "path": "target/classes/com/example/UserService$AuditLogger.class",
      "line": 28,
      "col": 96,
      "snippet": "\u0000\t\u0000K\u0001\u0000\u0019(Ljava/util/Collection;)V\u0001\u0000\u0005limit\u0001\u0000\u0001I\u0001\u0000\u0005start\u0001\u0000\u0010getEntriesByUser\u0001\u0000$(Ljava/lang/String;)Ljava/util/List;\u0001\u0000J(Ljava/lang/String;)Ljava/util/List<Lcom/example/UserService$AuditEntry;>;",
      "context_before": "\u0000G\u0000H\u0001\u0000\u0007subList\u0001\u0000\u0014(II)Ljava/util/List;\n\u0000\u000e\u0000J",
      "context_after": "\u0000%\u0000S\n\u0000T\u0000U\u0001\u0000\u0006stream\u0001\u0000\u001b()Ljava/util/stream/Stream;\u0012\u0000\u0000\u0000W"
    },
    {
      "path": "target/classes/com/example/UserService$AuditLogger.class",
      "line": 28,
      "col": 116,
      "snippet": "\u0000\t\u0000K\u0001\u0000\u0019(Ljava/util/Collection;)V\u0001\u0000\u0005limit\u0001\u0000\u0001I\u0001\u0000\u0005start\u0001\u0000\u0010getEntriesByUser\u0001\u0000$(Ljava/lang/String;)Ljava/util/List;\u0001\u0000J(Ljava/lang/String;)Ljava/util/List<Lcom/example/UserService$AuditEntry;>;",
      "context_before": "\u0000G\u0000H\u0001\u0000\u0007subList\u0001\u0000\u0014(II)Ljava/util/List;\n\u0000\u000e\u0000J",
      "context_after": "\u0000%\u0000S\n\u0000T\u0000U\u0001\u0000\u0006stream\u0001\u0000\u001b()Ljava/util/stream/Stream;\u0012\u0000\u0000\u0000W"
    },
    {
      "path": "target/classes/com/example/UserService$AuditLogger.class",
      "line": 28,
      "col": 135,
      "snippet": "\u0000\t\u0000K\u0001\u0000\u0019(Ljava/util/Collection;)V\u0001\u0000\u0005limit\u0001\u0000\u0001I\u0001\u0000\u0005start\u0001\u0000\u0010getEntriesByUser\u0001\u0000$(Ljava/lang/String;)Ljava/util/List;\u0001\u0000J(Ljava/lang/String;)Ljava/util/List<Lcom/example/UserService$AuditEntry;>;",
      "context_before": "\u0000G\u0000H\u0001\u0000\u0007subList\u0001\u0000\u0014(II)Ljava/util/List;\n\u0000\u000e\u0000J",
      "context_after": "\u0000%\u0000S\n\u0000T\u0000U\u0001\u0000\u0006stream\u0001\u0000\u001b()Ljava/util/stream/Stream;\u0012\u0000\u0000\u0000W"
    },
    {
      "path": "target/classes/com/example/UserService$AuditLogger.class",
      "line": 30,
      "col": 20,
      "snippet": "\u0000T\u0000U\u0001\u0000\u0006stream\u0001\u0000\u001b()Ljava/util/stream/Stream;\u0012\u0000\u0000\u0000W",
      "context_before": "\u0000\t\u0000K\u0001\u0000\u0019(Ljava/util/Collection;)V\u0001\u0000\u0005limit\u0001\u0000\u0001I\u0001\u0000\u0005start\u0001\u0000\u0010getEntriesByUser\u0001\u0000$(Ljava/lang/String;)Ljava/util/List;\u0001\u0000J(Ljava/lang/String;)Ljava/util/List<Lcom/example/UserService$AuditEntry;>;\n\u0000%\u0000S",
      "context_after": "\u0000X\u0000Y\u0001\u0000\u0004test\u0001\u00002(Ljava/lang/String;)Ljava/util/function/Predicate;\n\u0000[\u0000]\u0007\u0000\\\u0001\u0000\u0017java/util/stream/Stream"
    },
    {
      "path": "target/classes/com/example/UserService$AuditLogger.class",
      "line": 31,
      "col": 17,
      "snippet": "\u0000X\u0000Y\u0001\u0000\u0004test\u0001\u00002(Ljava/lang/String;)Ljava/util/function/Predicate;",
      "context_before": "\u0000%\u0000S\n\u0000T\u0000U\u0001\u0000\u0006stream\u0001\u0000\u001b()Ljava/util/stream/Stream;\u0012\u0000\u0000\u0000W",
      "context_after": "\u0000[\u0000]\u0007\u0000\\\u0001\u0000\u0017java/util/stream/Stream\n\u0000^\u0000_\u0001\u0000\u0006filter\u0001\u00009(Ljava/util/function/Predicate;)Ljava/util/stream/Stream;"
    },
    {
      "path": "target/classes/com/example/UserService$AuditLogger.class",
      "line": 31,
      "col": 36,
      "snippet": "\u0000X\u0000Y\u0001\u0000\u0004test\u0001\u00002(Ljava/lang/String;)Ljava/util/function/Predicate;",
      "context_before": "\u0000%\u0000S\n\u0000T\u0000U\u0001\u0000\u0006stream\u0001\u0000\u001b()Ljava/util/stream/Stream;\u0012\u0000\u0000\u0000W",
      "context_after": "\u0000[\u0000]\u0007\u0000\\\u0001\u0000\u0017java/util/stream/Stream\n\u0000^\u0000_\u0001\u0000\u0006filter\u0001\u00009(Ljava/util/function/Predicate;)Ljava/util/stream/Stream;"
    },
    {
      "path": "target/classes/com/example/UserService$AuditLogger.class",
      "line": 32,
      "col": 11,
      "snippet": "\u0000[\u0000]\u0007\u0000\\\u0001\u0000\u0017java/util/stream/Stream",
      "context_before": "\u0000T\u0000U\u0001\u0000\u0006stream\u0001\u0000\u001b()Ljava/util/stream/Stream;\u0012\u0000\u0000\u0000W\n\u0000X\u0000Y\u0001\u0000\u0004test\u0001\u00002(Ljava/lang/String;)Ljava/util/function/Predicate;",
      "context_after": "\u0000^\u0000_\u0001\u0000\u0006filter\u0001\u00009(Ljava/util/function/Predicate;)Ljava/util/stream/Stream;\n\u0000a\u0000c\u0007\u0000b\u0001\u0000\u001bjava/util/stream/Collectors"
    },
    {
      "path": "target/classes/com/example/UserService$AuditLogger.class",
      "line": 33,
      "col": 19,
      "snippet": "\u0000^\u0000_\u0001\u0000\u0006filter\u0001\u00009(Ljava/util/function/Predicate;)Ljava/util/stream/Stream;",
      "context_before": "\u0000X\u0000Y\u0001\u0000\u0004test\u0001\u00002(Ljava/lang/String;)Ljava/util/function/Predicate;\n\u0000[\u0000]\u0007\u0000\\\u0001\u0000\u0017java/util/stream/Stream",
      "context_after": "\u0000a\u0000c\u0007\u0000b\u0001\u0000\u001bjava/util/stream/Collectors\n\u0000d\u0000e\u0001\u0000\u0006toList\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/UserService$AuditLogger.class",
      "line": 33,
      "col": 50,
      "snippet": "\u0000^\u0000_\u0001\u0000\u0006filter\u0001\u00009(Ljava/util/function/Predicate;)Ljava/util/stream/Stream;",
      "context_before": "\u0000X\u0000Y\u0001\u0000\u0004test\u0001\u00002(Ljava/lang/String;)Ljava/util/function/Predicate;\n\u0000[\u0000]\u0007\u0000\\\u0001\u0000\u0017java/util/stream/Stream",
      "context_after": "\u0000a\u0000c\u0007\u0000b\u0001\u0000\u001bjava/util/stream/Collectors\n\u0000d\u0000e\u0001\u0000\u0006toList\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/UserService$AuditLogger.class",
      "line": 34,
      "col": 11,
      "snippet": "\u0000a\u0000c\u0007\u0000b\u0001\u0000\u001bjava/util/stream/Collectors",
      "context_before": "\u0000[\u0000]\u0007\u0000\\\u0001\u0000\u0017java/util/stream/Stream\n\u0000^\u0000_\u0001\u0000\u0006filter\u0001\u00009(Ljava/util/function/Predicate;)Ljava/util/stream/Stream;",
      "context_after": "\u0000d\u0000e\u0001\u0000\u0006toList\u0001\u0000\n()Ljava/util/stream/Collector;"
    },
    {
      "path": "target/classes/com/example/UserService$AuditLogger.class",
      "line": 36,
      "col": 4,
      "snippet": "()Ljava/util/stream/Collector;",
      "context_before": "\u0000a\u0000c\u0007\u0000b\u0001\u0000\u001bjava/util/stream/Collectors\n\u0000d\u0000e\u0001\u0000\u0006toList\u0001\u0000",
      "context_after": "\u0000[\u0000g\n\u0000h\u0000i\u0001\u0000\u0007collect\u0001\u00000(Ljava/util/stream/Collector;)Ljava/lang/Object;\u0007\u0000k\u0001\u0000\u0010java/lang/String\u0001\u0000\blambda$0\u0001\u00009(Ljava/lang/String;Lcom/example/UserService$AuditEntry;)Z"
    },
    {
      "path": "target/classes/com/example/UserService$AuditLogger.class",
      "line": 38,
      "col": 20,
      "snippet": "\u0000h\u0000i\u0001\u0000\u0007collect\u0001\u00000(Ljava/util/stream/Collector;)Ljava/lang/Object;\u0007\u0000k\u0001\u0000\u0010java/lang/String\u0001\u0000\blambda$0\u0001\u00009(Ljava/lang/String;Lcom/example/UserService$AuditEntry;)Z",
      "context_before": "()Ljava/util/stream/Collector;\n\u0000[\u0000g",
      "context_after": "\u0000\u0019\u0000o\n\u0000p\u0000q\u0001\u0000\tgetUserId\u0001\u0000\u0014()Ljava/lang/String;"
    },
    {
      "path": "target/classes/com/example/UserService$AuditLogger.class",
      "line": 38,
      "col": 49,
      "snippet": "\u0000h\u0000i\u0001\u0000\u0007collect\u0001\u00000(Ljava/util/stream/Collector;)Ljava/lang/Object;\u0007\u0000k\u0001\u0000\u0010java/lang/String\u0001\u0000\blambda$0\u0001\u00009(Ljava/lang/String;Lcom/example/UserService$AuditEntry;)Z",
      "context_before": "()Ljava/util/stream/Collector;\n\u0000[\u0000g",
      "context_after": "\u0000\u0019\u0000o\n\u0000p\u0000q\u0001\u0000\tgetUserId\u0001\u0000\u0014()Ljava/lang/String;"
    },
    {
      "path": "target/classes/com/example/UserService$AuditLogger.class",
      "line": 38,
      "col": 72,
      "snippet": "\u0000h\u0000i\u0001\u0000\u0007collect\u0001\u00000(Ljava/util/stream/Collector;)Ljava/lang/Object;\u0007\u0000k\u0001\u0000\u0010java/lang/String\u0001\u0000\blambda$0\u0001\u00009(Ljava/lang/String;Lcom/example/UserService$AuditEntry;)Z",
      "context_before": "()Ljava/util/stream/Collector;\n\u0000[\u0000g",
      "context_after": "\u0000\u0019\u0000o\n\u0000p\u0000q\u0001\u0000\tgetUserId\u0001\u0000\u0014()Ljava/lang/String;"
    },
    {
      "path": "target/classes/com/example/UserService$AuditLogger.class",
      "line": 38,
      "col": 104,
      "snippet": "\u0000h\u0000i\u0001\u0000\u0007collect\u0001\u00000(Ljava/util/stream/Collector;)Ljava/lang/Object;\u0007\u0000k\u0001\u0000\u0010java/lang/String\u0001\u0000\blambda$0\u0001\u00009(Ljava/lang/String;Lcom/example/UserService$AuditEntry;)Z",
      "context_before": "()Ljava/util/stream/Collector;\n\u0000[\u0000g",
      "context_after": "\u0000\u0019\u0000o\n\u0000p\u0000q\u0001\u0000\tgetUserId\u0001\u0000\u0014()Ljava/lang/String;"
    },
    {
      "path": "target/classes/com/example/UserService$AuditLogger.class",
      "line": 40,
      "col": 23,
      "snippet": "\u0000p\u0000q\u0001\u0000\tgetUserId\u0001\u0000\u0014()Ljava/lang/String;",
      "context_before": "\u0000h\u0000i\u0001\u0000\u0007collect\u0001\u00000(Ljava/util/stream/Collector;)Ljava/lang/Object;\u0007\u0000k\u0001\u0000\u0010java/lang/String\u0001\u0000\blambda$0\u0001\u00009(Ljava/lang/String;Lcom/example/UserService$AuditEntry;)Z\n\u0000\u0019\u0000o",
      "context_after": "\u0000j\u0000s\n\u0000t\u0000)\u0001\u0000\u0006equals\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/UserService$AuditLogger.class",
      "line": 43,
      "col": 26,
      "snippet": "SourceFile\u0001\u0000\u0010UserService.java\u0001\u0000\u0010BootstrapMethods",
      "context_before": "\u0000j\u0000s\n\u0000t\u0000)\u0001\u0000\u0006equals\u0001\u0000",
      "context_after": "\u0000y\u0000{\u0007\u0000z\u0001\u0000\"java/lang/invoke/LambdaMetafactory\n\u0000|\u0000}\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/UserService$AuditLogger.class",
      "line": 44,
      "col": 11,
      "snippet": "\u0000y\u0000{\u0007\u0000z\u0001\u0000\"java/lang/invoke/LambdaMetafactory",
      "context_before": "\u0000t\u0000)\u0001\u0000\u0006equals\u0001\u0000\nSourceFile\u0001\u0000\u0010UserService.java\u0001\u0000\u0010BootstrapMethods",
      "context_after": "\u0000|\u0000}\u0001\u0000\nmetafactory\u0001\u0000(Ljava/lang/invoke/MethodHandles$Lookup;Ljava/lang/String;Ljava/lang/invoke/MethodType;Ljava/lang/invoke/MethodType;Ljava/lang/invoke/MethodHandle;Ljava/lang/invoke/MethodType;)Ljava/lang/invoke/CallSite;\u000f\u0006\u0000x\u0010\u0000)"
    },
    {
      "path": "target/classes/com/example/UserService$AuditLogger.class",
      "line": 46,
      "col": 16,
      "snippet": "metafactory\u0001\u0000(Ljava/lang/invoke/MethodHandles$Lookup;Ljava/lang/String;Ljava/lang/invoke/MethodType;Ljava/lang/invoke/MethodType;Ljava/lang/invoke/MethodHandle;Ljava/lang/invoke/MethodType;)Ljava/lang/invoke/CallSite;\u000f\u0006\u0000x\u0010\u0000)",
      "context_before": "\u0000y\u0000{\u0007\u0000z\u0001\u0000\"java/lang/invoke/LambdaMetafactory\n\u0000|\u0000}\u0001\u0000",
      "context_after": "\u0000\u0001\u0000\n\u0000l\u0000m\u000f\u0006\u0000\u0001\u0000'(Lcom/example/UserService$AuditEntry;)Z\u0010\u0000\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/UserService$AuditLogger.class",
      "line": 46,
      "col": 55,
      "snippet": "metafactory\u0001\u0000(Ljava/lang/invoke/MethodHandles$Lookup;Ljava/lang/String;Ljava/lang/invoke/MethodType;Ljava/lang/invoke/MethodType;Ljava/lang/invoke/MethodHandle;Ljava/lang/invoke/MethodType;)Ljava/lang/invoke/CallSite;\u000f\u0006\u0000x\u0010\u0000)",
      "context_before": "\u0000y\u0000{\u0007\u0000z\u0001\u0000\"java/lang/invoke/LambdaMetafactory\n\u0000|\u0000}\u0001\u0000",
      "context_after": "\u0000\u0001\u0000\n\u0000l\u0000m\u000f\u0006\u0000\u0001\u0000'(Lcom/example/UserService$AuditEntry;)Z\u0010\u0000\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/UserService$AuditLogger.class",
      "line": 46,
      "col": 73,
      "snippet": "metafactory\u0001\u0000(Ljava/lang/invoke/MethodHandles$Lookup;Ljava/lang/String;Ljava/lang/invoke/MethodType;Ljava/lang/invoke/MethodType;Ljava/lang/invoke/MethodHandle;Ljava/lang/invoke/MethodType;)Ljava/lang/invoke/CallSite;\u000f\u0006\u0000x\u0010\u0000)",
      "context_before": "\u0000y\u0000{\u0007\u0000z\u0001\u0000\"java/lang/invoke/LambdaMetafactory\n\u0000|\u0000}\u0001\u0000",
      "context_after": "\u0000\u0001\u0000\n\u0000l\u0000m\u000f\u0006\u0000\u0001\u0000'(Lcom/example/UserService$AuditEntry;)Z\u0010\u0000\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/UserService$AuditLogger.class",
      "line": 46,
      "col": 102,
      "snippet": "metafactory\u0001\u0000(Ljava/lang/invoke/MethodHandles$Lookup;Ljava/lang/String;Ljava/lang/invoke/MethodType;Ljava/lang/invoke/MethodType;Ljava/lang/invoke/MethodHandle;Ljava/lang/invoke/MethodType;)Ljava/lang/invoke/CallSite;\u000f\u0006\u0000x\u0010\u0000)",
      "context_before": "\u0000y\u0000{\u0007\u0000z\u0001\u0000\"java/lang/invoke/LambdaMetafactory\n\u0000|\u0000}\u0001\u0000",
      "context_after": "\u0000\u0001\u0000\n\u0000l\u0000m\u000f\u0006\u0000\u0001\u0000'(Lcom/example/UserService$AuditEntry;)Z\u0010\u0000\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/UserService$AuditLogger.class",
      "line": 46,
      "col": 131,
      "snippet": "metafactory\u0001\u0000(Ljava/lang/invoke/MethodHandles$Lookup;Ljava/lang/String;Ljava/lang/invoke/MethodType;Ljava/lang/invoke/MethodType;Ljava/lang/invoke/MethodHandle;Ljava/lang/invoke/MethodType;)Ljava/lang/invoke/CallSite;\u000f\u0006\u0000x\u0010\u0000)",
      "context_before": "\u0000y\u0000{\u0007\u0000z\u0001\u0000\"java/lang/invoke/LambdaMetafactory\n\u0000|\u0000}\u0001\u0000",
      "context_after": "\u0000\u0001\u0000\n\u0000l\u0000m\u000f\u0006\u0000\u0001\u0000'(Lcom/example/UserService$AuditEntry;)Z\u0010\u0000\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/UserService$AuditLogger.class",
      "line": 46,
      "col": 162,
      "snippet": "metafactory\u0001\u0000(Ljava/lang/invoke/MethodHandles$Lookup;Ljava/lang/String;Ljava/lang/invoke/MethodType;Ljava/lang/invoke/MethodType;Ljava/lang/invoke/MethodHandle;Ljava/lang/invoke/MethodType;)Ljava/lang/invoke/CallSite;\u000f\u0006\u0000x\u0010\u0000)",
      "context_before": "\u0000y\u0000{\u0007\u0000z\u0001\u0000\"java/lang/invoke/LambdaMetafactory\n\u0000|\u0000}\u0001\u0000",
      "context_after": "\u0000\u0001\u0000\n\u0000l\u0000m\u000f\u0006\u0000\u0001\u0000'(Lcom/example/UserService$AuditEntry;)Z\u0010\u0000\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/UserService$AuditLogger.class",
      "line": 46,
      "col": 192,
      "snippet": "metafactory\u0001\u0000(Ljava/lang/invoke/MethodHandles$Lookup;Ljava/lang/String;Ljava/lang/invoke/MethodType;Ljava/lang/invoke/MethodType;Ljava/lang/invoke/MethodHandle;Ljava/lang/invoke/MethodType;)Ljava/lang/invoke/CallSite;\u000f\u0006\u0000x\u0010\u0000)",
      "context_before": "\u0000y\u0000{\u0007\u0000z\u0001\u0000\"java/lang/invoke/LambdaMetafactory\n\u0000|\u0000}\u0001\u0000",
      "context_after": "\u0000\u0001\u0000\n\u0000l\u0000m\u000f\u0006\u0000\u0001\u0000'(Lcom/example/UserService$AuditEntry;)Z\u0010\u0000\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/UserService$AuditLogger.class",
      "line": 52,
      "col": 19,
      "snippet": "OperationType\u0007\u0000\u0001\u0000%java/lang/invoke/MethodHandles$Lookup\u0007\u0000\u0001\u0000",
      "context_before": "AuditEntry\u0001\u0000\nAuditLogger\u0007\u0000\u0001\u0000%com/example/UserService$OperationType\u0001\u0000",
      "context_after": "java/lang/invoke/MethodHandles\u0001\u0000\u0006Lookup\u0001\u0000\bNestHost\u0000!\u0000\u0001\u0000\u0003\u0000\u0000\u0000\u0001\u0000\u0012\u0000\u0005\u0000\u0006\u0000\u0001\u0000\u0007\u0000\u0000\u0000\u0002\u0000\b\u0000\u0005\u0000\u0001\u0000\t\u0000\n\u0000\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/UserService$AuditLogger.class",
      "line": 53,
      "col": 1,
      "snippet": "java/lang/invoke/MethodHandles\u0001\u0000\u0006Lookup\u0001\u0000\bNestHost\u0000!\u0000\u0001\u0000\u0003\u0000\u0000\u0000\u0001\u0000\u0012\u0000\u0005\u0000\u0006\u0000\u0001\u0000\u0007\u0000\u0000\u0000\u0002\u0000\b\u0000\u0005\u0000\u0001\u0000\t\u0000",
      "context_before": "AuditLogger\u0007\u0000\u0001\u0000%com/example/UserService$OperationType\u0001\u0000\nOperationType\u0007\u0000\u0001\u0000%java/lang/invoke/MethodHandles$Lookup\u0007\u0000\u0001\u0000",
      "context_after": "\u0000\u0001\u0000\n\u0000\u0000\u0000B\u0000\u0003\u0000\u0001\u0000\u0000\u0000\u0010*\u0000"
    },
    {
      "path": "target/classes/com/example/AdvancedUtils$TimeUtils.class",
      "line": 1,
      "col": 53,
      "snippet": "\u0000\u0000\u00007\u0000\u0007\u0000\u0002\u0001\u0000#com/example/AdvancedUtils$TimeUtils\u0007\u0000\u0004\u0001\u0000\u0010java/lang/Object\u0001\u0000",
      "context_before": "",
      "context_after": "ISO_FORMATTER\u0001\u0000$Ljava/time/format/DateTimeFormatter;\u0001\u0000\b<clinit>\u0001\u0000\u0003()V\u0001\u0000\u0004Code\b\u0000\n\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/AdvancedUtils$TimeUtils.class",
      "line": 2,
      "col": 18,
      "snippet": "ISO_FORMATTER\u0001\u0000$Ljava/time/format/DateTimeFormatter;\u0001\u0000\b<clinit>\u0001\u0000\u0003()V\u0001\u0000\u0004Code\b\u0000",
      "context_before": "\u0000\u0000\u00007\u0000\u0007\u0000\u0002\u0001\u0000#com/example/AdvancedUtils$TimeUtils\u0007\u0000\u0004\u0001\u0000\u0010java/lang/Object\u0001\u0000",
      "context_after": "\u0001\u0000\nyyyy-MM-dd'T'HH:mm:ss.SSS'Z'"
    },
    {
      "path": "target/classes/com/example/AdvancedUtils$TimeUtils.class",
      "line": 6,
      "col": 9,
      "snippet": "\u0000\u000f\u0007\u0000\u000e\u0001\u0000\"java/time/format/DateTimeFormatter",
      "context_before": "yyyy-MM-dd'T'HH:mm:ss.SSS'Z'\n\u0000",
      "context_after": "\u0000\u0010\u0000\u0011\u0001\u0000\tofPattern\u0001\u00008(Ljava/lang/String;)Ljava/time/format/DateTimeFormatter;\t\u0000\u0001\u0000\u0013\n\u0000\u0005\u0000\u0006\u0001\u0000\u000fLineNumberTable\u0001\u0000\u0012LocalVariableTable\u0001\u0000\u0006<init>"
    },
    {
      "path": "target/classes/com/example/AdvancedUtils$TimeUtils.class",
      "line": 7,
      "col": 22,
      "snippet": "\u0000\u0010\u0000\u0011\u0001\u0000\tofPattern\u0001\u00008(Ljava/lang/String;)Ljava/time/format/DateTimeFormatter;\t\u0000\u0001\u0000\u0013",
      "context_before": "\u0000\n\u0000\u000f\u0007\u0000\u000e\u0001\u0000\"java/time/format/DateTimeFormatter",
      "context_after": "\u0000\u0005\u0000\u0006\u0001\u0000\u000fLineNumberTable\u0001\u0000\u0012LocalVariableTable\u0001\u0000\u0006<init>\n\u0000\u0003\u0000\u0018"
    },
    {
      "path": "target/classes/com/example/AdvancedUtils$TimeUtils.class",
      "line": 7,
      "col": 41,
      "snippet": "\u0000\u0010\u0000\u0011\u0001\u0000\tofPattern\u0001\u00008(Ljava/lang/String;)Ljava/time/format/DateTimeFormatter;\t\u0000\u0001\u0000\u0013",
      "context_before": "\u0000\n\u0000\u000f\u0007\u0000\u000e\u0001\u0000\"java/time/format/DateTimeFormatter",
      "context_after": "\u0000\u0005\u0000\u0006\u0001\u0000\u000fLineNumberTable\u0001\u0000\u0012LocalVariableTable\u0001\u0000\u0006<init>\n\u0000\u0003\u0000\u0018"
    },
    {
      "path": "target/classes/com/example/AdvancedUtils$TimeUtils.class",
      "line": 10,
      "col": 75,
      "snippet": "\u0000\u0016\u0000\b\u0001\u0000\u0004this\u0001\u0000%Lcom/example/AdvancedUtils$TimeUtils;\u0001\u0000\u000fformatTimestamp\u0001\u0000-(Ljava/time/LocalDateTime;)Ljava/lang/String;",
      "context_before": "\u0000\u0005\u0000\u0006\u0001\u0000\u000fLineNumberTable\u0001\u0000\u0012LocalVariableTable\u0001\u0000\u0006<init>\n\u0000\u0003\u0000\u0018",
      "context_after": "\u0000\n\u0000 \u0007\u0000\u001f\u0001\u0000\u0010java/time/ZoneId"
    },
    {
      "path": "target/classes/com/example/AdvancedUtils$TimeUtils.class",
      "line": 10,
      "col": 101,
      "snippet": "\u0000\u0016\u0000\b\u0001\u0000\u0004this\u0001\u0000%Lcom/example/AdvancedUtils$TimeUtils;\u0001\u0000\u000fformatTimestamp\u0001\u0000-(Ljava/time/LocalDateTime;)Ljava/lang/String;",
      "context_before": "\u0000\u0005\u0000\u0006\u0001\u0000\u000fLineNumberTable\u0001\u0000\u0012LocalVariableTable\u0001\u0000\u0006<init>\n\u0000\u0003\u0000\u0018",
      "context_after": "\u0000\n\u0000 \u0007\u0000\u001f\u0001\u0000\u0010java/time/ZoneId"
    },
    {
      "path": "target/classes/com/example/AdvancedUtils$TimeUtils.class",
      "line": 12,
      "col": 9,
      "snippet": "\u0000 \u0007\u0000\u001f\u0001\u0000\u0010java/time/ZoneId",
      "context_before": "\u0000\u0016\u0000\b\u0001\u0000\u0004this\u0001\u0000%Lcom/example/AdvancedUtils$TimeUtils;\u0001\u0000\u000fformatTimestamp\u0001\u0000-(Ljava/time/LocalDateTime;)Ljava/lang/String;\n\u0000",
      "context_after": "\u0000!\u0000\"\u0001\u0000\nsystemDefault\u0001\u0000\u0014()Ljava/time/ZoneId;"
    },
    {
      "path": "target/classes/com/example/AdvancedUtils$TimeUtils.class",
      "line": 14,
      "col": 20,
      "snippet": "systemDefault\u0001\u0000\u0014()Ljava/time/ZoneId;",
      "context_before": "\u0000 \u0007\u0000\u001f\u0001\u0000\u0010java/time/ZoneId\n\u0000!\u0000\"\u0001\u0000",
      "context_after": "\u0000$\u0000&\u0007\u0000%\u0001\u0000\u0017java/time/LocalDateTime\n\u0000'\u0000(\u0001\u0000\u0006atZone\u0001\u0000-(Ljava/time/ZoneId;)Ljava/time/ZonedDateTime;"
    },
    {
      "path": "target/classes/com/example/AdvancedUtils$TimeUtils.class",
      "line": 15,
      "col": 11,
      "snippet": "\u0000$\u0000&\u0007\u0000%\u0001\u0000\u0017java/time/LocalDateTime",
      "context_before": "\u0000!\u0000\"\u0001\u0000\nsystemDefault\u0001\u0000\u0014()Ljava/time/ZoneId;",
      "context_after": "\u0000'\u0000(\u0001\u0000\u0006atZone\u0001\u0000-(Ljava/time/ZoneId;)Ljava/time/ZonedDateTime;\n\u0000*\u0000,\u0007\u0000+\u0001\u0000\u0017java/time/ZonedDateTime"
    },
    {
      "path": "target/classes/com/example/AdvancedUtils$TimeUtils.class",
      "line": 16,
      "col": 19,
      "snippet": "\u0000'\u0000(\u0001\u0000\u0006atZone\u0001\u0000-(Ljava/time/ZoneId;)Ljava/time/ZonedDateTime;",
      "context_before": "systemDefault\u0001\u0000\u0014()Ljava/time/ZoneId;\n\u0000$\u0000&\u0007\u0000%\u0001\u0000\u0017java/time/LocalDateTime",
      "context_after": "\u0000*\u0000,\u0007\u0000+\u0001\u0000\u0017java/time/ZonedDateTime\n\u0000-\u0000.\u0001\u0000\u0006format\u0001\u00008(Ljava/time/format/DateTimeFormatter;)Ljava/lang/String;\u0001\u0000\ttimestamp\u0001\u0000\u0019Ljava/time/LocalDateTime;\u0001\u0000\u000eparseTimestamp\u0001\u0000-(Ljava/lang/String;)Ljava/time/LocalDateTime;"
    },
    {
      "path": "target/classes/com/example/AdvancedUtils$TimeUtils.class",
      "line": 16,
      "col": 38,
      "snippet": "\u0000'\u0000(\u0001\u0000\u0006atZone\u0001\u0000-(Ljava/time/ZoneId;)Ljava/time/ZonedDateTime;",
      "context_before": "systemDefault\u0001\u0000\u0014()Ljava/time/ZoneId;\n\u0000$\u0000&\u0007\u0000%\u0001\u0000\u0017java/time/LocalDateTime",
      "context_after": "\u0000*\u0000,\u0007\u0000+\u0001\u0000\u0017java/time/ZonedDateTime\n\u0000-\u0000.\u0001\u0000\u0006format\u0001\u00008(Ljava/time/format/DateTimeFormatter;)Ljava/lang/String;\u0001\u0000\ttimestamp\u0001\u0000\u0019Ljava/time/LocalDateTime;\u0001\u0000\u000eparseTimestamp\u0001\u0000-(Ljava/lang/String;)Ljava/time/LocalDateTime;"
    },
    {
      "path": "target/classes/com/example/AdvancedUtils$TimeUtils.class",
      "line": 17,
      "col": 11,
      "snippet": "\u0000*\u0000,\u0007\u0000+\u0001\u0000\u0017java/time/ZonedDateTime",
      "context_before": "\u0000$\u0000&\u0007\u0000%\u0001\u0000\u0017java/time/LocalDateTime\n\u0000'\u0000(\u0001\u0000\u0006atZone\u0001\u0000-(Ljava/time/ZoneId;)Ljava/time/ZonedDateTime;",
      "context_after": "\u0000-\u0000.\u0001\u0000\u0006format\u0001\u00008(Ljava/time/format/DateTimeFormatter;)Ljava/lang/String;\u0001\u0000\ttimestamp\u0001\u0000\u0019Ljava/time/LocalDateTime;\u0001\u0000\u000eparseTimestamp\u0001\u0000-(Ljava/lang/String;)Ljava/time/LocalDateTime;\n\u0000$\u00004"
    },
    {
      "path": "target/classes/com/example/AdvancedUtils$TimeUtils.class",
      "line": 18,
      "col": 19,
      "snippet": "\u0000-\u0000.\u0001\u0000\u0006format\u0001\u00008(Ljava/time/format/DateTimeFormatter;)Ljava/lang/String;\u0001\u0000\ttimestamp\u0001\u0000\u0019Ljava/time/LocalDateTime;\u0001\u0000\u000eparseTimestamp\u0001\u0000-(Ljava/lang/String;)Ljava/time/LocalDateTime;",
      "context_before": "\u0000'\u0000(\u0001\u0000\u0006atZone\u0001\u0000-(Ljava/time/ZoneId;)Ljava/time/ZonedDateTime;\n\u0000*\u0000,\u0007\u0000+\u0001\u0000\u0017java/time/ZonedDateTime",
      "context_after": "\u0000$\u00004\n\u00005\u00006\u0001\u0000\u0005parse\u0001\u0000W(Ljava/lang/CharSequence;Ljava/time/format/DateTimeFormatter;)Ljava/time/LocalDateTime;\u0001\u0000\u0012Ljava/lang/String;\u0001\u0000\u0011calculateDuration\u0001\u00005(Ljava/time/LocalDateTime;Ljava/time/LocalDateTime;)J"
    },
    {
      "path": "target/classes/com/example/AdvancedUtils$TimeUtils.class",
      "line": 18,
      "col": 56,
      "snippet": "\u0000-\u0000.\u0001\u0000\u0006format\u0001\u00008(Ljava/time/format/DateTimeFormatter;)Ljava/lang/String;\u0001\u0000\ttimestamp\u0001\u0000\u0019Ljava/time/LocalDateTime;\u0001\u0000\u000eparseTimestamp\u0001\u0000-(Ljava/lang/String;)Ljava/time/LocalDateTime;",
      "context_before": "\u0000'\u0000(\u0001\u0000\u0006atZone\u0001\u0000-(Ljava/time/ZoneId;)Ljava/time/ZonedDateTime;\n\u0000*\u0000,\u0007\u0000+\u0001\u0000\u0017java/time/ZonedDateTime",
      "context_after": "\u0000$\u00004\n\u00005\u00006\u0001\u0000\u0005parse\u0001\u0000W(Ljava/lang/CharSequence;Ljava/time/format/DateTimeFormatter;)Ljava/time/LocalDateTime;\u0001\u0000\u0012Ljava/lang/String;\u0001\u0000\u0011calculateDuration\u0001\u00005(Ljava/time/LocalDateTime;Ljava/time/LocalDateTime;)J"
    },
    {
      "path": "target/classes/com/example/AdvancedUtils$TimeUtils.class",
      "line": 18,
      "col": 89,
      "snippet": "\u0000-\u0000.\u0001\u0000\u0006format\u0001\u00008(Ljava/time/format/DateTimeFormatter;)Ljava/lang/String;\u0001\u0000\ttimestamp\u0001\u0000\u0019Ljava/time/LocalDateTime;\u0001\u0000\u000eparseTimestamp\u0001\u0000-(Ljava/lang/String;)Ljava/time/LocalDateTime;",
      "context_before": "\u0000'\u0000(\u0001\u0000\u0006atZone\u0001\u0000-(Ljava/time/ZoneId;)Ljava/time/ZonedDateTime;\n\u0000*\u0000,\u0007\u0000+\u0001\u0000\u0017java/time/ZonedDateTime",
      "context_after": "\u0000$\u00004\n\u00005\u00006\u0001\u0000\u0005parse\u0001\u0000W(Ljava/lang/CharSequence;Ljava/time/format/DateTimeFormatter;)Ljava/time/LocalDateTime;\u0001\u0000\u0012Ljava/lang/String;\u0001\u0000\u0011calculateDuration\u0001\u00005(Ljava/time/LocalDateTime;Ljava/time/LocalDateTime;)J"
    },
    {
      "path": "target/classes/com/example/AdvancedUtils$TimeUtils.class",
      "line": 18,
      "col": 135,
      "snippet": "\u0000-\u0000.\u0001\u0000\u0006format\u0001\u00008(Ljava/time/format/DateTimeFormatter;)Ljava/lang/String;\u0001\u0000\ttimestamp\u0001\u0000\u0019Ljava/time/LocalDateTime;\u0001\u0000\u000eparseTimestamp\u0001\u0000-(Ljava/lang/String;)Ljava/time/LocalDateTime;",
      "context_before": "\u0000'\u0000(\u0001\u0000\u0006atZone\u0001\u0000-(Ljava/time/ZoneId;)Ljava/time/ZonedDateTime;\n\u0000*\u0000,\u0007\u0000+\u0001\u0000\u0017java/time/ZonedDateTime",
      "context_after": "\u0000$\u00004\n\u00005\u00006\u0001\u0000\u0005parse\u0001\u0000W(Ljava/lang/CharSequence;Ljava/time/format/DateTimeFormatter;)Ljava/time/LocalDateTime;\u0001\u0000\u0012Ljava/lang/String;\u0001\u0000\u0011calculateDuration\u0001\u00005(Ljava/time/LocalDateTime;Ljava/time/LocalDateTime;)J"
    },
    {
      "path": "target/classes/com/example/AdvancedUtils$TimeUtils.class",
      "line": 18,
      "col": 154,
      "snippet": "\u0000-\u0000.\u0001\u0000\u0006format\u0001\u00008(Ljava/time/format/DateTimeFormatter;)Ljava/lang/String;\u0001\u0000\ttimestamp\u0001\u0000\u0019Ljava/time/LocalDateTime;\u0001\u0000\u000eparseTimestamp\u0001\u0000-(Ljava/lang/String;)Ljava/time/LocalDateTime;",
      "context_before": "\u0000'\u0000(\u0001\u0000\u0006atZone\u0001\u0000-(Ljava/time/ZoneId;)Ljava/time/ZonedDateTime;\n\u0000*\u0000,\u0007\u0000+\u0001\u0000\u0017java/time/ZonedDateTime",
      "context_after": "\u0000$\u00004\n\u00005\u00006\u0001\u0000\u0005parse\u0001\u0000W(Ljava/lang/CharSequence;Ljava/time/format/DateTimeFormatter;)Ljava/time/LocalDateTime;\u0001\u0000\u0012Ljava/lang/String;\u0001\u0000\u0011calculateDuration\u0001\u00005(Ljava/time/LocalDateTime;Ljava/time/LocalDateTime;)J"
    },
    {
      "path": "target/classes/com/example/AdvancedUtils$TimeUtils.class",
      "line": 20,
      "col": 18,
      "snippet": "\u00005\u00006\u0001\u0000\u0005parse\u0001\u0000W(Ljava/lang/CharSequence;Ljava/time/format/DateTimeFormatter;)Ljava/time/LocalDateTime;\u0001\u0000\u0012Ljava/lang/String;\u0001\u0000\u0011calculateDuration\u0001\u00005(Ljava/time/LocalDateTime;Ljava/time/LocalDateTime;)J",
      "context_before": "\u0000-\u0000.\u0001\u0000\u0006format\u0001\u00008(Ljava/time/format/DateTimeFormatter;)Ljava/lang/String;\u0001\u0000\ttimestamp\u0001\u0000\u0019Ljava/time/LocalDateTime;\u0001\u0000\u000eparseTimestamp\u0001\u0000-(Ljava/lang/String;)Ljava/time/LocalDateTime;\n\u0000$\u00004",
      "context_after": "\u0000;\u0000=\u0007\u0000<\u0001\u0000\u0012java/time/Duration\n\u0000>\u0000?\u0001\u0000\u0007between\u0001\u0000P(Ljava/time/temporal/Temporal;Ljava/time/temporal/Temporal;)Ljava/time/Duration;"
    },
    {
      "path": "target/classes/com/example/AdvancedUtils$TimeUtils.class",
      "line": 20,
      "col": 42,
      "snippet": "\u00005\u00006\u0001\u0000\u0005parse\u0001\u0000W(Ljava/lang/CharSequence;Ljava/time/format/DateTimeFormatter;)Ljava/time/LocalDateTime;\u0001\u0000\u0012Ljava/lang/String;\u0001\u0000\u0011calculateDuration\u0001\u00005(Ljava/time/LocalDateTime;Ljava/time/LocalDateTime;)J",
      "context_before": "\u0000-\u0000.\u0001\u0000\u0006format\u0001\u00008(Ljava/time/format/DateTimeFormatter;)Ljava/lang/String;\u0001\u0000\ttimestamp\u0001\u0000\u0019Ljava/time/LocalDateTime;\u0001\u0000\u000eparseTimestamp\u0001\u0000-(Ljava/lang/String;)Ljava/time/LocalDateTime;\n\u0000$\u00004",
      "context_after": "\u0000;\u0000=\u0007\u0000<\u0001\u0000\u0012java/time/Duration\n\u0000>\u0000?\u0001\u0000\u0007between\u0001\u0000P(Ljava/time/temporal/Temporal;Ljava/time/temporal/Temporal;)Ljava/time/Duration;"
    },
    {
      "path": "target/classes/com/example/AdvancedUtils$TimeUtils.class",
      "line": 20,
      "col": 79,
      "snippet": "\u00005\u00006\u0001\u0000\u0005parse\u0001\u0000W(Ljava/lang/CharSequence;Ljava/time/format/DateTimeFormatter;)Ljava/time/LocalDateTime;\u0001\u0000\u0012Ljava/lang/String;\u0001\u0000\u0011calculateDuration\u0001\u00005(Ljava/time/LocalDateTime;Ljava/time/LocalDateTime;)J",
      "context_before": "\u0000-\u0000.\u0001\u0000\u0006format\u0001\u00008(Ljava/time/format/DateTimeFormatter;)Ljava/lang/String;\u0001\u0000\ttimestamp\u0001\u0000\u0019Ljava/time/LocalDateTime;\u0001\u0000\u000eparseTimestamp\u0001\u0000-(Ljava/lang/String;)Ljava/time/LocalDateTime;\n\u0000$\u00004",
      "context_after": "\u0000;\u0000=\u0007\u0000<\u0001\u0000\u0012java/time/Duration\n\u0000>\u0000?\u0001\u0000\u0007between\u0001\u0000P(Ljava/time/temporal/Temporal;Ljava/time/temporal/Temporal;)Ljava/time/Duration;"
    },
    {
      "path": "target/classes/com/example/AdvancedUtils$TimeUtils.class",
      "line": 20,
      "col": 107,
      "snippet": "\u00005\u00006\u0001\u0000\u0005parse\u0001\u0000W(Ljava/lang/CharSequence;Ljava/time/format/DateTimeFormatter;)Ljava/time/LocalDateTime;\u0001\u0000\u0012Ljava/lang/String;\u0001\u0000\u0011calculateDuration\u0001\u00005(Ljava/time/LocalDateTime;Ljava/time/LocalDateTime;)J",
      "context_before": "\u0000-\u0000.\u0001\u0000\u0006format\u0001\u00008(Ljava/time/format/DateTimeFormatter;)Ljava/lang/String;\u0001\u0000\ttimestamp\u0001\u0000\u0019Ljava/time/LocalDateTime;\u0001\u0000\u000eparseTimestamp\u0001\u0000-(Ljava/lang/String;)Ljava/time/LocalDateTime;\n\u0000$\u00004",
      "context_after": "\u0000;\u0000=\u0007\u0000<\u0001\u0000\u0012java/time/Duration\n\u0000>\u0000?\u0001\u0000\u0007between\u0001\u0000P(Ljava/time/temporal/Temporal;Ljava/time/temporal/Temporal;)Ljava/time/Duration;"
    },
    {
      "path": "target/classes/com/example/AdvancedUtils$TimeUtils.class",
      "line": 20,
      "col": 149,
      "snippet": "\u00005\u00006\u0001\u0000\u0005parse\u0001\u0000W(Ljava/lang/CharSequence;Ljava/time/format/DateTimeFormatter;)Ljava/time/LocalDateTime;\u0001\u0000\u0012Ljava/lang/String;\u0001\u0000\u0011calculateDuration\u0001\u00005(Ljava/time/LocalDateTime;Ljava/time/LocalDateTime;)J",
      "context_before": "\u0000-\u0000.\u0001\u0000\u0006format\u0001\u00008(Ljava/time/format/DateTimeFormatter;)Ljava/lang/String;\u0001\u0000\ttimestamp\u0001\u0000\u0019Ljava/time/LocalDateTime;\u0001\u0000\u000eparseTimestamp\u0001\u0000-(Ljava/lang/String;)Ljava/time/LocalDateTime;\n\u0000$\u00004",
      "context_after": "\u0000;\u0000=\u0007\u0000<\u0001\u0000\u0012java/time/Duration\n\u0000>\u0000?\u0001\u0000\u0007between\u0001\u0000P(Ljava/time/temporal/Temporal;Ljava/time/temporal/Temporal;)Ljava/time/Duration;"
    },
    {
      "path": "target/classes/com/example/AdvancedUtils$TimeUtils.class",
      "line": 20,
      "col": 174,
      "snippet": "\u00005\u00006\u0001\u0000\u0005parse\u0001\u0000W(Ljava/lang/CharSequence;Ljava/time/format/DateTimeFormatter;)Ljava/time/LocalDateTime;\u0001\u0000\u0012Ljava/lang/String;\u0001\u0000\u0011calculateDuration\u0001\u00005(Ljava/time/LocalDateTime;Ljava/time/LocalDateTime;)J",
      "context_before": "\u0000-\u0000.\u0001\u0000\u0006format\u0001\u00008(Ljava/time/format/DateTimeFormatter;)Ljava/lang/String;\u0001\u0000\ttimestamp\u0001\u0000\u0019Ljava/time/LocalDateTime;\u0001\u0000\u000eparseTimestamp\u0001\u0000-(Ljava/lang/String;)Ljava/time/LocalDateTime;\n\u0000$\u00004",
      "context_after": "\u0000;\u0000=\u0007\u0000<\u0001\u0000\u0012java/time/Duration\n\u0000>\u0000?\u0001\u0000\u0007between\u0001\u0000P(Ljava/time/temporal/Temporal;Ljava/time/temporal/Temporal;)Ljava/time/Duration;"
    },
    {
      "path": "target/classes/com/example/AdvancedUtils$TimeUtils.class",
      "line": 21,
      "col": 11,
      "snippet": "\u0000;\u0000=\u0007\u0000<\u0001\u0000\u0012java/time/Duration",
      "context_before": "\u0000$\u00004\n\u00005\u00006\u0001\u0000\u0005parse\u0001\u0000W(Ljava/lang/CharSequence;Ljava/time/format/DateTimeFormatter;)Ljava/time/LocalDateTime;\u0001\u0000\u0012Ljava/lang/String;\u0001\u0000\u0011calculateDuration\u0001\u00005(Ljava/time/LocalDateTime;Ljava/time/LocalDateTime;)J",
      "context_after": "\u0000>\u0000?\u0001\u0000\u0007between\u0001\u0000P(Ljava/time/temporal/Temporal;Ljava/time/temporal/Temporal;)Ljava/time/Duration;\n\u0000;\u0000A"
    },
    {
      "path": "target/classes/com/example/AdvancedUtils$TimeUtils.class",
      "line": 22,
      "col": 20,
      "snippet": "\u0000>\u0000?\u0001\u0000\u0007between\u0001\u0000P(Ljava/time/temporal/Temporal;Ljava/time/temporal/Temporal;)Ljava/time/Duration;",
      "context_before": "\u00005\u00006\u0001\u0000\u0005parse\u0001\u0000W(Ljava/lang/CharSequence;Ljava/time/format/DateTimeFormatter;)Ljava/time/LocalDateTime;\u0001\u0000\u0012Ljava/lang/String;\u0001\u0000\u0011calculateDuration\u0001\u00005(Ljava/time/LocalDateTime;Ljava/time/LocalDateTime;)J\n\u0000;\u0000=\u0007\u0000<\u0001\u0000\u0012java/time/Duration",
      "context_after": "\u0000;\u0000A\n\u0000B\u0000C\u0001\u0000\btoMillis\u0001\u0000\u0003()J\u0001\u0000\u0005start\u0001\u0000\u0003end\u0001\u0000\u000eformatDuration\u0001\u0000\u0015(J)Ljava/lang/String;"
    },
    {
      "path": "target/classes/com/example/AdvancedUtils$TimeUtils.class",
      "line": 22,
      "col": 49,
      "snippet": "\u0000>\u0000?\u0001\u0000\u0007between\u0001\u0000P(Ljava/time/temporal/Temporal;Ljava/time/temporal/Temporal;)Ljava/time/Duration;",
      "context_before": "\u00005\u00006\u0001\u0000\u0005parse\u0001\u0000W(Ljava/lang/CharSequence;Ljava/time/format/DateTimeFormatter;)Ljava/time/LocalDateTime;\u0001\u0000\u0012Ljava/lang/String;\u0001\u0000\u0011calculateDuration\u0001\u00005(Ljava/time/LocalDateTime;Ljava/time/LocalDateTime;)J\n\u0000;\u0000=\u0007\u0000<\u0001\u0000\u0012java/time/Duration",
      "context_after": "\u0000;\u0000A\n\u0000B\u0000C\u0001\u0000\btoMillis\u0001\u0000\u0003()J\u0001\u0000\u0005start\u0001\u0000\u0003end\u0001\u0000\u000eformatDuration\u0001\u0000\u0015(J)Ljava/lang/String;"
    },
    {
      "path": "target/classes/com/example/AdvancedUtils$TimeUtils.class",
      "line": 22,
      "col": 79,
      "snippet": "\u0000>\u0000?\u0001\u0000\u0007between\u0001\u0000P(Ljava/time/temporal/Temporal;Ljava/time/temporal/Temporal;)Ljava/time/Duration;",
      "context_before": "\u00005\u00006\u0001\u0000\u0005parse\u0001\u0000W(Ljava/lang/CharSequence;Ljava/time/format/DateTimeFormatter;)Ljava/time/LocalDateTime;\u0001\u0000\u0012Ljava/lang/String;\u0001\u0000\u0011calculateDuration\u0001\u00005(Ljava/time/LocalDateTime;Ljava/time/LocalDateTime;)J\n\u0000;\u0000=\u0007\u0000<\u0001\u0000\u0012java/time/Duration",
      "context_after": "\u0000;\u0000A\n\u0000B\u0000C\u0001\u0000\btoMillis\u0001\u0000\u0003()J\u0001\u0000\u0005start\u0001\u0000\u0003end\u0001\u0000\u000eformatDuration\u0001\u0000\u0015(J)Ljava/lang/String;"
    },
    {
      "path": "target/classes/com/example/AdvancedUtils$TimeUtils.class",
      "line": 24,
      "col": 60,
      "snippet": "\u0000B\u0000C\u0001\u0000\btoMillis\u0001\u0000\u0003()J\u0001\u0000\u0005start\u0001\u0000\u0003end\u0001\u0000\u000eformatDuration\u0001\u0000\u0015(J)Ljava/lang/String;",
      "context_before": "\u0000>\u0000?\u0001\u0000\u0007between\u0001\u0000P(Ljava/time/temporal/Temporal;Ljava/time/temporal/Temporal;)Ljava/time/Duration;\n\u0000;\u0000A",
      "context_after": "\u0000;\u0000I\n\u0000J\u0000K\u0001\u0000\bofMillis\u0001\u0000\u0017(J)Ljava/time/Duration;"
    },
    {
      "path": "target/classes/com/example/AdvancedUtils$TimeUtils.class",
      "line": 26,
      "col": 23,
      "snippet": "\u0000J\u0000K\u0001\u0000\bofMillis\u0001\u0000\u0017(J)Ljava/time/Duration;",
      "context_before": "\u0000B\u0000C\u0001\u0000\btoMillis\u0001\u0000\u0003()J\u0001\u0000\u0005start\u0001\u0000\u0003end\u0001\u0000\u000eformatDuration\u0001\u0000\u0015(J)Ljava/lang/String;\n\u0000;\u0000I",
      "context_after": "\u0000;\u0000M\n\u0000N\u0000C\u0001\u0000\u0007toHours"
    },
    {
      "path": "target/classes/com/example/AdvancedUtils$TimeUtils.class",
      "line": 34,
      "col": 11,
      "snippet": "\u0000\\\u0000^\u0007\u0000]\u0001\u0000\u000ejava/lang/Long",
      "context_before": "\u0000V\u0000C\u0001\u0000\ngetSeconds\u0005\u0000\u0000\u0000\u0000\u0000\u0000\u0003\b\u0000Z\u0001\u0000\u0013%02d:%02d:%02d.%03d",
      "context_after": "\u0000_\u0000`\u0001\u0000\u0007valueOf\u0001\u0000\u0013(J)Ljava/lang/Long;\n\u0000b\u0000d\u0007\u0000c\u0001\u0000\u0010java/lang/String"
    },
    {
      "path": "target/classes/com/example/AdvancedUtils$TimeUtils.class",
      "line": 35,
      "col": 22,
      "snippet": "\u0000_\u0000`\u0001\u0000\u0007valueOf\u0001\u0000\u0013(J)Ljava/lang/Long;",
      "context_before": "getSeconds\u0005\u0000\u0000\u0000\u0000\u0000\u0000\u0003\b\u0000Z\u0001\u0000\u0013%02d:%02d:%02d.%03d\n\u0000\\\u0000^\u0007\u0000]\u0001\u0000\u000ejava/lang/Long",
      "context_after": "\u0000b\u0000d\u0007\u0000c\u0001\u0000\u0010java/lang/String\n\u0000-\u0000e\u0001\u00009(Ljava/lang/String;[Ljava/lang/Object;)Ljava/lang/String;\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/AdvancedUtils$TimeUtils.class",
      "line": 36,
      "col": 11,
      "snippet": "\u0000b\u0000d\u0007\u0000c\u0001\u0000\u0010java/lang/String",
      "context_before": "\u0000\\\u0000^\u0007\u0000]\u0001\u0000\u000ejava/lang/Long\n\u0000_\u0000`\u0001\u0000\u0007valueOf\u0001\u0000\u0013(J)Ljava/lang/Long;",
      "context_after": "\u0000-\u0000e\u0001\u00009(Ljava/lang/String;[Ljava/lang/Object;)Ljava/lang/String;\u0001\u0000\nmilliseconds\u0001\u0000\u0001J\u0001\u0000\bduration\u0001\u0000\u0014Ljava/time/Duration;\u0001\u0000\u0005hours\u0001\u0000\u0007minutes\u0001\u0000\u0007seconds\u0001\u0000\u0006millis\u0001\u0000\u000egetBusinessDay\u0001\u00005(Ljava/time/LocalDateTime;I)Ljava/time/LocalDateTime;"
    },
    {
      "path": "target/classes/com/example/AdvancedUtils$TimeUtils.class",
      "line": 37,
      "col": 10,
      "snippet": "\u0000-\u0000e\u0001\u00009(Ljava/lang/String;[Ljava/lang/Object;)Ljava/lang/String;\u0001\u0000",
      "context_before": "\u0000_\u0000`\u0001\u0000\u0007valueOf\u0001\u0000\u0013(J)Ljava/lang/Long;\n\u0000b\u0000d\u0007\u0000c\u0001\u0000\u0010java/lang/String",
      "context_after": "milliseconds\u0001\u0000\u0001J\u0001\u0000\bduration\u0001\u0000\u0014Ljava/time/Duration;\u0001\u0000\u0005hours\u0001\u0000\u0007minutes\u0001\u0000\u0007seconds\u0001\u0000\u0006millis\u0001\u0000\u000egetBusinessDay\u0001\u00005(Ljava/time/LocalDateTime;I)Ljava/time/LocalDateTime;\n\u0000q\u0000s\u0007\u0000r\u0001\u0000\u000ejava/lang/Math"
    },
    {
      "path": "target/classes/com/example/AdvancedUtils$TimeUtils.class",
      "line": 37,
      "col": 29,
      "snippet": "\u0000-\u0000e\u0001\u00009(Ljava/lang/String;[Ljava/lang/Object;)Ljava/lang/String;\u0001\u0000",
      "context_before": "\u0000_\u0000`\u0001\u0000\u0007valueOf\u0001\u0000\u0013(J)Ljava/lang/Long;\n\u0000b\u0000d\u0007\u0000c\u0001\u0000\u0010java/lang/String",
      "context_after": "milliseconds\u0001\u0000\u0001J\u0001\u0000\bduration\u0001\u0000\u0014Ljava/time/Duration;\u0001\u0000\u0005hours\u0001\u0000\u0007minutes\u0001\u0000\u0007seconds\u0001\u0000\u0006millis\u0001\u0000\u000egetBusinessDay\u0001\u00005(Ljava/time/LocalDateTime;I)Ljava/time/LocalDateTime;\n\u0000q\u0000s\u0007\u0000r\u0001\u0000\u000ejava/lang/Math"
    },
    {
      "path": "target/classes/com/example/AdvancedUtils$TimeUtils.class",
      "line": 37,
      "col": 48,
      "snippet": "\u0000-\u0000e\u0001\u00009(Ljava/lang/String;[Ljava/lang/Object;)Ljava/lang/String;\u0001\u0000",
      "context_before": "\u0000_\u0000`\u0001\u0000\u0007valueOf\u0001\u0000\u0013(J)Ljava/lang/Long;\n\u0000b\u0000d\u0007\u0000c\u0001\u0000\u0010java/lang/String",
      "context_after": "milliseconds\u0001\u0000\u0001J\u0001\u0000\bduration\u0001\u0000\u0014Ljava/time/Duration;\u0001\u0000\u0005hours\u0001\u0000\u0007minutes\u0001\u0000\u0007seconds\u0001\u0000\u0006millis\u0001\u0000\u000egetBusinessDay\u0001\u00005(Ljava/time/LocalDateTime;I)Ljava/time/LocalDateTime;\n\u0000q\u0000s\u0007\u0000r\u0001\u0000\u000ejava/lang/Math"
    },
    {
      "path": "target/classes/com/example/AdvancedUtils$TimeUtils.class",
      "line": 38,
      "col": 32,
      "snippet": "milliseconds\u0001\u0000\u0001J\u0001\u0000\bduration\u0001\u0000\u0014Ljava/time/Duration;\u0001\u0000\u0005hours\u0001\u0000\u0007minutes\u0001\u0000\u0007seconds\u0001\u0000\u0006millis\u0001\u0000\u000egetBusinessDay\u0001\u00005(Ljava/time/LocalDateTime;I)Ljava/time/LocalDateTime;",
      "context_before": "\u0000b\u0000d\u0007\u0000c\u0001\u0000\u0010java/lang/String\n\u0000-\u0000e\u0001\u00009(Ljava/lang/String;[Ljava/lang/Object;)Ljava/lang/String;\u0001\u0000",
      "context_after": "\u0000q\u0000s\u0007\u0000r\u0001\u0000\u000ejava/lang/Math\n\u0000t\u0000u\u0001\u0000\u0003abs\u0001\u0000\u0004(I)I"
    },
    {
      "path": "target/classes/com/example/AdvancedUtils$TimeUtils.class",
      "line": 38,
      "col": 110,
      "snippet": "milliseconds\u0001\u0000\u0001J\u0001\u0000\bduration\u0001\u0000\u0014Ljava/time/Duration;\u0001\u0000\u0005hours\u0001\u0000\u0007minutes\u0001\u0000\u0007seconds\u0001\u0000\u0006millis\u0001\u0000\u000egetBusinessDay\u0001\u00005(Ljava/time/LocalDateTime;I)Ljava/time/LocalDateTime;",
      "context_before": "\u0000b\u0000d\u0007\u0000c\u0001\u0000\u0010java/lang/String\n\u0000-\u0000e\u0001\u00009(Ljava/lang/String;[Ljava/lang/Object;)Ljava/lang/String;\u0001\u0000",
      "context_after": "\u0000q\u0000s\u0007\u0000r\u0001\u0000\u000ejava/lang/Math\n\u0000t\u0000u\u0001\u0000\u0003abs\u0001\u0000\u0004(I)I"
    },
    {
      "path": "target/classes/com/example/AdvancedUtils$TimeUtils.class",
      "line": 38,
      "col": 137,
      "snippet": "milliseconds\u0001\u0000\u0001J\u0001\u0000\bduration\u0001\u0000\u0014Ljava/time/Duration;\u0001\u0000\u0005hours\u0001\u0000\u0007minutes\u0001\u0000\u0007seconds\u0001\u0000\u0006millis\u0001\u0000\u000egetBusinessDay\u0001\u00005(Ljava/time/LocalDateTime;I)Ljava/time/LocalDateTime;",
      "context_before": "\u0000b\u0000d\u0007\u0000c\u0001\u0000\u0010java/lang/String\n\u0000-\u0000e\u0001\u00009(Ljava/lang/String;[Ljava/lang/Object;)Ljava/lang/String;\u0001\u0000",
      "context_after": "\u0000q\u0000s\u0007\u0000r\u0001\u0000\u000ejava/lang/Math\n\u0000t\u0000u\u0001\u0000\u0003abs\u0001\u0000\u0004(I)I"
    },
    {
      "path": "target/classes/com/example/AdvancedUtils$TimeUtils.class",
      "line": 39,
      "col": 11,
      "snippet": "\u0000q\u0000s\u0007\u0000r\u0001\u0000\u000ejava/lang/Math",
      "context_before": "\u0000-\u0000e\u0001\u00009(Ljava/lang/String;[Ljava/lang/Object;)Ljava/lang/String;\u0001\u0000\nmilliseconds\u0001\u0000\u0001J\u0001\u0000\bduration\u0001\u0000\u0014Ljava/time/Duration;\u0001\u0000\u0005hours\u0001\u0000\u0007minutes\u0001\u0000\u0007seconds\u0001\u0000\u0006millis\u0001\u0000\u000egetBusinessDay\u0001\u00005(Ljava/time/LocalDateTime;I)Ljava/time/LocalDateTime;",
      "context_after": "\u0000t\u0000u\u0001\u0000\u0003abs\u0001\u0000\u0004(I)I\n\u0000$\u0000w"
    },
    {
      "path": "target/classes/com/example/AdvancedUtils$TimeUtils.class",
      "line": 43,
      "col": 5,
      "snippet": "(J)Ljava/time/LocalDateTime;",
      "context_before": "\u0000$\u0000w\n\u0000x\u0000y\u0001\u0000\bplusDays\u0001\u0000",
      "context_after": "\u0000$\u0000{\n\u0000|\u0000}\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/AdvancedUtils$TimeUtils.class",
      "line": 46,
      "col": 18,
      "snippet": "toLocalDate\u0001\u0000\u0017()Ljava/time/LocalDate;",
      "context_before": "\u0000$\u0000{\n\u0000|\u0000}\u0001\u0000",
      "context_after": "\u0000\u0001\u0000\n\u0000\u0000\u0001\u0000\tisWeekend\u0001\u0000\u0018(Ljava/time/LocalDate;)Z\u0001\u0000\bdateTime\u0001\u0000\u0006offset\u0001\u0000\u0001I\u0001\u0000\u0006result\u0001\u0000\u0004days\u0001\u0000\tdirection\u0001\u0000\u0001i\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/AdvancedUtils$TimeUtils.class",
      "line": 48,
      "col": 20,
      "snippet": "\u0000\u0000\u0001\u0000\tisWeekend\u0001\u0000\u0018(Ljava/time/LocalDate;)Z\u0001\u0000\bdateTime\u0001\u0000\u0006offset\u0001\u0000\u0001I\u0001\u0000\u0006result\u0001\u0000\u0004days\u0001\u0000\tdirection\u0001\u0000\u0001i\u0001\u0000",
      "context_before": "toLocalDate\u0001\u0000\u0017()Ljava/time/LocalDate;\n\u0000\u0001\u0000",
      "context_after": "StackMapTable\n\u0000\u0000\u0007\u0000\u0001\u0000\u0013java/time/LocalDate"
    },
    {
      "path": "target/classes/com/example/AdvancedUtils$TimeUtils.class",
      "line": 50,
      "col": 8,
      "snippet": "\u0000\u0000\u0007\u0000\u0001\u0000\u0013java/time/LocalDate",
      "context_before": "\u0000\u0000\u0001\u0000\tisWeekend\u0001\u0000\u0018(Ljava/time/LocalDate;)Z\u0001\u0000\bdateTime\u0001\u0000\u0006offset\u0001\u0000\u0001I\u0001\u0000\u0006result\u0001\u0000\u0004days\u0001\u0000\tdirection\u0001\u0000\u0001i\u0001\u0000\nStackMapTable",
      "context_after": "\u0000\u0000\u0001\u0000\ngetDayOfWeek\u0001\u0000\u0017()Ljava/time/DayOfWeek;\t\u0000\u0000\u0007\u0000\u0001\u0000\u0013java/time/DayOfWeek"
    },
    {
      "path": "target/classes/com/example/AdvancedUtils$TimeUtils.class",
      "line": 52,
      "col": 19,
      "snippet": "getDayOfWeek\u0001\u0000\u0017()Ljava/time/DayOfWeek;\t\u0000\u0000\u0007\u0000\u0001\u0000\u0013java/time/DayOfWeek",
      "context_before": "\u0000\u0000\u0007\u0000\u0001\u0000\u0013java/time/LocalDate\n\u0000\u0000\u0001\u0000",
      "context_after": "\u0000\u0000\u0001\u0000\bSATURDAY\u0001\u0000\u0015Ljava/time/DayOfWeek;\t\u0000\u0000\n\u0000\u0000\u0001\u0000\u0006SUNDAY\u0001\u0000\u0004date\u0001\u0000\u0015Ljava/time/LocalDate;\u0001\u0000\u0003day\u0001\u0000\u000fgetBusinessDays\u0001\u0000<(Ljava/time/LocalDate;Ljava/time/LocalDate;)Ljava/util/List;\u0001\u0000\tSignature\u0001\u0000S(Ljava/time/LocalDate;Ljava/time/LocalDate;)Ljava/util/List<Ljava/time/LocalDate;>;\u0007\u0000\u0001\u0000\u0013java/util/ArrayList"
    },
    {
      "path": "target/classes/com/example/AdvancedUtils$TimeUtils.class",
      "line": 52,
      "col": 47,
      "snippet": "getDayOfWeek\u0001\u0000\u0017()Ljava/time/DayOfWeek;\t\u0000\u0000\u0007\u0000\u0001\u0000\u0013java/time/DayOfWeek",
      "context_before": "\u0000\u0000\u0007\u0000\u0001\u0000\u0013java/time/LocalDate\n\u0000\u0000\u0001\u0000",
      "context_after": "\u0000\u0000\u0001\u0000\bSATURDAY\u0001\u0000\u0015Ljava/time/DayOfWeek;\t\u0000\u0000\n\u0000\u0000\u0001\u0000\u0006SUNDAY\u0001\u0000\u0004date\u0001\u0000\u0015Ljava/time/LocalDate;\u0001\u0000\u0003day\u0001\u0000\u000fgetBusinessDays\u0001\u0000<(Ljava/time/LocalDate;Ljava/time/LocalDate;)Ljava/util/List;\u0001\u0000\tSignature\u0001\u0000S(Ljava/time/LocalDate;Ljava/time/LocalDate;)Ljava/util/List<Ljava/time/LocalDate;>;\u0007\u0000\u0001\u0000\u0013java/util/ArrayList"
    },
    {
      "path": "target/classes/com/example/AdvancedUtils$TimeUtils.class",
      "line": 53,
      "col": 18,
      "snippet": "\u0000\u0000\u0001\u0000\bSATURDAY\u0001\u0000\u0015Ljava/time/DayOfWeek;\t\u0000\u0000",
      "context_before": "\u0000\u0000\u0001\u0000\ngetDayOfWeek\u0001\u0000\u0017()Ljava/time/DayOfWeek;\t\u0000\u0000\u0007\u0000\u0001\u0000\u0013java/time/DayOfWeek",
      "context_after": "\u0000\u0000\u0001\u0000\u0006SUNDAY\u0001\u0000\u0004date\u0001\u0000\u0015Ljava/time/LocalDate;\u0001\u0000\u0003day\u0001\u0000\u000fgetBusinessDays\u0001\u0000<(Ljava/time/LocalDate;Ljava/time/LocalDate;)Ljava/util/List;\u0001\u0000\tSignature\u0001\u0000S(Ljava/time/LocalDate;Ljava/time/LocalDate;)Ljava/util/List<Ljava/time/LocalDate;>;\u0007\u0000\u0001\u0000\u0013java/util/ArrayList\n\u0000\u0000\u0018"
    },
    {
      "path": "target/classes/com/example/AdvancedUtils$TimeUtils.class",
      "line": 54,
      "col": 23,
      "snippet": "\u0000\u0000\u0001\u0000\u0006SUNDAY\u0001\u0000\u0004date\u0001\u0000\u0015Ljava/time/LocalDate;\u0001\u0000\u0003day\u0001\u0000\u000fgetBusinessDays\u0001\u0000<(Ljava/time/LocalDate;Ljava/time/LocalDate;)Ljava/util/List;\u0001\u0000\tSignature\u0001\u0000S(Ljava/time/LocalDate;Ljava/time/LocalDate;)Ljava/util/List<Ljava/time/LocalDate;>;\u0007\u0000\u0001\u0000\u0013java/util/ArrayList",
      "context_before": "getDayOfWeek\u0001\u0000\u0017()Ljava/time/DayOfWeek;\t\u0000\u0000\u0007\u0000\u0001\u0000\u0013java/time/DayOfWeek\n\u0000\u0000\u0001\u0000\bSATURDAY\u0001\u0000\u0015Ljava/time/DayOfWeek;\t\u0000\u0000",
      "context_after": "\u0000\u0000\u0018\n\u0000\u0000\u0007\u0000\u0001\u0000\u000ejava/util/List"
    },
    {
      "path": "target/classes/com/example/AdvancedUtils$TimeUtils.class",
      "line": 54,
      "col": 72,
      "snippet": "\u0000\u0000\u0001\u0000\u0006SUNDAY\u0001\u0000\u0004date\u0001\u0000\u0015Ljava/time/LocalDate;\u0001\u0000\u0003day\u0001\u0000\u000fgetBusinessDays\u0001\u0000<(Ljava/time/LocalDate;Ljava/time/LocalDate;)Ljava/util/List;\u0001\u0000\tSignature\u0001\u0000S(Ljava/time/LocalDate;Ljava/time/LocalDate;)Ljava/util/List<Ljava/time/LocalDate;>;\u0007\u0000\u0001\u0000\u0013java/util/ArrayList",
      "context_before": "getDayOfWeek\u0001\u0000\u0017()Ljava/time/DayOfWeek;\t\u0000\u0000\u0007\u0000\u0001\u0000\u0013java/time/DayOfWeek\n\u0000\u0000\u0001\u0000\bSATURDAY\u0001\u0000\u0015Ljava/time/DayOfWeek;\t\u0000\u0000",
      "context_after": "\u0000\u0000\u0018\n\u0000\u0000\u0007\u0000\u0001\u0000\u000ejava/util/List"
    },
    {
      "path": "target/classes/com/example/AdvancedUtils$TimeUtils.class",
      "line": 54,
      "col": 93,
      "snippet": "\u0000\u0000\u0001\u0000\u0006SUNDAY\u0001\u0000\u0004date\u0001\u0000\u0015Ljava/time/LocalDate;\u0001\u0000\u0003day\u0001\u0000\u000fgetBusinessDays\u0001\u0000<(Ljava/time/LocalDate;Ljava/time/LocalDate;)Ljava/util/List;\u0001\u0000\tSignature\u0001\u0000S(Ljava/time/LocalDate;Ljava/time/LocalDate;)Ljava/util/List<Ljava/time/LocalDate;>;\u0007\u0000\u0001\u0000\u0013java/util/ArrayList",
      "context_before": "getDayOfWeek\u0001\u0000\u0017()Ljava/time/DayOfWeek;\t\u0000\u0000\u0007\u0000\u0001\u0000\u0013java/time/DayOfWeek\n\u0000\u0000\u0001\u0000\bSATURDAY\u0001\u0000\u0015Ljava/time/DayOfWeek;\t\u0000\u0000",
      "context_after": "\u0000\u0000\u0018\n\u0000\u0000\u0007\u0000\u0001\u0000\u000ejava/util/List"
    },
    {
      "path": "target/classes/com/example/AdvancedUtils$TimeUtils.class",
      "line": 54,
      "col": 115,
      "snippet": "\u0000\u0000\u0001\u0000\u0006SUNDAY\u0001\u0000\u0004date\u0001\u0000\u0015Ljava/time/LocalDate;\u0001\u0000\u0003day\u0001\u0000\u000fgetBusinessDays\u0001\u0000<(Ljava/time/LocalDate;Ljava/time/LocalDate;)Ljava/util/List;\u0001\u0000\tSignature\u0001\u0000S(Ljava/time/LocalDate;Ljava/time/LocalDate;)Ljava/util/List<Ljava/time/LocalDate;>;\u0007\u0000\u0001\u0000\u0013java/util/ArrayList",
      "context_before": "getDayOfWeek\u0001\u0000\u0017()Ljava/time/DayOfWeek;\t\u0000\u0000\u0007\u0000\u0001\u0000\u0013java/time/DayOfWeek\n\u0000\u0000\u0001\u0000\bSATURDAY\u0001\u0000\u0015Ljava/time/DayOfWeek;\t\u0000\u0000",
      "context_after": "\u0000\u0000\u0018\n\u0000\u0000\u0007\u0000\u0001\u0000\u000ejava/util/List"
    },
    {
      "path": "target/classes/com/example/AdvancedUtils$TimeUtils.class",
      "line": 54,
      "col": 147,
      "snippet": "\u0000\u0000\u0001\u0000\u0006SUNDAY\u0001\u0000\u0004date\u0001\u0000\u0015Ljava/time/LocalDate;\u0001\u0000\u0003day\u0001\u0000\u000fgetBusinessDays\u0001\u0000<(Ljava/time/LocalDate;Ljava/time/LocalDate;)Ljava/util/List;\u0001\u0000\tSignature\u0001\u0000S(Ljava/time/LocalDate;Ljava/time/LocalDate;)Ljava/util/List<Ljava/time/LocalDate;>;\u0007\u0000\u0001\u0000\u0013java/util/ArrayList",
      "context_before": "getDayOfWeek\u0001\u0000\u0017()Ljava/time/DayOfWeek;\t\u0000\u0000\u0007\u0000\u0001\u0000\u0013java/time/DayOfWeek\n\u0000\u0000\u0001\u0000\bSATURDAY\u0001\u0000\u0015Ljava/time/DayOfWeek;\t\u0000\u0000",
      "context_after": "\u0000\u0000\u0018\n\u0000\u0000\u0007\u0000\u0001\u0000\u000ejava/util/List"
    },
    {
      "path": "target/classes/com/example/AdvancedUtils$TimeUtils.class",
      "line": 54,
      "col": 168,
      "snippet": "\u0000\u0000\u0001\u0000\u0006SUNDAY\u0001\u0000\u0004date\u0001\u0000\u0015Ljava/time/LocalDate;\u0001\u0000\u0003day\u0001\u0000\u000fgetBusinessDays\u0001\u0000<(Ljava/time/LocalDate;Ljava/time/LocalDate;)Ljava/util/List;\u0001\u0000\tSignature\u0001\u0000S(Ljava/time/LocalDate;Ljava/time/LocalDate;)Ljava/util/List<Ljava/time/LocalDate;>;\u0007\u0000\u0001\u0000\u0013java/util/ArrayList",
      "context_before": "getDayOfWeek\u0001\u0000\u0017()Ljava/time/DayOfWeek;\t\u0000\u0000\u0007\u0000\u0001\u0000\u0013java/time/DayOfWeek\n\u0000\u0000\u0001\u0000\bSATURDAY\u0001\u0000\u0015Ljava/time/DayOfWeek;\t\u0000\u0000",
      "context_after": "\u0000\u0000\u0018\n\u0000\u0000\u0007\u0000\u0001\u0000\u000ejava/util/List"
    },
    {
      "path": "target/classes/com/example/AdvancedUtils$TimeUtils.class",
      "line": 54,
      "col": 190,
      "snippet": "\u0000\u0000\u0001\u0000\u0006SUNDAY\u0001\u0000\u0004date\u0001\u0000\u0015Ljava/time/LocalDate;\u0001\u0000\u0003day\u0001\u0000\u000fgetBusinessDays\u0001\u0000<(Ljava/time/LocalDate;Ljava/time/LocalDate;)Ljava/util/List;\u0001\u0000\tSignature\u0001\u0000S(Ljava/time/LocalDate;Ljava/time/LocalDate;)Ljava/util/List<Ljava/time/LocalDate;>;\u0007\u0000\u0001\u0000\u0013java/util/ArrayList",
      "context_before": "getDayOfWeek\u0001\u0000\u0017()Ljava/time/DayOfWeek;\t\u0000\u0000\u0007\u0000\u0001\u0000\u0013java/time/DayOfWeek\n\u0000\u0000\u0001\u0000\bSATURDAY\u0001\u0000\u0015Ljava/time/DayOfWeek;\t\u0000\u0000",
      "context_after": "\u0000\u0000\u0018\n\u0000\u0000\u0007\u0000\u0001\u0000\u000ejava/util/List"
    },
    {
      "path": "target/classes/com/example/AdvancedUtils$TimeUtils.class",
      "line": 54,
      "col": 206,
      "snippet": "\u0000\u0000\u0001\u0000\u0006SUNDAY\u0001\u0000\u0004date\u0001\u0000\u0015Ljava/time/LocalDate;\u0001\u0000\u0003day\u0001\u0000\u000fgetBusinessDays\u0001\u0000<(Ljava/time/LocalDate;Ljava/time/LocalDate;)Ljava/util/List;\u0001\u0000\tSignature\u0001\u0000S(Ljava/time/LocalDate;Ljava/time/LocalDate;)Ljava/util/List<Ljava/time/LocalDate;>;\u0007\u0000\u0001\u0000\u0013java/util/ArrayList",
      "context_before": "getDayOfWeek\u0001\u0000\u0017()Ljava/time/DayOfWeek;\t\u0000\u0000\u0007\u0000\u0001\u0000\u0013java/time/DayOfWeek\n\u0000\u0000\u0001\u0000\bSATURDAY\u0001\u0000\u0015Ljava/time/DayOfWeek;\t\u0000\u0000",
      "context_after": "\u0000\u0000\u0018\n\u0000\u0000\u0007\u0000\u0001\u0000\u000ejava/util/List"
    },
    {
      "path": "target/classes/com/example/AdvancedUtils$TimeUtils.class",
      "line": 54,
      "col": 233,
      "snippet": "\u0000\u0000\u0001\u0000\u0006SUNDAY\u0001\u0000\u0004date\u0001\u0000\u0015Ljava/time/LocalDate;\u0001\u0000\u0003day\u0001\u0000\u000fgetBusinessDays\u0001\u0000<(Ljava/time/LocalDate;Ljava/time/LocalDate;)Ljava/util/List;\u0001\u0000\tSignature\u0001\u0000S(Ljava/time/LocalDate;Ljava/time/LocalDate;)Ljava/util/List<Ljava/time/LocalDate;>;\u0007\u0000\u0001\u0000\u0013java/util/ArrayList",
      "context_before": "getDayOfWeek\u0001\u0000\u0017()Ljava/time/DayOfWeek;\t\u0000\u0000\u0007\u0000\u0001\u0000\u0013java/time/DayOfWeek\n\u0000\u0000\u0001\u0000\bSATURDAY\u0001\u0000\u0015Ljava/time/DayOfWeek;\t\u0000\u0000",
      "context_after": "\u0000\u0000\u0018\n\u0000\u0000\u0007\u0000\u0001\u0000\u000ejava/util/List"
    },
    {
      "path": "target/classes/com/example/AdvancedUtils$TimeUtils.class",
      "line": 56,
      "col": 8,
      "snippet": "\u0000\u0000\u0007\u0000\u0001\u0000\u000ejava/util/List",
      "context_before": "\u0000\u0000\u0001\u0000\u0006SUNDAY\u0001\u0000\u0004date\u0001\u0000\u0015Ljava/time/LocalDate;\u0001\u0000\u0003day\u0001\u0000\u000fgetBusinessDays\u0001\u0000<(Ljava/time/LocalDate;Ljava/time/LocalDate;)Ljava/util/List;\u0001\u0000\tSignature\u0001\u0000S(Ljava/time/LocalDate;Ljava/time/LocalDate;)Ljava/util/List<Ljava/time/LocalDate;>;\u0007\u0000\u0001\u0000\u0013java/util/ArrayList\n\u0000\u0000\u0018",
      "context_after": "\u0000\u0000\u0001\u0000\u0003add\u0001\u0000\u0015(Ljava/lang/Object;)Z\n\u0000\u0000"
    },
    {
      "path": "target/classes/com/example/AdvancedUtils$TimeUtils.class",
      "line": 57,
      "col": 14,
      "snippet": "\u0000\u0000\u0001\u0000\u0003add\u0001\u0000\u0015(Ljava/lang/Object;)Z",
      "context_before": "\u0000\u0000\u0018\n\u0000\u0000\u0007\u0000\u0001\u0000\u000ejava/util/List",
      "context_after": "\u0000\u0000\n\u0000x\u0000\u0001\u0000\u0018(J)Ljava/time/LocalDate;"
    },
    {
      "path": "target/classes/com/example/AdvancedUtils$TimeUtils.class",
      "line": 59,
      "col": 11,
      "snippet": "\u0000x\u0000\u0001\u0000\u0018(J)Ljava/time/LocalDate;",
      "context_before": "\u0000\u0000\u0001\u0000\u0003add\u0001\u0000\u0015(Ljava/lang/Object;)Z\n\u0000\u0000",
      "context_after": "\u0000\u0000\n\u0000\u0000\u0001\u0000\u0007isAfter\u0001\u0000%(Ljava/time/chrono/ChronoLocalDate;)Z\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/AdvancedUtils$TimeUtils.class",
      "line": 61,
      "col": 18,
      "snippet": "\u0000\u0000\u0001\u0000\u0007isAfter\u0001\u0000%(Ljava/time/chrono/ChronoLocalDate;)Z\u0001\u0000",
      "context_before": "\u0000x\u0000\u0001\u0000\u0018(J)Ljava/time/LocalDate;\n\u0000\u0000",
      "context_after": "businessDays\u0001\u0000\u0010Ljava/util/List;\u0001\u0000\u0007current\u0001\u0000\u0016LocalVariableTypeTable\u0001\u0000'Ljava/util/List<Ljava/time/LocalDate;>;\u0001\u0000\nSourceFile\u0001\u0000\u0012AdvancedUtils.java\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/AdvancedUtils$TimeUtils.class",
      "line": 62,
      "col": 17,
      "snippet": "businessDays\u0001\u0000\u0010Ljava/util/List;\u0001\u0000\u0007current\u0001\u0000\u0016LocalVariableTypeTable\u0001\u0000'Ljava/util/List<Ljava/time/LocalDate;>;\u0001\u0000",
      "context_before": "\u0000\u0000\n\u0000\u0000\u0001\u0000\u0007isAfter\u0001\u0000%(Ljava/time/chrono/ChronoLocalDate;)Z\u0001\u0000",
      "context_after": "SourceFile\u0001\u0000\u0012AdvancedUtils.java\u0001\u0000\nInnerClasses\u0007\u0000\u0001\u0000\u0019com/example/AdvancedUtils\u0001\u0000\tTimeUtils\u0001\u0000\bNestHost\u0000!\u0000\u0001\u0000\u0003\u0000\u0000\u0000\u0001\u0000\u001a\u0000\u0005\u0000\u0006\u0000\u0000\u0000\t\u0000\b\u0000\u0007\u0000\b\u0000\u0001\u0000\t\u0000\u0000\u00001\u0000\u0001\u0000\u0000\u0000\u0000\u0000\t\u0012"
    },
    {
      "path": "target/classes/com/example/AdvancedUtils$TimeUtils.class",
      "line": 62,
      "col": 71,
      "snippet": "businessDays\u0001\u0000\u0010Ljava/util/List;\u0001\u0000\u0007current\u0001\u0000\u0016LocalVariableTypeTable\u0001\u0000'Ljava/util/List<Ljava/time/LocalDate;>;\u0001\u0000",
      "context_before": "\u0000\u0000\n\u0000\u0000\u0001\u0000\u0007isAfter\u0001\u0000%(Ljava/time/chrono/ChronoLocalDate;)Z\u0001\u0000",
      "context_after": "SourceFile\u0001\u0000\u0012AdvancedUtils.java\u0001\u0000\nInnerClasses\u0007\u0000\u0001\u0000\u0019com/example/AdvancedUtils\u0001\u0000\tTimeUtils\u0001\u0000\bNestHost\u0000!\u0000\u0001\u0000\u0003\u0000\u0000\u0000\u0001\u0000\u001a\u0000\u0005\u0000\u0006\u0000\u0000\u0000\t\u0000\b\u0000\u0007\u0000\b\u0000\u0001\u0000\t\u0000\u0000\u00001\u0000\u0001\u0000\u0000\u0000\u0000\u0000\t\u0012"
    },
    {
      "path": "target/classes/com/example/AdvancedUtils$TimeUtils.class",
      "line": 62,
      "col": 87,
      "snippet": "businessDays\u0001\u0000\u0010Ljava/util/List;\u0001\u0000\u0007current\u0001\u0000\u0016LocalVariableTypeTable\u0001\u0000'Ljava/util/List<Ljava/time/LocalDate;>;\u0001\u0000",
      "context_before": "\u0000\u0000\n\u0000\u0000\u0001\u0000\u0007isAfter\u0001\u0000%(Ljava/time/chrono/ChronoLocalDate;)Z\u0001\u0000",
      "context_after": "SourceFile\u0001\u0000\u0012AdvancedUtils.java\u0001\u0000\nInnerClasses\u0007\u0000\u0001\u0000\u0019com/example/AdvancedUtils\u0001\u0000\tTimeUtils\u0001\u0000\bNestHost\u0000!\u0000\u0001\u0000\u0003\u0000\u0000\u0000\u0001\u0000\u001a\u0000\u0005\u0000\u0006\u0000\u0000\u0000\t\u0000\b\u0000\u0007\u0000\b\u0000\u0001\u0000\t\u0000\u0000\u00001\u0000\u0001\u0000\u0000\u0000\u0000\u0000\t\u0012"
    },
    {
      "path": "target/classes/com/example/AdvancedUtils$TimeUtils.class",
      "line": 63,
      "col": 28,
      "snippet": "SourceFile\u0001\u0000\u0012AdvancedUtils.java\u0001\u0000",
      "context_before": "\u0000\u0000\u0001\u0000\u0007isAfter\u0001\u0000%(Ljava/time/chrono/ChronoLocalDate;)Z\u0001\u0000\nbusinessDays\u0001\u0000\u0010Ljava/util/List;\u0001\u0000\u0007current\u0001\u0000\u0016LocalVariableTypeTable\u0001\u0000'Ljava/util/List<Ljava/time/LocalDate;>;\u0001\u0000",
      "context_after": "InnerClasses\u0007\u0000\u0001\u0000\u0019com/example/AdvancedUtils\u0001\u0000\tTimeUtils\u0001\u0000\bNestHost\u0000!\u0000\u0001\u0000\u0003\u0000\u0000\u0000\u0001\u0000\u001a\u0000\u0005\u0000\u0006\u0000\u0000\u0000\t\u0000\b\u0000\u0007\u0000\b\u0000\u0001\u0000\t\u0000\u0000\u00001\u0000\u0001\u0000\u0000\u0000\u0000\u0000\t\u0012\n\u0000"
    },
    {
      "path": "target/classes/com/example/DecoratorManager$LoggingDecorator.class",
      "line": 1,
      "col": 64,
      "snippet": "\u0000\u0000\u00007\u0000n\u0007\u0000\u0002\u0001\u0000-com/example/DecoratorManager$LoggingDecorator\u0007\u0000\u0004\u0001\u0000\u0010java/lang/Object\u0007\u0000\u0006\u0001\u0000&com/example/DecoratorManager$Decorator\u0001\u0000",
      "context_before": "",
      "context_after": "loggerName\u0001\u0000\u0012Ljava/lang/String;\u0001\u0000\u0006<init>\u0001\u0000\u0015(Ljava/lang/String;)V\u0001\u0000\u0004Code\n\u0000\u0003\u0000"
    },
    {
      "path": "target/classes/com/example/DecoratorManager$LoggingDecorator.class",
      "line": 2,
      "col": 15,
      "snippet": "loggerName\u0001\u0000\u0012Ljava/lang/String;\u0001\u0000\u0006<init>\u0001\u0000\u0015(Ljava/lang/String;)V\u0001\u0000\u0004Code",
      "context_before": "\u0000\u0000\u00007\u0000n\u0007\u0000\u0002\u0001\u0000-com/example/DecoratorManager$LoggingDecorator\u0007\u0000\u0004\u0001\u0000\u0010java/lang/Object\u0007\u0000\u0006\u0001\u0000&com/example/DecoratorManager$Decorator\u0001\u0000",
      "context_after": "\u0000\u0003\u0000\n"
    },
    {
      "path": "target/classes/com/example/DecoratorManager$LoggingDecorator.class",
      "line": 2,
      "col": 46,
      "snippet": "loggerName\u0001\u0000\u0012Ljava/lang/String;\u0001\u0000\u0006<init>\u0001\u0000\u0015(Ljava/lang/String;)V\u0001\u0000\u0004Code",
      "context_before": "\u0000\u0000\u00007\u0000n\u0007\u0000\u0002\u0001\u0000-com/example/DecoratorManager$LoggingDecorator\u0007\u0000\u0004\u0001\u0000\u0010java/lang/Object\u0007\u0000\u0006\u0001\u0000&com/example/DecoratorManager$Decorator\u0001\u0000",
      "context_after": "\u0000\u0003\u0000\n"
    },
    {
      "path": "target/classes/com/example/DecoratorManager$LoggingDecorator.class",
      "line": 6,
      "col": 197,
      "snippet": "\u0000\u0007\u0000\b\u0001\u0000\u000fLineNumberTable\u0001\u0000\u0012LocalVariableTable\u0001\u0000\u0004this\u0001\u0000/Lcom/example/DecoratorManager$LoggingDecorator;\u0001\u0000\u0016LocalVariableTypeTable\u0001\u00004Lcom/example/DecoratorManager$LoggingDecorator<TT;>;\u0001\u0000\bdecorate\u0001\u0000&(Ljava/lang/Object;)Ljava/lang/Object;\u0001\u0000\tSignature\u0001\u0000\b(TT;)TT;\u0007\u0000",
      "context_before": "\n\u0000\t\u0000\u000e\u0001\u0000\u0003()V\t\u0000\u0001\u0000\u0010",
      "context_after": "\u0001\u0000\u001bjava/util/function/Function\u0012\u0000\u0000\u0000\n"
    },
    {
      "path": "target/classes/com/example/DecoratorManager$LoggingDecorator.class",
      "line": 6,
      "col": 216,
      "snippet": "\u0000\u0007\u0000\b\u0001\u0000\u000fLineNumberTable\u0001\u0000\u0012LocalVariableTable\u0001\u0000\u0004this\u0001\u0000/Lcom/example/DecoratorManager$LoggingDecorator;\u0001\u0000\u0016LocalVariableTypeTable\u0001\u00004Lcom/example/DecoratorManager$LoggingDecorator<TT;>;\u0001\u0000\bdecorate\u0001\u0000&(Ljava/lang/Object;)Ljava/lang/Object;\u0001\u0000\tSignature\u0001\u0000\b(TT;)TT;\u0007\u0000",
      "context_before": "\n\u0000\t\u0000\u000e\u0001\u0000\u0003()V\t\u0000\u0001\u0000\u0010",
      "context_after": "\u0001\u0000\u001bjava/util/function/Function\u0012\u0000\u0000\u0000\n"
    },
    {
      "path": "target/classes/com/example/DecoratorManager$LoggingDecorator.class",
      "line": 7,
      "col": 4,
      "snippet": "\u0001\u0000\u001bjava/util/function/Function\u0012\u0000\u0000\u0000",
      "context_before": "\u0000\t\u0000\u000e\u0001\u0000\u0003()V\t\u0000\u0001\u0000\u0010\n\u0000\u0007\u0000\b\u0001\u0000\u000fLineNumberTable\u0001\u0000\u0012LocalVariableTable\u0001\u0000\u0004this\u0001\u0000/Lcom/example/DecoratorManager$LoggingDecorator;\u0001\u0000\u0016LocalVariableTypeTable\u0001\u00004Lcom/example/DecoratorManager$LoggingDecorator<TT;>;\u0001\u0000\bdecorate\u0001\u0000&(Ljava/lang/Object;)Ljava/lang/Object;\u0001\u0000\tSignature\u0001\u0000\b(TT;)TT;\u0007\u0000",
      "context_after": "\n\u0000\u001f\u0000 \u0001\u0000\u0005apply\u0001\u0000k(Lcom/example/DecoratorManager$LoggingDecorator;Ljava/util/function/Function;)Ljava/util/function/Function;\u0001\u0000\u0006target\u0001\u0000\u0012Ljava/lang/Object;\u0001\u0000\bfunction\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/DecoratorManager$LoggingDecorator.class",
      "line": 9,
      "col": 65,
      "snippet": "\u0000\u001f\u0000 \u0001\u0000\u0005apply\u0001\u0000k(Lcom/example/DecoratorManager$LoggingDecorator;Ljava/util/function/Function;)Ljava/util/function/Function;\u0001\u0000\u0006target\u0001\u0000\u0012Ljava/lang/Object;\u0001\u0000\bfunction\u0001\u0000",
      "context_before": "\u0001\u0000\u001bjava/util/function/Function\u0012\u0000\u0000\u0000\n",
      "context_after": "Ljava/util/function/Function;\u0001\u0000\u0011decoratedFunction\u0001\u0000\u0006result\u0001\u0000\u0003TT;\u0001\u0000CLjava/util/function/Function<Ljava/lang/Object;Ljava/lang/Object;>;\u0001\u0000\nStackMapTable\u0001\u0000\u0007getType\u0001\u0000\u0014()Ljava/lang/String;\b\u0000-\u0001\u0000\u0007logging\u0001\u0000\blambda$0\u0001\u0000C(Ljava/util/function/Function;Ljava/lang/Object;)Ljava/lang/Object;\t\u00001\u00003\u0007\u00002\u0001\u0000\u0010java/lang/System"
    },
    {
      "path": "target/classes/com/example/DecoratorManager$LoggingDecorator.class",
      "line": 9,
      "col": 95,
      "snippet": "\u0000\u001f\u0000 \u0001\u0000\u0005apply\u0001\u0000k(Lcom/example/DecoratorManager$LoggingDecorator;Ljava/util/function/Function;)Ljava/util/function/Function;\u0001\u0000\u0006target\u0001\u0000\u0012Ljava/lang/Object;\u0001\u0000\bfunction\u0001\u0000",
      "context_before": "\u0001\u0000\u001bjava/util/function/Function\u0012\u0000\u0000\u0000\n",
      "context_after": "Ljava/util/function/Function;\u0001\u0000\u0011decoratedFunction\u0001\u0000\u0006result\u0001\u0000\u0003TT;\u0001\u0000CLjava/util/function/Function<Ljava/lang/Object;Ljava/lang/Object;>;\u0001\u0000\nStackMapTable\u0001\u0000\u0007getType\u0001\u0000\u0014()Ljava/lang/String;\b\u0000-\u0001\u0000\u0007logging\u0001\u0000\blambda$0\u0001\u0000C(Ljava/util/function/Function;Ljava/lang/Object;)Ljava/lang/Object;\t\u00001\u00003\u0007\u00002\u0001\u0000\u0010java/lang/System"
    },
    {
      "path": "target/classes/com/example/DecoratorManager$LoggingDecorator.class",
      "line": 9,
      "col": 136,
      "snippet": "\u0000\u001f\u0000 \u0001\u0000\u0005apply\u0001\u0000k(Lcom/example/DecoratorManager$LoggingDecorator;Ljava/util/function/Function;)Ljava/util/function/Function;\u0001\u0000\u0006target\u0001\u0000\u0012Ljava/lang/Object;\u0001\u0000\bfunction\u0001\u0000",
      "context_before": "\u0001\u0000\u001bjava/util/function/Function\u0012\u0000\u0000\u0000\n",
      "context_after": "Ljava/util/function/Function;\u0001\u0000\u0011decoratedFunction\u0001\u0000\u0006result\u0001\u0000\u0003TT;\u0001\u0000CLjava/util/function/Function<Ljava/lang/Object;Ljava/lang/Object;>;\u0001\u0000\nStackMapTable\u0001\u0000\u0007getType\u0001\u0000\u0014()Ljava/lang/String;\b\u0000-\u0001\u0000\u0007logging\u0001\u0000\blambda$0\u0001\u0000C(Ljava/util/function/Function;Ljava/lang/Object;)Ljava/lang/Object;\t\u00001\u00003\u0007\u00002\u0001\u0000\u0010java/lang/System"
    },
    {
      "path": "target/classes/com/example/DecoratorManager$LoggingDecorator.class",
      "line": 10,
      "col": 2,
      "snippet": "Ljava/util/function/Function;\u0001\u0000\u0011decoratedFunction\u0001\u0000\u0006result\u0001\u0000\u0003TT;\u0001\u0000CLjava/util/function/Function<Ljava/lang/Object;Ljava/lang/Object;>;\u0001\u0000",
      "context_before": "\n\u0000\u001f\u0000 \u0001\u0000\u0005apply\u0001\u0000k(Lcom/example/DecoratorManager$LoggingDecorator;Ljava/util/function/Function;)Ljava/util/function/Function;\u0001\u0000\u0006target\u0001\u0000\u0012Ljava/lang/Object;\u0001\u0000\bfunction\u0001\u0000",
      "context_after": "StackMapTable\u0001\u0000\u0007getType\u0001\u0000\u0014()Ljava/lang/String;\b\u0000-\u0001\u0000\u0007logging\u0001\u0000\blambda$0\u0001\u0000C(Ljava/util/function/Function;Ljava/lang/Object;)Ljava/lang/Object;\t\u00001\u00003\u0007\u00002\u0001\u0000\u0010java/lang/System\n\u00004\u00005\u0001\u0000\u0003out\u0001\u0000\u0015Ljava/io/PrintStream;"
    },
    {
      "path": "target/classes/com/example/DecoratorManager$LoggingDecorator.class",
      "line": 10,
      "col": 69,
      "snippet": "Ljava/util/function/Function;\u0001\u0000\u0011decoratedFunction\u0001\u0000\u0006result\u0001\u0000\u0003TT;\u0001\u0000CLjava/util/function/Function<Ljava/lang/Object;Ljava/lang/Object;>;\u0001\u0000",
      "context_before": "\n\u0000\u001f\u0000 \u0001\u0000\u0005apply\u0001\u0000k(Lcom/example/DecoratorManager$LoggingDecorator;Ljava/util/function/Function;)Ljava/util/function/Function;\u0001\u0000\u0006target\u0001\u0000\u0012Ljava/lang/Object;\u0001\u0000\bfunction\u0001\u0000",
      "context_after": "StackMapTable\u0001\u0000\u0007getType\u0001\u0000\u0014()Ljava/lang/String;\b\u0000-\u0001\u0000\u0007logging\u0001\u0000\blambda$0\u0001\u0000C(Ljava/util/function/Function;Ljava/lang/Object;)Ljava/lang/Object;\t\u00001\u00003\u0007\u00002\u0001\u0000\u0010java/lang/System\n\u00004\u00005\u0001\u0000\u0003out\u0001\u0000\u0015Ljava/io/PrintStream;"
    },
    {
      "path": "target/classes/com/example/DecoratorManager$LoggingDecorator.class",
      "line": 10,
      "col": 98,
      "snippet": "Ljava/util/function/Function;\u0001\u0000\u0011decoratedFunction\u0001\u0000\u0006result\u0001\u0000\u0003TT;\u0001\u0000CLjava/util/function/Function<Ljava/lang/Object;Ljava/lang/Object;>;\u0001\u0000",
      "context_before": "\n\u0000\u001f\u0000 \u0001\u0000\u0005apply\u0001\u0000k(Lcom/example/DecoratorManager$LoggingDecorator;Ljava/util/function/Function;)Ljava/util/function/Function;\u0001\u0000\u0006target\u0001\u0000\u0012Ljava/lang/Object;\u0001\u0000\bfunction\u0001\u0000",
      "context_after": "StackMapTable\u0001\u0000\u0007getType\u0001\u0000\u0014()Ljava/lang/String;\b\u0000-\u0001\u0000\u0007logging\u0001\u0000\blambda$0\u0001\u0000C(Ljava/util/function/Function;Ljava/lang/Object;)Ljava/lang/Object;\t\u00001\u00003\u0007\u00002\u0001\u0000\u0010java/lang/System\n\u00004\u00005\u0001\u0000\u0003out\u0001\u0000\u0015Ljava/io/PrintStream;"
    },
    {
      "path": "target/classes/com/example/DecoratorManager$LoggingDecorator.class",
      "line": 10,
      "col": 116,
      "snippet": "Ljava/util/function/Function;\u0001\u0000\u0011decoratedFunction\u0001\u0000\u0006result\u0001\u0000\u0003TT;\u0001\u0000CLjava/util/function/Function<Ljava/lang/Object;Ljava/lang/Object;>;\u0001\u0000",
      "context_before": "\n\u0000\u001f\u0000 \u0001\u0000\u0005apply\u0001\u0000k(Lcom/example/DecoratorManager$LoggingDecorator;Ljava/util/function/Function;)Ljava/util/function/Function;\u0001\u0000\u0006target\u0001\u0000\u0012Ljava/lang/Object;\u0001\u0000\bfunction\u0001\u0000",
      "context_after": "StackMapTable\u0001\u0000\u0007getType\u0001\u0000\u0014()Ljava/lang/String;\b\u0000-\u0001\u0000\u0007logging\u0001\u0000\blambda$0\u0001\u0000C(Ljava/util/function/Function;Ljava/lang/Object;)Ljava/lang/Object;\t\u00001\u00003\u0007\u00002\u0001\u0000\u0010java/lang/System\n\u00004\u00005\u0001\u0000\u0003out\u0001\u0000\u0015Ljava/io/PrintStream;"
    },
    {
      "path": "target/classes/com/example/DecoratorManager$LoggingDecorator.class",
      "line": 11,
      "col": 30,
      "snippet": "StackMapTable\u0001\u0000\u0007getType\u0001\u0000\u0014()Ljava/lang/String;\b\u0000-\u0001\u0000\u0007logging\u0001\u0000\blambda$0\u0001\u0000C(Ljava/util/function/Function;Ljava/lang/Object;)Ljava/lang/Object;\t\u00001\u00003\u0007\u00002\u0001\u0000\u0010java/lang/System",
      "context_before": "\u0000\u001f\u0000 \u0001\u0000\u0005apply\u0001\u0000k(Lcom/example/DecoratorManager$LoggingDecorator;Ljava/util/function/Function;)Ljava/util/function/Function;\u0001\u0000\u0006target\u0001\u0000\u0012Ljava/lang/Object;\u0001\u0000\bfunction\u0001\u0000\nLjava/util/function/Function;\u0001\u0000\u0011decoratedFunction\u0001\u0000\u0006result\u0001\u0000\u0003TT;\u0001\u0000CLjava/util/function/Function<Ljava/lang/Object;Ljava/lang/Object;>;\u0001\u0000",
      "context_after": "\u00004\u00005\u0001\u0000\u0003out\u0001\u0000\u0015Ljava/io/PrintStream;\n\u00007\u00009\u0007\u00008\u0001\u0000\u0010java/lang/String"
    },
    {
      "path": "target/classes/com/example/DecoratorManager$LoggingDecorator.class",
      "line": 11,
      "col": 76,
      "snippet": "StackMapTable\u0001\u0000\u0007getType\u0001\u0000\u0014()Ljava/lang/String;\b\u0000-\u0001\u0000\u0007logging\u0001\u0000\blambda$0\u0001\u0000C(Ljava/util/function/Function;Ljava/lang/Object;)Ljava/lang/Object;\t\u00001\u00003\u0007\u00002\u0001\u0000\u0010java/lang/System",
      "context_before": "\u0000\u001f\u0000 \u0001\u0000\u0005apply\u0001\u0000k(Lcom/example/DecoratorManager$LoggingDecorator;Ljava/util/function/Function;)Ljava/util/function/Function;\u0001\u0000\u0006target\u0001\u0000\u0012Ljava/lang/Object;\u0001\u0000\bfunction\u0001\u0000\nLjava/util/function/Function;\u0001\u0000\u0011decoratedFunction\u0001\u0000\u0006result\u0001\u0000\u0003TT;\u0001\u0000CLjava/util/function/Function<Ljava/lang/Object;Ljava/lang/Object;>;\u0001\u0000",
      "context_after": "\u00004\u00005\u0001\u0000\u0003out\u0001\u0000\u0015Ljava/io/PrintStream;\n\u00007\u00009\u0007\u00008\u0001\u0000\u0010java/lang/String"
    },
    {
      "path": "target/classes/com/example/DecoratorManager$LoggingDecorator.class",
      "line": 11,
      "col": 105,
      "snippet": "StackMapTable\u0001\u0000\u0007getType\u0001\u0000\u0014()Ljava/lang/String;\b\u0000-\u0001\u0000\u0007logging\u0001\u0000\blambda$0\u0001\u0000C(Ljava/util/function/Function;Ljava/lang/Object;)Ljava/lang/Object;\t\u00001\u00003\u0007\u00002\u0001\u0000\u0010java/lang/System",
      "context_before": "\u0000\u001f\u0000 \u0001\u0000\u0005apply\u0001\u0000k(Lcom/example/DecoratorManager$LoggingDecorator;Ljava/util/function/Function;)Ljava/util/function/Function;\u0001\u0000\u0006target\u0001\u0000\u0012Ljava/lang/Object;\u0001\u0000\bfunction\u0001\u0000\nLjava/util/function/Function;\u0001\u0000\u0011decoratedFunction\u0001\u0000\u0006result\u0001\u0000\u0003TT;\u0001\u0000CLjava/util/function/Function<Ljava/lang/Object;Ljava/lang/Object;>;\u0001\u0000",
      "context_after": "\u00004\u00005\u0001\u0000\u0003out\u0001\u0000\u0015Ljava/io/PrintStream;\n\u00007\u00009\u0007\u00008\u0001\u0000\u0010java/lang/String"
    },
    {
      "path": "target/classes/com/example/DecoratorManager$LoggingDecorator.class",
      "line": 11,
      "col": 124,
      "snippet": "StackMapTable\u0001\u0000\u0007getType\u0001\u0000\u0014()Ljava/lang/String;\b\u0000-\u0001\u0000\u0007logging\u0001\u0000\blambda$0\u0001\u0000C(Ljava/util/function/Function;Ljava/lang/Object;)Ljava/lang/Object;\t\u00001\u00003\u0007\u00002\u0001\u0000\u0010java/lang/System",
      "context_before": "\u0000\u001f\u0000 \u0001\u0000\u0005apply\u0001\u0000k(Lcom/example/DecoratorManager$LoggingDecorator;Ljava/util/function/Function;)Ljava/util/function/Function;\u0001\u0000\u0006target\u0001\u0000\u0012Ljava/lang/Object;\u0001\u0000\bfunction\u0001\u0000\nLjava/util/function/Function;\u0001\u0000\u0011decoratedFunction\u0001\u0000\u0006result\u0001\u0000\u0003TT;\u0001\u0000CLjava/util/function/Function<Ljava/lang/Object;Ljava/lang/Object;>;\u0001\u0000",
      "context_after": "\u00004\u00005\u0001\u0000\u0003out\u0001\u0000\u0015Ljava/io/PrintStream;\n\u00007\u00009\u0007\u00008\u0001\u0000\u0010java/lang/String"
    },
    {
      "path": "target/classes/com/example/DecoratorManager$LoggingDecorator.class",
      "line": 11,
      "col": 152,
      "snippet": "StackMapTable\u0001\u0000\u0007getType\u0001\u0000\u0014()Ljava/lang/String;\b\u0000-\u0001\u0000\u0007logging\u0001\u0000\blambda$0\u0001\u0000C(Ljava/util/function/Function;Ljava/lang/Object;)Ljava/lang/Object;\t\u00001\u00003\u0007\u00002\u0001\u0000\u0010java/lang/System",
      "context_before": "\u0000\u001f\u0000 \u0001\u0000\u0005apply\u0001\u0000k(Lcom/example/DecoratorManager$LoggingDecorator;Ljava/util/function/Function;)Ljava/util/function/Function;\u0001\u0000\u0006target\u0001\u0000\u0012Ljava/lang/Object;\u0001\u0000\bfunction\u0001\u0000\nLjava/util/function/Function;\u0001\u0000\u0011decoratedFunction\u0001\u0000\u0006result\u0001\u0000\u0003TT;\u0001\u0000CLjava/util/function/Function<Ljava/lang/Object;Ljava/lang/Object;>;\u0001\u0000",
      "context_after": "\u00004\u00005\u0001\u0000\u0003out\u0001\u0000\u0015Ljava/io/PrintStream;\n\u00007\u00009\u0007\u00008\u0001\u0000\u0010java/lang/String"
    },
    {
      "path": "target/classes/com/example/DecoratorManager$LoggingDecorator.class",
      "line": 12,
      "col": 15,
      "snippet": "\u00004\u00005\u0001\u0000\u0003out\u0001\u0000\u0015Ljava/io/PrintStream;",
      "context_before": "Ljava/util/function/Function;\u0001\u0000\u0011decoratedFunction\u0001\u0000\u0006result\u0001\u0000\u0003TT;\u0001\u0000CLjava/util/function/Function<Ljava/lang/Object;Ljava/lang/Object;>;\u0001\u0000\nStackMapTable\u0001\u0000\u0007getType\u0001\u0000\u0014()Ljava/lang/String;\b\u0000-\u0001\u0000\u0007logging\u0001\u0000\blambda$0\u0001\u0000C(Ljava/util/function/Function;Ljava/lang/Object;)Ljava/lang/Object;\t\u00001\u00003\u0007\u00002\u0001\u0000\u0010java/lang/System",
      "context_after": "\u00007\u00009\u0007\u00008\u0001\u0000\u0010java/lang/String\n\u0000:\u0000;\u0001\u0000\u0007valueOf\u0001\u0000&(Ljava/lang/Object;)Ljava/lang/String;\u0012\u0000\u0001\u0000="
    },
    {
      "path": "target/classes/com/example/DecoratorManager$LoggingDecorator.class",
      "line": 13,
      "col": 11,
      "snippet": "\u00007\u00009\u0007\u00008\u0001\u0000\u0010java/lang/String",
      "context_before": "StackMapTable\u0001\u0000\u0007getType\u0001\u0000\u0014()Ljava/lang/String;\b\u0000-\u0001\u0000\u0007logging\u0001\u0000\blambda$0\u0001\u0000C(Ljava/util/function/Function;Ljava/lang/Object;)Ljava/lang/Object;\t\u00001\u00003\u0007\u00002\u0001\u0000\u0010java/lang/System\n\u00004\u00005\u0001\u0000\u0003out\u0001\u0000\u0015Ljava/io/PrintStream;",
      "context_after": "\u0000:\u0000;\u0001\u0000\u0007valueOf\u0001\u0000&(Ljava/lang/Object;)Ljava/lang/String;\u0012\u0000\u0001\u0000=\n\u0000>\u0000?\u0001\u0000\u0017makeConcatWithConstants\u0001\u00008(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;"
    },
    {
      "path": "target/classes/com/example/DecoratorManager$LoggingDecorator.class",
      "line": 14,
      "col": 20,
      "snippet": "\u0000:\u0000;\u0001\u0000\u0007valueOf\u0001\u0000&(Ljava/lang/Object;)Ljava/lang/String;\u0012\u0000\u0001\u0000=",
      "context_before": "\u00004\u00005\u0001\u0000\u0003out\u0001\u0000\u0015Ljava/io/PrintStream;\n\u00007\u00009\u0007\u00008\u0001\u0000\u0010java/lang/String",
      "context_after": "\u0000>\u0000?\u0001\u0000\u0017makeConcatWithConstants\u0001\u00008(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;\n\u0000A\u0000C\u0007\u0000B\u0001\u0000\u0013java/io/PrintStream"
    },
    {
      "path": "target/classes/com/example/DecoratorManager$LoggingDecorator.class",
      "line": 14,
      "col": 39,
      "snippet": "\u0000:\u0000;\u0001\u0000\u0007valueOf\u0001\u0000&(Ljava/lang/Object;)Ljava/lang/String;\u0012\u0000\u0001\u0000=",
      "context_before": "\u00004\u00005\u0001\u0000\u0003out\u0001\u0000\u0015Ljava/io/PrintStream;\n\u00007\u00009\u0007\u00008\u0001\u0000\u0010java/lang/String",
      "context_after": "\u0000>\u0000?\u0001\u0000\u0017makeConcatWithConstants\u0001\u00008(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;\n\u0000A\u0000C\u0007\u0000B\u0001\u0000\u0013java/io/PrintStream"
    },
    {
      "path": "target/classes/com/example/DecoratorManager$LoggingDecorator.class",
      "line": 15,
      "col": 36,
      "snippet": "\u0000>\u0000?\u0001\u0000\u0017makeConcatWithConstants\u0001\u00008(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;",
      "context_before": "\u00007\u00009\u0007\u00008\u0001\u0000\u0010java/lang/String\n\u0000:\u0000;\u0001\u0000\u0007valueOf\u0001\u0000&(Ljava/lang/Object;)Ljava/lang/String;\u0012\u0000\u0001\u0000=",
      "context_after": "\u0000A\u0000C\u0007\u0000B\u0001\u0000\u0013java/io/PrintStream\n\u0000D\u0000"
    },
    {
      "path": "target/classes/com/example/DecoratorManager$LoggingDecorator.class",
      "line": 15,
      "col": 54,
      "snippet": "\u0000>\u0000?\u0001\u0000\u0017makeConcatWithConstants\u0001\u00008(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;",
      "context_before": "\u00007\u00009\u0007\u00008\u0001\u0000\u0010java/lang/String\n\u0000:\u0000;\u0001\u0000\u0007valueOf\u0001\u0000&(Ljava/lang/Object;)Ljava/lang/String;\u0012\u0000\u0001\u0000=",
      "context_after": "\u0000A\u0000C\u0007\u0000B\u0001\u0000\u0013java/io/PrintStream\n\u0000D\u0000"
    },
    {
      "path": "target/classes/com/example/DecoratorManager$LoggingDecorator.class",
      "line": 15,
      "col": 73,
      "snippet": "\u0000>\u0000?\u0001\u0000\u0017makeConcatWithConstants\u0001\u00008(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;",
      "context_before": "\u00007\u00009\u0007\u00008\u0001\u0000\u0010java/lang/String\n\u0000:\u0000;\u0001\u0000\u0007valueOf\u0001\u0000&(Ljava/lang/Object;)Ljava/lang/String;\u0012\u0000\u0001\u0000=",
      "context_after": "\u0000A\u0000C\u0007\u0000B\u0001\u0000\u0013java/io/PrintStream\n\u0000D\u0000"
    },
    {
      "path": "target/classes/com/example/DecoratorManager$LoggingDecorator.class",
      "line": 16,
      "col": 11,
      "snippet": "\u0000A\u0000C\u0007\u0000B\u0001\u0000\u0013java/io/PrintStream",
      "context_before": "\u0000:\u0000;\u0001\u0000\u0007valueOf\u0001\u0000&(Ljava/lang/Object;)Ljava/lang/String;\u0012\u0000\u0001\u0000=\n\u0000>\u0000?\u0001\u0000\u0017makeConcatWithConstants\u0001\u00008(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;",
      "context_after": "\u0000D\u0000\n\u0001\u0000\u0007println"
    },
    {
      "path": "target/classes/com/example/DecoratorManager$LoggingDecorator.class",
      "line": 21,
      "col": 31,
      "snippet": "SourceFile\u0001\u0000\u0015DecoratorManager.java\u0001\u0000U<T:Ljava/lang/Object;>Ljava/lang/Object;Lcom/example/DecoratorManager$Decorator<TT;>;\u0001\u0000\u0010BootstrapMethods",
      "context_before": "\u0000\u001b\u0000F\n\u0000\u001f\u0000\u0018\u0012\u0000\u0002\u0000=\u0001\u0000\u0005input\u0001\u0000",
      "context_after": "\u0000N\u0000P\u0007\u0000O\u0001\u0000\"java/lang/invoke/LambdaMetafactory\n\u0000Q\u0000R\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/DecoratorManager$LoggingDecorator.class",
      "line": 21,
      "col": 42,
      "snippet": "SourceFile\u0001\u0000\u0015DecoratorManager.java\u0001\u0000U<T:Ljava/lang/Object;>Ljava/lang/Object;Lcom/example/DecoratorManager$Decorator<TT;>;\u0001\u0000\u0010BootstrapMethods",
      "context_before": "\u0000\u001b\u0000F\n\u0000\u001f\u0000\u0018\u0012\u0000\u0002\u0000=\u0001\u0000\u0005input\u0001\u0000",
      "context_after": "\u0000N\u0000P\u0007\u0000O\u0001\u0000\"java/lang/invoke/LambdaMetafactory\n\u0000Q\u0000R\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/DecoratorManager$LoggingDecorator.class",
      "line": 21,
      "col": 61,
      "snippet": "SourceFile\u0001\u0000\u0015DecoratorManager.java\u0001\u0000U<T:Ljava/lang/Object;>Ljava/lang/Object;Lcom/example/DecoratorManager$Decorator<TT;>;\u0001\u0000\u0010BootstrapMethods",
      "context_before": "\u0000\u001b\u0000F\n\u0000\u001f\u0000\u0018\u0012\u0000\u0002\u0000=\u0001\u0000\u0005input\u0001\u0000",
      "context_after": "\u0000N\u0000P\u0007\u0000O\u0001\u0000\"java/lang/invoke/LambdaMetafactory\n\u0000Q\u0000R\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/DecoratorManager$LoggingDecorator.class",
      "line": 22,
      "col": 11,
      "snippet": "\u0000N\u0000P\u0007\u0000O\u0001\u0000\"java/lang/invoke/LambdaMetafactory",
      "context_before": "\u0000\u001f\u0000\u0018\u0012\u0000\u0002\u0000=\u0001\u0000\u0005input\u0001\u0000\nSourceFile\u0001\u0000\u0015DecoratorManager.java\u0001\u0000U<T:Ljava/lang/Object;>Ljava/lang/Object;Lcom/example/DecoratorManager$Decorator<TT;>;\u0001\u0000\u0010BootstrapMethods",
      "context_after": "\u0000Q\u0000R\u0001\u0000\nmetafactory\u0001\u0000(Ljava/lang/invoke/MethodHandles$Lookup;Ljava/lang/String;Ljava/lang/invoke/MethodType;Ljava/lang/invoke/MethodType;Ljava/lang/invoke/MethodHandle;Ljava/lang/invoke/MethodType;)Ljava/lang/invoke/CallSite;\u000f\u0006\u0000M\u0010\u0000\u0018"
    },
    {
      "path": "target/classes/com/example/DecoratorManager$LoggingDecorator.class",
      "line": 24,
      "col": 16,
      "snippet": "metafactory\u0001\u0000(Ljava/lang/invoke/MethodHandles$Lookup;Ljava/lang/String;Ljava/lang/invoke/MethodType;Ljava/lang/invoke/MethodType;Ljava/lang/invoke/MethodHandle;Ljava/lang/invoke/MethodType;)Ljava/lang/invoke/CallSite;\u000f\u0006\u0000M\u0010\u0000\u0018",
      "context_before": "\u0000N\u0000P\u0007\u0000O\u0001\u0000\"java/lang/invoke/LambdaMetafactory\n\u0000Q\u0000R\u0001\u0000",
      "context_after": "\u0000\u0001\u0000V\n\u0000.\u0000/\u000f\u0007\u0000U\u0010\u0000\u0018"
    },
    {
      "path": "target/classes/com/example/DecoratorManager$LoggingDecorator.class",
      "line": 24,
      "col": 55,
      "snippet": "metafactory\u0001\u0000(Ljava/lang/invoke/MethodHandles$Lookup;Ljava/lang/String;Ljava/lang/invoke/MethodType;Ljava/lang/invoke/MethodType;Ljava/lang/invoke/MethodHandle;Ljava/lang/invoke/MethodType;)Ljava/lang/invoke/CallSite;\u000f\u0006\u0000M\u0010\u0000\u0018",
      "context_before": "\u0000N\u0000P\u0007\u0000O\u0001\u0000\"java/lang/invoke/LambdaMetafactory\n\u0000Q\u0000R\u0001\u0000",
      "context_after": "\u0000\u0001\u0000V\n\u0000.\u0000/\u000f\u0007\u0000U\u0010\u0000\u0018"
    },
    {
      "path": "target/classes/com/example/DecoratorManager$LoggingDecorator.class",
      "line": 24,
      "col": 73,
      "snippet": "metafactory\u0001\u0000(Ljava/lang/invoke/MethodHandles$Lookup;Ljava/lang/String;Ljava/lang/invoke/MethodType;Ljava/lang/invoke/MethodType;Ljava/lang/invoke/MethodHandle;Ljava/lang/invoke/MethodType;)Ljava/lang/invoke/CallSite;\u000f\u0006\u0000M\u0010\u0000\u0018",
      "context_before": "\u0000N\u0000P\u0007\u0000O\u0001\u0000\"java/lang/invoke/LambdaMetafactory\n\u0000Q\u0000R\u0001\u0000",
      "context_after": "\u0000\u0001\u0000V\n\u0000.\u0000/\u000f\u0007\u0000U\u0010\u0000\u0018"
    },
    {
      "path": "target/classes/com/example/DecoratorManager$LoggingDecorator.class",
      "line": 24,
      "col": 102,
      "snippet": "metafactory\u0001\u0000(Ljava/lang/invoke/MethodHandles$Lookup;Ljava/lang/String;Ljava/lang/invoke/MethodType;Ljava/lang/invoke/MethodType;Ljava/lang/invoke/MethodHandle;Ljava/lang/invoke/MethodType;)Ljava/lang/invoke/CallSite;\u000f\u0006\u0000M\u0010\u0000\u0018",
      "context_before": "\u0000N\u0000P\u0007\u0000O\u0001\u0000\"java/lang/invoke/LambdaMetafactory\n\u0000Q\u0000R\u0001\u0000",
      "context_after": "\u0000\u0001\u0000V\n\u0000.\u0000/\u000f\u0007\u0000U\u0010\u0000\u0018"
    },
    {
      "path": "target/classes/com/example/DecoratorManager$LoggingDecorator.class",
      "line": 24,
      "col": 131,
      "snippet": "metafactory\u0001\u0000(Ljava/lang/invoke/MethodHandles$Lookup;Ljava/lang/String;Ljava/lang/invoke/MethodType;Ljava/lang/invoke/MethodType;Ljava/lang/invoke/MethodHandle;Ljava/lang/invoke/MethodType;)Ljava/lang/invoke/CallSite;\u000f\u0006\u0000M\u0010\u0000\u0018",
      "context_before": "\u0000N\u0000P\u0007\u0000O\u0001\u0000\"java/lang/invoke/LambdaMetafactory\n\u0000Q\u0000R\u0001\u0000",
      "context_after": "\u0000\u0001\u0000V\n\u0000.\u0000/\u000f\u0007\u0000U\u0010\u0000\u0018"
    },
    {
      "path": "target/classes/com/example/DecoratorManager$LoggingDecorator.class",
      "line": 24,
      "col": 162,
      "snippet": "metafactory\u0001\u0000(Ljava/lang/invoke/MethodHandles$Lookup;Ljava/lang/String;Ljava/lang/invoke/MethodType;Ljava/lang/invoke/MethodType;Ljava/lang/invoke/MethodHandle;Ljava/lang/invoke/MethodType;)Ljava/lang/invoke/CallSite;\u000f\u0006\u0000M\u0010\u0000\u0018",
      "context_before": "\u0000N\u0000P\u0007\u0000O\u0001\u0000\"java/lang/invoke/LambdaMetafactory\n\u0000Q\u0000R\u0001\u0000",
      "context_after": "\u0000\u0001\u0000V\n\u0000.\u0000/\u000f\u0007\u0000U\u0010\u0000\u0018"
    },
    {
      "path": "target/classes/com/example/DecoratorManager$LoggingDecorator.class",
      "line": 24,
      "col": 192,
      "snippet": "metafactory\u0001\u0000(Ljava/lang/invoke/MethodHandles$Lookup;Ljava/lang/String;Ljava/lang/invoke/MethodType;Ljava/lang/invoke/MethodType;Ljava/lang/invoke/MethodHandle;Ljava/lang/invoke/MethodType;)Ljava/lang/invoke/CallSite;\u000f\u0006\u0000M\u0010\u0000\u0018",
      "context_before": "\u0000N\u0000P\u0007\u0000O\u0001\u0000\"java/lang/invoke/LambdaMetafactory\n\u0000Q\u0000R\u0001\u0000",
      "context_after": "\u0000\u0001\u0000V\n\u0000.\u0000/\u000f\u0007\u0000U\u0010\u0000\u0018"
    },
    {
      "path": "target/classes/com/example/DecoratorManager$LoggingDecorator.class",
      "line": 27,
      "col": 11,
      "snippet": "\u0000Z\u0000\\\u0007\u0000[\u0001\u0000$java/lang/invoke/StringConcatFactory",
      "context_before": "\u0000\u0001\u0000V\n\u0000.\u0000/\u000f\u0007\u0000U\u0010\u0000\u0018",
      "context_after": "\u0000>\u0000]\u0001\u0000(Ljava/lang/invoke/MethodHandles$Lookup;Ljava/lang/String;Ljava/lang/invoke/MethodType;Ljava/lang/String;[Ljava/lang/Object;)Ljava/lang/invoke/CallSite;\u000f\u0006\u0000Y\b\u0000`\u0001\u0000\n[\u0001] Input: \u0001\b\u0000b\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/DecoratorManager$LoggingDecorator.class",
      "line": 28,
      "col": 9,
      "snippet": "\u0000>\u0000]\u0001\u0000(Ljava/lang/invoke/MethodHandles$Lookup;Ljava/lang/String;Ljava/lang/invoke/MethodType;Ljava/lang/String;[Ljava/lang/Object;)Ljava/lang/invoke/CallSite;\u000f\u0006\u0000Y\b\u0000`\u0001\u0000",
      "context_before": "\u0000.\u0000/\u000f\u0007\u0000U\u0010\u0000\u0018\n\u0000Z\u0000\\\u0007\u0000[\u0001\u0000$java/lang/invoke/StringConcatFactory",
      "context_after": "[\u0001] Input: \u0001\b\u0000b\u0001\u0000\n[\u0001] Output: \u0001\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/DecoratorManager$LoggingDecorator.class",
      "line": 28,
      "col": 48,
      "snippet": "\u0000>\u0000]\u0001\u0000(Ljava/lang/invoke/MethodHandles$Lookup;Ljava/lang/String;Ljava/lang/invoke/MethodType;Ljava/lang/String;[Ljava/lang/Object;)Ljava/lang/invoke/CallSite;\u000f\u0006\u0000Y\b\u0000`\u0001\u0000",
      "context_before": "\u0000.\u0000/\u000f\u0007\u0000U\u0010\u0000\u0018\n\u0000Z\u0000\\\u0007\u0000[\u0001\u0000$java/lang/invoke/StringConcatFactory",
      "context_after": "[\u0001] Input: \u0001\b\u0000b\u0001\u0000\n[\u0001] Output: \u0001\u0001\u0000"
    }
  ],
  "tool_iter": 7,
  "call_index": 3
}
```

### Call 12
```json
{
  "tool": "read_file_range_tool",
  "args": {
    "start_line": 1,
    "path": "/home/ran/Documents/work/VectorCode/mini_code_index/test_code_index_project/src/main/python/config.py",
    "end_line": 50
  },
  "result": {
    "content": "#!/usr/bin/env python3\n\"\"\"\n配置模块\n提供配置管理功能\n\"\"\"\n\nimport os\nimport json\nimport yaml\nimport logging\nfrom typing import Dict, Any, Optional, Union, List\nfrom dataclasses import dataclass, field\nfrom pathlib import Path\nimport hashlib\nimport base64\nfrom functools import lru_cache\nimport threading\nfrom abc import ABC, abstractmethod\n\nlogger = logging.getLogger(__name__)\n\n\nclass ConfigError(Exception):\n    \"\"\"配置异常\"\"\"\n    pass\n\n\nclass ConfigProvider(ABC):\n    \"\"\"配置提供者抽象基类\"\"\"\n\n    @abstractmethod\n    def load_config(self, key: str) -> Any:\n        \"\"\"加载配置\"\"\"\n        pass\n\n    @abstractmethod\n    def save_config(self, key: str, value: Any):\n        \"\"\"保存配置\"\"\"\n        pass\n\n    @abstractmethod\n    def has_config(self, key: str) -> bool:\n        \"\"\"检查配置是否存在\"\"\"\n        pass\n\n\nclass EnvironmentConfigProvider(ConfigProvider):\n    \"\"\"环境变量配置提供者\"\"\"\n\n    def __init__(self, prefix: str = \"\"):"
  },
  "tool_iter": 7,
  "call_index": 4
}
```