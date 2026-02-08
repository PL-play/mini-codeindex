# Subtask Debug Report

**Title**: Identify entry points and controllers
**Instruction**: Find REST controllers or API endpoints that expose user management functionality to determine how requests are handled.

## Tool Calls
### Think Reflection
Reflection recorded: I need to identify REST controllers or API endpoints related to user management. I'll start by exploring the directory structure to find where controllers or API definitions might be located, and then search for keywords like "UserController", "UserRestController", "@RestController", or "@RequestMapping" (assuming a Java/Spring environment, but I'll keep it general first). I'll also look for "user" related files.

### Call 1
```json
{
  "tool": "tree_summary_tool",
  "args": {
    "max_depth": 3,
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
                  "children": []
                },
                {
                  "name": "python",
                  "path": "src/main/python",
                  "type": "dir",
                  "children": []
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
                  "children": []
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
                  "children": []
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
  "tool": "text_search_tool",
  "args": {
    "query": "UserController|UserRestController|@RestController|@RequestMapping|@GetMapping|@PostMapping|@PutMapping|@DeleteMapping",
    "root_dir": "/home/ran/Documents/work/VectorCode/mini_code_index/test_code_index_project"
  },
  "result": [],
  "tool_iter": 1,
  "call_index": 2
}
```

### Think Reflection
Reflection recorded: The previous search for common Java Spring annotations and controller names returned nothing. The directory structure shows both `src/main/java` and `src/main/python`. I'll explore the contents of these directories to see what's inside. I'll also search for "user" in a more general way and look for common Python web framework patterns (like Flask or FastAPI) since there's a `requirements.txt` and `src/main/python`.

### Call 3
```json
{
  "tool": "tree_summary_tool",
  "args": {
    "max_depth": 5,
    "root_dir": "/home/ran/Documents/work/VectorCode/mini_code_index/test_code_index_project/src/main"
  },
  "result": {
    "tree": {
      "name": "main",
      "path": "main",
      "type": "dir",
      "children": [
        {
          "name": "java",
          "path": "java",
          "type": "dir",
          "children": [
            {
              "name": "com",
              "path": "java/com",
              "type": "dir",
              "children": [
                {
                  "name": "example",
                  "path": "java/com/example",
                  "type": "dir",
                  "children": [
                    {
                      "name": "AdapterManager.java",
                      "path": "java/com/example/AdapterManager.java",
                      "type": "file"
                    },
                    {
                      "name": "AdvancedUtils.java",
                      "path": "java/com/example/AdvancedUtils.java",
                      "type": "file"
                    },
                    {
                      "name": "AuditLogger.java",
                      "path": "java/com/example/AuditLogger.java",
                      "type": "file"
                    },
                    {
                      "name": "CacheManager.java",
                      "path": "java/com/example/CacheManager.java",
                      "type": "file"
                    },
                    {
                      "name": "CommandManager.java",
                      "path": "java/com/example/CommandManager.java",
                      "type": "file"
                    },
                    {
                      "name": "DataProcessor.java",
                      "path": "java/com/example/DataProcessor.java",
                      "type": "file"
                    },
                    {
                      "name": "DecoratorManager.java",
                      "path": "java/com/example/DecoratorManager.java",
                      "type": "file"
                    },
                    {
                      "name": "EventSystem.java",
                      "path": "java/com/example/EventSystem.java",
                      "type": "file"
                    },
                    {
                      "name": "FactoryManager.java",
                      "path": "java/com/example/FactoryManager.java",
                      "type": "file"
                    },
                    {
                      "name": "NotificationService.java",
                      "path": "java/com/example/NotificationService.java",
                      "type": "file"
                    },
                    {
                      "name": "ObserverManager.java",
                      "path": "java/com/example/ObserverManager.java",
                      "type": "file"
                    },
                    {
                      "name": "PermissionManager.java",
                      "path": "java/com/example/PermissionManager.java",
                      "type": "file"
                    },
                    {
                      "name": "ReportGenerator.java",
                      "path": "java/com/example/ReportGenerator.java",
                      "type": "file"
                    },
                    {
                      "name": "StrategyManager.java",
                      "path": "java/com/example/StrategyManager.java",
                      "type": "file"
                    },
                    {
                      "name": "User.java",
                      "path": "java/com/example/User.java",
                      "type": "file"
                    },
                    {
                      "name": "UserService.java",
                      "path": "java/com/example/UserService.java",
                      "type": "file"
                    }
                  ]
                }
              ]
            }
          ]
        },
        {
          "name": "python",
          "path": "python",
          "type": "dir",
          "children": [
            {
              "name": "api_client.py",
              "path": "python/api_client.py",
              "type": "file"
            },
            {
              "name": "config.py",
              "path": "python/config.py",
              "type": "file"
            },
            {
              "name": "data_processor.py",
              "path": "python/data_processor.py",
              "type": "file"
            },
            {
              "name": "database.py",
              "path": "python/database.py",
              "type": "file"
            },
            {
              "name": "notification.py",
              "path": "python/notification.py",
              "type": "file"
            }
          ]
        }
      ]
    }
  },
  "tool_iter": 3,
  "call_index": 1
}
```

### Call 4
```json
{
  "tool": "text_search_tool",
  "args": {
    "query": "user",
    "root_dir": "/home/ran/Documents/work/VectorCode/mini_code_index/test_code_index_project"
  },
  "result": [
    {
      "path": "target/classes/com/example/UserService$AuditLogger.class",
      "line": 21,
      "col": 95,
      "snippet": "\u00000\u00001\u0001\u0000\u0006remove\u0001\u0000\u0015(I)Ljava/lang/Object;\u0001\u0000\toperation\u0001\u0000'Lcom/example/UserService$OperationType;\u0001\u0000\u0006userId\u0001\u0000\u0012Ljava/lang/String;\u0001\u0000\u0007details\u0001\u0000\u0005entry\u0001\u0000$Lcom/example/UserService$AuditEntry;\u0001\u0000",
      "context_before": "\u0000,\u0000-\u0001\u0000\u0004size\u0001\u0000\u0003()I\n\u0000%\u0000/",
      "context_after": "StackMapTable\u0007\u0000;\u0001\u0000\u0013java/lang/Throwable\u0001\u0000\u0010getRecentEntries\u0001\u0000\u0013(I)Ljava/util/List;\u0001\u00009(I)Ljava/util/List<Lcom/example/UserService$AuditEntry;>;\n\u0000@\u0000B\u0007\u0000A\u0001\u0000\u000ejava/lang/Math"
    },
    {
      "path": "target/classes/com/example/AuditLogger$AuditEvent.class",
      "line": 1,
      "col": 138,
      "snippet": "\u0000\u0000\u00007\u0000[\u0007\u0000\u0002\u0001\u0000\"com/example/AuditLogger$AuditEvent\u0007\u0000\u0004\u0001\u0000\u0010java/lang/Object\u0001\u0000\u0002id\u0001\u0000\u0012Ljava/lang/String;\u0001\u0000\ttimestamp\u0001\u0000\u0019Ljava/time/LocalDateTime;\u0001\u0000\u0006userId\u0001\u0000\teventType\u0001\u0000(Lcom/example/AuditLogger$AuditEventType;\u0001\u0000\bresource\u0001\u0000\u0006action\u0001\u0000\bseverity\u0001\u0000'Lcom/example/AuditLogger$AuditSeverity;\u0001\u0000\u0007details\u0001\u0000\u0007context\u0001\u0000\u000fLjava/util/Map;\u0001\u0000\tSignature\u0001\u00005Ljava/util/Map<Ljava/lang/String;Ljava/lang/String;>;\u0001\u0000\u0006<init>\u0001\u0000(Ljava/lang/String;Ljava/time/LocalDateTime;Ljava/lang/String;Lcom/example/AuditLogger$AuditEventType;Ljava/lang/String;Ljava/lang/String;Lcom/example/AuditLogger$AuditSeverity;Ljava/lang/String;Ljava/util/Map;)V\u0001\u0000(Ljava/lang/String;Ljava/time/LocalDateTime;Ljava/lang/String;Lcom/example/AuditLogger$AuditEventType;Ljava/lang/String;Ljava/lang/String;Lcom/example/AuditLogger$AuditSeverity;Ljava/lang/String;Ljava/util/Map<Ljava/lang/String;Ljava/lang/String;>;)V\u0001\u0000\u0004Code",
      "context_before": "",
      "context_after": "\u0000\u0003\u0000\u001a\n\u0000\u0015\u0000\u001b\u0001\u0000\u0003()V\t\u0000\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/ObserverManager.class",
      "line": 28,
      "col": 1,
      "snippet": "user_login",
      "context_before": "\u0000\u0001\u0000\u0017\u0001\u0000\nStackMapTable\u0007\u0000<\u0001\u0000\u0013java/lang/Throwable\b\u0000>\u0001\u0000",
      "context_after": "\u0000\u0001\u0000@\n\u0000A\u0000B\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/ObserverManager.class",
      "line": 32,
      "col": 1,
      "snippet": "user_logout\b\u0000F\u0001\u0000\u0011user_registration\b\u0000H\u0001\u0000\u0013user_profile_update\b\u0000J\u0001\u0000\u000esystem_startup\b\u0000L\u0001\u0000\u000fsystem_shutdown\b\u0000N\u0001\u0000",
      "context_before": "\u0000A\u0000B\u0001\u0000\ncreateSubject\u0001\u00009(Ljava/lang/String;)Lcom/example/ObserverManager$Subject;\b\u0000D\u0001\u0000",
      "context_after": "system_error\b\u0000P\u0001\u0000\u0012system_maintenance\b\u0000R\u0001\u0000\ndata_created\b\u0000T\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/ObserverManager.class",
      "line": 32,
      "col": 18,
      "snippet": "user_logout\b\u0000F\u0001\u0000\u0011user_registration\b\u0000H\u0001\u0000\u0013user_profile_update\b\u0000J\u0001\u0000\u000esystem_startup\b\u0000L\u0001\u0000\u000fsystem_shutdown\b\u0000N\u0001\u0000",
      "context_before": "\u0000A\u0000B\u0001\u0000\ncreateSubject\u0001\u00009(Ljava/lang/String;)Lcom/example/ObserverManager$Subject;\b\u0000D\u0001\u0000",
      "context_after": "system_error\b\u0000P\u0001\u0000\u0012system_maintenance\b\u0000R\u0001\u0000\ndata_created\b\u0000T\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/ObserverManager.class",
      "line": 32,
      "col": 41,
      "snippet": "user_logout\b\u0000F\u0001\u0000\u0011user_registration\b\u0000H\u0001\u0000\u0013user_profile_update\b\u0000J\u0001\u0000\u000esystem_startup\b\u0000L\u0001\u0000\u000fsystem_shutdown\b\u0000N\u0001\u0000",
      "context_before": "\u0000A\u0000B\u0001\u0000\ncreateSubject\u0001\u00009(Ljava/lang/String;)Lcom/example/ObserverManager$Subject;\b\u0000D\u0001\u0000",
      "context_after": "system_error\b\u0000P\u0001\u0000\u0012system_maintenance\b\u0000R\u0001\u0000\ndata_created\b\u0000T\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/CommandManager$UserCreateCommandFactory.class",
      "line": 6,
      "col": 81,
      "snippet": "\u0000\u0007\u0000\u0018\u0001\u0000'(Ljava/lang/String;Ljava/lang/String;)V\u0001\u0000\u0006params\u0001\u0000\u0013[Ljava/lang/Object;\u0001\u0000\busername\u0001\u0000\u0012Ljava/lang/String;\u0001\u0000\u0005email\u0001\u0000",
      "context_before": "\u0000\u0007\u0000\b\u0001\u0000\u000fLineNumberTable\u0001\u0000\u0012LocalVariableTable\u0001\u0000\u0004this\u0001\u00005Lcom/example/CommandManager$UserCreateCommandFactory;\u0001\u0000\u0006create\u0001\u00009([Ljava/lang/Object;)Lcom/example/CommandManager$Command;\u0007\u0000\u0013\u0001\u0000\u0010java/lang/String\u0007\u0000\u0015\u0001\u0000,com/example/CommandManager$UserCreateCommand\n\u0000\u0014\u0000\u0017",
      "context_after": "SourceFile\u0001\u0000\u0013CommandManager.java\u0001\u0000\nInnerClasses\u0007\u0000\"\u0001\u0000\"com/example/CommandManager$Command\u0007\u0000$\u0001\u0000\u001acom/example/CommandManager\u0001\u0000\u0007Command\u0001\u0000\u000eCommandFactory\u0001\u0000\u0011UserCreateCommand\u0001\u0000\u0018UserCreateCommandFactory\u0001\u0000\bNestHost\u0000!\u0000\u0001\u0000\u0003\u0000\u0001\u0000\u0005\u0000\u0000\u0000\u0002\u0000\u0001\u0000\u0007\u0000\b\u0000\u0001\u0000\t\u0000\u0000\u0000/\u0000\u0001\u0000\u0001\u0000\u0000\u0000\u0005*\u0000"
    },
    {
      "path": "target/classes/com/example/ReportGenerator.class",
      "line": 28,
      "col": 1,
      "snippet": "user_activity\u0007\u0000G\u0001\u0000*com/example/ReportGenerator$ReportTemplate\b\u0000I\u0001\u0000\u0014User Activity Report\t\u0000K\u0000M\u0007\u0000L\u0001\u0000&com/example/ReportGenerator$ReportType",
      "context_before": "\u0000A\u0000\u0015\u0001\u0000\u0013initializeTemplates\u0001\u0000\u0004this\u0001\u0000\nLcom/example/ReportGenerator;\b\u0000E\u0001\u0000",
      "context_after": "\u0000N\u0000O\u0001\u0000\nUSER_ACTIVITY\u0001\u0000(Lcom/example/ReportGenerator$ReportType;\u0007\u0000Q\u0001\u0000\u0010java/lang/String\b\u0000S\u0001\u0000\u0006userId\b\u0000U\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/ReportGenerator.class",
      "line": 30,
      "col": 85,
      "snippet": "USER_ACTIVITY\u0001\u0000(Lcom/example/ReportGenerator$ReportType;\u0007\u0000Q\u0001\u0000\u0010java/lang/String\b\u0000S\u0001\u0000\u0006userId\b\u0000U\u0001\u0000",
      "context_before": "user_activity\u0007\u0000G\u0001\u0000*com/example/ReportGenerator$ReportTemplate\b\u0000I\u0001\u0000\u0014User Activity Report\t\u0000K\u0000M\u0007\u0000L\u0001\u0000&com/example/ReportGenerator$ReportType\n\u0000N\u0000O\u0001\u0000",
      "context_after": "loginCount\b\u0000W\u0001\u0000\tlastLogin\b\u0000Y\u0001\u0000\ttotalTime\b\u0000[\u0001\u0000\u0007actions\n\u0000]\u0000_\u0007\u0000^\u0001\u0000\u0010java/util/Arrays"
    },
    {
      "path": "target/classes/com/example/ReportGenerator.class",
      "line": 46,
      "col": 16,
      "snippet": "department\b\u0000\u0001\u0000\tuserCount\b\u0000\u0001\u0000",
      "context_before": "AUDIT_TRAIL\b\u0000\u0001\u0000\u0006action\b\u0000\u0001\u0000\bresource\b\u0000\u0001\u0000\u0007details\u0012\u0000\u0003\u0000c\b\u0000\u0001\u0000\u0013department_analysis\b\u0000\u0001\u0000\u001aDepartment Analysis Report\t\u0000K\u0000\n\u0000\u0000O\u0001\u0000\u0013DEPARTMENT_ANALYSIS\b\u0000\u0001\u0000",
      "context_after": "activityLevel\b\u0000\u0001\u0000\nperformance\b\u0000\u0001\u0000\u0006issues\u0012\u0000\u0004\u0000c\u0001\u0000\u000egenerateReport\u0001\u0000u(Ljava/lang/String;Ljava/util/Map;Lcom/example/ReportGenerator$OutputFormat;)Ljava/util/concurrent/CompletableFuture;\u0001\u0000(Ljava/lang/String;Ljava/util/Map<Ljava/lang/String;Ljava/lang/Object;>;Lcom/example/ReportGenerator$OutputFormat;)Ljava/util/concurrent/CompletableFuture<Lcom/example/ReportGenerator$ReportResult;>;\u0012\u0000\u0005\u0000"
    },
    {
      "path": "target/classes/com/example/PermissionManager.class",
      "line": 2,
      "col": 55,
      "snippet": "com/example/PermissionManager\u0007\u0000\u0004\u0001\u0000\u0010java/lang/Object\u0001\u0000\u000fuserPermissions\u0001\u0000\u000fLjava/util/Map;\u0001\u0000\tSignature\u0001\u0000FLjava/util/Map<Ljava/lang/String;Ljava/util/Set<Ljava/lang/String;>;>;\u0001\u0000\u000frolePermissions\u0001\u0000\tuserRoles\u0001\u0000\u000fpermissionRules\u0001\u0000QLjava/util/Map<Ljava/lang/String;Lcom/example/PermissionManager$PermissionRule;>;\u0001\u0000\tREAD_USER\u0001\u0000\u0012Ljava/lang/String;\u0001\u0000",
      "context_before": "\u0000\u0000\u00007\u0001\u0007\u0000\u0002\u0001\u0000",
      "context_after": "ConstantValue\b\u0000\u0011\u0001\u0000\tuser:read\u0001\u0000\nWRITE_USER\b\u0000\u0014\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/PermissionManager.class",
      "line": 2,
      "col": 194,
      "snippet": "com/example/PermissionManager\u0007\u0000\u0004\u0001\u0000\u0010java/lang/Object\u0001\u0000\u000fuserPermissions\u0001\u0000\u000fLjava/util/Map;\u0001\u0000\tSignature\u0001\u0000FLjava/util/Map<Ljava/lang/String;Ljava/util/Set<Ljava/lang/String;>;>;\u0001\u0000\u000frolePermissions\u0001\u0000\tuserRoles\u0001\u0000\u000fpermissionRules\u0001\u0000QLjava/util/Map<Ljava/lang/String;Lcom/example/PermissionManager$PermissionRule;>;\u0001\u0000\tREAD_USER\u0001\u0000\u0012Ljava/lang/String;\u0001\u0000",
      "context_before": "\u0000\u0000\u00007\u0001\u0007\u0000\u0002\u0001\u0000",
      "context_after": "ConstantValue\b\u0000\u0011\u0001\u0000\tuser:read\u0001\u0000\nWRITE_USER\b\u0000\u0014\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/PermissionManager.class",
      "line": 3,
      "col": 20,
      "snippet": "ConstantValue\b\u0000\u0011\u0001\u0000\tuser:read\u0001\u0000",
      "context_before": "\u0000\u0000\u00007\u0001\u0007\u0000\u0002\u0001\u0000\ncom/example/PermissionManager\u0007\u0000\u0004\u0001\u0000\u0010java/lang/Object\u0001\u0000\u000fuserPermissions\u0001\u0000\u000fLjava/util/Map;\u0001\u0000\tSignature\u0001\u0000FLjava/util/Map<Ljava/lang/String;Ljava/util/Set<Ljava/lang/String;>;>;\u0001\u0000\u000frolePermissions\u0001\u0000\tuserRoles\u0001\u0000\u000fpermissionRules\u0001\u0000QLjava/util/Map<Ljava/lang/String;Lcom/example/PermissionManager$PermissionRule;>;\u0001\u0000\tREAD_USER\u0001\u0000\u0012Ljava/lang/String;\u0001\u0000",
      "context_after": "WRITE_USER\b\u0000\u0014\u0001\u0000\nuser:write\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/PermissionManager.class",
      "line": 5,
      "col": 1,
      "snippet": "user:write\u0001\u0000",
      "context_before": "ConstantValue\b\u0000\u0011\u0001\u0000\tuser:read\u0001\u0000\nWRITE_USER\b\u0000\u0014\u0001\u0000",
      "context_after": "DELETE_USER\b\u0000\u0017\u0001\u0000\nuser:delete\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/PermissionManager.class",
      "line": 7,
      "col": 1,
      "snippet": "user:delete\u0001\u0000",
      "context_before": "user:write\u0001\u0000\nDELETE_USER\b\u0000\u0017\u0001\u0000",
      "context_after": "ADMIN_USER\b\u0000\u001a\u0001\u0000\nuser:admin\u0001\u0000\u000fREAD_DEPARTMENT\b\u0000"
    },
    {
      "path": "target/classes/com/example/PermissionManager.class",
      "line": 9,
      "col": 1,
      "snippet": "user:admin\u0001\u0000\u000fREAD_DEPARTMENT\b\u0000",
      "context_before": "user:delete\u0001\u0000\nADMIN_USER\b\u0000\u001a\u0001\u0000",
      "context_after": "\u0001\u0000\u000fdepartment:read\u0001\u0000\u0010WRITE_DEPARTMENT\b\u0000 \u0001\u0000\u0010department:write\u0001\u0000\nREAD_REPORT\b\u0000#\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/PermissionManager.class",
      "line": 42,
      "col": 45,
      "snippet": "\u0000g\u0000h\u0001\u0000\u0006addAll\u0001\u0000\u0019(Ljava/util/Collection;)Z\u0001\u0000\tuserPerms\u0001\u0000\u000fLjava/util/Set;\u0001\u0000",
      "context_before": "\u0000d\u0000f\u0007\u0000e\u0001\u0000\njava/util/Set",
      "context_after": "managerPerms\u0001\u0000\nadminPerms\u0001\u0000\u000fsuperAdminPerms\u0001\u0000\u0016LocalVariableTypeTable\u0001\u0000#Ljava/util/Set<Ljava/lang/String;>;\b\u0000q\u0001\u0000\u0010admin_manage_all\u0007\u0000s\u0001\u0000,com/example/PermissionManager$PermissionRule\b\u0000u\u0001\u0000\u0017user_id != principal_id\t\u0000w\u0000y\u0007\u0000x\u0001\u0000.com/example/PermissionManager$PermissionEffect"
    },
    {
      "path": "target/classes/com/example/PermissionManager.class",
      "line": 44,
      "col": 170,
      "snippet": "adminPerms\u0001\u0000\u000fsuperAdminPerms\u0001\u0000\u0016LocalVariableTypeTable\u0001\u0000#Ljava/util/Set<Ljava/lang/String;>;\b\u0000q\u0001\u0000\u0010admin_manage_all\u0007\u0000s\u0001\u0000,com/example/PermissionManager$PermissionRule\b\u0000u\u0001\u0000\u0017user_id != principal_id\t\u0000w\u0000y\u0007\u0000x\u0001\u0000.com/example/PermissionManager$PermissionEffect",
      "context_before": "\u0000g\u0000h\u0001\u0000\u0006addAll\u0001\u0000\u0019(Ljava/util/Collection;)Z\u0001\u0000\tuserPerms\u0001\u0000\u000fLjava/util/Set;\u0001\u0000\nmanagerPerms\u0001\u0000",
      "context_after": "\u0000z\u0000{\u0001\u0000\u0005ALLOW\u0001\u00000Lcom/example/PermissionManager$PermissionEffect;\n\u0000r\u0000}"
    },
    {
      "path": "target/classes/com/example/PermissionManager.class",
      "line": 47,
      "col": 98,
      "snippet": "\u00006\u0000~\u0001\u0000U(Ljava/util/List;Ljava/lang/String;Lcom/example/PermissionManager$PermissionEffect;)V\b\u0000\u0001\u0000\u0010user_self_modify\b\u0000\u0001\u0000\u0017user_id == principal_id\b\u0000\u0001\u0000\u0018manager_department_users\b\u0000\u0001\u0000'user_department == principal_department\u0001\u0000",
      "context_before": "\u0000z\u0000{\u0001\u0000\u0005ALLOW\u0001\u00000Lcom/example/PermissionManager$PermissionEffect;\n\u0000r\u0000}",
      "context_after": "assignRole\u0001\u0000'(Ljava/lang/String;Ljava/lang/String;)V\u0012\u0000\u0000\u0000\n\u0000\u0000\u0001\u0000\u0005apply\u0001\u0000\u001f()Ljava/util/function/Function;"
    },
    {
      "path": "target/classes/com/example/PermissionManager.class",
      "line": 47,
      "col": 119,
      "snippet": "\u00006\u0000~\u0001\u0000U(Ljava/util/List;Ljava/lang/String;Lcom/example/PermissionManager$PermissionEffect;)V\b\u0000\u0001\u0000\u0010user_self_modify\b\u0000\u0001\u0000\u0017user_id == principal_id\b\u0000\u0001\u0000\u0018manager_department_users\b\u0000\u0001\u0000'user_department == principal_department\u0001\u0000",
      "context_before": "\u0000z\u0000{\u0001\u0000\u0005ALLOW\u0001\u00000Lcom/example/PermissionManager$PermissionEffect;\n\u0000r\u0000}",
      "context_after": "assignRole\u0001\u0000'(Ljava/lang/String;Ljava/lang/String;)V\u0012\u0000\u0000\u0000\n\u0000\u0000\u0001\u0000\u0005apply\u0001\u0000\u001f()Ljava/util/function/Function;"
    },
    {
      "path": "target/classes/com/example/PermissionManager.class",
      "line": 47,
      "col": 166,
      "snippet": "\u00006\u0000~\u0001\u0000U(Ljava/util/List;Ljava/lang/String;Lcom/example/PermissionManager$PermissionEffect;)V\b\u0000\u0001\u0000\u0010user_self_modify\b\u0000\u0001\u0000\u0017user_id == principal_id\b\u0000\u0001\u0000\u0018manager_department_users\b\u0000\u0001\u0000'user_department == principal_department\u0001\u0000",
      "context_before": "\u0000z\u0000{\u0001\u0000\u0005ALLOW\u0001\u00000Lcom/example/PermissionManager$PermissionEffect;\n\u0000r\u0000}",
      "context_after": "assignRole\u0001\u0000'(Ljava/lang/String;Ljava/lang/String;)V\u0012\u0000\u0000\u0000\n\u0000\u0000\u0001\u0000\u0005apply\u0001\u0000\u001f()Ljava/util/function/Function;"
    },
    {
      "path": "target/classes/com/example/PermissionManager.class",
      "line": 47,
      "col": 176,
      "snippet": "\u00006\u0000~\u0001\u0000U(Ljava/util/List;Ljava/lang/String;Lcom/example/PermissionManager$PermissionEffect;)V\b\u0000\u0001\u0000\u0010user_self_modify\b\u0000\u0001\u0000\u0017user_id == principal_id\b\u0000\u0001\u0000\u0018manager_department_users\b\u0000\u0001\u0000'user_department == principal_department\u0001\u0000",
      "context_before": "\u0000z\u0000{\u0001\u0000\u0005ALLOW\u0001\u00000Lcom/example/PermissionManager$PermissionEffect;\n\u0000r\u0000}",
      "context_after": "assignRole\u0001\u0000'(Ljava/lang/String;Ljava/lang/String;)V\u0012\u0000\u0000\u0000\n\u0000\u0000\u0001\u0000\u0005apply\u0001\u0000\u001f()Ljava/util/function/Function;"
    },
    {
      "path": "target/classes/com/example/PermissionManager.class",
      "line": 55,
      "col": 54,
      "snippet": "\u0000\u0000\u0001\u0000\u0015updateUserPermissions\u0001\u0000\u0015(Ljava/lang/String;)V\u0001\u0000\u0006userId\u0001\u0000\u0004role\u0001\u0000",
      "context_before": "\u0000\u0000\u0001\u0000\u0003add\u0001\u0000\u0015(Ljava/lang/Object;)Z\n\u0000\u0001\u0000",
      "context_after": "revokeRole\n\u0000^\u0000"
    },
    {
      "path": "target/classes/com/example/PermissionManager.class",
      "line": 74,
      "col": 1,
      "snippet": "userRoleSet\u0001\u0000\trolePerms\u0001\u0000\u0010hasAnyPermission\u0001\u0000+(Ljava/lang/String;Ljava/util/Collection;)Z\u0001\u0000?(Ljava/lang/String;Ljava/util/Collection<Ljava/lang/String;>;)Z",
      "context_before": "\u0000\u0000\u0001\u0000\u0007hasNext\u0001\u0000\u0003()Z\u0001\u0000\ndirectPerms\u0001\u0000",
      "context_after": "\u0000\u0000\u0007\u0000\u0001\u0000\u0014java/util/Collection\n\u0000\u0000\u0001\u0000\u0006stream\u0001\u0000\u001b()Ljava/util/stream/Stream;\u0012\u0000\u0002\u0000"
    },
    {
      "path": "target/classes/com/example/PermissionManager.class",
      "line": 120,
      "col": 19,
      "snippet": "\u0001.\u0000\u0001\u0000\u0006equals\b\u00010\u0001\u0000\u0007user_id\t\u0000r\u00012",
      "context_before": "\u0001+\u0000\u000e\u0001\u0000\tcondition\n\u0000R\u0001-",
      "context_after": "\u0001&\u0000{\t\u0000w\u00014\n\u00015\u0000{\u0001\u0000\u0007NEUTRAL\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/PermissionManager.class",
      "line": 135,
      "col": 6,
      "snippet": "\u0000\u0000\u0001\u0000\u0007userIds\u0001\u0000\u000ebulkRevokeRole",
      "context_before": "\u0001L\u0001M\u0001\u0000\u0007collect\u0001\u00000(Ljava/util/stream/Collector;)Ljava/lang/Object;\u0001\u0000\u0010getUsersWithRole\u0012\u0000\t\u0001\u0002\u0001\u0000\u000ebulkAssignRole\u0001\u0000+(Ljava/util/Collection;Ljava/lang/String;)V\u0001\u0000?(Ljava/util/Collection<Ljava/lang/String;>;Ljava/lang/String;)V\n\u0000\u0001\u0001T",
      "context_after": "\u0000\u0001\u0001X\n\u0000\u0000\u0001\u0000\blambda$0\u0001\u0000\u0001k\u0001\u0000\blambda$1\u0001\u0000\blambda$2\u0001\u0000\u0004perm\u0001\u0000\blambda$3\u0001\u0000\blambda$4\u0001\u0000\blambda$5\u0001\u0000*(Ljava/lang/String;Ljava/util/Map$Entry;)Z"
    },
    {
      "path": "target/classes/com/example/FactoryManager.class",
      "line": 21,
      "col": 45,
      "snippet": "StackMapTable\u0007\u0000/\u0001\u0000\u0013java/lang/Throwable\b\u00001\u0001\u0000\u0004user\u0007\u00003\u0001\u0000&com/example/FactoryManager$UserFactory",
      "context_before": "\u0000\u0005\u0000\u0006\n\u0000\u0001\u0000\u0015\u0001\u0000",
      "context_after": "\u00002\u0000\u0015\n\u0000\u0001\u00006"
    },
    {
      "path": "target/classes/com/example/FactoryManager.class",
      "line": 25,
      "col": 1,
      "snippet": "userService\u0007\u0000<\u0001\u0000-com/example/FactoryManager$UserServiceFactory",
      "context_before": "\u0000\u0001\u00006\n\u00007\u00008\u0001\u0000\u000fregisterFactory\u0001\u0000?(Ljava/lang/String;Lcom/example/FactoryManager$ObjectFactory;)V\b\u0000:\u0001\u0000",
      "context_after": "\u0000;\u0000\u0015\b\u0000?\u0001\u0000\u0011permissionManager\u0007\u0000A\u0001\u00003com/example/FactoryManager$PermissionManagerFactory\n\u0000@\u0000\u0015\b\u0000D\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/DecoratorManager$SecurityDecoratorFactory.class",
      "line": 4,
      "col": 289,
      "snippet": "\u0000\u0007\u0000\b\u0001\u0000\u000fLineNumberTable\u0001\u0000\u0012LocalVariableTable\u0001\u0000\u0004this\u0001\u00007Lcom/example/DecoratorManager$SecurityDecoratorFactory;\u0001\u0000\u0006create\u0001\u0000=([Ljava/lang/Object;)Lcom/example/DecoratorManager$Decorator;\u0001\u0000\tSignature\u0001\u0000@([Ljava/lang/Object;)Lcom/example/DecoratorManager$Decorator<*>;\u0007\u0000\u0015\u0001\u0000\u0010java/lang/String\b\u0000\u0017\u0001\u0000\u0004user\u0007\u0000\u0019\u0001\u0000.com/example/DecoratorManager$SecurityDecorator",
      "context_before": "\u0000\u0003\u0000\n",
      "context_after": "\u0000\u0018\u0000\u001b\n\u0000\u0007\u0000"
    },
    {
      "path": "target/classes/com/example/UserService$UserValidator.class",
      "line": 11,
      "col": 21,
      "snippet": "\u0001\u0000\bvalidate\u0001\u0000\u0003()Z\u0001\u0000\u0004user\u0001\u0000\u0012Lcom/example/User;\u0001\u0000",
      "context_before": "\u0000\n\u0000",
      "context_after": "StackMapTable\u0001\u0000\u000evalidateUserId\n\u0000#\u0000%\u0007\u0000$\u0001\u0000\u0010java/lang/String"
    },
    {
      "path": "target/classes/com/example/UserService$UserValidator.class",
      "line": 17,
      "col": 51,
      "snippet": "\u0001\u0000\u0007isEmpty\b\u0000,\u0001\u0000\u001fUser ID cannot be null or empty\u0001\u0000\u0006userId\u0001\u0000\u0012Ljava/lang/String;\u0001\u0000",
      "context_before": "\u0000#\u0000)\n\u0000*\u0000",
      "context_after": "SourceFile\u0001\u0000\u0010UserService.java\u0001\u0000\nInnerClasses\u0001\u0000\u0013ValidationException\u0007\u00004\u0001\u0000\u0017com/example/UserService\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/CommandManager$UserDeleteCommand.class",
      "line": 1,
      "col": 122,
      "snippet": "\u0000\u0000\u00007\u0000o\u0007\u0000\u0002\u0001\u0000,com/example/CommandManager$UserDeleteCommand\u0007\u0000\u0004\u0001\u0000\u0010java/lang/Object\u0007\u0000\u0006\u0001\u0000\"com/example/CommandManager$Command\u0001\u0000\u0006userId\u0001\u0000\u0010Ljava/lang/Long;\u0001\u0000",
      "context_before": "",
      "context_after": "deletedData\u0001\u0000\u000fLjava/util/Map;\u0001\u0000\tSignature\u0001\u00005Ljava/util/Map<Ljava/lang/String;Ljava/lang/Object;>;\u0001\u0000\bexecuted\u0001\u0000\u0001Z\u0001\u0000\u0006<init>\u0001\u0000\u0013(Ljava/lang/Long;)V\u0001\u0000\u0004Code\n\u0000\u0003\u0000\u0013"
    },
    {
      "path": "target/classes/com/example/CommandManager$UserDeleteCommand.class",
      "line": 8,
      "col": 50,
      "snippet": "Exceptions\u0007\u0000!\u0001\u0000\u0013java/lang/Exception\b\u0000#\u0001\u0000\u0002id\b\u0000%\u0001\u0000\busername\b\u0000'\u0001\u0000\btestuser\b\u0000)\u0001\u0000\u0005email\b\u0000+\u0001\u0000\u0010test@example.com",
      "context_before": "\u0000\u000e\t\u0000\u0001\u0000\u0018\n\u0000\u0007\u0000\b\u0001\u0000\u000fLineNumberTable\u0001\u0000\u0012LocalVariableTable\u0001\u0000\u0004this\u0001\u0000.Lcom/example/CommandManager$UserDeleteCommand;\u0001\u0000\u0007execute\u0001\u0000\u0014()Ljava/lang/Object;\u0001\u0000",
      "context_after": "\u0000-\u0000/\u0007\u0000.\u0001\u0000\njava/util/Map"
    },
    {
      "path": "target/classes/com/example/CommandManager$UserDeleteCommand.class",
      "line": 8,
      "col": 68,
      "snippet": "Exceptions\u0007\u0000!\u0001\u0000\u0013java/lang/Exception\b\u0000#\u0001\u0000\u0002id\b\u0000%\u0001\u0000\busername\b\u0000'\u0001\u0000\btestuser\b\u0000)\u0001\u0000\u0005email\b\u0000+\u0001\u0000\u0010test@example.com",
      "context_before": "\u0000\u000e\t\u0000\u0001\u0000\u0018\n\u0000\u0007\u0000\b\u0001\u0000\u000fLineNumberTable\u0001\u0000\u0012LocalVariableTable\u0001\u0000\u0004this\u0001\u0000.Lcom/example/CommandManager$UserDeleteCommand;\u0001\u0000\u0007execute\u0001\u0000\u0014()Ljava/lang/Object;\u0001\u0000",
      "context_after": "\u0000-\u0000/\u0007\u0000.\u0001\u0000\njava/util/Map"
    },
    {
      "path": "target/classes/com/example/CommandManager$UserDeleteCommand.class",
      "line": 22,
      "col": 1,
      "snippet": "user_delete\u0001\u0000",
      "context_before": "StackMapTable\u0001\u0000\nisUndoable\u0001\u0000\u0003()Z\u0001\u0000\u000egetDescription\u0001\u0000\u0014()Ljava/lang/String;\u0012\u0000\u0002\u0000A\u0001\u0000\u0007getType\b\u0000T\u0001\u0000",
      "context_after": "SourceFile\u0001\u0000\u0013CommandManager.java\u0001\u0000\u0010BootstrapMethods\n\u0000Y\u0000[\u0007\u0000Z\u0001\u0000$java/lang/invoke/StringConcatFactory"
    },
    {
      "path": "target/classes/com/example/CommandManager$UserDeleteCommand.class",
      "line": 26,
      "col": 44,
      "snippet": "User deletion undone for ID: \u0001\b\u0000c\u0001\u0000\u000eDelete user: \u0001\u0001\u0000",
      "context_before": "\u0000Y\u0000[\u0007\u0000Z\u0001\u0000$java/lang/invoke/StringConcatFactory\n\u0000B\u0000\\\u0001\u0000(Ljava/lang/invoke/MethodHandles$Lookup;Ljava/lang/String;Ljava/lang/invoke/MethodType;Ljava/lang/String;[Ljava/lang/Object;)Ljava/lang/invoke/CallSite;\u000f\u0006\u0000X\b\u0000_\u0001\u0000\u0012User deleted: ID \u0001\b\u0000a\u0001\u0000",
      "context_after": "InnerClasses\u0007\u0000f\u0001\u0000\u001acom/example/CommandManager\u0001\u0000\u0007Command\u0001\u0000\u0011UserDeleteCommand\u0007\u0000j\u0001\u0000%java/lang/invoke/MethodHandles$Lookup\u0007\u0000l\u0001\u0000\njava/lang/invoke/MethodHandles\u0001\u0000\u0006Lookup\u0001\u0000\bNestHost\u0000!\u0000\u0001\u0000\u0003\u0000\u0001\u0000\u0005\u0000\u0003\u0000\u0012\u0000\u0007\u0000\b\u0000\u0000\u0000\u0002\u0000\t\u0000"
    },
    {
      "path": "target/classes/com/example/AdapterManager$AuthenticationAdapter.class",
      "line": 13,
      "col": 17,
      "snippet": "\u0001\u0000\u0007println\b\u0000)\u0001\u0000\busername",
      "context_before": "\u0000$\u0000&\u0007\u0000%\u0001\u0000\u0013java/io/PrintStream\n\u0000'\u0000",
      "context_after": "\u0000+\u0000-\u0007\u0000,\u0001\u0000\njava/util/Map"
    },
    {
      "path": "target/classes/com/example/AdapterManager$AuthenticationAdapter.class",
      "line": 30,
      "col": 45,
      "snippet": "\u0000S\u0000T\u0001\u0000\btoString\u0001\u0000\u0014()Ljava/lang/String;\b\u0000V\u0001\u0000\u0007user_id\b\u0000X\u0001\u0000\u000512345\b\u0000Z\u0001\u0000\u0005roles\b\u0000\\\u0001\u0000\u0004user",
      "context_before": "randomUUID\u0001\u0000\u0012()Ljava/util/UUID;\n\u0000L\u0000R",
      "context_after": "\u0000^\u0000`\u0007\u0000_\u0001\u0000\u0010java/util/Arrays\n\u0000a\u0000b\u0001\u0000\u0006asList\u0001\u0000%([Ljava/lang/Object;)Ljava/util/List;\b\u0000d\u0001\u0000\u0005error\b\u0000f\u0001\u0000\u0013Invalid credentials\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/AdapterManager$AuthenticationAdapter.class",
      "line": 30,
      "col": 80,
      "snippet": "\u0000S\u0000T\u0001\u0000\btoString\u0001\u0000\u0014()Ljava/lang/String;\b\u0000V\u0001\u0000\u0007user_id\b\u0000X\u0001\u0000\u000512345\b\u0000Z\u0001\u0000\u0005roles\b\u0000\\\u0001\u0000\u0004user",
      "context_before": "randomUUID\u0001\u0000\u0012()Ljava/util/UUID;\n\u0000L\u0000R",
      "context_after": "\u0000^\u0000`\u0007\u0000_\u0001\u0000\u0010java/util/Arrays\n\u0000a\u0000b\u0001\u0000\u0006asList\u0001\u0000%([Ljava/lang/Object;)Ljava/util/List;\b\u0000d\u0001\u0000\u0005error\b\u0000f\u0001\u0000\u0013Invalid credentials\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/UserService$AuditEntry.class",
      "line": 1,
      "col": 126,
      "snippet": "\u0000\u0000\u00007\u0000/\u0007\u0000\u0002\u0001\u0000\"com/example/UserService$AuditEntry\u0007\u0000\u0004\u0001\u0000\u0010java/lang/Object\u0001\u0000\toperation\u0001\u0000'Lcom/example/UserService$OperationType;\u0001\u0000\u0006userId\u0001\u0000\u0012Ljava/lang/String;\u0001\u0000\u0007details\u0001\u0000\ttimestamp\u0001\u0000\u0019Ljava/time/LocalDateTime;\u0001\u0000\u0006<init>\u0001\u0000g(Lcom/example/UserService$OperationType;Ljava/lang/String;Ljava/lang/String;Ljava/time/LocalDateTime;)V\u0001\u0000\u0004Code",
      "context_before": "",
      "context_after": "\u0000\u0003\u0000\u0010\n\u0000"
    },
    {
      "path": "target/classes/com/example/CommandManager$UserUpdateCommandFactory.class",
      "line": 7,
      "col": 76,
      "snippet": "\u0000\u0007\u0000\u001a\u0001\u0000\"(Ljava/lang/Long;Ljava/util/Map;)V\u0001\u0000\u0006params\u0001\u0000\u0013[Ljava/lang/Object;\u0001\u0000\u0006userId\u0001\u0000\u0010Ljava/lang/Long;\u0001\u0000\u0007updates\u0001\u0000\u000fLjava/util/Map;\u0001\u0000\u0016LocalVariableTypeTable\u0001\u00005Ljava/util/Map<Ljava/lang/String;Ljava/lang/Object;>;\u0001\u0000",
      "context_before": "java/util/Map\u0007\u0000\u0017\u0001\u0000,com/example/CommandManager$UserUpdateCommand\n\u0000\u0016\u0000\u0019",
      "context_after": "SourceFile\u0001\u0000\u0013CommandManager.java\u0001\u0000\nInnerClasses\u0007\u0000'\u0001\u0000\"com/example/CommandManager$Command\u0007\u0000)\u0001\u0000\u001acom/example/CommandManager\u0001\u0000\u0007Command\u0001\u0000\u000eCommandFactory\u0001\u0000\u0011UserUpdateCommand\u0001\u0000\u0018UserUpdateCommandFactory\u0001\u0000\bNestHost\u0000!\u0000\u0001\u0000\u0003\u0000\u0001\u0000\u0005\u0000\u0000\u0000\u0002\u0000\u0001\u0000\u0007\u0000\b\u0000\u0001\u0000\t\u0000\u0000\u0000/\u0000\u0001\u0000\u0001\u0000\u0000\u0000\u0005*\u0000"
    },
    {
      "path": "target/classes/com/example/ReportGenerator$DepartmentData.class",
      "line": 1,
      "col": 108,
      "snippet": "\u0000\u0000\u00007\u0000(\u0007\u0000\u0002\u0001\u0000*com/example/ReportGenerator$DepartmentData\u0007\u0000\u0004\u0001\u0000\u0010java/lang/Object\u0001\u0000\u0004name\u0001\u0000\u0012Ljava/lang/String;\u0001\u0000\tuserCount\u0001\u0000\u0001I\u0001\u0000",
      "context_before": "",
      "context_after": "activityLevel\u0001\u0000\u0010performanceScore\u0001\u0000\u0001D\u0001\u0000\nopenIssues\u0001\u0000\u0006<init>\u0001\u0000*(Ljava/lang/String;ILjava/lang/String;DI)V\u0001\u0000\u0004Code"
    },
    {
      "path": "target/classes/com/example/FactoryManager$DefaultReportDataProvider.class",
      "line": 4,
      "col": 406,
      "snippet": "\u0000\u0007\u0000\b\u0001\u0000\u000fLineNumberTable\u0001\u0000\u0012LocalVariableTable\u0001\u0000\u0004this\u0001\u00006Lcom/example/FactoryManager$DefaultReportDataProvider;\u0001\u0000\u0011getUserActivities\u0001\u0000N(Ljava/time/LocalDate;Ljava/time/LocalDate;Ljava/lang/String;)Ljava/util/List;\u0001\u0000\tSignature\u0001\u0000~(Ljava/time/LocalDate;Ljava/time/LocalDate;Ljava/lang/String;)Ljava/util/List<Lcom/example/ReportGenerator$UserActivityData;>;\u0007\u0000\u0015\u0001\u0000,com/example/ReportGenerator$UserActivityData\b\u0000\u0017\u0001\u0000\u0005user1",
      "context_before": "\u0000\u0003\u0000\n",
      "context_after": "\u0000\u0019\u0000\u001b\u0007\u0000\u001a\u0001\u0000\u0017java/time/LocalDateTime\n\u0000"
    },
    {
      "path": "target/classes/com/example/FactoryManager$DefaultReportDataProvider.class",
      "line": 10,
      "col": 63,
      "snippet": "\u0000\u0007\u0000\"\u0001\u00001(Ljava/lang/String;ILjava/time/LocalDateTime;JI)V\b\u0000$\u0001\u0000\u0005user2",
      "context_before": "\u0001\u0000\u0003now\u0001\u0000\u001b()Ljava/time/LocalDateTime;\u0005\u0000\u0000\u0000\u0000\u00006\n\u0000\u0014\u0000!",
      "context_after": "\u0000\u0019\u0000&\n\u0000'\u0000(\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/FactoryManager$DefaultReportDataProvider.class",
      "line": 30,
      "col": 111,
      "snippet": "\u0000\u0007\u0000s\u0001\u0000d(Ljava/time/LocalDateTime;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)V\u0001\u0000\u0006userId\u0001\u0000\teventType\u0001\u0000\u0011getDepartmentData\u0001\u0000\u0012()Ljava/util/List;\u0001\u0000@()Ljava/util/List<Lcom/example/ReportGenerator$DepartmentData;>;\u0007\u0000z\u0001\u0000*com/example/ReportGenerator$DepartmentData\b\u0000|\u0001\u0000",
      "context_before": "\u0000\u0007\u0000e\u0001\u0000X(Ljava/lang/String;Ljava/math/BigDecimal;Ljava/math/BigDecimal;Ljava/math/BigDecimal;D)V\u0001\u0000\u000egetAuditEvents\u0001\u0000h(Ljava/time/LocalDateTime;Ljava/time/LocalDateTime;Ljava/lang/String;Ljava/lang/String;)Ljava/util/List;\u0001\u0000(Ljava/time/LocalDateTime;Ljava/time/LocalDateTime;Ljava/lang/String;Ljava/lang/String;)Ljava/util/List<Lcom/example/ReportGenerator$AuditEventData;>;\u0007\u0000j\u0001\u0000*com/example/ReportGenerator$AuditEventData\b\u0000l\u0001\u0000\u0005LOGIN\b\u0000n\u0001\u0000\u000eauthentication\b\u0000p\u0001\u0000\u000eUser logged in\n\u0000i\u0000r",
      "context_after": "Engineering\b\u0000~\u0001\u0000\u0004High\u0006@U`\u0000\u0000\u0000\u0000\u0000\n\u0000y\u0000"
    },
    {
      "path": "target/classes/com/example/User$Builder.class",
      "line": 38,
      "col": 25,
      "snippet": "\u0000^\u0000_\u0001\u0000\bvalidate\u0001\u0000\u0003()Z\u0001\u0000\u0004user\u0001\u0000\u0012Lcom/example/User;\u0001\u0000",
      "context_before": "setMetadata\u0001\u0000\u0012(Ljava/util/Map;)V\n\u0000O\u0000]",
      "context_after": "SourceFile\u0001\u0000\tUser.java\u0001\u0000\nInnerClasses\u0001\u0000\u0007Builder\u0001\u0000\u0013ValidationException\u0001\u0000\bNestHost\u0000!\u0000\u0001\u0000\u0003\u0000\u0000\u0000\u0007\u0000\u0002\u0000\u0005\u0000\u0006\u0000\u0000\u0000\u0002\u0000\u0007\u0000\u0006\u0000\u0000\u0000\u0002\u0000\b\u0000\u0006\u0000\u0000\u0000\u0002\u0000\t\u0000"
    },
    {
      "path": "target/classes/com/example/DecoratorManager$SecurityDecorator.class",
      "line": 14,
      "col": 46,
      "snippet": "\u00009\u0000:\u0001\u0000\u0007valueOf\u0001\u0000\u0016(I)Ljava/lang/Integer;\b\u0000<\u0001\u0000\u0004user\b\u0000>\u0001\u0000\tmoderator\b\u0000@\u0001\u0000",
      "context_before": "hasPermission\u0001\u0000'(Ljava/lang/String;Ljava/lang/String;)Z\b\u00004\u0001\u0000\u0005guest\n\u00006\u00008\u0007\u00007\u0001\u0000\u0011java/lang/Integer",
      "context_after": "superadmin\n\u0000B\u0000D\u0007\u0000C\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/DecoratorManager$SecurityDecorator.class",
      "line": 23,
      "col": 25,
      "snippet": "\u0000M\u0000N\u0001\u0000\bintValue\u0001\u0000\u0003()I\u0001\u0000\buserRole\u0001\u0000",
      "context_before": "getOrDefault\u0001\u00008(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;\n\u00006\u0000L",
      "context_after": "roleHierarchy\u0001\u0000\u000fLjava/util/Map;\u0001\u0000\tuserLevel\u0001\u0000\u0013Ljava/lang/Integer;\u0001\u0000\nrequiredLevel\u0001\u00006Ljava/util/Map<Ljava/lang/String;Ljava/lang/Integer;>;\u0001\u0000\blambda$0\u0001\u0000C(Ljava/util/function/Function;Ljava/lang/Object;)Ljava/lang/Object;"
    },
    {
      "path": "target/classes/com/example/DecoratorManager$SecurityDecorator.class",
      "line": 24,
      "col": 35,
      "snippet": "roleHierarchy\u0001\u0000\u000fLjava/util/Map;\u0001\u0000\tuserLevel\u0001\u0000\u0013Ljava/lang/Integer;\u0001\u0000",
      "context_before": "\u00006\u0000L\n\u0000M\u0000N\u0001\u0000\bintValue\u0001\u0000\u0003()I\u0001\u0000\buserRole\u0001\u0000",
      "context_after": "requiredLevel\u0001\u00006Ljava/util/Map<Ljava/lang/String;Ljava/lang/Integer;>;\u0001\u0000\blambda$0\u0001\u0000C(Ljava/util/function/Function;Ljava/lang/Object;)Ljava/lang/Object;\n\u0000\u0001\u0000Y"
    },
    {
      "path": "target/classes/com/example/AuditLogger$FileAuditHandler.class",
      "line": 16,
      "col": 8,
      "snippet": "\u0000.\u0000\b\u0001\u0000\u0006userId\t\u0000\u001b\u00000",
      "context_before": "\u0000'\u0000)\u0007\u0000(\u0001\u0000\u0017java/time/LocalDateTime\n\u0000*\u0000+\u0001\u0000\u0006format\u0001\u00008(Ljava/time/format/DateTimeFormatter;)Ljava/lang/String;\t\u0000\u001b\u0000-",
      "context_after": "\u00001\u00002\u0001\u0000\teventType\u0001\u0000(Lcom/example/AuditLogger$AuditEventType;\n\u00004\u00006\u0007\u00005\u0001\u0000&com/example/AuditLogger$AuditEventType"
    },
    {
      "path": "target/classes/com/example/CommandManager$UserUpdateCommand.class",
      "line": 1,
      "col": 122,
      "snippet": "\u0000\u0000\u00007\u0000y\u0007\u0000\u0002\u0001\u0000,com/example/CommandManager$UserUpdateCommand\u0007\u0000\u0004\u0001\u0000\u0010java/lang/Object\u0007\u0000\u0006\u0001\u0000\"com/example/CommandManager$Command\u0001\u0000\u0006userId\u0001\u0000\u0010Ljava/lang/Long;\u0001\u0000\u0007updates\u0001\u0000\u000fLjava/util/Map;\u0001\u0000\tSignature\u0001\u00005Ljava/util/Map<Ljava/lang/String;Ljava/lang/Object;>;\u0001\u0000\u0007oldData\u0001\u0000\bexecuted\u0001\u0000\u0001Z\u0001\u0000\u0006<init>\u0001\u0000\"(Ljava/lang/Long;Ljava/util/Map;)V\u0001\u0000H(Ljava/lang/Long;Ljava/util/Map<Ljava/lang/String;Ljava/lang/Object;>;)V\u0001\u0000\u0004Code",
      "context_before": "",
      "context_after": "\u0000\u0003\u0000\u0015\n\u0000\u0010\u0000\u0016\u0001\u0000\u0003()V\t\u0000\u0001\u0000\u0018"
    },
    {
      "path": "target/classes/com/example/CommandManager$UserUpdateCommand.class",
      "line": 12,
      "col": 42,
      "snippet": "Exceptions\u0007\u0000+\u0001\u0000\u0013java/lang/Exception\b\u0000-\u0001\u0000\busername\b\u0000/\u0001\u0000\u0007olduser\b\u00001\u0001\u0000\u0005email\b\u00003\u0001\u0000\u000fold@example.com",
      "context_before": "\u0000\t\u0000\n\u0001\u0000\u000fLineNumberTable\u0001\u0000\u0012LocalVariableTable\u0001\u0000\u0004this\u0001\u0000.Lcom/example/CommandManager$UserUpdateCommand;\u0001\u0000\u0016LocalVariableTypeTable\u0001\u0000\u0007execute\u0001\u0000\u0014()Ljava/lang/Object;\u0001\u0000",
      "context_after": "\u00005\u00007\u0007\u00006\u0001\u0000\njava/util/Map"
    },
    {
      "path": "target/classes/com/example/CommandManager$UserUpdateCommand.class",
      "line": 12,
      "col": 59,
      "snippet": "Exceptions\u0007\u0000+\u0001\u0000\u0013java/lang/Exception\b\u0000-\u0001\u0000\busername\b\u0000/\u0001\u0000\u0007olduser\b\u00001\u0001\u0000\u0005email\b\u00003\u0001\u0000\u000fold@example.com",
      "context_before": "\u0000\t\u0000\n\u0001\u0000\u000fLineNumberTable\u0001\u0000\u0012LocalVariableTable\u0001\u0000\u0004this\u0001\u0000.Lcom/example/CommandManager$UserUpdateCommand;\u0001\u0000\u0016LocalVariableTypeTable\u0001\u0000\u0007execute\u0001\u0000\u0014()Ljava/lang/Object;\u0001\u0000",
      "context_after": "\u00005\u00007\u0007\u00006\u0001\u0000\njava/util/Map"
    },
    {
      "path": "target/classes/com/example/CommandManager$UserUpdateCommand.class",
      "line": 28,
      "col": 1,
      "snippet": "user_update\u0001\u0000",
      "context_before": "StackMapTable\u0001\u0000\nisUndoable\u0001\u0000\u0003()Z\u0001\u0000\u000egetDescription\u0001\u0000\u0014()Ljava/lang/String;\u0012\u0000\u0002\u0000T\u0001\u0000\u0007getType\b\u0000^\u0001\u0000",
      "context_after": "SourceFile\u0001\u0000\u0013CommandManager.java\u0001\u0000\u0010BootstrapMethods\n\u0000c\u0000e\u0007\u0000d\u0001\u0000$java/lang/invoke/StringConcatFactory"
    },
    {
      "path": "target/classes/com/example/CommandManager$UserUpdateCommand.class",
      "line": 32,
      "col": 42,
      "snippet": "User update undone for ID: \u0001\b\u0000m\u0001\u0000\u000eUpdate user: \u0001\u0001\u0000",
      "context_before": "\u0000c\u0000e\u0007\u0000d\u0001\u0000$java/lang/invoke/StringConcatFactory\n\u0000J\u0000f\u0001\u0000(Ljava/lang/invoke/MethodHandles$Lookup;Ljava/lang/String;Ljava/lang/invoke/MethodType;Ljava/lang/String;[Ljava/lang/Object;)Ljava/lang/invoke/CallSite;\u000f\u0006\u0000b\b\u0000i\u0001\u0000\u0019User updated: ID \u0001 with \u0001\b\u0000k\u0001\u0000",
      "context_after": "InnerClasses\u0007\u0000p\u0001\u0000\u001acom/example/CommandManager\u0001\u0000\u0007Command\u0001\u0000\u0011UserUpdateCommand\u0007\u0000t\u0001\u0000%java/lang/invoke/MethodHandles$Lookup\u0007\u0000v\u0001\u0000\njava/lang/invoke/MethodHandles\u0001\u0000\u0006Lookup\u0001\u0000\bNestHost\u0000!\u0000\u0001\u0000\u0003\u0000\u0001\u0000\u0005\u0000\u0004\u0000\u0012\u0000\u0007\u0000\b\u0000\u0000\u0000\u0012\u0000\t\u0000"
    },
    {
      "path": "target/classes/com/example/FactoryManager$UserServiceFactory.class",
      "line": 10,
      "col": 1,
      "snippet": "userService\u0001\u0000\u0019Lcom/example/UserService;\u0001\u0000\u0006config\u0001\u0000\u000fLjava/util/Map;\u0001\u0000\u0016LocalVariableTypeTable\u0001\u00005Ljava/util/Map<Ljava/lang/String;Ljava/lang/Object;>;\u0001\u0000",
      "context_before": "\u0000\u0001\u0000\u0018\n\u0000\u0019\u0000\u001a\u0001\u0000\u0014configureUserService\u0001\u0000+(Lcom/example/UserService;Ljava/util/Map;)V\u0001\u0000\u0004args\u0001\u0000\u0013[Ljava/lang/Object;\u0001\u0000",
      "context_after": "StackMapTable\u0001\u0000\tSignature\u0001\u0000Q(Lcom/example/UserService;Ljava/util/Map<Ljava/lang/String;Ljava/lang/Object;>;)V\b\u0000'\u0001\u0000\nenableCache"
    },
    {
      "path": "target/classes/com/example/EventSystem.class",
      "line": 30,
      "col": 1,
      "snippet": "user.created",
      "context_before": "\u0000\u0001\u0000\u0019\u0001\u0000\nStackMapTable\u0007\u0000@\u0001\u0000\u0013java/lang/Throwable\b\u0000B\u0001\u0000",
      "context_after": "\u0000\u0001\u0000D\n\u0000E\u0000F\u0001\u0000\u0011registerEventType\u0001\u0000\u0015(Ljava/lang/String;)V\b\u0000H\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/EventSystem.class",
      "line": 33,
      "col": 1,
      "snippet": "user.updated\b\u0000J\u0001\u0000",
      "context_before": "\u0000\u0001\u0000D\n\u0000E\u0000F\u0001\u0000\u0011registerEventType\u0001\u0000\u0015(Ljava/lang/String;)V\b\u0000H\u0001\u0000",
      "context_after": "user.deleted\b\u0000L\u0001\u0000\nuser.login\b\u0000N\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/EventSystem.class",
      "line": 34,
      "col": 1,
      "snippet": "user.deleted\b\u0000L\u0001\u0000",
      "context_before": "\u0000E\u0000F\u0001\u0000\u0011registerEventType\u0001\u0000\u0015(Ljava/lang/String;)V\b\u0000H\u0001\u0000\nuser.updated\b\u0000J\u0001\u0000",
      "context_after": "user.login\b\u0000N\u0001\u0000\nuser.logout\b\u0000P\u0001\u0000\u000esystem.startup\b\u0000R\u0001\u0000\u000fsystem.shutdown\b\u0000T\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/EventSystem.class",
      "line": 35,
      "col": 1,
      "snippet": "user.login\b\u0000N\u0001\u0000",
      "context_before": "user.updated\b\u0000J\u0001\u0000\nuser.deleted\b\u0000L\u0001\u0000",
      "context_after": "user.logout\b\u0000P\u0001\u0000\u000esystem.startup\b\u0000R\u0001\u0000\u000fsystem.shutdown\b\u0000T\u0001\u0000\nsystem.error\b\u0000V\u0001\u0000\u000edata.processed\b\u0000X\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/EventSystem.class",
      "line": 36,
      "col": 1,
      "snippet": "user.logout\b\u0000P\u0001\u0000\u000esystem.startup\b\u0000R\u0001\u0000\u000fsystem.shutdown\b\u0000T\u0001\u0000",
      "context_before": "user.deleted\b\u0000L\u0001\u0000\nuser.login\b\u0000N\u0001\u0000",
      "context_after": "system.error\b\u0000V\u0001\u0000\u000edata.processed\b\u0000X\u0001\u0000\ndata.exported\b\u0000Z\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/ReportGenerator$UserActivityData.class",
      "line": 1,
      "col": 82,
      "snippet": "\u0000\u0000\u00007\u0000)\u0007\u0000\u0002\u0001\u0000,com/example/ReportGenerator$UserActivityData\u0007\u0000\u0004\u0001\u0000\u0010java/lang/Object\u0001\u0000\u0006userId\u0001\u0000\u0012Ljava/lang/String;\u0001\u0000",
      "context_before": "",
      "context_after": "loginCount\u0001\u0000\u0001I\u0001\u0000\tlastLogin\u0001\u0000\u0019Ljava/time/LocalDateTime;\u0001\u0000\u0010totalTimeMinutes\u0001\u0000\u0001J\u0001\u0000\nactionCount\u0001\u0000\u0006<init>\u0001\u00001(Ljava/lang/String;ILjava/time/LocalDateTime;JI)V\u0001\u0000\u0004Code"
    },
    {
      "path": "target/classes/com/example/ReportGenerator$AuditEventData.class",
      "line": 1,
      "col": 120,
      "snippet": "\u0000\u0000\u00007\u0000'\u0007\u0000\u0002\u0001\u0000*com/example/ReportGenerator$AuditEventData\u0007\u0000\u0004\u0001\u0000\u0010java/lang/Object\u0001\u0000\ttimestamp\u0001\u0000\u0019Ljava/time/LocalDateTime;\u0001\u0000\u0006userId\u0001\u0000\u0012Ljava/lang/String;\u0001\u0000\u0006action\u0001\u0000\bresource\u0001\u0000\u0007details\u0001\u0000\u0006<init>\u0001\u0000d(Ljava/time/LocalDateTime;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)V\u0001\u0000\u0004Code",
      "context_before": "",
      "context_after": "\u0000\u0003\u0000\u0010\n\u0000"
    },
    {
      "path": "target/classes/com/example/CommandManager$UserLoginCommand.class",
      "line": 1,
      "col": 121,
      "snippet": "\u0000\u0000\u00007\u0000s\u0007\u0000\u0002\u0001\u0000+com/example/CommandManager$UserLoginCommand\u0007\u0000\u0004\u0001\u0000\u0010java/lang/Object\u0007\u0000\u0006\u0001\u0000\"com/example/CommandManager$Command\u0001\u0000\busername\u0001\u0000\u0012Ljava/lang/String;\u0001\u0000\bpassword\u0001\u0000",
      "context_before": "",
      "context_after": "sessionToken\u0001\u0000\bexecuted\u0001\u0000\u0001Z\u0001\u0000\u0006<init>\u0001\u0000'(Ljava/lang/String;Ljava/lang/String;)V\u0001\u0000\u0004Code\n\u0000\u0003\u0000\u0011"
    },
    {
      "path": "target/classes/com/example/CommandManager$UserLoginCommand.class",
      "line": 31,
      "col": 1,
      "snippet": "user_login\u0001\u0000",
      "context_before": "\u0000?\u0000Q\u0001\u0000&(Ljava/lang/String;)Ljava/lang/String;\u0001\u0000\nisUndoable\u0001\u0000\u0003()Z\u0001\u0000\u000egetDescription\u0012\u0000\u0002\u0000P\u0001\u0000\u0007getType\b\u0000X\u0001\u0000",
      "context_after": "SourceFile\u0001\u0000\u0013CommandManager.java\u0001\u0000\u0010BootstrapMethods\n\u0000]\u0000_\u0007\u0000^\u0001\u0000$java/lang/invoke/StringConcatFactory"
    },
    {
      "path": "target/classes/com/example/CommandManager$UserLoginCommand.class",
      "line": 36,
      "col": 7,
      "snippet": "Login user: \u0001\u0001\u0000",
      "context_before": "\u0000?\u0000`\u0001\u0000(Ljava/lang/invoke/MethodHandles$Lookup;Ljava/lang/String;Ljava/lang/invoke/MethodType;Ljava/lang/String;[Ljava/lang/Object;)Ljava/lang/invoke/CallSite;\u000f\u0006\u0000\\\b\u0000c\u0001\u0000\nUser logged in: \u0001, Session: \u0001\b\u0000e\u0001\u0000 User login undone for session: \u0001\b\u0000g\u0001\u0000",
      "context_after": "InnerClasses\u0007\u0000j\u0001\u0000\u001acom/example/CommandManager\u0001\u0000\u0007Command\u0001\u0000\u0010UserLoginCommand\u0007\u0000n\u0001\u0000%java/lang/invoke/MethodHandles$Lookup\u0007\u0000p\u0001\u0000\njava/lang/invoke/MethodHandles\u0001\u0000\u0006Lookup\u0001\u0000\bNestHost\u0000!\u0000\u0001\u0000\u0003\u0000\u0001\u0000\u0005\u0000\u0004\u0000\u0012\u0000\u0007\u0000\b\u0000\u0000\u0000\u0012\u0000\t\u0000\b\u0000\u0000\u0000\u0002\u0000"
    },
    {
      "path": "target/classes/com/example/UserService$UserStatistics.class",
      "line": 51,
      "col": 6,
      "snippet": "\u0000\u000e\u0001\u0000\u0005users\u0001\u0000\u0010Ljava/util/List;\u0001\u0000\u0016LocalVariableTypeTable\u0001\u0000$Ljava/util/List<Lcom/example/User;>;\u0001\u0000",
      "context_before": "\u0000v\u0000w\u0001\u0000\u0006orElse\u0001\u0000\u0004(D)D\t\u0000\u0001\u0000y\n\u0000",
      "context_after": "getTotalUsers\u0001\u0000\u000egetActiveUsers\u0001\u0000\u0013getDepartmentCounts\u0001\u0000\u0011()Ljava/util/Map;\u0001\u00008()Ljava/util/Map<Ljava/lang/String;Ljava/lang/Integer;>;\n\u0000\u0016\u0000"
    },
    {
      "path": "target/classes/com/example/UserService$UserStatistics.class",
      "line": 60,
      "col": 41,
      "snippet": "\u0000\u0000\u0001\u0000\bcontains\u0001\u0000\u0015(Ljava/lang/Object;)Z\u0001\u0000\u0004user\u0001\u0000\u0012Lcom/example/User;\u0001\u0000",
      "context_before": "\u0000\u0000\u0007\u0000\u0001\u0000\njava/util/Set",
      "context_after": "StackMapTable\u0001\u0000\blambda$2\u0001\u0000\u0015(Lcom/example/User;)I\u0001\u0000\blambda$3\u0001\u0000-(Lcom/example/User;)Ljava/util/stream/Stream;\n\u0000\u0000"
    },
    {
      "path": "target/classes/com/example/AuditLogger.class",
      "line": 89,
      "col": 6,
      "snippet": "\u0000\u0000\u0001\u0000\u0006userId\u0001\u0000\u0012Ljava/lang/String;\u0001\u0000\teventType\u0001\u0000(Lcom/example/AuditLogger$AuditEventType;\u0001\u0000\bresource\u0001\u0000\u0006action\u0001\u0000\bseverity\u0001\u0000'Lcom/example/AuditLogger$AuditSeverity;\u0001\u0000\u0007details\u0001\u0000",
      "context_before": "\u00005\u0000\u0001\u0000(Ljava/lang/String;Ljava/time/LocalDateTime;Ljava/lang/String;Lcom/example/AuditLogger$AuditEventType;Ljava/lang/String;Ljava/lang/String;Lcom/example/AuditLogger$AuditSeverity;Ljava/lang/String;Ljava/util/Map;)V\n\u0000\u0001\u0000",
      "context_after": "logUserLogin\u0001\u0000((Ljava/lang/String;Ljava/lang/String;Z)V\b\u0000\u0001\u0000&Login attempt from IP: %s, Success: %s\n\u0000\u0000\u0007\u0000\u0001\u0000\u0011java/lang/Boolean"
    },
    {
      "path": "target/classes/com/example/AuditLogger.class",
      "line": 104,
      "col": 70,
      "snippet": "logUserCreate\u0001\u0000'(Ljava/lang/String;Ljava/lang/String;)V\b\u0001\u0017\u0001\u0000\u0010Created user: %s\t\u0000\u0001\u0019",
      "context_before": "\u0001\u000f\u0000\u0001\u0000\nUSER_LOGOUT\b\u0001\u0011\u0001\u0000\u0006logout\b\u0001\u0013\u0001\u0000\u000fUser logged out\u0001\u0000",
      "context_after": "\u0001\u001a\u0000\u0001\u0000\nUSER_CREATE\b\u0001"
    },
    {
      "path": "target/classes/com/example/AuditLogger.class",
      "line": 107,
      "col": 4,
      "snippet": "\u0001\u0000\u000fuser_management\b\u0001",
      "context_before": "\u0001\u001a\u0000\u0001\u0000\nUSER_CREATE\b\u0001",
      "context_after": "\u0001\u0000\ncreate_user\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/AuditLogger.class",
      "line": 109,
      "col": 8,
      "snippet": "create_user\u0001\u0000",
      "context_before": "\u0001\u0000\u000fuser_management\b\u0001\n\u0001\u0000",
      "context_after": "createdUserId\u0001\u0000\nlogUserUpdate\u0001\u00009(Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)V\b\u0001#\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/AuditLogger.class",
      "line": 112,
      "col": 9,
      "snippet": "Updated user: %s, Changes: %s\t\u0000\u0001%",
      "context_before": "createdUserId\u0001\u0000\nlogUserUpdate\u0001\u00009(Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)V\b\u0001#\u0001\u0000",
      "context_after": "\u0001&\u0000\u0001\u0000\nUSER_UPDATE\b\u0001(\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/AuditLogger.class",
      "line": 115,
      "col": 8,
      "snippet": "update_user\u0001\u0000",
      "context_before": "\u0001&\u0000\u0001\u0000\nUSER_UPDATE\b\u0001(\u0001\u0000",
      "context_after": "updatedUserId\u0001\u0000\u0007changes\u0001\u0000\nlogUserDelete\b\u0001-\u0001\u0000\u0010Deleted user: %s\t\u0000\u0001/"
    },
    {
      "path": "target/classes/com/example/AuditLogger.class",
      "line": 117,
      "col": 28,
      "snippet": "logUserDelete\b\u0001-\u0001\u0000\u0010Deleted user: %s\t\u0000\u0001/",
      "context_before": "update_user\u0001\u0000\nupdatedUserId\u0001\u0000\u0007changes\u0001\u0000",
      "context_after": "\u00010\u0000\u0001\u0000\nUSER_DELETE\b\u00012\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/AuditLogger.class",
      "line": 120,
      "col": 8,
      "snippet": "delete_user\t\u0001\u0001\u00014",
      "context_before": "\u00010\u0000\u0001\u0000\nUSER_DELETE\b\u00012\u0001\u0000",
      "context_after": "\u00015\u0000\u0001\u0000\u0004HIGH\u0001\u0000\ndeletedUserId\u0001\u0000\u0013logPermissionChange\u0001\u0000](Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)V\b\u0001:\u0001\u00000Permission change for user %s: %s %s, Reason: %s\t\u0000\u0001<"
    },
    {
      "path": "target/classes/com/example/AuditLogger.class",
      "line": 122,
      "col": 160,
      "snippet": "deletedUserId\u0001\u0000\u0013logPermissionChange\u0001\u0000](Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)V\b\u0001:\u0001\u00000Permission change for user %s: %s %s, Reason: %s\t\u0000\u0001<",
      "context_before": "delete_user\t\u0001\u0001\u00014\n\u00015\u0000\u0001\u0000\u0004HIGH\u0001\u0000",
      "context_after": "\u0001=\u0000\u0001\u0000\u0011PERMISSION_CHANGE\b\u0001?\u0001\u0000\u0015permission_management\b\u0001A\u0001\u0000\u0011change_permission\u0001\u0000\ntargetUserId\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/CommandManager$UserDeleteCommandFactory.class",
      "line": 6,
      "col": 61,
      "snippet": "\u0000\u0007\u0000\u0018\u0001\u0000\u0013(Ljava/lang/Long;)V\u0001\u0000\u0006params\u0001\u0000\u0013[Ljava/lang/Object;\u0001\u0000\u0006userId\u0001\u0000\u0010Ljava/lang/Long;\u0001\u0000",
      "context_before": "\u0000\u0007\u0000\b\u0001\u0000\u000fLineNumberTable\u0001\u0000\u0012LocalVariableTable\u0001\u0000\u0004this\u0001\u00005Lcom/example/CommandManager$UserDeleteCommandFactory;\u0001\u0000\u0006create\u0001\u00009([Ljava/lang/Object;)Lcom/example/CommandManager$Command;\u0007\u0000\u0013\u0001\u0000\u000ejava/lang/Long\u0007\u0000\u0015\u0001\u0000,com/example/CommandManager$UserDeleteCommand\n\u0000\u0014\u0000\u0017",
      "context_after": "SourceFile\u0001\u0000\u0013CommandManager.java\u0001\u0000\nInnerClasses\u0007\u0000!\u0001\u0000\"com/example/CommandManager$Command\u0007\u0000#\u0001\u0000\u001acom/example/CommandManager\u0001\u0000\u0007Command\u0001\u0000\u000eCommandFactory\u0001\u0000\u0011UserDeleteCommand\u0001\u0000\u0018UserDeleteCommandFactory\u0001\u0000\bNestHost\u0000!\u0000\u0001\u0000\u0003\u0000\u0001\u0000\u0005\u0000\u0000\u0000\u0002\u0000\u0001\u0000\u0007\u0000\b\u0000\u0001\u0000\t\u0000\u0000\u0000/\u0000\u0001\u0000\u0001\u0000\u0000\u0000\u0005*\u0000"
    },
    {
      "path": "target/classes/com/example/CommandManager.class",
      "line": 44,
      "col": 1,
      "snippet": "user_create\u0007\u0000p\u0001\u00003com/example/CommandManager$UserCreateCommandFactory",
      "context_before": "data_query\u0007\u0000k\u0001\u00002com/example/CommandManager$DataQueryCommandFactory\n\u0000j\u0000\u0019\b\u0000n\u0001\u0000",
      "context_after": "\u0000o\u0000\u0019\b\u0000s\u0001\u0000\nuser_update\u0007\u0000u\u0001\u00003com/example/CommandManager$UserUpdateCommandFactory"
    },
    {
      "path": "target/classes/com/example/CommandManager.class",
      "line": 46,
      "col": 1,
      "snippet": "user_update\u0007\u0000u\u0001\u00003com/example/CommandManager$UserUpdateCommandFactory",
      "context_before": "user_create\u0007\u0000p\u0001\u00003com/example/CommandManager$UserCreateCommandFactory\n\u0000o\u0000\u0019\b\u0000s\u0001\u0000",
      "context_after": "\u0000t\u0000\u0019\b\u0000x\u0001\u0000\nuser_delete\u0007\u0000z\u0001\u00003com/example/CommandManager$UserDeleteCommandFactory"
    },
    {
      "path": "target/classes/com/example/CommandManager.class",
      "line": 48,
      "col": 1,
      "snippet": "user_delete\u0007\u0000z\u0001\u00003com/example/CommandManager$UserDeleteCommandFactory",
      "context_before": "user_update\u0007\u0000u\u0001\u00003com/example/CommandManager$UserUpdateCommandFactory\n\u0000t\u0000\u0019\b\u0000x\u0001\u0000",
      "context_after": "\u0000y\u0000\u0019\b\u0000}\u0001\u0000\nuser_login\u0007\u0000\u0001\u00002com/example/CommandManager$UserLoginCommandFactory"
    },
    {
      "path": "target/classes/com/example/CommandManager.class",
      "line": 50,
      "col": 1,
      "snippet": "user_login\u0007\u0000\u0001\u00002com/example/CommandManager$UserLoginCommandFactory",
      "context_before": "user_delete\u0007\u0000z\u0001\u00003com/example/CommandManager$UserDeleteCommandFactory\n\u0000y\u0000\u0019\b\u0000}\u0001\u0000",
      "context_after": "\u0000~\u0000\u0019\b\u0000\u0001\u0000\nsystem_backup\u0007\u0000\u0001\u00005com/example/CommandManager$SystemBackupCommandFactory"
    },
    {
      "path": "target/classes/com/example/UserService.class",
      "line": 1,
      "col": 60,
      "snippet": "\u0000\u0000\u00007\u0002\u0007\u0000\u0002\u0001\u0000\u0017com/example/UserService\u0007\u0000\u0004\u0001\u0000\u0010java/lang/Object\u0001\u0000\u0005users\u0001\u0000\u000fLjava/util/Map;\u0001\u0000\tSignature\u0001\u00005Ljava/util/Map<Ljava/lang/String;Lcom/example/User;>;\u0001\u0000\u0004lock\u0001\u0000*Ljava/util/concurrent/locks/ReadWriteLock;\u0001\u0000\tuserCache\u0001\u0000\tlisteners\u0001\u0000\u0010Ljava/util/List;\u0001\u0000?Ljava/util/List<Lcom/example/UserService$UserServiceListener;>;\u0001\u0000",
      "context_before": "",
      "context_after": "auditLogger\u0001\u0000%Lcom/example/UserService$AuditLogger;\u0001\u0000\tvalidator\u0001\u0000'Lcom/example/UserService$UserValidator;\u0001\u0000\nstatistics\u0001\u0000(Lcom/example/UserService$UserStatistics;\u0001\u0000\u000eMAX_CACHE_SIZE\u0001\u0000\u0001I\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/UserService.class",
      "line": 1,
      "col": 206,
      "snippet": "\u0000\u0000\u00007\u0002\u0007\u0000\u0002\u0001\u0000\u0017com/example/UserService\u0007\u0000\u0004\u0001\u0000\u0010java/lang/Object\u0001\u0000\u0005users\u0001\u0000\u000fLjava/util/Map;\u0001\u0000\tSignature\u0001\u00005Ljava/util/Map<Ljava/lang/String;Lcom/example/User;>;\u0001\u0000\u0004lock\u0001\u0000*Ljava/util/concurrent/locks/ReadWriteLock;\u0001\u0000\tuserCache\u0001\u0000\tlisteners\u0001\u0000\u0010Ljava/util/List;\u0001\u0000?Ljava/util/List<Lcom/example/UserService$UserServiceListener;>;\u0001\u0000",
      "context_before": "",
      "context_after": "auditLogger\u0001\u0000%Lcom/example/UserService$AuditLogger;\u0001\u0000\tvalidator\u0001\u0000'Lcom/example/UserService$UserValidator;\u0001\u0000\nstatistics\u0001\u0000(Lcom/example/UserService$UserStatistics;\u0001\u0000\u000eMAX_CACHE_SIZE\u0001\u0000\u0001I\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/UserService.class",
      "line": 63,
      "col": 13,
      "snippet": "\u0001\u0000\u0006unlock\u0001\u0000\u0004user\u0001\u0000\u0012Lcom/example/User;\u0001\u0000",
      "context_before": "\u0000b\u0000\n\u0000\u0000",
      "context_after": "StackMapTable\u0007\u0000\u0001\u0000\u0013java/lang/Throwable\u0001\u0000\ngetUserById\u0001\u0000&(Ljava/lang/String;)Lcom/example/User;\u0007\u0000\u0001\u0000-com/example/UserService$UserNotFoundException"
    },
    {
      "path": "target/classes/com/example/UserService.class",
      "line": 71,
      "col": 39,
      "snippet": "\u0000\u0000p\b\u0000\u0001\u0000\u001bUser retrieved from storage\u0001\u0000\u0006userId\u0001\u0000\u0012Ljava/lang/String;\u0001\u0000",
      "context_before": "\u0000\\\u0000\n\u0000\u0000`\u0001\u0000\breadLock\u0012\u0000\u0002\u0000l",
      "context_after": "cachedUser\u0007\u0000\u0001\u0000\u0010java/lang/String\u0001\u0000\nupdateUser\u0012\u0000\u0003\u0000l\t\u0000y\u0000"
    },
    {
      "path": "target/classes/com/example/UserService.class",
      "line": 142,
      "col": 33,
      "snippet": "\u0000I\u0000p\u0007\u0001?\u0001\u0000\u0013java/lang/Exception\u0001\u0000\buserList\u0001\u0000",
      "context_before": "\u0001;\n\u0000m\u0001<\u0001\u0000\u0015(I)Ljava/lang/String;",
      "context_after": "createdUsers\u0001\u0000\u0006errors\u0001\u0000\u0001e\u0001\u0000\u0015Ljava/lang/Exception;\u0001\u0000$Ljava/util/List<Lcom/example/User;>;\u0001\u0000'Ljava/util/List<Ljava/lang/Exception;>;\u0001\u0000\ngetAllUsers\u0001\u0000\u0012()Ljava/util/List;\u0001\u0000&()Ljava/util/List<Lcom/example/User;>;"
    },
    {
      "path": "target/classes/com/example/UserService.class",
      "line": 185,
      "col": 1,
      "snippet": "usersToUpdate\u0001\u0000\u000egenerateReport\u0001\u00007()Ljava/util/Map<Ljava/lang/String;Ljava/lang/Object;>;\u0007\u0001\u0001\u0000\u0011java/util/HashMap",
      "context_before": "\u0000\u0000G\u0012\u0000\u0010\u0001\n\u0000m\u0001\u0001\u00008(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;\u0001\u0000\boldSkill\u0001\u0000\bnewSkill\u0001\u0000",
      "context_after": "\u0001\u0000!\b\u0001\u0001\u0000\ntotalUsers"
    },
    {
      "path": "target/classes/com/example/UserService.class",
      "line": 226,
      "col": 56,
      "snippet": "\u0001\u0001\u0005\u0012\u0000\u0013\u0000l\u0012\u0000\u0014\u0000l\u0001\u0000\u0004args\u0001\u0000\u0013[Ljava/lang/String;\u0001\u0000\u0007service\u0001\u0000\u0005user1\u0001\u0000\u0005user2\u0001\u0000\tfoundUser\u0001\u0000\tengineers\u0007\u0002\u0005\u0001\u0000\blambda$0\u0001\u0000B(Lcom/example/User;Lcom/example/UserService$UserServiceListener;)V",
      "context_before": "\u0001\u0001\u0001\u0000&(Ljava/lang/Object;)Ljava/lang/String;\u0012\u0000\u0011\u0000l\u0012\u0000\u0012\u0000l\n\u0000\u0001\u0002\u0001",
      "context_after": "\u0001X\u0002\u000f\n\u0002\u0010\u0000P\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/UserService.class",
      "line": 226,
      "col": 64,
      "snippet": "\u0001\u0001\u0005\u0012\u0000\u0013\u0000l\u0012\u0000\u0014\u0000l\u0001\u0000\u0004args\u0001\u0000\u0013[Ljava/lang/String;\u0001\u0000\u0007service\u0001\u0000\u0005user1\u0001\u0000\u0005user2\u0001\u0000\tfoundUser\u0001\u0000\tengineers\u0007\u0002\u0005\u0001\u0000\blambda$0\u0001\u0000B(Lcom/example/User;Lcom/example/UserService$UserServiceListener;)V",
      "context_before": "\u0001\u0001\u0001\u0000&(Ljava/lang/Object;)Ljava/lang/String;\u0012\u0000\u0011\u0000l\u0012\u0000\u0012\u0000l\n\u0000\u0001\u0002\u0001",
      "context_after": "\u0001X\u0002\u000f\n\u0002\u0010\u0000P\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/UserService.class",
      "line": 300,
      "col": 32,
      "snippet": "\u0002?\u0002@\u000f\u0006\u0002\u0010\u0002\b\u0002\u0001\u0000\u001aFailed to update user \u0001: \u0001\b\u0002\u0001\u0000",
      "context_before": "\u0002>\u0000n\u000f\u0006\u0002\u0010\u0000n\b\u0002\u0001\u0000(Batch creation failed: \u0001 errors occurred\b\u0002\u0001\u0000\u001fListener notification failed: \u0001\u0010\u0000j\n\u0000\u0001\u0002",
      "context_after": "Found user: \u0001\b\u0002\u0001\u0000\nEngineers: \u0001\b\u0002\u0001\u0000\tReport: \u0001\b\u0002\u0001\u0000\bError: \u0001\u0010\u0000j"
    },
    {
      "path": "target/classes/com/example/UserService.class",
      "line": 301,
      "col": 7,
      "snippet": "Found user: \u0001\b\u0002\u0001\u0000",
      "context_before": "\u0000\u0001\u0002\n\u0002?\u0002@\u000f\u0006\u0002\u0010\u0002\b\u0002\u0001\u0000\u001aFailed to update user \u0001: \u0001\b\u0002\u0001\u0000",
      "context_after": "Engineers: \u0001\b\u0002\u0001\u0000\tReport: \u0001\b\u0002\u0001\u0000\bError: \u0001\u0010\u0000j\n\u0000\u0001\u0002"
    },
    {
      "path": "target/classes/com/example/User.class",
      "line": 143,
      "col": 15,
      "snippet": "\u0000k\u0000l\u0001\u0000\u0004data\u0001\u0000\u0004user\u0001\u0000\u0012filterByDepartment\u0001\u00004(Ljava/util/List;Ljava/lang/String;)Ljava/util/List;\u0001\u0000\\(Ljava/util/List<Lcom/example/User;>;Ljava/lang/String;)Ljava/util/List<Lcom/example/User;>;\u0012\u0000\b\u0000\u0001\u0000\u0005users\u0001\u0000$Ljava/util/List<Lcom/example/User;>;\u0001\u0000",
      "context_before": "\u0001C\u0001D\u0001\u0000\tsetSkills\u0001\u0000\u0013(Ljava/util/List;)V\n\u0000\u0001\u0001F",
      "context_after": "filterBySkill\u0012\u0000\t\u0000\u0001\u0000\u0011groupByDepartment\u0001\u0000!(Ljava/util/List;)Ljava/util/Map;\u0001\u0000m(Ljava/util/List<Lcom/example/User;>;)Ljava/util/Map<Ljava/lang/String;Ljava/util/List<Lcom/example/User;>;>;\u0012\u0000\n\u0001\u0015"
    },
    {
      "path": "target/classes/com/example/User.class",
      "line": 143,
      "col": 197,
      "snippet": "\u0000k\u0000l\u0001\u0000\u0004data\u0001\u0000\u0004user\u0001\u0000\u0012filterByDepartment\u0001\u00004(Ljava/util/List;Ljava/lang/String;)Ljava/util/List;\u0001\u0000\\(Ljava/util/List<Lcom/example/User;>;Ljava/lang/String;)Ljava/util/List<Lcom/example/User;>;\u0012\u0000\b\u0000\u0001\u0000\u0005users\u0001\u0000$Ljava/util/List<Lcom/example/User;>;\u0001\u0000",
      "context_before": "\u0001C\u0001D\u0001\u0000\tsetSkills\u0001\u0000\u0013(Ljava/util/List;)V\n\u0000\u0001\u0001F",
      "context_after": "filterBySkill\u0012\u0000\t\u0000\u0001\u0000\u0011groupByDepartment\u0001\u0000!(Ljava/util/List;)Ljava/util/Map;\u0001\u0000m(Ljava/util/List<Lcom/example/User;>;)Ljava/util/Map<Ljava/lang/String;Ljava/util/List<Lcom/example/User;>;>;\u0012\u0000\n\u0001\u0015"
    },
    {
      "path": "target/classes/com/example/FactoryManager$PermissionManagerFactory.class",
      "line": 12,
      "col": 4,
      "snippet": "\u0001\u0000\u0004user\b\u0000 \u0001\u0000\u0004USER\u0001\u0000\u0004args\u0001\u0000\u0013[Ljava/lang/Object;\u0001\u0000\u0007manager\u0001\u0000\u001fLcom/example/PermissionManager;\u0001\u0000'([Ljava/lang/Object;)Ljava/lang/Object;",
      "context_before": "\u0001\u0000\nassignRole\u0001\u0000'(Ljava/lang/String;Ljava/lang/String;)V\b\u0000",
      "context_after": "\u0000\u0001\u0000'\n\u0000\u0010\u0000\u0011\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/FactoryManager$UserFactory.class",
      "line": 22,
      "col": 82,
      "snippet": "\u0000\u0007\u00007\u0001\u0000*(Ljava/lang/String;Ljava/lang/Throwable;)V\u0001\u0000\u0004args\u0001\u0000\u0013[Ljava/lang/Object;\u0001\u0000\u0006userId\u0001\u0000\u0012Ljava/lang/String;\u0001\u0000\busername\u0001\u0000\u0001e\u0001\u0000&Lcom/example/User$ValidationException;\u0001\u0000",
      "context_before": "\u00003\u00004\u0001\u0000\u0017makeConcatWithConstants\u0001\u0000&(Ljava/lang/String;)Ljava/lang/String;\n\u0000)\u00006",
      "context_after": "StackMapTable\u0001\u0000'([Ljava/lang/Object;)Ljava/lang/Object;\n\u0000\u0001\u0000B"
    },
    {
      "path": "target/classes/com/example/FactoryManager$UserFactory.class",
      "line": 22,
      "col": 112,
      "snippet": "\u0000\u0007\u00007\u0001\u0000*(Ljava/lang/String;Ljava/lang/Throwable;)V\u0001\u0000\u0004args\u0001\u0000\u0013[Ljava/lang/Object;\u0001\u0000\u0006userId\u0001\u0000\u0012Ljava/lang/String;\u0001\u0000\busername\u0001\u0000\u0001e\u0001\u0000&Lcom/example/User$ValidationException;\u0001\u0000",
      "context_before": "\u00003\u00004\u0001\u0000\u0017makeConcatWithConstants\u0001\u0000&(Ljava/lang/String;)Ljava/lang/String;\n\u0000)\u00006",
      "context_after": "StackMapTable\u0001\u0000'([Ljava/lang/Object;)Ljava/lang/Object;\n\u0000\u0001\u0000B"
    },
    {
      "path": "target/classes/com/example/FactoryManager$UserFactory.class",
      "line": 28,
      "col": 186,
      "snippet": "\u00003\u0000L\u0001\u0000(Ljava/lang/invoke/MethodHandles$Lookup;Ljava/lang/String;Ljava/lang/invoke/MethodType;Ljava/lang/String;[Ljava/lang/Object;)Ljava/lang/invoke/CallSite;\u000f\u0006\u0000H\b\u0000O\u0001\u0000\u0018Failed to create user: \u0001\u0001\u0000",
      "context_before": "SourceFile\u0001\u0000\u0013FactoryManager.java\u0001\u0000\tSignature\u0001\u0000PLjava/lang/Object;Lcom/example/FactoryManager$ObjectFactory<Lcom/example/User;>;\u0001\u0000\u0010BootstrapMethods\n\u0000I\u0000K\u0007\u0000J\u0001\u0000$java/lang/invoke/StringConcatFactory",
      "context_after": "InnerClasses\u0007\u0000R\u0001\u0000\u001acom/example/FactoryManager\u0001\u0000\nObjectFactory\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/CommandManager$UserCreateCommand.class",
      "line": 1,
      "col": 122,
      "snippet": "\u0000\u0000\u00007\u0000k\u0007\u0000\u0002\u0001\u0000,com/example/CommandManager$UserCreateCommand\u0007\u0000\u0004\u0001\u0000\u0010java/lang/Object\u0007\u0000\u0006\u0001\u0000\"com/example/CommandManager$Command\u0001\u0000\busername\u0001\u0000\u0012Ljava/lang/String;\u0001\u0000\u0005email\u0001\u0000\u0006userId\u0001\u0000\u0010Ljava/lang/Long;\u0001\u0000\bexecuted\u0001\u0000\u0001Z\u0001\u0000\u0006<init>\u0001\u0000'(Ljava/lang/String;Ljava/lang/String;)V\u0001\u0000\u0004Code",
      "context_before": "",
      "context_after": "\u0000\u0003\u0000\u0012\n\u0000\u000e\u0000\u0013\u0001\u0000\u0003()V\t\u0000\u0001\u0000\u0015"
    },
    {
      "path": "target/classes/com/example/CommandManager$UserCreateCommand.class",
      "line": 1,
      "col": 162,
      "snippet": "\u0000\u0000\u00007\u0000k\u0007\u0000\u0002\u0001\u0000,com/example/CommandManager$UserCreateCommand\u0007\u0000\u0004\u0001\u0000\u0010java/lang/Object\u0007\u0000\u0006\u0001\u0000\"com/example/CommandManager$Command\u0001\u0000\busername\u0001\u0000\u0012Ljava/lang/String;\u0001\u0000\u0005email\u0001\u0000\u0006userId\u0001\u0000\u0010Ljava/lang/Long;\u0001\u0000\bexecuted\u0001\u0000\u0001Z\u0001\u0000\u0006<init>\u0001\u0000'(Ljava/lang/String;Ljava/lang/String;)V\u0001\u0000\u0004Code",
      "context_before": "",
      "context_after": "\u0000\u0003\u0000\u0012\n\u0000\u000e\u0000\u0013\u0001\u0000\u0003()V\t\u0000\u0001\u0000\u0015"
    },
    {
      "path": "target/classes/com/example/CommandManager$UserCreateCommand.class",
      "line": 26,
      "col": 1,
      "snippet": "user_create\u0001\u0000",
      "context_before": "StackMapTable\u0001\u0000\nisUndoable\u0001\u0000\u0003()Z\u0001\u0000\u000egetDescription\u0001\u0000\u0014()Ljava/lang/String;\u0012\u0000\u0002\u0000F\u0001\u0000\u0007getType\b\u0000P\u0001\u0000",
      "context_after": "SourceFile\u0001\u0000\u0013CommandManager.java\u0001\u0000\u0010BootstrapMethods\n\u0000U\u0000W\u0007\u0000V\u0001\u0000$java/lang/invoke/StringConcatFactory"
    },
    {
      "path": "target/classes/com/example/CommandManager$UserCreateCommand.class",
      "line": 31,
      "col": 44,
      "snippet": "User creation undone for ID: \u0001\b\u0000_\u0001\u0000\u000eCreate user: \u0001\u0001\u0000",
      "context_before": "\u0000<\u0000X\u0001\u0000(Ljava/lang/invoke/MethodHandles$Lookup;Ljava/lang/String;Ljava/lang/invoke/MethodType;Ljava/lang/String;[Ljava/lang/Object;)Ljava/lang/invoke/CallSite;\u000f\u0006\u0000T\b\u0000[\u0001\u0000\nUser created: \u0001 (\u0001) with ID: \u0001\b\u0000]\u0001\u0000",
      "context_after": "InnerClasses\u0007\u0000b\u0001\u0000\u001acom/example/CommandManager\u0001\u0000\u0007Command\u0001\u0000\u0011UserCreateCommand\u0007\u0000f\u0001\u0000%java/lang/invoke/MethodHandles$Lookup\u0007\u0000h\u0001\u0000\njava/lang/invoke/MethodHandles\u0001\u0000\u0006Lookup\u0001\u0000\bNestHost\u0000!\u0000\u0001\u0000\u0003\u0000\u0001\u0000\u0005\u0000\u0004\u0000\u0012\u0000\u0007\u0000\b\u0000\u0000\u0000\u0012\u0000\t\u0000\b\u0000\u0000\u0000\u0002\u0000"
    },
    {
      "path": "target/classes/com/example/CommandManager$UserLoginCommandFactory.class",
      "line": 6,
      "col": 81,
      "snippet": "\u0000\u0007\u0000\u0018\u0001\u0000'(Ljava/lang/String;Ljava/lang/String;)V\u0001\u0000\u0006params\u0001\u0000\u0013[Ljava/lang/Object;\u0001\u0000\busername\u0001\u0000\u0012Ljava/lang/String;\u0001\u0000\bpassword\u0001\u0000",
      "context_before": "\u0000\u0007\u0000\b\u0001\u0000\u000fLineNumberTable\u0001\u0000\u0012LocalVariableTable\u0001\u0000\u0004this\u0001\u00004Lcom/example/CommandManager$UserLoginCommandFactory;\u0001\u0000\u0006create\u0001\u00009([Ljava/lang/Object;)Lcom/example/CommandManager$Command;\u0007\u0000\u0013\u0001\u0000\u0010java/lang/String\u0007\u0000\u0015\u0001\u0000+com/example/CommandManager$UserLoginCommand\n\u0000\u0014\u0000\u0017",
      "context_after": "SourceFile\u0001\u0000\u0013CommandManager.java\u0001\u0000\nInnerClasses\u0007\u0000\"\u0001\u0000\"com/example/CommandManager$Command\u0007\u0000$\u0001\u0000\u001acom/example/CommandManager\u0001\u0000\u0007Command\u0001\u0000\u000eCommandFactory\u0001\u0000\u0010UserLoginCommand\u0001\u0000\u0017UserLoginCommandFactory\u0001\u0000\bNestHost\u0000!\u0000\u0001\u0000\u0003\u0000\u0001\u0000\u0005\u0000\u0000\u0000\u0002\u0000\u0001\u0000\u0007\u0000\b\u0000\u0001\u0000\t\u0000\u0000\u0000/\u0000\u0001\u0000\u0001\u0000\u0000\u0000\u0005*\u0000"
    },
    {
      "path": "src/caching.py",
      "line": 884,
      "col": 22,
      "snippet": "await cache.set(\"user:123\", {\"name\": \"John\", \"age\": 30}, ttl=3600)",
      "context_before": "\n    # Basic operations",
      "context_after": "    user = await cache.get(\"user:123\")\n    print(f\"Cached user: {user}\")"
    },
    {
      "path": "src/caching.py",
      "line": 885,
      "col": 5,
      "snippet": "user = await cache.get(\"user:123\")",
      "context_before": "    # Basic operations\n    await cache.set(\"user:123\", {\"name\": \"John\", \"age\": 30}, ttl=3600)",
      "context_after": "    print(f\"Cached user: {user}\")\n"
    },
    {
      "path": "src/caching.py",
      "line": 885,
      "col": 29,
      "snippet": "user = await cache.get(\"user:123\")",
      "context_before": "    # Basic operations\n    await cache.set(\"user:123\", {\"name\": \"John\", \"age\": 30}, ttl=3600)",
      "context_after": "    print(f\"Cached user: {user}\")\n"
    },
    {
      "path": "src/caching.py",
      "line": 886,
      "col": 20,
      "snippet": "print(f\"Cached user: {user}\")",
      "context_before": "    await cache.set(\"user:123\", {\"name\": \"John\", \"age\": 30}, ttl=3600)\n    user = await cache.get(\"user:123\")",
      "context_after": "\n    # Tagged caching"
    },
    {
      "path": "src/caching.py",
      "line": 886,
      "col": 27,
      "snippet": "print(f\"Cached user: {user}\")",
      "context_before": "    await cache.set(\"user:123\", {\"name\": \"John\", \"age\": 30}, ttl=3600)\n    user = await cache.get(\"user:123\")",
      "context_after": "\n    # Tagged caching"
    },
    {
      "path": "src/caching.py",
      "line": 894,
      "col": 21,
      "snippet": "async def fetch_user_data(user_id: str):",
      "context_before": "    # Cached function\n    @cache.cached(ttl=300, tags={\"api_calls\"})",
      "context_after": "        # Simulate API call\n        await asyncio.sleep(0.1)"
    },
    {
      "path": "src/caching.py",
      "line": 894,
      "col": 31,
      "snippet": "async def fetch_user_data(user_id: str):",
      "context_before": "    # Cached function\n    @cache.cached(ttl=300, tags={\"api_calls\"})",
      "context_after": "        # Simulate API call\n        await asyncio.sleep(0.1)"
    },
    {
      "path": "src/caching.py",
      "line": 897,
      "col": 23,
      "snippet": "return {\"id\": user_id, \"data\": f\"User {user_id} data\"}",
      "context_before": "        # Simulate API call\n        await asyncio.sleep(0.1)",
      "context_after": "\n    # First call (cache miss)"
    },
    {
      "path": "src/caching.py",
      "line": 897,
      "col": 48,
      "snippet": "return {\"id\": user_id, \"data\": f\"User {user_id} data\"}",
      "context_before": "        # Simulate API call\n        await asyncio.sleep(0.1)",
      "context_after": "\n    # First call (cache miss)"
    },
    {
      "path": "src/caching.py",
      "line": 900,
      "col": 25,
      "snippet": "data1 = await fetch_user_data(\"user123\")",
      "context_before": "\n    # First call (cache miss)",
      "context_after": "    print(f\"First call: {data1}\")\n"
    },
    {
      "path": "src/caching.py",
      "line": 900,
      "col": 36,
      "snippet": "data1 = await fetch_user_data(\"user123\")",
      "context_before": "\n    # First call (cache miss)",
      "context_after": "    print(f\"First call: {data1}\")\n"
    },
    {
      "path": "src/caching.py",
      "line": 904,
      "col": 25,
      "snippet": "data2 = await fetch_user_data(\"user123\")",
      "context_before": "\n    # Second call (cache hit)",
      "context_after": "    print(f\"Second call: {data2}\")\n"
    },
    {
      "path": "src/caching.py",
      "line": 904,
      "col": 36,
      "snippet": "data2 = await fetch_user_data(\"user123\")",
      "context_before": "\n    # Second call (cache hit)",
      "context_after": "    print(f\"Second call: {data2}\")\n"
    },
    {
      "path": "src/authentication.py",
      "line": 2,
      "col": 27,
      "snippet": "Authentication module for user management system.",
      "context_before": "\"\"\"",
      "context_after": "Handles user authentication, session management, and security features.\n\"\"\""
    },
    {
      "path": "src/authentication.py",
      "line": 3,
      "col": 9,
      "snippet": "Handles user authentication, session management, and security features.",
      "context_before": "\"\"\"\nAuthentication module for user management system.",
      "context_after": "\"\"\"\n"
    },
    {
      "path": "src/authentication.py",
      "line": 74,
      "col": 5,
      "snippet": "user_id: str",
      "context_before": "class User:\n    \"\"\"User data class with authentication information.\"\"\"",
      "context_after": "    username: str\n    email: str"
    },
    {
      "path": "src/authentication.py",
      "line": 75,
      "col": 5,
      "snippet": "username: str",
      "context_before": "    \"\"\"User data class with authentication information.\"\"\"\n    user_id: str",
      "context_after": "    email: str\n    password_hash: str"
    },
    {
      "path": "src/authentication.py",
      "line": 93,
      "col": 21,
      "snippet": "\"\"\"Check if user account is currently locked.\"\"\"",
      "context_before": "\n    def is_locked(self) -> bool:",
      "context_after": "        if self.status == UserStatus.LOCKED:\n            return True"
    },
    {
      "path": "src/authentication.py",
      "line": 101,
      "col": 21,
      "snippet": "\"\"\"Check if user can attempt to login.\"\"\"",
      "context_before": "\n    def can_login(self) -> bool:",
      "context_after": "        return (self.status == UserStatus.ACTIVE and\n                not self.is_locked() and"
    },
    {
      "path": "src/authentication.py",
      "line": 118,
      "col": 18,
      "snippet": "\"\"\"Reset user password.\"\"\"",
      "context_before": "\n    def reset_password(self, new_password: str):",
      "context_after": "        self.password_hash = self._hash_password(new_password)\n        self.password_reset_token = None"
    },
    {
      "path": "src/authentication.py",
      "line": 138,
      "col": 5,
      "snippet": "user_id: str",
      "context_before": "    \"\"\"User session data class.\"\"\"\n    session_id: str",
      "context_after": "    created_at: datetime = field(default_factory=datetime.now)\n    expires_at: datetime = field(default_factory=lambda: datetime.now() + timedelta(hours=8))"
    },
    {
      "path": "src/authentication.py",
      "line": 143,
      "col": 5,
      "snippet": "user_agent: Optional[str] = None",
      "context_before": "    last_activity: datetime = field(default_factory=datetime.now)\n    ip_address: Optional[str] = None",
      "context_after": "    is_active: bool = True\n    metadata: Dict[str, Any] = field(default_factory=dict)"
    },
    {
      "path": "src/authentication.py",
      "line": 166,
      "col": 5,
      "snippet": "user_id: str = \"\"",
      "context_before": "    token: str\n    token_type: str = \"Bearer\"",
      "context_after": "    expires_at: datetime = field(default_factory=lambda: datetime.now() + timedelta(hours=1))\n    scopes: Set[str] = field(default_factory=set)"
    },
    {
      "path": "src/authentication.py",
      "line": 197,
      "col": 51,
      "snippet": "def __init__(self, config: AuthConfig = None, user_store: 'UserStore' = None):",
      "context_before": "    \"\"\"Main authentication service class.\"\"\"\n",
      "context_after": "        self.config = config or AuthConfig()\n        self.user_store = user_store or InMemoryUserStore()"
    },
    {
      "path": "src/authentication.py",
      "line": 199,
      "col": 14,
      "snippet": "self.user_store = user_store or InMemoryUserStore()",
      "context_before": "    def __init__(self, config: AuthConfig = None, user_store: 'UserStore' = None):\n        self.config = config or AuthConfig()",
      "context_after": "        self.session_store = InMemorySessionStore()\n        self.token_store = InMemoryTokenStore()"
    },
    {
      "path": "src/authentication.py",
      "line": 199,
      "col": 27,
      "snippet": "self.user_store = user_store or InMemoryUserStore()",
      "context_before": "    def __init__(self, config: AuthConfig = None, user_store: 'UserStore' = None):\n        self.config = config or AuthConfig()",
      "context_after": "        self.session_store = InMemorySessionStore()\n        self.token_store = InMemoryTokenStore()"
    },
    {
      "path": "src/authentication.py",
      "line": 208,
      "col": 28,
      "snippet": "async def authenticate_user(self, username: str, password: str,",
      "context_before": "        self._lock = threading.RLock()\n",
      "context_after": "                              ip_address: str = None, user_agent: str = None) -> Tuple[User, Session]:\n        \"\"\"Authenticate user with username and password.\"\"\""
    },
    {
      "path": "src/authentication.py",
      "line": 208,
      "col": 39,
      "snippet": "async def authenticate_user(self, username: str, password: str,",
      "context_before": "        self._lock = threading.RLock()\n",
      "context_after": "                              ip_address: str = None, user_agent: str = None) -> Tuple[User, Session]:\n        \"\"\"Authenticate user with username and password.\"\"\""
    },
    {
      "path": "src/authentication.py",
      "line": 209,
      "col": 55,
      "snippet": "ip_address: str = None, user_agent: str = None) -> Tuple[User, Session]:",
      "context_before": "\n    async def authenticate_user(self, username: str, password: str,",
      "context_after": "        \"\"\"Authenticate user with username and password.\"\"\"\n        # Rate limiting check"
    },
    {
      "path": "src/authentication.py",
      "line": 210,
      "col": 25,
      "snippet": "\"\"\"Authenticate user with username and password.\"\"\"",
      "context_before": "    async def authenticate_user(self, username: str, password: str,\n                              ip_address: str = None, user_agent: str = None) -> Tuple[User, Session]:",
      "context_after": "        # Rate limiting check\n        if not self.rate_limiter.check_limit(f\"login:{username}\"):"
    },
    {
      "path": "src/authentication.py",
      "line": 210,
      "col": 35,
      "snippet": "\"\"\"Authenticate user with username and password.\"\"\"",
      "context_before": "    async def authenticate_user(self, username: str, password: str,\n                              ip_address: str = None, user_agent: str = None) -> Tuple[User, Session]:",
      "context_after": "        # Rate limiting check\n        if not self.rate_limiter.check_limit(f\"login:{username}\"):"
    },
    {
      "path": "src/authentication.py",
      "line": 212,
      "col": 55,
      "snippet": "if not self.rate_limiter.check_limit(f\"login:{username}\"):",
      "context_before": "        \"\"\"Authenticate user with username and password.\"\"\"\n        # Rate limiting check",
      "context_after": "            raise AuthenticationError(\"Too many login attempts. Please try again later.\")\n"
    },
    {
      "path": "src/authentication.py",
      "line": 216,
      "col": 19,
      "snippet": "# Get user",
      "context_before": "\n        try:",
      "context_after": "            user = await self.user_store.get_user_by_username(username)\n            if not user:"
    },
    {
      "path": "src/authentication.py",
      "line": 217,
      "col": 13,
      "snippet": "user = await self.user_store.get_user_by_username(username)",
      "context_before": "        try:\n            # Get user",
      "context_after": "            if not user:\n                raise InvalidCredentialsError(\"Invalid username or password\")"
    },
    {
      "path": "src/authentication.py",
      "line": 217,
      "col": 31,
      "snippet": "user = await self.user_store.get_user_by_username(username)",
      "context_before": "        try:\n            # Get user",
      "context_after": "            if not user:\n                raise InvalidCredentialsError(\"Invalid username or password\")"
    },
    {
      "path": "src/authentication.py",
      "line": 217,
      "col": 46,
      "snippet": "user = await self.user_store.get_user_by_username(username)",
      "context_before": "        try:\n            # Get user",
      "context_after": "            if not user:\n                raise InvalidCredentialsError(\"Invalid username or password\")"
    },
    {
      "path": "src/authentication.py",
      "line": 217,
      "col": 54,
      "snippet": "user = await self.user_store.get_user_by_username(username)",
      "context_before": "        try:\n            # Get user",
      "context_after": "            if not user:\n                raise InvalidCredentialsError(\"Invalid username or password\")"
    },
    {
      "path": "src/authentication.py",
      "line": 217,
      "col": 63,
      "snippet": "user = await self.user_store.get_user_by_username(username)",
      "context_before": "        try:\n            # Get user",
      "context_after": "            if not user:\n                raise InvalidCredentialsError(\"Invalid username or password\")"
    },
    {
      "path": "src/authentication.py",
      "line": 218,
      "col": 20,
      "snippet": "if not user:",
      "context_before": "            # Get user\n            user = await self.user_store.get_user_by_username(username)",
      "context_after": "                raise InvalidCredentialsError(\"Invalid username or password\")\n"
    },
    {
      "path": "src/authentication.py",
      "line": 219,
      "col": 56,
      "snippet": "raise InvalidCredentialsError(\"Invalid username or password\")",
      "context_before": "            user = await self.user_store.get_user_by_username(username)\n            if not user:",
      "context_after": "\n            # Check account status"
    },
    {
      "path": "src/authentication.py",
      "line": 222,
      "col": 20,
      "snippet": "if not user.can_login():",
      "context_before": "\n            # Check account status",
      "context_after": "                if user.is_locked():\n                    raise AccountLockedError(\"Account is locked due to security reasons\")"
    },
    {
      "path": "src/authentication.py",
      "line": 223,
      "col": 20,
      "snippet": "if user.is_locked():",
      "context_before": "            # Check account status\n            if not user.can_login():",
      "context_after": "                    raise AccountLockedError(\"Account is locked due to security reasons\")\n                raise AuthenticationError(\"Account is not active\")"
    },
    {
      "path": "src/authentication.py",
      "line": 228,
      "col": 20,
      "snippet": "if not user.verify_password(password):",
      "context_before": "\n            # Verify password",
      "context_after": "                user.record_login_attempt(False)\n                await self.user_store.update_user(user)"
    },
    {
      "path": "src/authentication.py",
      "line": 229,
      "col": 17,
      "snippet": "user.record_login_attempt(False)",
      "context_before": "            # Verify password\n            if not user.verify_password(password):",
      "context_after": "                await self.user_store.update_user(user)\n                await self.audit_logger.log_failed_login(username, ip_address, \"invalid_password\")"
    },
    {
      "path": "src/authentication.py",
      "line": 230,
      "col": 28,
      "snippet": "await self.user_store.update_user(user)",
      "context_before": "            if not user.verify_password(password):\n                user.record_login_attempt(False)",
      "context_after": "                await self.audit_logger.log_failed_login(username, ip_address, \"invalid_password\")\n                raise InvalidCredentialsError(\"Invalid username or password\")"
    },
    {
      "path": "src/authentication.py",
      "line": 230,
      "col": 46,
      "snippet": "await self.user_store.update_user(user)",
      "context_before": "            if not user.verify_password(password):\n                user.record_login_attempt(False)",
      "context_after": "                await self.audit_logger.log_failed_login(username, ip_address, \"invalid_password\")\n                raise InvalidCredentialsError(\"Invalid username or password\")"
    },
    {
      "path": "src/authentication.py",
      "line": 230,
      "col": 51,
      "snippet": "await self.user_store.update_user(user)",
      "context_before": "            if not user.verify_password(password):\n                user.record_login_attempt(False)",
      "context_after": "                await self.audit_logger.log_failed_login(username, ip_address, \"invalid_password\")\n                raise InvalidCredentialsError(\"Invalid username or password\")"
    },
    {
      "path": "src/authentication.py",
      "line": 231,
      "col": 58,
      "snippet": "await self.audit_logger.log_failed_login(username, ip_address, \"invalid_password\")",
      "context_before": "                user.record_login_attempt(False)\n                await self.user_store.update_user(user)",
      "context_after": "                raise InvalidCredentialsError(\"Invalid username or password\")\n"
    },
    {
      "path": "src/authentication.py",
      "line": 232,
      "col": 56,
      "snippet": "raise InvalidCredentialsError(\"Invalid username or password\")",
      "context_before": "                await self.user_store.update_user(user)\n                await self.audit_logger.log_failed_login(username, ip_address, \"invalid_password\")",
      "context_after": "\n            # Successful authentication"
    },
    {
      "path": "src/authentication.py",
      "line": 235,
      "col": 13,
      "snippet": "user.record_login_attempt(True)",
      "context_before": "\n            # Successful authentication",
      "context_after": "            await self.user_store.update_user(user)\n"
    },
    {
      "path": "src/authentication.py",
      "line": 236,
      "col": 24,
      "snippet": "await self.user_store.update_user(user)",
      "context_before": "            # Successful authentication\n            user.record_login_attempt(True)",
      "context_after": "\n            # Create session"
    },
    {
      "path": "src/authentication.py",
      "line": 236,
      "col": 42,
      "snippet": "await self.user_store.update_user(user)",
      "context_before": "            # Successful authentication\n            user.record_login_attempt(True)",
      "context_after": "\n            # Create session"
    },
    {
      "path": "src/authentication.py",
      "line": 236,
      "col": 47,
      "snippet": "await self.user_store.update_user(user)",
      "context_before": "            # Successful authentication\n            user.record_login_attempt(True)",
      "context_after": "\n            # Create session"
    },
    {
      "path": "src/authentication.py",
      "line": 239,
      "col": 50,
      "snippet": "session = await self._create_session(user, ip_address, user_agent)",
      "context_before": "\n            # Create session",
      "context_after": "\n            # Log successful login"
    },
    {
      "path": "src/authentication.py",
      "line": 239,
      "col": 68,
      "snippet": "session = await self._create_session(user, ip_address, user_agent)",
      "context_before": "\n            # Create session",
      "context_after": "\n            # Log successful login"
    },
    {
      "path": "src/authentication.py",
      "line": 242,
      "col": 58,
      "snippet": "await self.audit_logger.log_successful_login(user.user_id, ip_address, user_agent)",
      "context_before": "\n            # Log successful login",
      "context_after": "\n            return user, session"
    },
    {
      "path": "src/authentication.py",
      "line": 242,
      "col": 63,
      "snippet": "await self.audit_logger.log_successful_login(user.user_id, ip_address, user_agent)",
      "context_before": "\n            # Log successful login",
      "context_after": "\n            return user, session"
    },
    {
      "path": "src/authentication.py",
      "line": 242,
      "col": 84,
      "snippet": "await self.audit_logger.log_successful_login(user.user_id, ip_address, user_agent)",
      "context_before": "\n            # Log successful login",
      "context_after": "\n            return user, session"
    },
    {
      "path": "src/authentication.py",
      "line": 244,
      "col": 20,
      "snippet": "return user, session",
      "context_before": "            await self.audit_logger.log_successful_login(user.user_id, ip_address, user_agent)\n",
      "context_after": "\n        except AuthenticationError:"
    },
    {
      "path": "src/authentication.py",
      "line": 249,
      "col": 53,
      "snippet": "logger.error(f\"Authentication error for user {username}: {e}\")",
      "context_before": "            raise\n        except Exception as e:",
      "context_after": "            raise AuthenticationError(\"Authentication failed\")\n"
    },
    {
      "path": "src/authentication.py",
      "line": 249,
      "col": 59,
      "snippet": "logger.error(f\"Authentication error for user {username}: {e}\")",
      "context_before": "            raise\n        except Exception as e:",
      "context_after": "            raise AuthenticationError(\"Authentication failed\")\n"
    },
    {
      "path": "src/authentication.py",
      "line": 253,
      "col": 25,
      "snippet": "\"\"\"Authenticate user using JWT token.\"\"\"",
      "context_before": "\n    async def authenticate_token(self, token: str) -> Tuple[User, Session]:",
      "context_after": "        try:\n            # Decode and validate token"
    },
    {
      "path": "src/authentication.py",
      "line": 259,
      "col": 13,
      "snippet": "user_id = payload.get('user_id')",
      "context_before": "                               algorithms=[self.config.jwt_algorithm])\n",
      "context_after": "            session_id = payload.get('session_id')\n"
    },
    {
      "path": "src/authentication.py",
      "line": 259,
      "col": 36,
      "snippet": "user_id = payload.get('user_id')",
      "context_before": "                               algorithms=[self.config.jwt_algorithm])\n",
      "context_after": "            session_id = payload.get('session_id')\n"
    },
    {
      "path": "src/authentication.py",
      "line": 262,
      "col": 20,
      "snippet": "if not user_id or not session_id:",
      "context_before": "            session_id = payload.get('session_id')\n",
      "context_after": "                raise TokenValidationError(\"Invalid token payload\")\n"
    },
    {
      "path": "src/authentication.py",
      "line": 265,
      "col": 19,
      "snippet": "# Get user and session",
      "context_before": "                raise TokenValidationError(\"Invalid token payload\")\n",
      "context_after": "            user = await self.user_store.get_user(user_id)\n            session = await self.session_store.get_session(session_id)"
    },
    {
      "path": "src/authentication.py",
      "line": 266,
      "col": 13,
      "snippet": "user = await self.user_store.get_user(user_id)",
      "context_before": "\n            # Get user and session",
      "context_after": "            session = await self.session_store.get_session(session_id)\n"
    },
    {
      "path": "src/authentication.py",
      "line": 266,
      "col": 31,
      "snippet": "user = await self.user_store.get_user(user_id)",
      "context_before": "\n            # Get user and session",
      "context_after": "            session = await self.session_store.get_session(session_id)\n"
    },
    {
      "path": "src/authentication.py",
      "line": 266,
      "col": 46,
      "snippet": "user = await self.user_store.get_user(user_id)",
      "context_before": "\n            # Get user and session",
      "context_after": "            session = await self.session_store.get_session(session_id)\n"
    },
    {
      "path": "src/authentication.py",
      "line": 266,
      "col": 51,
      "snippet": "user = await self.user_store.get_user(user_id)",
      "context_before": "\n            # Get user and session",
      "context_after": "            session = await self.session_store.get_session(session_id)\n"
    },
    {
      "path": "src/authentication.py",
      "line": 269,
      "col": 20,
      "snippet": "if not user or not session:",
      "context_before": "            session = await self.session_store.get_session(session_id)\n",
      "context_after": "                raise TokenValidationError(\"Invalid token\")\n"
    },
    {
      "path": "src/authentication.py",
      "line": 279,
      "col": 20,
      "snippet": "return user, session",
      "context_before": "            await self.session_store.update_session(session)\n",
      "context_after": "\n        except jwt.ExpiredSignatureError:"
    },
    {
      "path": "src/authentication.py",
      "line": 286,
      "col": 34,
      "snippet": "async def create_token(self, user: User, session: Session, scopes: Set[str] = None) -> AuthToken:",
      "context_before": "            raise TokenValidationError(\"Invalid token\")\n",
      "context_after": "        \"\"\"Create JWT token for authenticated user.\"\"\"\n        expires_at = datetime.now() + timedelta(hours=self.config.token_timeout_hours)"
    },
    {
      "path": "src/authentication.py",
      "line": 287,
      "col": 47,
      "snippet": "\"\"\"Create JWT token for authenticated user.\"\"\"",
      "context_before": "\n    async def create_token(self, user: User, session: Session, scopes: Set[str] = None) -> AuthToken:",
      "context_after": "        expires_at = datetime.now() + timedelta(hours=self.config.token_timeout_hours)\n"
    },
    {
      "path": "src/authentication.py",
      "line": 291,
      "col": 14,
      "snippet": "'user_id': user.user_id,",
      "context_before": "\n        payload = {",
      "context_after": "            'session_id': session.session_id,\n            'scopes': list(scopes or set()),"
    },
    {
      "path": "src/authentication.py",
      "line": 291,
      "col": 24,
      "snippet": "'user_id': user.user_id,",
      "context_before": "\n        payload = {",
      "context_after": "            'session_id': session.session_id,\n            'scopes': list(scopes or set()),"
    },
    {
      "path": "src/authentication.py",
      "line": 291,
      "col": 29,
      "snippet": "'user_id': user.user_id,",
      "context_before": "\n        payload = {",
      "context_after": "            'session_id': session.session_id,\n            'scopes': list(scopes or set()),"
    },
    {
      "path": "src/authentication.py",
      "line": 303,
      "col": 13,
      "snippet": "user_id=user.user_id,",
      "context_before": "        auth_token = AuthToken(\n            token=token,",
      "context_after": "            expires_at=expires_at,\n            scopes=scopes or set()"
    },
    {
      "path": "src/authentication.py",
      "line": 303,
      "col": 21,
      "snippet": "user_id=user.user_id,",
      "context_before": "        auth_token = AuthToken(\n            token=token,",
      "context_after": "            expires_at=expires_at,\n            scopes=scopes or set()"
    },
    {
      "path": "src/authentication.py",
      "line": 303,
      "col": 26,
      "snippet": "user_id=user.user_id,",
      "context_before": "        auth_token = AuthToken(\n            token=token,",
      "context_after": "            expires_at=expires_at,\n            scopes=scopes or set()"
    },
    {
      "path": "src/authentication.py",
      "line": 311,
      "col": 22,
      "snippet": "async def logout_user(self, session_id: str):",
      "context_before": "        return auth_token\n",
      "context_after": "        \"\"\"Logout user by invalidating session.\"\"\"\n        session = await self.session_store.get_session(session_id)"
    },
    {
      "path": "src/authentication.py",
      "line": 312,
      "col": 19,
      "snippet": "\"\"\"Logout user by invalidating session.\"\"\"",
      "context_before": "\n    async def logout_user(self, session_id: str):",
      "context_after": "        session = await self.session_store.get_session(session_id)\n        if session:"
    },
    {
      "path": "src/authentication.py",
      "line": 317,
      "col": 56,
      "snippet": "await self.audit_logger.log_logout(session.user_id)",
      "context_before": "            session.invalidate()\n            await self.session_store.update_session(session)",
      "context_after": "\n    async def initiate_password_reset(self, email: str) -> str:"
    },
    {
      "path": "src/authentication.py",
      "line": 321,
      "col": 9,
      "snippet": "user = await self.user_store.get_user_by_email(email)",
      "context_before": "    async def initiate_password_reset(self, email: str) -> str:\n        \"\"\"Initiate password reset process.\"\"\"",
      "context_after": "        if not user:\n            # Don't reveal if email exists"
    },
    {
      "path": "src/authentication.py",
      "line": 321,
      "col": 27,
      "snippet": "user = await self.user_store.get_user_by_email(email)",
      "context_before": "    async def initiate_password_reset(self, email: str) -> str:\n        \"\"\"Initiate password reset process.\"\"\"",
      "context_after": "        if not user:\n            # Don't reveal if email exists"
    },
    {
      "path": "src/authentication.py",
      "line": 321,
      "col": 42,
      "snippet": "user = await self.user_store.get_user_by_email(email)",
      "context_before": "    async def initiate_password_reset(self, email: str) -> str:\n        \"\"\"Initiate password reset process.\"\"\"",
      "context_after": "        if not user:\n            # Don't reveal if email exists"
    },
    {
      "path": "src/authentication.py",
      "line": 322,
      "col": 16,
      "snippet": "if not user:",
      "context_before": "        \"\"\"Initiate password reset process.\"\"\"\n        user = await self.user_store.get_user_by_email(email)",
      "context_after": "            # Don't reveal if email exists\n            return \"If the email exists, a reset link has been sent.\""
    },
    {
      "path": "src/authentication.py",
      "line": 330,
      "col": 9,
      "snippet": "user.password_reset_token = reset_token",
      "context_before": "        expires_at = datetime.now() + timedelta(hours=24)\n",
      "context_after": "        user.password_reset_expires = expires_at\n        await self.user_store.update_user(user)"
    },
    {
      "path": "src/authentication.py",
      "line": 331,
      "col": 9,
      "snippet": "user.password_reset_expires = expires_at",
      "context_before": "\n        user.password_reset_token = reset_token",
      "context_after": "        await self.user_store.update_user(user)\n"
    },
    {
      "path": "src/authentication.py",
      "line": 332,
      "col": 20,
      "snippet": "await self.user_store.update_user(user)",
      "context_before": "        user.password_reset_token = reset_token\n        user.password_reset_expires = expires_at",
      "context_after": "\n        # In real implementation, send email here"
    },
    {
      "path": "src/authentication.py",
      "line": 332,
      "col": 38,
      "snippet": "await self.user_store.update_user(user)",
      "context_before": "        user.password_reset_token = reset_token\n        user.password_reset_expires = expires_at",
      "context_after": "\n        # In real implementation, send email here"
    },
    {
      "path": "src/authentication.py",
      "line": 332,
      "col": 43,
      "snippet": "await self.user_store.update_user(user)",
      "context_before": "        user.password_reset_token = reset_token\n        user.password_reset_expires = expires_at",
      "context_after": "\n        # In real implementation, send email here"
    },
    {
      "path": "src/authentication.py",
      "line": 335,
      "col": 62,
      "snippet": "await self.audit_logger.log_password_reset_initiated(user.user_id, email)",
      "context_before": "\n        # In real implementation, send email here",
      "context_after": "\n        return \"If the email exists, a reset link has been sent.\""
    },
    {
      "path": "src/authentication.py",
      "line": 335,
      "col": 67,
      "snippet": "await self.audit_logger.log_password_reset_initiated(user.user_id, email)",
      "context_before": "\n        # In real implementation, send email here",
      "context_after": "\n        return \"If the email exists, a reset link has been sent.\""
    },
    {
      "path": "src/authentication.py",
      "line": 344,
      "col": 9,
      "snippet": "user = await self.user_store.get_user_by_reset_token(reset_token)",
      "context_before": "            raise AuthenticationError(f\"Password must be at least {self.config.password_min_length} characters\")\n",
      "context_after": "        if not user or not user.password_reset_expires or datetime.now() > user.password_reset_expires:\n            raise AuthenticationError(\"Invalid or expired reset token\")"
    },
    {
      "path": "src/authentication.py",
      "line": 344,
      "col": 27,
      "snippet": "user = await self.user_store.get_user_by_reset_token(reset_token)",
      "context_before": "            raise AuthenticationError(f\"Password must be at least {self.config.password_min_length} characters\")\n",
      "context_after": "        if not user or not user.password_reset_expires or datetime.now() > user.password_reset_expires:\n            raise AuthenticationError(\"Invalid or expired reset token\")"
    },
    {
      "path": "src/authentication.py",
      "line": 344,
      "col": 42,
      "snippet": "user = await self.user_store.get_user_by_reset_token(reset_token)",
      "context_before": "            raise AuthenticationError(f\"Password must be at least {self.config.password_min_length} characters\")\n",
      "context_after": "        if not user or not user.password_reset_expires or datetime.now() > user.password_reset_expires:\n            raise AuthenticationError(\"Invalid or expired reset token\")"
    }
  ],
  "tool_iter": 3,
  "call_index": 2
}
```

### Think Reflection
Reflection recorded: The search results show a lot of "user" related code in both Java and Python.

In Java:
- `com.example.UserService` seems to be a core service.
- `com.example.CommandManager` has several user-related commands: `UserCreateCommand`, `UserUpdateCommand`, `UserDeleteCommand`, `UserLoginCommand`.
- `com.example.PermissionManager` handles user permissions.
- `com.example.User` is the data model.
- `com.example.AdapterManager$AuthenticationAdapter` seems to handle authentication.

In Python:
- `src/authentication.py` has `authenticate_user`, `logout_user`, `initiate_password_reset`, etc.
- `src/caching.py` has `fetch_user_data`.
- `src/main/python/api_client.py` might be relevant.

I haven't found explicit REST controllers yet (like `@RestController` in Java or Flask/FastAPI routes in Python). The Java code seems to be using a Command pattern (`CommandManager`). I'll look closer at `src/main/java/com/example` to see if there are any other files I missed or if the "controllers" are implemented differently. I'll also check `src/main/python/api_client.py` and look for any web framework usage in `requirements.txt`.

Wait, I see `target/classes/...` in the search results, which means the Java code is compiled. The source files are in `src/main/java/com/example/`.

Let's check `requirements.txt` and `pom.xml` to see what frameworks are used. Then I'll look for entry points.

### Call 5
```json
{
  "tool": "read_file_range_tool",
  "args": {
    "path": "/home/ran/Documents/work/VectorCode/mini_code_index/test_code_index_project/pom.xml",
    "start_line": 1,
    "end_line": 50
  },
  "result": {
    "content": "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<project xmlns=\"http://maven.apache.org/POM/4.0.0\"\n         xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n         xsi:schemaLocation=\"http://maven.apache.org/POM/4.0.0\n         http://maven.apache.org/xsd/maven-4.0.0.xsd\">\n    <modelVersion>4.0.0</modelVersion>\n\n    <groupId>com.example</groupId>\n    <artifactId>test-code-index</artifactId>\n    <version>1.0-SNAPSHOT</version>\n\n    <properties>\n        <maven.compiler.source>11</maven.compiler.source>\n        <maven.compiler.target>11</maven.compiler.target>\n    </properties>\n\n    <dependencies>\n        <dependency>\n            <groupId>com.google.code.gson</groupId>\n            <artifactId>gson</artifactId>\n            <version>2.10.1</version>\n        </dependency>\n    </dependencies>\n</project>"
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
    "path": "/home/ran/Documents/work/VectorCode/mini_code_index/test_code_index_project/requirements.txt",
    "start_line": 1,
    "end_line": 50
  },
  "result": {
    "content": "requests==2.31.0\npandas==2.1.4\nnumpy==1.24.3"
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
    "path": "/home/ran/Documents/work/VectorCode/mini_code_index/test_code_index_project/src/main/python/api_client.py",
    "end_line": 100,
    "start_line": 1
  },
  "result": {
    "content": "#!/usr/bin/env python3\n\"\"\"\nAPI 客户端模块\n提供外部 API 集成功能\n\"\"\"\n\nimport requests\nimport aiohttp\nimport asyncio\nfrom typing import Dict, Any, List, Optional, Union\nimport json\nimport logging\nfrom dataclasses import dataclass\nimport time\nfrom functools import wraps\nimport jwt\nimport hashlib\nimport hmac\nimport base64\nfrom urllib.parse import urlencode\nimport threading\nfrom concurrent.futures import ThreadPoolExecutor\nimport backoff\n\nlogger = logging.getLogger(__name__)\n\n\n@dataclass\nclass APIConfig:\n    \"\"\"API 配置\"\"\"\n    base_url: str\n    api_key: Optional[str] = None\n    api_secret: Optional[str] = None\n    timeout: int = 30\n    retries: int = 3\n    rate_limit: int = 100  # requests per minute\n    auth_type: str = \"bearer\"  # bearer, basic, api_key, hmac\n\n\n@dataclass\nclass APIResponse:\n    \"\"\"API 响应\"\"\"\n    status_code: int\n    data: Any\n    headers: Dict[str, str]\n    success: bool\n    error_message: Optional[str] = None\n    request_time: float = 0.0\n\n\nclass APIError(Exception):\n    \"\"\"API 异常\"\"\"\n    def __init__(self, message: str, status_code: int = 0, response_data: Any = None):\n        super().__init__(message)\n        self.status_code = status_code\n        self.response_data = response_data\n\n\nclass RateLimiter:\n    \"\"\"速率限制器\"\"\"\n\n    def __init__(self, requests_per_minute: int):\n        self.requests_per_minute = requests_per_minute\n        self.requests = []\n        self.lock = threading.Lock()\n\n    def wait_if_needed(self):\n        \"\"\"如果需要，等待以遵守速率限制\"\"\"\n        with self.lock:\n            now = time.time()\n            # 移除一分钟前的请求\n            self.requests = [req_time for req_time in self.requests if now - req_time < 60]\n\n            if len(self.requests) >= self.requests_per_minute:\n                # 计算需要等待的时间\n                oldest_request = min(self.requests)\n                wait_time = 60 - (now - oldest_request)\n                if wait_time > 0:\n                    time.sleep(wait_time)\n\n            self.requests.append(now)\n\n\nclass APIClient:\n    \"\"\"API 客户端基类\"\"\"\n\n    def __init__(self, config: APIConfig):\n        self.config = config\n        self.session = requests.Session()\n        self.rate_limiter = RateLimiter(config.rate_limit)\n        self._setup_auth()\n\n    def _setup_auth(self):\n        \"\"\"设置认证\"\"\"\n        if self.config.auth_type == \"bearer\" and self.config.api_key:\n            self.session.headers.update({\"Authorization\": f\"Bearer {self.config.api_key}\"})\n        elif self.config.auth_type == \"basic\" and self.config.api_key and self.config.api_secret:\n            auth = requests.auth.HTTPBasicAuth(self.config.api_key, self.config.api_secret)\n            self.session.auth = auth\n        elif self.config.auth_type == \"api_key\" and self.config.api_key:"
  },
  "tool_iter": 5,
  "call_index": 3
}
```

### Think Reflection
Reflection recorded: The `pom.xml` only has `gson` as a dependency, and `requirements.txt` has `requests`, `pandas`, and `numpy`. This suggests that this might not be a standard Spring Boot or Flask/FastAPI application. It looks more like a library or a set of utility classes.

However, the subtask asks for "REST controllers or API endpoints that expose user management functionality".

In the Java code, I saw `AdapterManager$AuthenticationAdapter` and `CommandManager` with `UserCreateCommand`, etc. It's possible that the "API" is exposed through these adapters or commands, or maybe there's a main class that acts as an entry point.

Let's look at `src/main/java/com/example/AdapterManager.java` and `src/main/java/com/example/CommandManager.java` to see how they are used. I'll also check `src/main/java/com/example/UserService.java` as it seems to be the core service.

I'll also search for any "main" methods in the Java files.

### Call 8
```json
{
  "tool": "text_search_tool",
  "args": {
    "root_dir": "/home/ran/Documents/work/VectorCode/mini_code_index/test_code_index_project/src/main/java",
    "query": "public static void main"
  },
  "result": [
    {
      "path": "com/example/UserService.java",
      "line": 491,
      "col": 5,
      "snippet": "public static void main(String[] args) {",
      "context_before": "\n    // 主方法，用于测试",
      "context_after": "        UserService service = new UserService();\n"
    }
  ],
  "tool_iter": 7,
  "call_index": 1
}
```

### Call 9
```json
{
  "tool": "read_file_range_tool",
  "args": {
    "start_line": 1,
    "end_line": 100,
    "path": "/home/ran/Documents/work/VectorCode/mini_code_index/test_code_index_project/src/main/java/com/example/UserService.java"
  },
  "result": {
    "content": "package com.example;\n\nimport java.util.*;\nimport java.util.concurrent.ConcurrentHashMap;\nimport java.util.concurrent.locks.ReadWriteLock;\nimport java.util.concurrent.locks.ReentrantReadWriteLock;\nimport java.util.stream.Collectors;\nimport java.util.function.Predicate;\nimport java.util.function.Function;\nimport java.util.function.Consumer;\nimport java.time.LocalDateTime;\nimport java.time.temporal.ChronoUnit;\n\n/**\n * 用户服务类，提供用户管理的功能\n * 支持并发操作、缓存、审计日志等高级功能\n */\npublic class UserService {\n    private final Map<String, User> users;\n    private final ReadWriteLock lock;\n    private final Map<String, User> userCache;\n    private final List<UserServiceListener> listeners;\n    private final AuditLogger auditLogger;\n    private final UserValidator validator;\n    private final UserStatistics statistics;\n\n    // 常量\n    private static final int MAX_CACHE_SIZE = 1000;\n    private static final long CACHE_EXPIRY_MINUTES = 30;\n\n    // 枚举\n    public enum OperationType {\n        CREATE, READ, UPDATE, DELETE, SEARCH\n    }\n\n    // 内部类\n    public static class UserStatistics {\n        private int totalUsers;\n        private int activeUsers;\n        private Map<String, Integer> departmentCounts;\n        private Map<String, Integer> skillCounts;\n        private double averageAge;\n        private LocalDateTime lastUpdated;\n\n        public UserStatistics() {\n            this.departmentCounts = new HashMap<>();\n            this.skillCounts = new HashMap<>();\n            this.lastUpdated = LocalDateTime.now();\n        }\n\n        public synchronized void update(List<User> users) {\n            this.totalUsers = users.size();\n            this.activeUsers = (int) users.stream()\n                    .filter(user -> !user.getRoles().contains(\"inactive\"))\n                    .count();\n\n            this.departmentCounts = users.stream()\n                    .collect(Collectors.groupingBy(\n                            User::getDepartment,\n                            Collectors.summingInt(user -> 1)\n                    ));\n\n            this.skillCounts = users.stream()\n                    .flatMap(user -> user.getSkills().stream())\n                    .collect(Collectors.groupingBy(\n                            skill -> skill,\n                            Collectors.summingInt(skill -> 1)\n                    ));\n\n            this.averageAge = users.stream()\n                    .mapToInt(User::getAge)\n                    .average()\n                    .orElse(0.0);\n\n            this.lastUpdated = LocalDateTime.now();\n        }\n\n        // Getters\n        public int getTotalUsers() { return totalUsers; }\n        public int getActiveUsers() { return activeUsers; }\n        public Map<String, Integer> getDepartmentCounts() { return new HashMap<>(departmentCounts); }\n        public Map<String, Integer> getSkillCounts() { return new HashMap<>(skillCounts); }\n        public double getAverageAge() { return averageAge; }\n        public LocalDateTime getLastUpdated() { return lastUpdated; }\n    }\n\n    public static class AuditLogger {\n        private final List<AuditEntry> auditLog;\n\n        public AuditLogger() {\n            this.auditLog = new ArrayList<>();\n        }\n\n        public void log(OperationType operation, String userId, String details) {\n            AuditEntry entry = new AuditEntry(operation, userId, details, LocalDateTime.now());\n            synchronized (auditLog) {\n                auditLog.add(entry);\n                // 保持日志大小\n                if (auditLog.size() > 10000) {\n                    auditLog.remove(0);"
  },
  "tool_iter": 7,
  "call_index": 2
}
```

### Call 10
```json
{
  "tool": "read_file_range_tool",
  "args": {
    "start_line": 1,
    "end_line": 100,
    "path": "/home/ran/Documents/work/VectorCode/mini_code_index/test_code_index_project/src/main/java/com/example/CommandManager.java"
  },
  "result": {
    "content": "package com.example;\n\nimport java.util.*;\nimport java.util.function.*;\nimport java.util.concurrent.*;\nimport java.util.stream.*;\nimport java.io.*;\nimport java.time.*;\nimport java.time.temporal.*;\nimport java.math.*;\nimport java.math.RoundingMode;\nimport java.net.*;\nimport java.nio.file.*;\n\n/**\n * 命令模式实现\n * 将请求封装为对象，支持撤销、重做、队列等操作\n */\npublic class CommandManager {\n\n    // 单例模式\n    private static volatile CommandManager instance;\n    private static final Object LOCK = new Object();\n\n    private final Map<String, CommandFactory> commandFactories;\n    private final Deque<Command> commandHistory;\n    private final Deque<Command> undoHistory;\n    private final ExecutorService executor;\n    private final Map<String, Command> activeCommands;\n\n    private CommandManager() {\n        this.commandFactories = new ConcurrentHashMap<>();\n        this.commandHistory = new ConcurrentLinkedDeque<>();\n        this.undoHistory = new ConcurrentLinkedDeque<>();\n        this.executor = Executors.newCachedThreadPool();\n        this.activeCommands = new ConcurrentHashMap<>();\n        initializeDefaultCommands();\n    }\n\n    public static CommandManager getInstance() {\n        if (instance == null) {\n            synchronized (LOCK) {\n                if (instance == null) {\n                    instance = new CommandManager();\n                }\n            }\n        }\n        return instance;\n    }\n\n    /**\n     * 初始化默认命令\n     */\n    private void initializeDefaultCommands() {\n        // 文件操作命令\n        registerCommand(\"file_create\", new FileCreateCommandFactory());\n        registerCommand(\"file_delete\", new FileDeleteCommandFactory());\n        registerCommand(\"file_copy\", new FileCopyCommandFactory());\n        registerCommand(\"file_move\", new FileMoveCommandFactory());\n\n        // 数据操作命令\n        registerCommand(\"data_insert\", new DataInsertCommandFactory());\n        registerCommand(\"data_update\", new DataUpdateCommandFactory());\n        registerCommand(\"data_delete\", new DataDeleteCommandFactory());\n        registerCommand(\"data_query\", new DataQueryCommandFactory());\n\n        // 用户操作命令\n        registerCommand(\"user_create\", new UserCreateCommandFactory());\n        registerCommand(\"user_update\", new UserUpdateCommandFactory());\n        registerCommand(\"user_delete\", new UserDeleteCommandFactory());\n        registerCommand(\"user_login\", new UserLoginCommandFactory());\n\n        // 系统操作命令\n        registerCommand(\"system_backup\", new SystemBackupCommandFactory());\n        registerCommand(\"system_restore\", new SystemRestoreCommandFactory());\n        registerCommand(\"system_shutdown\", new SystemShutdownCommandFactory());\n        registerCommand(\"system_restart\", new SystemRestartCommandFactory());\n\n        // 网络操作命令\n        registerCommand(\"network_connect\", new NetworkConnectCommandFactory());\n        registerCommand(\"network_disconnect\", new NetworkDisconnectCommandFactory());\n        registerCommand(\"network_send\", new NetworkSendCommandFactory());\n        registerCommand(\"network_receive\", new NetworkReceiveCommandFactory());\n\n        // 复合命令\n        registerCommand(\"composite\", new CompositeCommandFactory());\n    }\n\n    /**\n     * 注册命令工厂\n     */\n    public void registerCommand(String commandType, CommandFactory factory) {\n        commandFactories.put(commandType, factory);\n    }\n\n    /**\n     * 创建命令\n     */\n    public Command createCommand(String commandType, Object... params) {\n        CommandFactory factory = commandFactories.get(commandType);"
  },
  "tool_iter": 7,
  "call_index": 3
}
```