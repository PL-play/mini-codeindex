# Test Code Index Project

这是一个用于测试代码索引功能的示例项目，包含 Java 和 Python 代码。

## 项目结构

- `src/main/java/com/example/` - Java 源代码
- `src/main/python/` - Python 脚本
- `pom.xml` - Maven 配置（Java）
- `requirements.txt` - Python 依赖

## 功能

- Java 部分：用户管理服务
- Python 部分：数据处理工具

## 运行

### Java
```bash
mvn compile
mvn exec:java -Dexec.mainClass="com.example.UserService"
```

### Python
```bash
python src/main/python/data_processor.py
```