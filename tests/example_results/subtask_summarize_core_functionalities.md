# Subtask Debug Report

**Title**: Summarize core functionalities
**Instruction**: Based on the module names and public interfaces, categorize the key features and capabilities provided by the project.

## Tool Calls
### Think Reflection
Reflection recorded: I will start by exploring the directory structure and listing the symbols in the project to understand the core modules and their public interfaces. This will help in categorizing the key features and capabilities.

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
  "tool": "symbol_index_tool",
  "args": {
    "root_dir": "/home/ran/Documents/work/VectorCode/mini_code_index/test_code_index_project"
  },
  "result": [
    {
      "symbol": "CacheError",
      "kind": "class",
      "path": "src/caching.py",
      "line": 31
    },
    {
      "symbol": "CacheMissError",
      "kind": "class",
      "path": "src/caching.py",
      "line": 36
    },
    {
      "symbol": "CacheBackendError",
      "kind": "class",
      "path": "src/caching.py",
      "line": 41
    },
    {
      "symbol": "SerializationError",
      "kind": "class",
      "path": "src/caching.py",
      "line": 46
    },
    {
      "symbol": "CacheStrategy",
      "kind": "class",
      "path": "src/caching.py",
      "line": 51
    },
    {
      "symbol": "CacheBackend",
      "kind": "class",
      "path": "src/caching.py",
      "line": 60
    },
    {
      "symbol": "CacheEntry",
      "kind": "class",
      "path": "src/caching.py",
      "line": 70
    },
    {
      "symbol": "CacheStats",
      "kind": "class",
      "path": "src/caching.py",
      "line": 100
    },
    {
      "symbol": "Serializer",
      "kind": "class",
      "path": "src/caching.py",
      "line": 123
    },
    {
      "symbol": "PickleSerializer",
      "kind": "class",
      "path": "src/caching.py",
      "line": 137
    },
    {
      "symbol": "JSONSerializer",
      "kind": "class",
      "path": "src/caching.py",
      "line": 153
    },
    {
      "symbol": "CacheBackendBase",
      "kind": "class",
      "path": "src/caching.py",
      "line": 169
    },
    {
      "symbol": "MemoryCacheBackend",
      "kind": "class",
      "path": "src/caching.py",
      "line": 211
    },
    {
      "symbol": "RedisCacheBackend",
      "kind": "class",
      "path": "src/caching.py",
      "line": 347
    },
    {
      "symbol": "SQLiteCacheBackend",
      "kind": "class",
      "path": "src/caching.py",
      "line": 414
    },
    {
      "symbol": "DistributedCacheBackend",
      "kind": "class",
      "path": "src/caching.py",
      "line": 552
    },
    {
      "symbol": "CacheManager",
      "kind": "class",
      "path": "src/caching.py",
      "line": 657
    },
    {
      "symbol": "create_cache_manager",
      "kind": "function",
      "path": "src/caching.py",
      "line": 824
    },
    {
      "symbol": "warmup_cache",
      "kind": "async_function",
      "path": "src/caching.py",
      "line": 843
    },
    {
      "symbol": "backup_cache",
      "kind": "async_function",
      "path": "src/caching.py",
      "line": 850
    },
    {
      "symbol": "restore_cache",
      "kind": "async_function",
      "path": "src/caching.py",
      "line": 867
    },
    {
      "symbol": "example_usage",
      "kind": "async_function",
      "path": "src/caching.py",
      "line": 877
    },
    {
      "symbol": "is_expired",
      "kind": "function",
      "path": "src/caching.py",
      "line": 82
    },
    {
      "symbol": "touch",
      "kind": "function",
      "path": "src/caching.py",
      "line": 86
    },
    {
      "symbol": "calculate_size",
      "kind": "function",
      "path": "src/caching.py",
      "line": 91
    },
    {
      "symbol": "update_hit_rate",
      "kind": "function",
      "path": "src/caching.py",
      "line": 111
    },
    {
      "symbol": "reset",
      "kind": "function",
      "path": "src/caching.py",
      "line": 116
    },
    {
      "symbol": "serialize",
      "kind": "function",
      "path": "src/caching.py",
      "line": 127
    },
    {
      "symbol": "deserialize",
      "kind": "function",
      "path": "src/caching.py",
      "line": 132
    },
    {
      "symbol": "serialize",
      "kind": "function",
      "path": "src/caching.py",
      "line": 140
    },
    {
      "symbol": "deserialize",
      "kind": "function",
      "path": "src/caching.py",
      "line": 146
    },
    {
      "symbol": "serialize",
      "kind": "function",
      "path": "src/caching.py",
      "line": 156
    },
    {
      "symbol": "deserialize",
      "kind": "function",
      "path": "src/caching.py",
      "line": 162
    },
    {
      "symbol": "__init__",
      "kind": "function",
      "path": "src/caching.py",
      "line": 172
    },
    {
      "symbol": "get",
      "kind": "async_function",
      "path": "src/caching.py",
      "line": 176
    },
    {
      "symbol": "set",
      "kind": "async_function",
      "path": "src/caching.py",
      "line": 181
    },
    {
      "symbol": "delete",
      "kind": "async_function",
      "path": "src/caching.py",
      "line": 186
    },
    {
      "symbol": "exists",
      "kind": "async_function",
      "path": "src/caching.py",
      "line": 191
    },
    {
      "symbol": "clear",
      "kind": "async_function",
      "path": "src/caching.py",
      "line": 196
    },
    {
      "symbol": "size",
      "kind": "async_function",
      "path": "src/caching.py",
      "line": 201
    },
    {
      "symbol": "keys",
      "kind": "async_function",
      "path": "src/caching.py",
      "line": 206
    },
    {
      "symbol": "__init__",
      "kind": "function",
      "path": "src/caching.py",
      "line": 214
    },
    {
      "symbol": "get",
      "kind": "async_function",
      "path": "src/caching.py",
      "line": 225
    },
    {
      "symbol": "set",
      "kind": "async_function",
      "path": "src/caching.py",
      "line": 238
    },
    {
      "symbol": "delete",
      "kind": "async_function",
      "path": "src/caching.py",
      "line": 256
    },
    {
      "symbol": "exists",
      "kind": "async_function",
      "path": "src/caching.py",
      "line": 264
    },
    {
      "symbol": "clear",
      "kind": "async_function",
      "path": "src/caching.py",
      "line": 269
    },
    {
      "symbol": "size",
      "kind": "async_function",
      "path": "src/caching.py",
      "line": 277
    },
    {
      "symbol": "keys",
      "kind": "async_function",
      "path": "src/caching.py",
      "line": 282
    },
    {
      "symbol": "_cleanup_expired",
      "kind": "function",
      "path": "src/caching.py",
      "line": 290
    },
    {
      "symbol": "_evict_entries",
      "kind": "function",
      "path": "src/caching.py",
      "line": 297
    },
    {
      "symbol": "_add_to_tracking",
      "kind": "function",
      "path": "src/caching.py",
      "line": 319
    },
    {
      "symbol": "_remove_from_tracking",
      "kind": "function",
      "path": "src/caching.py",
      "line": 328
    },
    {
      "symbol": "_update_access_tracking",
      "kind": "function",
      "path": "src/caching.py",
      "line": 337
    },
    {
      "symbol": "__init__",
      "kind": "function",
      "path": "src/caching.py",
      "line": 350
    },
    {
      "symbol": "get",
      "kind": "async_function",
      "path": "src/caching.py",
      "line": 359
    },
    {
      "symbol": "set",
      "kind": "async_function",
      "path": "src/caching.py",
      "line": 369
    },
    {
      "symbol": "delete",
      "kind": "async_function",
      "path": "src/caching.py",
      "line": 377
    },
    {
      "symbol": "exists",
      "kind": "async_function",
      "path": "src/caching.py",
      "line": 384
    },
    {
      "symbol": "clear",
      "kind": "async_function",
      "path": "src/caching.py",
      "line": 391
    },
    {
      "symbol": "size",
      "kind": "async_function",
      "path": "src/caching.py",
      "line": 398
    },
    {
      "symbol": "keys",
      "kind": "async_function",
      "path": "src/caching.py",
      "line": 405
    },
    {
      "symbol": "__init__",
      "kind": "function",
      "path": "src/caching.py",
      "line": 417
    },
    {
      "symbol": "_init_db",
      "kind": "function",
      "path": "src/caching.py",
      "line": 423
    },
    {
      "symbol": "_get_connection",
      "kind": "function",
      "path": "src/caching.py",
      "line": 440
    },
    {
      "symbol": "get",
      "kind": "async_function",
      "path": "src/caching.py",
      "line": 448
    },
    {
      "symbol": "set",
      "kind": "async_function",
      "path": "src/caching.py",
      "line": 478
    },
    {
      "symbol": "delete",
      "kind": "async_function",
      "path": "src/caching.py",
      "line": 496
    },
    {
      "symbol": "exists",
      "kind": "async_function",
      "path": "src/caching.py",
      "line": 506
    },
    {
      "symbol": "clear",
      "kind": "async_function",
      "path": "src/caching.py",
      "line": 516
    },
    {
      "symbol": "size",
      "kind": "async_function",
      "path": "src/caching.py",
      "line": 526
    },
    {
      "symbol": "keys",
      "kind": "async_function",
      "path": "src/caching.py",
      "line": 536
    },
    {
      "symbol": "__init__",
      "kind": "function",
      "path": "src/caching.py",
      "line": 555
    },
    {
      "symbol": "get",
      "kind": "async_function",
      "path": "src/caching.py",
      "line": 560
    },
    {
      "symbol": "set",
      "kind": "async_function",
      "path": "src/caching.py",
      "line": 580
    },
    {
      "symbol": "delete",
      "kind": "async_function",
      "path": "src/caching.py",
      "line": 596
    },
    {
      "symbol": "exists",
      "kind": "async_function",
      "path": "src/caching.py",
      "line": 609
    },
    {
      "symbol": "clear",
      "kind": "async_function",
      "path": "src/caching.py",
      "line": 622
    },
    {
      "symbol": "size",
      "kind": "async_function",
      "path": "src/caching.py",
      "line": 635
    },
    {
      "symbol": "keys",
      "kind": "async_function",
      "path": "src/caching.py",
      "line": 644
    },
    {
      "symbol": "__init__",
      "kind": "function",
      "path": "src/caching.py",
      "line": 660
    },
    {
      "symbol": "get",
      "kind": "async_function",
      "path": "src/caching.py",
      "line": 667
    },
    {
      "symbol": "set",
      "kind": "async_function",
      "path": "src/caching.py",
      "line": 685
    },
    {
      "symbol": "get_or_set",
      "kind": "async_function",
      "path": "src/caching.py",
      "line": 705
    },
    {
      "symbol": "delete",
      "kind": "async_function",
      "path": "src/caching.py",
      "line": 714
    },
    {
      "symbol": "delete_by_tags",
      "kind": "async_function",
      "path": "src/caching.py",
      "line": 734
    },
    {
      "symbol": "invalidate_pattern",
      "kind": "async_function",
      "path": "src/caching.py",
      "line": 748
    },
    {
      "symbol": "exists",
      "kind": "async_function",
      "path": "src/caching.py",
      "line": 757
    },
    {
      "symbol": "clear",
      "kind": "async_function",
      "path": "src/caching.py",
      "line": 761
    },
    {
      "symbol": "size",
      "kind": "async_function",
      "path": "src/caching.py",
      "line": 778
    },
    {
      "symbol": "keys",
      "kind": "async_function",
      "path": "src/caching.py",
      "line": 782
    },
    {
      "symbol": "get_stats",
      "kind": "function",
      "path": "src/caching.py",
      "line": 786
    },
    {
      "symbol": "reset_stats",
      "kind": "function",
      "path": "src/caching.py",
      "line": 790
    },
    {
      "symbol": "cached",
      "kind": "function",
      "path": "src/caching.py",
      "line": 795
    },
    {
      "symbol": "fetch_user_data",
      "kind": "async_function",
      "path": "src/caching.py",
      "line": 894
    },
    {
      "symbol": "_get",
      "kind": "function",
      "path": "src/caching.py",
      "line": 360
    },
    {
      "symbol": "_set",
      "kind": "function",
      "path": "src/caching.py",
      "line": 370
    },
    {
      "symbol": "_delete",
      "kind": "function",
      "path": "src/caching.py",
      "line": 378
    },
    {
      "symbol": "_exists",
      "kind": "function",
      "path": "src/caching.py",
      "line": 385
    },
    {
      "symbol": "_clear",
      "kind": "function",
      "path": "src/caching.py",
      "line": 392
    },
    {
      "symbol": "_size",
      "kind": "function",
      "path": "src/caching.py",
      "line": 399
    },
    {
      "symbol": "_keys",
      "kind": "function",
      "path": "src/caching.py",
      "line": 406
    },
    {
      "symbol": "_get",
      "kind": "function",
      "path": "src/caching.py",
      "line": 449
    },
    {
      "symbol": "_set",
      "kind": "function",
      "path": "src/caching.py",
      "line": 479
    },
    {
      "symbol": "_delete",
      "kind": "function",
      "path": "src/caching.py",
      "line": 497
    },
    {
      "symbol": "_exists",
      "kind": "function",
      "path": "src/caching.py",
      "line": 507
    },
    {
      "symbol": "_clear",
      "kind": "function",
      "path": "src/caching.py",
      "line": 517
    },
    {
      "symbol": "_size",
      "kind": "function",
      "path": "src/caching.py",
      "line": 527
    },
    {
      "symbol": "_keys",
      "kind": "function",
      "path": "src/caching.py",
      "line": 537
    },
    {
      "symbol": "decorator",
      "kind": "function",
      "path": "src/caching.py",
      "line": 798
    },
    {
      "symbol": "wrapper",
      "kind": "async_function",
      "path": "src/caching.py",
      "line": 800
    },
    {
      "symbol": "AuthenticationError",
      "kind": "class",
      "path": "src/authentication.py",
      "line": 28
    },
    {
      "symbol": "InvalidCredentialsError",
      "kind": "class",
      "path": "src/authentication.py",
      "line": 33
    },
    {
      "symbol": "AccountLockedError",
      "kind": "class",
      "path": "src/authentication.py",
      "line": 38
    },
    {
      "symbol": "SessionExpiredError",
      "kind": "class",
      "path": "src/authentication.py",
      "line": 43
    },
    {
      "symbol": "TokenValidationError",
      "kind": "class",
      "path": "src/authentication.py",
      "line": 48
    },
    {
      "symbol": "UserStatus",
      "kind": "class",
      "path": "src/authentication.py",
      "line": 53
    },
    {
      "symbol": "AuthenticationMethod",
      "kind": "class",
      "path": "src/authentication.py",
      "line": 62
    },
    {
      "symbol": "User",
      "kind": "class",
      "path": "src/authentication.py",
      "line": 72
    },
    {
      "symbol": "Session",
      "kind": "class",
      "path": "src/authentication.py",
      "line": 135
    },
    {
      "symbol": "AuthToken",
      "kind": "class",
      "path": "src/authentication.py",
      "line": 162
    },
    {
      "symbol": "AuthConfig",
      "kind": "class",
      "path": "src/authentication.py",
      "line": 176
    },
    {
      "symbol": "AuthenticationService",
      "kind": "class",
      "path": "src/authentication.py",
      "line": 194
    },
    {
      "symbol": "RateLimiter",
      "kind": "class",
      "path": "src/authentication.py",
      "line": 442
    },
    {
      "symbol": "AuditLogger",
      "kind": "class",
      "path": "src/authentication.py",
      "line": 469
    },
    {
      "symbol": "UserStore",
      "kind": "class",
      "path": "src/authentication.py",
      "line": 504
    },
    {
      "symbol": "InMemoryUserStore",
      "kind": "class",
      "path": "src/authentication.py",
      "line": 525
    },
    {
      "symbol": "SessionStore",
      "kind": "class",
      "path": "src/authentication.py",
      "line": 560
    },
    {
      "symbol": "InMemorySessionStore",
      "kind": "class",
      "path": "src/authentication.py",
      "line": 578
    },
    {
      "symbol": "TokenStore",
      "kind": "class",
      "path": "src/authentication.py",
      "line": 608
    },
    {
      "symbol": "InMemoryTokenStore",
      "kind": "class",
      "path": "src/authentication.py",
      "line": 620
    },
    {
      "symbol": "generate_password_hash",
      "kind": "function",
      "path": "src/authentication.py",
      "line": 637
    },
    {
      "symbol": "verify_password",
      "kind": "function",
      "path": "src/authentication.py",
      "line": 642
    },
    {
      "symbol": "generate_secure_token",
      "kind": "function",
      "path": "src/authentication.py",
      "line": 647
    },
    {
      "symbol": "hash_string",
      "kind": "function",
      "path": "src/authentication.py",
      "line": 652
    },
    {
      "symbol": "create_hmac_signature",
      "kind": "function",
      "path": "src/authentication.py",
      "line": 659
    },
    {
      "symbol": "example_usage",
      "kind": "async_function",
      "path": "src/authentication.py",
      "line": 666
    },
    {
      "symbol": "is_locked",
      "kind": "function",
      "path": "src/authentication.py",
      "line": 92
    },
    {
      "symbol": "can_login",
      "kind": "function",
      "path": "src/authentication.py",
      "line": 100
    },
    {
      "symbol": "record_login_attempt",
      "kind": "function",
      "path": "src/authentication.py",
      "line": 106
    },
    {
      "symbol": "reset_password",
      "kind": "function",
      "path": "src/authentication.py",
      "line": 117
    },
    {
      "symbol": "_hash_password",
      "kind": "function",
      "path": "src/authentication.py",
      "line": 125
    },
    {
      "symbol": "verify_password",
      "kind": "function",
      "path": "src/authentication.py",
      "line": 129
    },
    {
      "symbol": "is_expired",
      "kind": "function",
      "path": "src/authentication.py",
      "line": 147
    },
    {
      "symbol": "extend",
      "kind": "function",
      "path": "src/authentication.py",
      "line": 151
    },
    {
      "symbol": "invalidate",
      "kind": "function",
      "path": "src/authentication.py",
      "line": 156
    },
    {
      "symbol": "is_expired",
      "kind": "function",
      "path": "src/authentication.py",
      "line": 171
    },
    {
      "symbol": "__init__",
      "kind": "function",
      "path": "src/authentication.py",
      "line": 178
    },
    {
      "symbol": "__init__",
      "kind": "function",
      "path": "src/authentication.py",
      "line": 197
    },
    {
      "symbol": "authenticate_user",
      "kind": "async_function",
      "path": "src/authentication.py",
      "line": 208
    },
    {
      "symbol": "authenticate_token",
      "kind": "async_function",
      "path": "src/authentication.py",
      "line": 252
    },
    {
      "symbol": "create_token",
      "kind": "async_function",
      "path": "src/authentication.py",
      "line": 286
    },
    {
      "symbol": "logout_user",
      "kind": "async_function",
      "path": "src/authentication.py",
      "line": 311
    },
    {
      "symbol": "initiate_password_reset",
      "kind": "async_function",
      "path": "src/authentication.py",
      "line": 319
    },
    {
      "symbol": "reset_password",
      "kind": "async_function",
      "path": "src/authentication.py",
      "line": 339
    },
    {
      "symbol": "change_password",
      "kind": "async_function",
      "path": "src/authentication.py",
      "line": 352
    },
    {
      "symbol": "enable_two_factor",
      "kind": "async_function",
      "path": "src/authentication.py",
      "line": 368
    },
    {
      "symbol": "verify_two_factor",
      "kind": "async_function",
      "path": "src/authentication.py",
      "line": 379
    },
    {
      "symbol": "require_auth",
      "kind": "function",
      "path": "src/authentication.py",
      "line": 389
    },
    {
      "symbol": "cleanup_expired_sessions",
      "kind": "async_function",
      "path": "src/authentication.py",
      "line": 413
    },
    {
      "symbol": "get_user_sessions",
      "kind": "async_function",
      "path": "src/authentication.py",
      "line": 417
    },
    {
      "symbol": "invalidate_user_sessions",
      "kind": "async_function",
      "path": "src/authentication.py",
      "line": 421
    },
    {
      "symbol": "_create_session",
      "kind": "async_function",
      "path": "src/authentication.py",
      "line": 429
    },
    {
      "symbol": "__init__",
      "kind": "function",
      "path": "src/authentication.py",
      "line": 445
    },
    {
      "symbol": "check_limit",
      "kind": "function",
      "path": "src/authentication.py",
      "line": 451
    },
    {
      "symbol": "log_successful_login",
      "kind": "async_function",
      "path": "src/authentication.py",
      "line": 472
    },
    {
      "symbol": "log_failed_login",
      "kind": "async_function",
      "path": "src/authentication.py",
      "line": 477
    },
    {
      "symbol": "log_logout",
      "kind": "async_function",
      "path": "src/authentication.py",
      "line": 482
    },
    {
      "symbol": "log_password_reset_initiated",
      "kind": "async_function",
      "path": "src/authentication.py",
      "line": 486
    },
    {
      "symbol": "log_password_reset_completed",
      "kind": "async_function",
      "path": "src/authentication.py",
      "line": 490
    },
    {
      "symbol": "log_password_changed",
      "kind": "async_function",
      "path": "src/authentication.py",
      "line": 494
    },
    {
      "symbol": "log_two_factor_enabled",
      "kind": "async_function",
      "path": "src/authentication.py",
      "line": 498
    },
    {
      "symbol": "get_user",
      "kind": "async_function",
      "path": "src/authentication.py",
      "line": 506
    },
    {
      "symbol": "get_user_by_username",
      "kind": "async_function",
      "path": "src/authentication.py",
      "line": 509
    },
    {
      "symbol": "get_user_by_email",
      "kind": "async_function",
      "path": "src/authentication.py",
      "line": 512
    },
    {
      "symbol": "get_user_by_reset_token",
      "kind": "async_function",
      "path": "src/authentication.py",
      "line": 515
    },
    {
      "symbol": "update_user",
      "kind": "async_function",
      "path": "src/authentication.py",
      "line": 518
    },
    {
      "symbol": "create_user",
      "kind": "async_function",
      "path": "src/authentication.py",
      "line": 521
    },
    {
      "symbol": "__init__",
      "kind": "function",
      "path": "src/authentication.py",
      "line": 528
    },
    {
      "symbol": "get_user",
      "kind": "async_function",
      "path": "src/authentication.py",
      "line": 534
    },
    {
      "symbol": "get_user_by_username",
      "kind": "async_function",
      "path": "src/authentication.py",
      "line": 537
    },
    {
      "symbol": "get_user_by_email",
      "kind": "async_function",
      "path": "src/authentication.py",
      "line": 541
    },
    {
      "symbol": "get_user_by_reset_token",
      "kind": "async_function",
      "path": "src/authentication.py",
      "line": 545
    },
    {
      "symbol": "update_user",
      "kind": "async_function",
      "path": "src/authentication.py",
      "line": 549
    },
    {
      "symbol": "create_user",
      "kind": "async_function",
      "path": "src/authentication.py",
      "line": 556
    },
    {
      "symbol": "store_session",
      "kind": "async_function",
      "path": "src/authentication.py",
      "line": 562
    },
    {
      "symbol": "get_session",
      "kind": "async_function",
      "path": "src/authentication.py",
      "line": 565
    },
    {
      "symbol": "update_session",
      "kind": "async_function",
      "path": "src/authentication.py",
      "line": 568
    },
    {
      "symbol": "get_user_sessions",
      "kind": "async_function",
      "path": "src/authentication.py",
      "line": 571
    },
    {
      "symbol": "cleanup_expired",
      "kind": "async_function",
      "path": "src/authentication.py",
      "line": 574
    },
    {
      "symbol": "__init__",
      "kind": "function",
      "path": "src/authentication.py",
      "line": 581
    },
    {
      "symbol": "store_session",
      "kind": "async_function",
      "path": "src/authentication.py",
      "line": 585
    },
    {
      "symbol": "get_session",
      "kind": "async_function",
      "path": "src/authentication.py",
      "line": 589
    },
    {
      "symbol": "update_session",
      "kind": "async_function",
      "path": "src/authentication.py",
      "line": 592
    },
    {
      "symbol": "get_user_sessions",
      "kind": "async_function",
      "path": "src/authentication.py",
      "line": 595
    },
    {
      "symbol": "cleanup_expired",
      "kind": "async_function",
      "path": "src/authentication.py",
      "line": 599
    },
    {
      "symbol": "store_token",
      "kind": "async_function",
      "path": "src/authentication.py",
      "line": 610
    },
    {
      "symbol": "get_token",
      "kind": "async_function",
      "path": "src/authentication.py",
      "line": 613
    },
    {
      "symbol": "invalidate_token",
      "kind": "async_function",
      "path": "src/authentication.py",
      "line": 616
    },
    {
      "symbol": "__init__",
      "kind": "function",
      "path": "src/authentication.py",
      "line": 623
    },
    {
      "symbol": "store_token",
      "kind": "async_function",
      "path": "src/authentication.py",
      "line": 626
    },
    {
      "symbol": "get_token",
      "kind": "async_function",
      "path": "src/authentication.py",
      "line": 629
    },
    {
      "symbol": "invalidate_token",
      "kind": "async_function",
      "path": "src/authentication.py",
      "line": 632
    },
    {
      "symbol": "decorator",
      "kind": "function",
      "path": "src/authentication.py",
      "line": 391
    },
    {
      "symbol": "wrapper",
      "kind": "async_function",
      "path": "src/authentication.py",
      "line": 393
    },
    {
      "symbol": "DecoratorManager",
      "kind": "class",
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 17
    },
    {
      "symbol": "Decorator",
      "kind": "interface",
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 138
    },
    {
      "symbol": "DecoratorFactory",
      "kind": "interface",
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 144
    },
    {
      "symbol": "LoggingDecoratorFactory",
      "kind": "class",
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 149
    },
    {
      "symbol": "LoggingDecorator",
      "kind": "class",
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 157
    },
    {
      "symbol": "CachingDecoratorFactory",
      "kind": "class",
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 189
    },
    {
      "symbol": "CachingDecorator",
      "kind": "class",
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 197
    },
    {
      "symbol": "ValidationDecoratorFactory",
      "kind": "class",
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 248
    },
    {
      "symbol": "ValidationDecorator",
      "kind": "class",
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 257
    },
    {
      "symbol": "PerformanceDecoratorFactory",
      "kind": "class",
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 289
    },
    {
      "symbol": "PerformanceDecorator",
      "kind": "class",
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 297
    },
    {
      "symbol": "SecurityDecoratorFactory",
      "kind": "class",
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 338
    },
    {
      "symbol": "SecurityDecorator",
      "kind": "class",
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 346
    },
    {
      "symbol": "RetryDecoratorFactory",
      "kind": "class",
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 402
    },
    {
      "symbol": "RetryDecorator",
      "kind": "class",
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 411
    },
    {
      "symbol": "TransactionDecoratorFactory",
      "kind": "class",
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 460
    },
    {
      "symbol": "TransactionDecorator",
      "kind": "class",
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 467
    },
    {
      "symbol": "AsyncDecoratorFactory",
      "kind": "class",
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 498
    },
    {
      "symbol": "AsyncDecorator",
      "kind": "class",
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 507
    },
    {
      "symbol": "CompressionDecoratorFactory",
      "kind": "class",
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 545
    },
    {
      "symbol": "CompressionDecorator",
      "kind": "class",
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 553
    },
    {
      "symbol": "EncryptionDecoratorFactory",
      "kind": "class",
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 590
    },
    {
      "symbol": "EncryptionDecorator",
      "kind": "class",
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 598
    },
    {
      "symbol": "FactoryManager",
      "kind": "class",
      "path": "src/main/java/com/example/FactoryManager.java",
      "line": 12
    },
    {
      "symbol": "ObjectFactory",
      "kind": "interface",
      "path": "src/main/java/com/example/FactoryManager.java",
      "line": 121
    },
    {
      "symbol": "ServiceRegistry",
      "kind": "interface",
      "path": "src/main/java/com/example/FactoryManager.java",
      "line": 126
    },
    {
      "symbol": "UserFactory",
      "kind": "class",
      "path": "src/main/java/com/example/FactoryManager.java",
      "line": 132
    },
    {
      "symbol": "UserServiceFactory",
      "kind": "class",
      "path": "src/main/java/com/example/FactoryManager.java",
      "line": 159
    },
    {
      "symbol": "PermissionManagerFactory",
      "kind": "class",
      "path": "src/main/java/com/example/FactoryManager.java",
      "line": 186
    },
    {
      "symbol": "DataProcessorFactory",
      "kind": "class",
      "path": "src/main/java/com/example/FactoryManager.java",
      "line": 199
    },
    {
      "symbol": "ReportGeneratorFactory",
      "kind": "class",
      "path": "src/main/java/com/example/FactoryManager.java",
      "line": 206
    },
    {
      "symbol": "AuditLoggerFactory",
      "kind": "class",
      "path": "src/main/java/com/example/FactoryManager.java",
      "line": 222
    },
    {
      "symbol": "CacheManagerFactory",
      "kind": "class",
      "path": "src/main/java/com/example/FactoryManager.java",
      "line": 229
    },
    {
      "symbol": "NotificationServiceFactory",
      "kind": "class",
      "path": "src/main/java/com/example/FactoryManager.java",
      "line": 236
    },
    {
      "symbol": "DatabaseServiceRegistry",
      "kind": "class",
      "path": "src/main/java/com/example/FactoryManager.java",
      "line": 244
    },
    {
      "symbol": "ApiServiceRegistry",
      "kind": "class",
      "path": "src/main/java/com/example/FactoryManager.java",
      "line": 259
    },
    {
      "symbol": "CacheServiceRegistry",
      "kind": "class",
      "path": "src/main/java/com/example/FactoryManager.java",
      "line": 274
    },
    {
      "symbol": "DefaultReportDataProvider",
      "kind": "class",
      "path": "src/main/java/com/example/FactoryManager.java",
      "line": 290
    },
    {
      "symbol": "CommandManager",
      "kind": "class",
      "path": "src/main/java/com/example/CommandManager.java",
      "line": 19
    },
    {
      "symbol": "Command",
      "kind": "interface",
      "path": "src/main/java/com/example/CommandManager.java",
      "line": 217
    },
    {
      "symbol": "CommandFactory",
      "kind": "interface",
      "path": "src/main/java/com/example/CommandManager.java",
      "line": 226
    },
    {
      "symbol": "FileCreateCommandFactory",
      "kind": "class",
      "path": "src/main/java/com/example/CommandManager.java",
      "line": 231
    },
    {
      "symbol": "FileCreateCommand",
      "kind": "class",
      "path": "src/main/java/com/example/CommandManager.java",
      "line": 240
    },
    {
      "symbol": "FileDeleteCommandFactory",
      "kind": "class",
      "path": "src/main/java/com/example/CommandManager.java",
      "line": 292
    },
    {
      "symbol": "FileDeleteCommand",
      "kind": "class",
      "path": "src/main/java/com/example/CommandManager.java",
      "line": 300
    },
    {
      "symbol": "FileCopyCommandFactory",
      "kind": "class",
      "path": "src/main/java/com/example/CommandManager.java",
      "line": 353
    },
    {
      "symbol": "FileCopyCommand",
      "kind": "class",
      "path": "src/main/java/com/example/CommandManager.java",
      "line": 362
    },
    {
      "symbol": "FileMoveCommandFactory",
      "kind": "class",
      "path": "src/main/java/com/example/CommandManager.java",
      "line": 414
    },
    {
      "symbol": "FileMoveCommand",
      "kind": "class",
      "path": "src/main/java/com/example/CommandManager.java",
      "line": 423
    },
    {
      "symbol": "DataInsertCommandFactory",
      "kind": "class",
      "path": "src/main/java/com/example/CommandManager.java",
      "line": 476
    },
    {
      "symbol": "DataInsertCommand",
      "kind": "class",
      "path": "src/main/java/com/example/CommandManager.java",
      "line": 485
    },
    {
      "symbol": "DataUpdateCommandFactory",
      "kind": "class",
      "path": "src/main/java/com/example/CommandManager.java",
      "line": 531
    },
    {
      "symbol": "DataUpdateCommand",
      "kind": "class",
      "path": "src/main/java/com/example/CommandManager.java",
      "line": 541
    },
    {
      "symbol": "DataDeleteCommandFactory",
      "kind": "class",
      "path": "src/main/java/com/example/CommandManager.java",
      "line": 591
    },
    {
      "symbol": "DataDeleteCommand",
      "kind": "class",
      "path": "src/main/java/com/example/CommandManager.java",
      "line": 600
    },
    {
      "symbol": "DataQueryCommandFactory",
      "kind": "class",
      "path": "src/main/java/com/example/CommandManager.java",
      "line": 648
    },
    {
      "symbol": "DataQueryCommand",
      "kind": "class",
      "path": "src/main/java/com/example/CommandManager.java",
      "line": 657
    },
    {
      "symbol": "UserCreateCommandFactory",
      "kind": "class",
      "path": "src/main/java/com/example/CommandManager.java",
      "line": 702
    },
    {
      "symbol": "UserUpdateCommandFactory",
      "kind": "class",
      "path": "src/main/java/com/example/CommandManager.java",
      "line": 711
    },
    {
      "symbol": "UserDeleteCommandFactory",
      "kind": "class",
      "path": "src/main/java/com/example/CommandManager.java",
      "line": 720
    },
    {
      "symbol": "UserCreateCommand",
      "kind": "class",
      "path": "src/main/java/com/example/CommandManager.java",
      "line": 728
    },
    {
      "symbol": "UserUpdateCommand",
      "kind": "class",
      "path": "src/main/java/com/example/CommandManager.java",
      "line": 773
    },
    {
      "symbol": "UserDeleteCommand",
      "kind": "class",
      "path": "src/main/java/com/example/CommandManager.java",
      "line": 817
    },
    {
      "symbol": "UserLoginCommandFactory",
      "kind": "class",
      "path": "src/main/java/com/example/CommandManager.java",
      "line": 860
    },
    {
      "symbol": "UserLoginCommand",
      "kind": "class",
      "path": "src/main/java/com/example/CommandManager.java",
      "line": 869
    },
    {
      "symbol": "SystemBackupCommandFactory",
      "kind": "class",
      "path": "src/main/java/com/example/CommandManager.java",
      "line": 919
    },
    {
      "symbol": "SystemRestoreCommandFactory",
      "kind": "class",
      "path": "src/main/java/com/example/CommandManager.java",
      "line": 928
    },
    {
      "symbol": "SystemShutdownCommandFactory",
      "kind": "class",
      "path": "src/main/java/com/example/CommandManager.java",
      "line": 937
    },
    {
      "symbol": "SystemRestartCommandFactory",
      "kind": "class",
      "path": "src/main/java/com/example/CommandManager.java",
      "line": 945
    },
    {
      "symbol": "SystemBackupCommand",
      "kind": "class",
      "path": "src/main/java/com/example/CommandManager.java",
      "line": 953
    },
    {
      "symbol": "SystemRestoreCommand",
      "kind": "class",
      "path": "src/main/java/com/example/CommandManager.java",
      "line": 998
    },
    {
      "symbol": "SystemShutdownCommand",
      "kind": "class",
      "path": "src/main/java/com/example/CommandManager.java",
      "line": 1039
    },
    {
      "symbol": "SystemRestartCommand",
      "kind": "class",
      "path": "src/main/java/com/example/CommandManager.java",
      "line": 1078
    },
    {
      "symbol": "NetworkConnectCommandFactory",
      "kind": "class",
      "path": "src/main/java/com/example/CommandManager.java",
      "line": 1118
    },
    {
      "symbol": "NetworkDisconnectCommandFactory",
      "kind": "class",
      "path": "src/main/java/com/example/CommandManager.java",
      "line": 1127
    },
    {
      "symbol": "NetworkSendCommandFactory",
      "kind": "class",
      "path": "src/main/java/com/example/CommandManager.java",
      "line": 1135
    },
    {
      "symbol": "NetworkReceiveCommandFactory",
      "kind": "class",
      "path": "src/main/java/com/example/CommandManager.java",
      "line": 1144
    },
    {
      "symbol": "NetworkConnectCommand",
      "kind": "class",
      "path": "src/main/java/com/example/CommandManager.java",
      "line": 1153
    },
    {
      "symbol": "NetworkDisconnectCommand",
      "kind": "class",
      "path": "src/main/java/com/example/CommandManager.java",
      "line": 1199
    },
    {
      "symbol": "NetworkSendCommand",
      "kind": "class",
      "path": "src/main/java/com/example/CommandManager.java",
      "line": 1238
    },
    {
      "symbol": "NetworkReceiveCommand",
      "kind": "class",
      "path": "src/main/java/com/example/CommandManager.java",
      "line": 1279
    },
    {
      "symbol": "CompositeCommandFactory",
      "kind": "class",
      "path": "src/main/java/com/example/CommandManager.java",
      "line": 1327
    },
    {
      "symbol": "CompositeCommand",
      "kind": "class",
      "path": "src/main/java/com/example/CommandManager.java",
      "line": 1336
    },
    {
      "symbol": "CommandQueue",
      "kind": "class",
      "path": "src/main/java/com/example/CommandManager.java",
      "line": 1402
    },
    {
      "symbol": "UserService",
      "kind": "class",
      "path": "src/main/java/com/example/UserService.java",
      "line": 18
    },
    {
      "symbol": "OperationType",
      "kind": "enum",
      "path": "src/main/java/com/example/UserService.java",
      "line": 32
    },
    {
      "symbol": "UserStatistics",
      "kind": "class",
      "path": "src/main/java/com/example/UserService.java",
      "line": 37
    },
    {
      "symbol": "AuditLogger",
      "kind": "class",
      "path": "src/main/java/com/example/UserService.java",
      "line": 87
    },
    {
      "symbol": "AuditEntry",
      "kind": "class",
      "path": "src/main/java/com/example/UserService.java",
      "line": 122
    },
    {
      "symbol": "UserServiceListener",
      "kind": "interface",
      "path": "src/main/java/com/example/UserService.java",
      "line": 142
    },
    {
      "symbol": "UserValidator",
      "kind": "class",
      "path": "src/main/java/com/example/UserService.java",
      "line": 148
    },
    {
      "symbol": "ValidationException",
      "kind": "class",
      "path": "src/main/java/com/example/UserService.java",
      "line": 163
    },
    {
      "symbol": "DuplicateUserException",
      "kind": "class",
      "path": "src/main/java/com/example/UserService.java",
      "line": 419
    },
    {
      "symbol": "UserNotFoundException",
      "kind": "class",
      "path": "src/main/java/com/example/UserService.java",
      "line": 425
    },
    {
      "symbol": "ReportGenerator",
      "kind": "class",
      "path": "src/main/java/com/example/ReportGenerator.java",
      "line": 24
    },
    {
      "symbol": "ReportType",
      "kind": "enum",
      "path": "src/main/java/com/example/ReportGenerator.java",
      "line": 35
    },
    {
      "symbol": "OutputFormat",
      "kind": "enum",
      "path": "src/main/java/com/example/ReportGenerator.java",
      "line": 57
    },
    {
      "symbol": "ReportTemplate",
      "kind": "class",
      "path": "src/main/java/com/example/ReportGenerator.java",
      "line": 490
    },
    {
      "symbol": "ReportResult",
      "kind": "class",
      "path": "src/main/java/com/example/ReportGenerator.java",
      "line": 505
    },
    {
      "symbol": "ReportDataProvider",
      "kind": "interface",
      "path": "src/main/java/com/example/ReportGenerator.java",
      "line": 525
    },
    {
      "symbol": "ReportDataGenerator",
      "kind": "interface",
      "path": "src/main/java/com/example/ReportGenerator.java",
      "line": 534
    },
    {
      "symbol": "UserActivityData",
      "kind": "class",
      "path": "src/main/java/com/example/ReportGenerator.java",
      "line": 539
    },
    {
      "symbol": "PerformanceMetric",
      "kind": "class",
      "path": "src/main/java/com/example/ReportGenerator.java",
      "line": 556
    },
    {
      "symbol": "FinancialData",
      "kind": "class",
      "path": "src/main/java/com/example/ReportGenerator.java",
      "line": 568
    },
    {
      "symbol": "AuditEventData",
      "kind": "class",
      "path": "src/main/java/com/example/ReportGenerator.java",
      "line": 585
    },
    {
      "symbol": "DepartmentData",
      "kind": "class",
      "path": "src/main/java/com/example/ReportGenerator.java",
      "line": 602
    },
    {
      "symbol": "ReportCache",
      "kind": "class",
      "path": "src/main/java/com/example/ReportGenerator.java",
      "line": 622
    },
    {
      "symbol": "EventSystem",
      "kind": "class",
      "path": "src/main/java/com/example/EventSystem.java",
      "line": 13
    },
    {
      "symbol": "Event",
      "kind": "class",
      "path": "src/main/java/com/example/EventSystem.java",
      "line": 259
    },
    {
      "symbol": "EventListener",
      "kind": "interface",
      "path": "src/main/java/com/example/EventSystem.java",
      "line": 283
    },
    {
      "symbol": "EventFilter",
      "kind": "interface",
      "path": "src/main/java/com/example/EventSystem.java",
      "line": 289
    },
    {
      "symbol": "EventTransformer",
      "kind": "interface",
      "path": "src/main/java/com/example/EventSystem.java",
      "line": 295
    },
    {
      "symbol": "EventQueue",
      "kind": "class",
      "path": "src/main/java/com/example/EventSystem.java",
      "line": 300
    },
    {
      "symbol": "EventStatistics",
      "kind": "class",
      "path": "src/main/java/com/example/EventSystem.java",
      "line": 336
    },
    {
      "symbol": "LoggingEventListener",
      "kind": "class",
      "path": "src/main/java/com/example/EventSystem.java",
      "line": 356
    },
    {
      "symbol": "MetricsEventListener",
      "kind": "class",
      "path": "src/main/java/com/example/EventSystem.java",
      "line": 370
    },
    {
      "symbol": "ConditionalEventListener",
      "kind": "class",
      "path": "src/main/java/com/example/EventSystem.java",
      "line": 387
    },
    {
      "symbol": "TypeBasedEventFilter",
      "kind": "class",
      "path": "src/main/java/com/example/EventSystem.java",
      "line": 405
    },
    {
      "symbol": "ContextBasedEventFilter",
      "kind": "class",
      "path": "src/main/java/com/example/EventSystem.java",
      "line": 418
    },
    {
      "symbol": "DataTransformingEventTransformer",
      "kind": "class",
      "path": "src/main/java/com/example/EventSystem.java",
      "line": 434
    },
    {
      "symbol": "ContextEnrichingEventTransformer",
      "kind": "class",
      "path": "src/main/java/com/example/EventSystem.java",
      "line": 449
    },
    {
      "symbol": "StrategyManager",
      "kind": "class",
      "path": "src/main/java/com/example/StrategyManager.java",
      "line": 15
    },
    {
      "symbol": "Strategy",
      "kind": "interface",
      "path": "src/main/java/com/example/StrategyManager.java",
      "line": 156
    },
    {
      "symbol": "StrategyFactory",
      "kind": "interface",
      "path": "src/main/java/com/example/StrategyManager.java",
      "line": 161
    },
    {
      "symbol": "StrategySelector",
      "kind": "interface",
      "path": "src/main/java/com/example/StrategyManager.java",
      "line": 166
    },
    {
      "symbol": "SortingStrategyFactory",
      "kind": "class",
      "path": "src/main/java/com/example/StrategyManager.java",
      "line": 171
    },
    {
      "symbol": "SearchingStrategyFactory",
      "kind": "class",
      "path": "src/main/java/com/example/StrategyManager.java",
      "line": 258
    },
    {
      "symbol": "CachingStrategyFactory",
      "kind": "class",
      "path": "src/main/java/com/example/StrategyManager.java",
      "line": 326
    },
    {
      "symbol": "NotificationStrategyFactory",
      "kind": "class",
      "path": "src/main/java/com/example/StrategyManager.java",
      "line": 343
    },
    {
      "symbol": "ValidationStrategyFactory",
      "kind": "class",
      "path": "src/main/java/com/example/StrategyManager.java",
      "line": 369
    },
    {
      "symbol": "PricingStrategyFactory",
      "kind": "class",
      "path": "src/main/java/com/example/StrategyManager.java",
      "line": 392
    },
    {
      "symbol": "DiscountStrategyFactory",
      "kind": "class",
      "path": "src/main/java/com/example/StrategyManager.java",
      "line": 415
    },
    {
      "symbol": "PaymentStrategyFactory",
      "kind": "class",
      "path": "src/main/java/com/example/StrategyManager.java",
      "line": 445
    },
    {
      "symbol": "ReportingStrategyFactory",
      "kind": "class",
      "path": "src/main/java/com/example/StrategyManager.java",
      "line": 473
    },
    {
      "symbol": "CompressionStrategyFactory",
      "kind": "class",
      "path": "src/main/java/com/example/StrategyManager.java",
      "line": 506
    },
    {
      "symbol": "CacheStrategy",
      "kind": "interface",
      "path": "src/main/java/com/example/StrategyManager.java",
      "line": 532
    },
    {
      "symbol": "LRUCacheStrategy",
      "kind": "class",
      "path": "src/main/java/com/example/StrategyManager.java",
      "line": 541
    },
    {
      "symbol": "LFUCacheStrategy",
      "kind": "class",
      "path": "src/main/java/com/example/StrategyManager.java",
      "line": 595
    },
    {
      "symbol": "FIFOCacheStrategy",
      "kind": "class",
      "path": "src/main/java/com/example/StrategyManager.java",
      "line": 664
    },
    {
      "symbol": "SearchInput",
      "kind": "class",
      "path": "src/main/java/com/example/StrategyManager.java",
      "line": 725
    },
    {
      "symbol": "NotificationData",
      "kind": "class",
      "path": "src/main/java/com/example/StrategyManager.java",
      "line": 735
    },
    {
      "symbol": "BulkDiscountInput",
      "kind": "class",
      "path": "src/main/java/com/example/StrategyManager.java",
      "line": 747
    },
    {
      "symbol": "PaymentData",
      "kind": "class",
      "path": "src/main/java/com/example/StrategyManager.java",
      "line": 757
    },
    {
      "symbol": "PaymentResult",
      "kind": "class",
      "path": "src/main/java/com/example/StrategyManager.java",
      "line": 769
    },
    {
      "symbol": "AdapterManager",
      "kind": "class",
      "path": "src/main/java/com/example/AdapterManager.java",
      "line": 22
    },
    {
      "symbol": "Adapter",
      "kind": "interface",
      "path": "src/main/java/com/example/AdapterManager.java",
      "line": 118
    },
    {
      "symbol": "AdapterFactory",
      "kind": "interface",
      "path": "src/main/java/com/example/AdapterManager.java",
      "line": 124
    },
    {
      "symbol": "DatabaseAdapterFactory",
      "kind": "class",
      "path": "src/main/java/com/example/AdapterManager.java",
      "line": 129
    },
    {
      "symbol": "DatabaseAdapter",
      "kind": "class",
      "path": "src/main/java/com/example/AdapterManager.java",
      "line": 137
    },
    {
      "symbol": "HttpAdapterFactory",
      "kind": "class",
      "path": "src/main/java/com/example/AdapterManager.java",
      "line": 159
    },
    {
      "symbol": "HttpAdapter",
      "kind": "class",
      "path": "src/main/java/com/example/AdapterManager.java",
      "line": 167
    },
    {
      "symbol": "FileSystemAdapterFactory",
      "kind": "class",
      "path": "src/main/java/com/example/AdapterManager.java",
      "line": 205
    },
    {
      "symbol": "FileSystemAdapter",
      "kind": "class",
      "path": "src/main/java/com/example/AdapterManager.java",
      "line": 213
    },
    {
      "symbol": "CacheAdapterFactory",
      "kind": "class",
      "path": "src/main/java/com/example/AdapterManager.java",
      "line": 237
    },
    {
      "symbol": "CacheAdapter",
      "kind": "class",
      "path": "src/main/java/com/example/AdapterManager.java",
      "line": 245
    },
    {
      "symbol": "MessageQueueAdapterFactory",
      "kind": "class",
      "path": "src/main/java/com/example/AdapterManager.java",
      "line": 271
    },
    {
      "symbol": "MessageQueueAdapter",
      "kind": "class",
      "path": "src/main/java/com/example/AdapterManager.java",
      "line": 279
    },
    {
      "symbol": "PaymentAdapterFactory",
      "kind": "class",
      "path": "src/main/java/com/example/AdapterManager.java",
      "line": 310
    },
    {
      "symbol": "PaymentAdapter",
      "kind": "class",
      "path": "src/main/java/com/example/AdapterManager.java",
      "line": 318
    },
    {
      "symbol": "EmailAdapterFactory",
      "kind": "class",
      "path": "src/main/java/com/example/AdapterManager.java",
      "line": 347
    },
    {
      "symbol": "EmailAdapter",
      "kind": "class",
      "path": "src/main/java/com/example/AdapterManager.java",
      "line": 355
    },
    {
      "symbol": "StorageAdapterFactory",
      "kind": "class",
      "path": "src/main/java/com/example/AdapterManager.java",
      "line": 385
    },
    {
      "symbol": "StorageAdapter",
      "kind": "class",
      "path": "src/main/java/com/example/AdapterManager.java",
      "line": 393
    },
    {
      "symbol": "AuthenticationAdapterFactory",
      "kind": "class",
      "path": "src/main/java/com/example/AdapterManager.java",
      "line": 422
    },
    {
      "symbol": "AuthenticationAdapter",
      "kind": "class",
      "path": "src/main/java/com/example/AdapterManager.java",
      "line": 430
    },
    {
      "symbol": "LoggingAdapterFactory",
      "kind": "class",
      "path": "src/main/java/com/example/AdapterManager.java",
      "line": 466
    },
    {
      "symbol": "LoggingAdapter",
      "kind": "class",
      "path": "src/main/java/com/example/AdapterManager.java",
      "line": 474
    },
    {
      "symbol": "CompositeAdapter",
      "kind": "class",
      "path": "src/main/java/com/example/AdapterManager.java",
      "line": 508
    },
    {
      "symbol": "AdapterChainBuilder",
      "kind": "class",
      "path": "src/main/java/com/example/AdapterManager.java",
      "line": 533
    },
    {
      "symbol": "AdvancedUtils",
      "kind": "class",
      "path": "src/main/java/com/example/AdvancedUtils.java",
      "line": 20
    },
    {
      "symbol": "TimeUtils",
      "kind": "class",
      "path": "src/main/java/com/example/AdvancedUtils.java",
      "line": 23
    },
    {
      "symbol": "StringUtils",
      "kind": "class",
      "path": "src/main/java/com/example/AdvancedUtils.java",
      "line": 85
    },
    {
      "symbol": "MathUtils",
      "kind": "class",
      "path": "src/main/java/com/example/AdvancedUtils.java",
      "line": 190
    },
    {
      "symbol": "CollectionUtils",
      "kind": "class",
      "path": "src/main/java/com/example/AdvancedUtils.java",
      "line": 283
    },
    {
      "symbol": "ValidationUtils",
      "kind": "class",
      "path": "src/main/java/com/example/AdvancedUtils.java",
      "line": 377
    },
    {
      "symbol": "ValidationResult",
      "kind": "class",
      "path": "src/main/java/com/example/AdvancedUtils.java",
      "line": 459
    },
    {
      "symbol": "ConcurrencyUtils",
      "kind": "class",
      "path": "src/main/java/com/example/AdvancedUtils.java",
      "line": 479
    },
    {
      "symbol": "CircuitBreaker",
      "kind": "class",
      "path": "src/main/java/com/example/AdvancedUtils.java",
      "line": 545
    },
    {
      "symbol": "RateLimiter",
      "kind": "class",
      "path": "src/main/java/com/example/AdvancedUtils.java",
      "line": 581
    },
    {
      "symbol": "FileUtils",
      "kind": "class",
      "path": "src/main/java/com/example/AdvancedUtils.java",
      "line": 617
    },
    {
      "symbol": "CryptoUtils",
      "kind": "class",
      "path": "src/main/java/com/example/AdvancedUtils.java",
      "line": 684
    },
    {
      "symbol": "NetworkUtils",
      "kind": "class",
      "path": "src/main/java/com/example/AdvancedUtils.java",
      "line": 732
    },
    {
      "symbol": "AuditLogger",
      "kind": "class",
      "path": "src/main/java/com/example/AuditLogger.java",
      "line": 15
    },
    {
      "symbol": "AuditEventType",
      "kind": "enum",
      "path": "src/main/java/com/example/AuditLogger.java",
      "line": 28
    },
    {
      "symbol": "AuditSeverity",
      "kind": "enum",
      "path": "src/main/java/com/example/AuditLogger.java",
      "line": 54
    },
    {
      "symbol": "AuditEvent",
      "kind": "class",
      "path": "src/main/java/com/example/AuditLogger.java",
      "line": 356
    },
    {
      "symbol": "AuditHandler",
      "kind": "interface",
      "path": "src/main/java/com/example/AuditLogger.java",
      "line": 392
    },
    {
      "symbol": "ConsoleAuditHandler",
      "kind": "class",
      "path": "src/main/java/com/example/AuditLogger.java",
      "line": 399
    },
    {
      "symbol": "FileAuditHandler",
      "kind": "class",
      "path": "src/main/java/com/example/AuditLogger.java",
      "line": 409
    },
    {
      "symbol": "DatabaseAuditHandler",
      "kind": "class",
      "path": "src/main/java/com/example/AuditLogger.java",
      "line": 428
    },
    {
      "symbol": "AuditStatistics",
      "kind": "class",
      "path": "src/main/java/com/example/AuditLogger.java",
      "line": 439
    },
    {
      "symbol": "ObserverManager",
      "kind": "class",
      "path": "src/main/java/com/example/ObserverManager.java",
      "line": 17
    },
    {
      "symbol": "Subject",
      "kind": "interface",
      "path": "src/main/java/com/example/ObserverManager.java",
      "line": 176
    },
    {
      "symbol": "Observer",
      "kind": "interface",
      "path": "src/main/java/com/example/ObserverManager.java",
      "line": 184
    },
    {
      "symbol": "NotificationStrategy",
      "kind": "interface",
      "path": "src/main/java/com/example/ObserverManager.java",
      "line": 191
    },
    {
      "symbol": "ConcreteSubject",
      "kind": "class",
      "path": "src/main/java/com/example/ObserverManager.java",
      "line": 197
    },
    {
      "symbol": "ImmediateNotificationStrategy",
      "kind": "class",
      "path": "src/main/java/com/example/ObserverManager.java",
      "line": 240
    },
    {
      "symbol": "AsyncNotificationStrategy",
      "kind": "class",
      "path": "src/main/java/com/example/ObserverManager.java",
      "line": 253
    },
    {
      "symbol": "BatchedNotificationStrategy",
      "kind": "class",
      "path": "src/main/java/com/example/ObserverManager.java",
      "line": 268
    },
    {
      "symbol": "FilteredNotificationStrategy",
      "kind": "class",
      "path": "src/main/java/com/example/ObserverManager.java",
      "line": 303
    },
    {
      "symbol": "PrioritizedNotificationStrategy",
      "kind": "class",
      "path": "src/main/java/com/example/ObserverManager.java",
      "line": 325
    },
    {
      "symbol": "NotificationTask",
      "kind": "class",
      "path": "src/main/java/com/example/ObserverManager.java",
      "line": 354
    },
    {
      "symbol": "AbstractObserver",
      "kind": "class",
      "path": "src/main/java/com/example/ObserverManager.java",
      "line": 369
    },
    {
      "symbol": "LoggingObserver",
      "kind": "class",
      "path": "src/main/java/com/example/ObserverManager.java",
      "line": 393
    },
    {
      "symbol": "EmailNotificationObserver",
      "kind": "class",
      "path": "src/main/java/com/example/ObserverManager.java",
      "line": 406
    },
    {
      "symbol": "DatabaseLoggingObserver",
      "kind": "class",
      "path": "src/main/java/com/example/ObserverManager.java",
      "line": 423
    },
    {
      "symbol": "PerformanceMonitoringObserver",
      "kind": "class",
      "path": "src/main/java/com/example/ObserverManager.java",
      "line": 437
    },
    {
      "symbol": "SecurityMonitoringObserver",
      "kind": "class",
      "path": "src/main/java/com/example/ObserverManager.java",
      "line": 481
    },
    {
      "symbol": "CacheInvalidationObserver",
      "kind": "class",
      "path": "src/main/java/com/example/ObserverManager.java",
      "line": 510
    },
    {
      "symbol": "BusinessRuleObserver",
      "kind": "class",
      "path": "src/main/java/com/example/ObserverManager.java",
      "line": 540
    },
    {
      "symbol": "ObserverFactory",
      "kind": "class",
      "path": "src/main/java/com/example/ObserverManager.java",
      "line": 580
    },
    {
      "symbol": "ObserverGroup",
      "kind": "class",
      "path": "src/main/java/com/example/ObserverManager.java",
      "line": 611
    },
    {
      "symbol": "DataProcessor",
      "kind": "class",
      "path": "src/main/java/com/example/DataProcessor.java",
      "line": 7
    },
    {
      "symbol": "PermissionManager",
      "kind": "class",
      "path": "src/main/java/com/example/PermissionManager.java",
      "line": 11
    },
    {
      "symbol": "PermissionRule",
      "kind": "class",
      "path": "src/main/java/com/example/PermissionManager.java",
      "line": 359
    },
    {
      "symbol": "PermissionEffect",
      "kind": "enum",
      "path": "src/main/java/com/example/PermissionManager.java",
      "line": 374
    },
    {
      "symbol": "PermissionCheckResult",
      "kind": "class",
      "path": "src/main/java/com/example/PermissionManager.java",
      "line": 381
    },
    {
      "symbol": "NotificationService",
      "kind": "class",
      "path": "src/main/java/com/example/NotificationService.java",
      "line": 7
    },
    {
      "symbol": "User",
      "kind": "class",
      "path": "src/main/java/com/example/User.java",
      "line": 14
    },
    {
      "symbol": "UserStatus",
      "kind": "enum",
      "path": "src/main/java/com/example/User.java",
      "line": 35
    },
    {
      "symbol": "Department",
      "kind": "enum",
      "path": "src/main/java/com/example/User.java",
      "line": 39
    },
    {
      "symbol": "UserPreferences",
      "kind": "class",
      "path": "src/main/java/com/example/User.java",
      "line": 44
    },
    {
      "symbol": "UserActivity",
      "kind": "class",
      "path": "src/main/java/com/example/User.java",
      "line": 81
    },
    {
      "symbol": "ValidationException",
      "kind": "class",
      "path": "src/main/java/com/example/User.java",
      "line": 359
    },
    {
      "symbol": "Builder",
      "kind": "class",
      "path": "src/main/java/com/example/User.java",
      "line": 366
    },
    {
      "symbol": "CacheManager",
      "kind": "class",
      "path": "src/main/java/com/example/CacheManager.java",
      "line": 10
    },
    {
      "symbol": "APIConfig",
      "kind": "class",
      "path": "src/main/python/api_client.py",
      "line": 29
    },
    {
      "symbol": "APIResponse",
      "kind": "class",
      "path": "src/main/python/api_client.py",
      "line": 41
    },
    {
      "symbol": "APIError",
      "kind": "class",
      "path": "src/main/python/api_client.py",
      "line": 51
    },
    {
      "symbol": "RateLimiter",
      "kind": "class",
      "path": "src/main/python/api_client.py",
      "line": 59
    },
    {
      "symbol": "APIClient",
      "kind": "class",
      "path": "src/main/python/api_client.py",
      "line": 84
    },
    {
      "symbol": "AsyncAPIClient",
      "kind": "class",
      "path": "src/main/python/api_client.py",
      "line": 208
    },
    {
      "symbol": "UserAPIClient",
      "kind": "class",
      "path": "src/main/python/api_client.py",
      "line": 295
    },
    {
      "symbol": "NotificationAPIClient",
      "kind": "class",
      "path": "src/main/python/api_client.py",
      "line": 336
    },
    {
      "symbol": "AnalyticsAPIClient",
      "kind": "class",
      "path": "src/main/python/api_client.py",
      "line": 381
    },
    {
      "symbol": "ExternalServiceIntegrator",
      "kind": "class",
      "path": "src/main/python/api_client.py",
      "line": 413
    },
    {
      "symbol": "get_external_integrator",
      "kind": "function",
      "path": "src/main/python/api_client.py",
      "line": 519
    },
    {
      "symbol": "initialize_external_services",
      "kind": "function",
      "path": "src/main/python/api_client.py",
      "line": 524
    },
    {
      "symbol": "__init__",
      "kind": "function",
      "path": "src/main/python/api_client.py",
      "line": 53
    },
    {
      "symbol": "__init__",
      "kind": "function",
      "path": "src/main/python/api_client.py",
      "line": 62
    },
    {
      "symbol": "wait_if_needed",
      "kind": "function",
      "path": "src/main/python/api_client.py",
      "line": 67
    },
    {
      "symbol": "__init__",
      "kind": "function",
      "path": "src/main/python/api_client.py",
      "line": 87
    },
    {
      "symbol": "_setup_auth",
      "kind": "function",
      "path": "src/main/python/api_client.py",
      "line": 93
    },
    {
      "symbol": "_generate_hmac_signature",
      "kind": "function",
      "path": "src/main/python/api_client.py",
      "line": 103
    },
    {
      "symbol": "_make_request",
      "kind": "function",
      "path": "src/main/python/api_client.py",
      "line": 121
    },
    {
      "symbol": "get",
      "kind": "function",
      "path": "src/main/python/api_client.py",
      "line": 183
    },
    {
      "symbol": "post",
      "kind": "function",
      "path": "src/main/python/api_client.py",
      "line": 187
    },
    {
      "symbol": "put",
      "kind": "function",
      "path": "src/main/python/api_client.py",
      "line": 195
    },
    {
      "symbol": "delete",
      "kind": "function",
      "path": "src/main/python/api_client.py",
      "line": 203
    },
    {
      "symbol": "__init__",
      "kind": "function",
      "path": "src/main/python/api_client.py",
      "line": 211
    },
    {
      "symbol": "_setup_auth",
      "kind": "function",
      "path": "src/main/python/api_client.py",
      "line": 216
    },
    {
      "symbol": "_make_request",
      "kind": "async_function",
      "path": "src/main/python/api_client.py",
      "line": 225
    },
    {
      "symbol": "get",
      "kind": "async_function",
      "path": "src/main/python/api_client.py",
      "line": 280
    },
    {
      "symbol": "post",
      "kind": "async_function",
      "path": "src/main/python/api_client.py",
      "line": 286
    },
    {
      "symbol": "__init__",
      "kind": "function",
      "path": "src/main/python/api_client.py",
      "line": 298
    },
    {
      "symbol": "get_user",
      "kind": "function",
      "path": "src/main/python/api_client.py",
      "line": 301
    },
    {
      "symbol": "create_user",
      "kind": "function",
      "path": "src/main/python/api_client.py",
      "line": 306
    },
    {
      "symbol": "update_user",
      "kind": "function",
      "path": "src/main/python/api_client.py",
      "line": 311
    },
    {
      "symbol": "delete_user",
      "kind": "function",
      "path": "src/main/python/api_client.py",
      "line": 316
    },
    {
      "symbol": "search_users",
      "kind": "function",
      "path": "src/main/python/api_client.py",
      "line": 321
    },
    {
      "symbol": "get_department_users",
      "kind": "function",
      "path": "src/main/python/api_client.py",
      "line": 330
    },
    {
      "symbol": "__init__",
      "kind": "function",
      "path": "src/main/python/api_client.py",
      "line": 339
    },
    {
      "symbol": "send_email",
      "kind": "function",
      "path": "src/main/python/api_client.py",
      "line": 342
    },
    {
      "symbol": "send_sms",
      "kind": "function",
      "path": "src/main/python/api_client.py",
      "line": 355
    },
    {
      "symbol": "send_push_notification",
      "kind": "function",
      "path": "src/main/python/api_client.py",
      "line": 364
    },
    {
      "symbol": "get_notification_history",
      "kind": "function",
      "path": "src/main/python/api_client.py",
      "line": 375
    },
    {
      "symbol": "__init__",
      "kind": "function",
      "path": "src/main/python/api_client.py",
      "line": 384
    },
    {
      "symbol": "track_event",
      "kind": "function",
      "path": "src/main/python/api_client.py",
      "line": 387
    },
    {
      "symbol": "get_user_analytics",
      "kind": "function",
      "path": "src/main/python/api_client.py",
      "line": 398
    },
    {
      "symbol": "get_system_metrics",
      "kind": "function",
      "path": "src/main/python/api_client.py",
      "line": 407
    },
    {
      "symbol": "__init__",
      "kind": "function",
      "path": "src/main/python/api_client.py",
      "line": 416
    },
    {
      "symbol": "configure_user_api",
      "kind": "function",
      "path": "src/main/python/api_client.py",
      "line": 422
    },
    {
      "symbol": "configure_notification_api",
      "kind": "function",
      "path": "src/main/python/api_client.py",
      "line": 426
    },
    {
      "symbol": "configure_analytics_api",
      "kind": "function",
      "path": "src/main/python/api_client.py",
      "line": 430
    },
    {
      "symbol": "sync_user_from_external",
      "kind": "function",
      "path": "src/main/python/api_client.py",
      "line": 434
    },
    {
      "symbol": "_transform_external_user",
      "kind": "function",
      "path": "src/main/python/api_client.py",
      "line": 449
    },
    {
      "symbol": "notify_user_action",
      "kind": "function",
      "path": "src/main/python/api_client.py",
      "line": 465
    },
    {
      "symbol": "track_user_activity",
      "kind": "function",
      "path": "src/main/python/api_client.py",
      "line": 499
    },
    {
      "symbol": "ConfigError",
      "kind": "class",
      "path": "src/main/python/config.py",
      "line": 23
    },
    {
      "symbol": "ConfigProvider",
      "kind": "class",
      "path": "src/main/python/config.py",
      "line": 28
    },
    {
      "symbol": "EnvironmentConfigProvider",
      "kind": "class",
      "path": "src/main/python/config.py",
      "line": 47
    },
    {
      "symbol": "FileConfigProvider",
      "kind": "class",
      "path": "src/main/python/config.py",
      "line": 94
    },
    {
      "symbol": "DatabaseConfigProvider",
      "kind": "class",
      "path": "src/main/python/config.py",
      "line": 157
    },
    {
      "symbol": "DatabaseSettings",
      "kind": "class",
      "path": "src/main/python/config.py",
      "line": 191
    },
    {
      "symbol": "EmailSettings",
      "kind": "class",
      "path": "src/main/python/config.py",
      "line": 203
    },
    {
      "symbol": "SecuritySettings",
      "kind": "class",
      "path": "src/main/python/config.py",
      "line": 214
    },
    {
      "symbol": "APISettings",
      "kind": "class",
      "path": "src/main/python/config.py",
      "line": 225
    },
    {
      "symbol": "NotificationSettings",
      "kind": "class",
      "path": "src/main/python/config.py",
      "line": 236
    },
    {
      "symbol": "LoggingSettings",
      "kind": "class",
      "path": "src/main/python/config.py",
      "line": 246
    },
    {
      "symbol": "ApplicationConfig",
      "kind": "class",
      "path": "src/main/python/config.py",
      "line": 257
    },
    {
      "symbol": "ConfigManager",
      "kind": "class",
      "path": "src/main/python/config.py",
      "line": 273
    },
    {
      "symbol": "get_config_manager",
      "kind": "function",
      "path": "src/main/python/config.py",
      "line": 439
    },
    {
      "symbol": "initialize_config",
      "kind": "function",
      "path": "src/main/python/config.py",
      "line": 444
    },
    {
      "symbol": "get_app_config",
      "kind": "function",
      "path": "src/main/python/config.py",
      "line": 459
    },
    {
      "symbol": "get_config",
      "kind": "function",
      "path": "src/main/python/config.py",
      "line": 464
    },
    {
      "symbol": "set_config",
      "kind": "function",
      "path": "src/main/python/config.py",
      "line": 469
    },
    {
      "symbol": "encrypt_config_value",
      "kind": "function",
      "path": "src/main/python/config.py",
      "line": 475
    },
    {
      "symbol": "decrypt_config_value",
      "kind": "function",
      "path": "src/main/python/config.py",
      "line": 482
    },
    {
      "symbol": "validate_config",
      "kind": "function",
      "path": "src/main/python/config.py",
      "line": 489
    },
    {
      "symbol": "ConfigWatcher",
      "kind": "class",
      "path": "src/main/python/config.py",
      "line": 518
    },
    {
      "symbol": "load_config",
      "kind": "function",
      "path": "src/main/python/config.py",
      "line": 32
    },
    {
      "symbol": "save_config",
      "kind": "function",
      "path": "src/main/python/config.py",
      "line": 37
    },
    {
      "symbol": "has_config",
      "kind": "function",
      "path": "src/main/python/config.py",
      "line": 42
    },
    {
      "symbol": "__init__",
      "kind": "function",
      "path": "src/main/python/config.py",
      "line": 50
    },
    {
      "symbol": "load_config",
      "kind": "function",
      "path": "src/main/python/config.py",
      "line": 53
    },
    {
      "symbol": "save_config",
      "kind": "function",
      "path": "src/main/python/config.py",
      "line": 60
    },
    {
      "symbol": "has_config",
      "kind": "function",
      "path": "src/main/python/config.py",
      "line": 65
    },
    {
      "symbol": "_parse_value",
      "kind": "function",
      "path": "src/main/python/config.py",
      "line": 69
    },
    {
      "symbol": "__init__",
      "kind": "function",
      "path": "src/main/python/config.py",
      "line": 97
    },
    {
      "symbol": "_get_file_path",
      "kind": "function",
      "path": "src/main/python/config.py",
      "line": 104
    },
    {
      "symbol": "load_config",
      "kind": "function",
      "path": "src/main/python/config.py",
      "line": 107
    },
    {
      "symbol": "save_config",
      "kind": "function",
      "path": "src/main/python/config.py",
      "line": 129
    },
    {
      "symbol": "has_config",
      "kind": "function",
      "path": "src/main/python/config.py",
      "line": 144
    },
    {
      "symbol": "invalidate_cache",
      "kind": "function",
      "path": "src/main/python/config.py",
      "line": 147
    },
    {
      "symbol": "__init__",
      "kind": "function",
      "path": "src/main/python/config.py",
      "line": 160
    },
    {
      "symbol": "load_config",
      "kind": "function",
      "path": "src/main/python/config.py",
      "line": 163
    },
    {
      "symbol": "save_config",
      "kind": "function",
      "path": "src/main/python/config.py",
      "line": 176
    },
    {
      "symbol": "has_config",
      "kind": "function",
      "path": "src/main/python/config.py",
      "line": 184
    },
    {
      "symbol": "__init__",
      "kind": "function",
      "path": "src/main/python/config.py",
      "line": 276
    },
    {
      "symbol": "add_provider",
      "kind": "function",
      "path": "src/main/python/config.py",
      "line": 281
    },
    {
      "symbol": "get_config",
      "kind": "function",
      "path": "src/main/python/config.py",
      "line": 293
    },
    {
      "symbol": "set_config",
      "kind": "function",
      "path": "src/main/python/config.py",
      "line": 313
    },
    {
      "symbol": "has_config",
      "kind": "function",
      "path": "src/main/python/config.py",
      "line": 323
    },
    {
      "symbol": "invalidate_cache",
      "kind": "function",
      "path": "src/main/python/config.py",
      "line": 330
    },
    {
      "symbol": "load_application_config",
      "kind": "function",
      "path": "src/main/python/config.py",
      "line": 343
    },
    {
      "symbol": "save_application_config",
      "kind": "function",
      "path": "src/main/python/config.py",
      "line": 390
    },
    {
      "symbol": "__init__",
      "kind": "function",
      "path": "src/main/python/config.py",
      "line": 521
    },
    {
      "symbol": "start_watching",
      "kind": "function",
      "path": "src/main/python/config.py",
      "line": 527
    },
    {
      "symbol": "stop_watching",
      "kind": "function",
      "path": "src/main/python/config.py",
      "line": 542
    },
    {
      "symbol": "_check_changes",
      "kind": "function",
      "path": "src/main/python/config.py",
      "line": 546
    },
    {
      "symbol": "watch_loop",
      "kind": "function",
      "path": "src/main/python/config.py",
      "line": 533
    },
    {
      "symbol": "DataProcessingError",
      "kind": "class",
      "path": "src/main/python/data_processor.py",
      "line": 30
    },
    {
      "symbol": "ValidationError",
      "kind": "class",
      "path": "src/main/python/data_processor.py",
      "line": 35
    },
    {
      "symbol": "ProcessingTimeoutError",
      "kind": "class",
      "path": "src/main/python/data_processor.py",
      "line": 40
    },
    {
      "symbol": "UserData",
      "kind": "class",
      "path": "src/main/python/data_processor.py",
      "line": 47
    },
    {
      "symbol": "ProcessingResult",
      "kind": "class",
      "path": "src/main/python/data_processor.py",
      "line": 84
    },
    {
      "symbol": "DataTransformer",
      "kind": "class",
      "path": "src/main/python/data_processor.py",
      "line": 94
    },
    {
      "symbol": "EmailNormalizer",
      "kind": "class",
      "path": "src/main/python/data_processor.py",
      "line": 108
    },
    {
      "symbol": "AgeCategorizer",
      "kind": "class",
      "path": "src/main/python/data_processor.py",
      "line": 121
    },
    {
      "symbol": "SkillAnalyzer",
      "kind": "class",
      "path": "src/main/python/data_processor.py",
      "line": 141
    },
    {
      "symbol": "timing_decorator",
      "kind": "function",
      "path": "src/main/python/data_processor.py",
      "line": 157
    },
    {
      "symbol": "retry_decorator",
      "kind": "function",
      "path": "src/main/python/data_processor.py",
      "line": 170
    },
    {
      "symbol": "ProcessingMode",
      "kind": "class",
      "path": "src/main/python/data_processor.py",
      "line": 189
    },
    {
      "symbol": "DataFormat",
      "kind": "class",
      "path": "src/main/python/data_processor.py",
      "line": 195
    },
    {
      "symbol": "DataProcessor",
      "kind": "class",
      "path": "src/main/python/data_processor.py",
      "line": 206
    },
    {
      "symbol": "create_data_processor",
      "kind": "function",
      "path": "src/main/python/data_processor.py",
      "line": 436
    },
    {
      "symbol": "DataProcessingContext",
      "kind": "class",
      "path": "src/main/python/data_processor.py",
      "line": 449
    },
    {
      "symbol": "data_stream_generator",
      "kind": "function",
      "path": "src/main/python/data_processor.py",
      "line": 467
    },
    {
      "symbol": "fibonacci_generator",
      "kind": "function",
      "path": "src/main/python/data_processor.py",
      "line": 474
    },
    {
      "symbol": "compose_transformers",
      "kind": "function",
      "path": "src/main/python/data_processor.py",
      "line": 485
    },
    {
      "symbol": "memoize",
      "kind": "function",
      "path": "src/main/python/data_processor.py",
      "line": 494
    },
    {
      "symbol": "expensive_calculation",
      "kind": "function",
      "path": "src/main/python/data_processor.py",
      "line": 508
    },
    {
      "symbol": "DataValidator",
      "kind": "class",
      "path": "src/main/python/data_processor.py",
      "line": 515
    },
    {
      "symbol": "ReportGenerator",
      "kind": "class",
      "path": "src/main/python/data_processor.py",
      "line": 546
    },
    {
      "symbol": "main",
      "kind": "function",
      "path": "src/main/python/data_processor.py",
      "line": 606
    },
    {
      "symbol": "validate",
      "kind": "function",
      "path": "src/main/python/data_processor.py",
      "line": 59
    },
    {
      "symbol": "to_dict",
      "kind": "function",
      "path": "src/main/python/data_processor.py",
      "line": 68
    },
    {
      "symbol": "transform",
      "kind": "function",
      "path": "src/main/python/data_processor.py",
      "line": 98
    },
    {
      "symbol": "get_name",
      "kind": "function",
      "path": "src/main/python/data_processor.py",
      "line": 103
    },
    {
      "symbol": "transform",
      "kind": "function",
      "path": "src/main/python/data_processor.py",
      "line": 111
    },
    {
      "symbol": "get_name",
      "kind": "function",
      "path": "src/main/python/data_processor.py",
      "line": 117
    },
    {
      "symbol": "transform",
      "kind": "function",
      "path": "src/main/python/data_processor.py",
      "line": 124
    },
    {
      "symbol": "get_name",
      "kind": "function",
      "path": "src/main/python/data_processor.py",
      "line": 137
    },
    {
      "symbol": "transform",
      "kind": "function",
      "path": "src/main/python/data_processor.py",
      "line": 144
    },
    {
      "symbol": "get_name",
      "kind": "function",
      "path": "src/main/python/data_processor.py",
      "line": 152
    },
    {
      "symbol": "wrapper",
      "kind": "function",
      "path": "src/main/python/data_processor.py",
      "line": 160
    },
    {
      "symbol": "decorator",
      "kind": "function",
      "path": "src/main/python/data_processor.py",
      "line": 172
    },
    {
      "symbol": "__init__",
      "kind": "function",
      "path": "src/main/python/data_processor.py",
      "line": 209
    },
    {
      "symbol": "add_transformer",
      "kind": "function",
      "path": "src/main/python/data_processor.py",
      "line": 216
    },
    {
      "symbol": "load_data",
      "kind": "function",
      "path": "src/main/python/data_processor.py",
      "line": 221
    },
    {
      "symbol": "process_data",
      "kind": "function",
      "path": "src/main/python/data_processor.py",
      "line": 238
    },
    {
      "symbol": "_add_complex_calculations",
      "kind": "function",
      "path": "src/main/python/data_processor.py",
      "line": 257
    },
    {
      "symbol": "_add_text_analysis",
      "kind": "function",
      "path": "src/main/python/data_processor.py",
      "line": 275
    },
    {
      "symbol": "_add_statistical_features",
      "kind": "function",
      "path": "src/main/python/data_processor.py",
      "line": 295
    },
    {
      "symbol": "calculate_stats",
      "kind": "function",
      "path": "src/main/python/data_processor.py",
      "line": 312
    },
    {
      "symbol": "save_processed_data",
      "kind": "function",
      "path": "src/main/python/data_processor.py",
      "line": 344
    },
    {
      "symbol": "process_async",
      "kind": "async_function",
      "path": "src/main/python/data_processor.py",
      "line": 358
    },
    {
      "symbol": "process_parallel",
      "kind": "function",
      "path": "src/main/python/data_processor.py",
      "line": 387
    },
    {
      "symbol": "__init__",
      "kind": "function",
      "path": "src/main/python/data_processor.py",
      "line": 452
    },
    {
      "symbol": "__enter__",
      "kind": "function",
      "path": "src/main/python/data_processor.py",
      "line": 455
    },
    {
      "symbol": "__exit__",
      "kind": "function",
      "path": "src/main/python/data_processor.py",
      "line": 459
    },
    {
      "symbol": "composed",
      "kind": "function",
      "path": "src/main/python/data_processor.py",
      "line": 487
    },
    {
      "symbol": "memoized",
      "kind": "function",
      "path": "src/main/python/data_processor.py",
      "line": 499
    },
    {
      "symbol": "__init__",
      "kind": "function",
      "path": "src/main/python/data_processor.py",
      "line": 518
    },
    {
      "symbol": "_default_rules",
      "kind": "function",
      "path": "src/main/python/data_processor.py",
      "line": 521
    },
    {
      "symbol": "validate_record",
      "kind": "function",
      "path": "src/main/python/data_processor.py",
      "line": 529
    },
    {
      "symbol": "validate_dataset",
      "kind": "function",
      "path": "src/main/python/data_processor.py",
      "line": 541
    },
    {
      "symbol": "__init__",
      "kind": "function",
      "path": "src/main/python/data_processor.py",
      "line": 549
    },
    {
      "symbol": "_default_template",
      "kind": "function",
      "path": "src/main/python/data_processor.py",
      "line": 552
    },
    {
      "symbol": "generate_report",
      "kind": "function",
      "path": "src/main/python/data_processor.py",
      "line": 576
    },
    {
      "symbol": "test_async",
      "kind": "async_function",
      "path": "src/main/python/data_processor.py",
      "line": 654
    },
    {
      "symbol": "wrapper",
      "kind": "function",
      "path": "src/main/python/data_processor.py",
      "line": 174
    },
    {
      "symbol": "worker",
      "kind": "function",
      "path": "src/main/python/data_processor.py",
      "line": 396
    },
    {
      "symbol": "DatabaseType",
      "kind": "class",
      "path": "src/main/python/database.py",
      "line": 22
    },
    {
      "symbol": "DatabaseConfig",
      "kind": "class",
      "path": "src/main/python/database.py",
      "line": 29
    },
    {
      "symbol": "DatabaseConnectionError",
      "kind": "class",
      "path": "src/main/python/database.py",
      "line": 42
    },
    {
      "symbol": "DatabaseQueryError",
      "kind": "class",
      "path": "src/main/python/database.py",
      "line": 47
    },
    {
      "symbol": "DatabaseManager",
      "kind": "class",
      "path": "src/main/python/database.py",
      "line": 52
    },
    {
      "symbol": "SQLiteManager",
      "kind": "class",
      "path": "src/main/python/database.py",
      "line": 107
    },
    {
      "symbol": "PostgreSQLManager",
      "kind": "class",
      "path": "src/main/python/database.py",
      "line": 190
    },
    {
      "symbol": "MySQLManager",
      "kind": "class",
      "path": "src/main/python/database.py",
      "line": 278
    },
    {
      "symbol": "DatabaseFactory",
      "kind": "class",
      "path": "src/main/python/database.py",
      "line": 366
    },
    {
      "symbol": "UserRepository",
      "kind": "class",
      "path": "src/main/python/database.py",
      "line": 381
    },
    {
      "symbol": "ActivityRepository",
      "kind": "class",
      "path": "src/main/python/database.py",
      "line": 462
    },
    {
      "symbol": "AuditRepository",
      "kind": "class",
      "path": "src/main/python/database.py",
      "line": 499
    },
    {
      "symbol": "initialize_database",
      "kind": "function",
      "path": "src/main/python/database.py",
      "line": 523
    },
    {
      "symbol": "get_user_repository",
      "kind": "function",
      "path": "src/main/python/database.py",
      "line": 537
    },
    {
      "symbol": "get_activity_repository",
      "kind": "function",
      "path": "src/main/python/database.py",
      "line": 544
    },
    {
      "symbol": "get_audit_repository",
      "kind": "function",
      "path": "src/main/python/database.py",
      "line": 551
    },
    {
      "symbol": "get_db_manager",
      "kind": "function",
      "path": "src/main/python/database.py",
      "line": 558
    },
    {
      "symbol": "__init__",
      "kind": "function",
      "path": "src/main/python/database.py",
      "line": 55
    },
    {
      "symbol": "connect",
      "kind": "function",
      "path": "src/main/python/database.py",
      "line": 61
    },
    {
      "symbol": "execute_query",
      "kind": "function",
      "path": "src/main/python/database.py",
      "line": 66
    },
    {
      "symbol": "execute_update",
      "kind": "function",
      "path": "src/main/python/database.py",
      "line": 71
    },
    {
      "symbol": "create_tables",
      "kind": "function",
      "path": "src/main/python/database.py",
      "line": 76
    },
    {
      "symbol": "get_connection",
      "kind": "function",
      "path": "src/main/python/database.py",
      "line": 80
    },
    {
      "symbol": "return_connection",
      "kind": "function",
      "path": "src/main/python/database.py",
      "line": 86
    },
    {
      "symbol": "transaction",
      "kind": "function",
      "path": "src/main/python/database.py",
      "line": 94
    },
    {
      "symbol": "connect",
      "kind": "function",
      "path": "src/main/python/database.py",
      "line": 110
    },
    {
      "symbol": "execute_query",
      "kind": "function",
      "path": "src/main/python/database.py",
      "line": 121
    },
    {
      "symbol": "execute_update",
      "kind": "function",
      "path": "src/main/python/database.py",
      "line": 133
    },
    {
      "symbol": "create_tables",
      "kind": "function",
      "path": "src/main/python/database.py",
      "line": 146
    },
    {
      "symbol": "connect",
      "kind": "function",
      "path": "src/main/python/database.py",
      "line": 193
    },
    {
      "symbol": "execute_query",
      "kind": "function",
      "path": "src/main/python/database.py",
      "line": 207
    },
    {
      "symbol": "execute_update",
      "kind": "function",
      "path": "src/main/python/database.py",
      "line": 220
    },
    {
      "symbol": "create_tables",
      "kind": "function",
      "path": "src/main/python/database.py",
      "line": 233
    },
    {
      "symbol": "connect",
      "kind": "function",
      "path": "src/main/python/database.py",
      "line": 281
    },
    {
      "symbol": "execute_query",
      "kind": "function",
      "path": "src/main/python/database.py",
      "line": 295
    },
    {
      "symbol": "execute_update",
      "kind": "function",
      "path": "src/main/python/database.py",
      "line": 307
    },
    {
      "symbol": "create_tables",
      "kind": "function",
      "path": "src/main/python/database.py",
      "line": 320
    },
    {
      "symbol": "create_manager",
      "kind": "function",
      "path": "src/main/python/database.py",
      "line": 370
    },
    {
      "symbol": "__init__",
      "kind": "function",
      "path": "src/main/python/database.py",
      "line": 384
    },
    {
      "symbol": "save_user",
      "kind": "function",
      "path": "src/main/python/database.py",
      "line": 387
    },
    {
      "symbol": "find_user_by_id",
      "kind": "function",
      "path": "src/main/python/database.py",
      "line": 414
    },
    {
      "symbol": "find_users_by_department",
      "kind": "function",
      "path": "src/main/python/database.py",
      "line": 425
    },
    {
      "symbol": "delete_user",
      "kind": "function",
      "path": "src/main/python/database.py",
      "line": 434
    },
    {
      "symbol": "get_all_users",
      "kind": "function",
      "path": "src/main/python/database.py",
      "line": 439
    },
    {
      "symbol": "search_users",
      "kind": "function",
      "path": "src/main/python/database.py",
      "line": 448
    },
    {
      "symbol": "__init__",
      "kind": "function",
      "path": "src/main/python/database.py",
      "line": 465
    },
    {
      "symbol": "save_activity",
      "kind": "function",
      "path": "src/main/python/database.py",
      "line": 468
    },
    {
      "symbol": "get_user_activities",
      "kind": "function",
      "path": "src/main/python/database.py",
      "line": 485
    },
    {
      "symbol": "__init__",
      "kind": "function",
      "path": "src/main/python/database.py",
      "line": 502
    },
    {
      "symbol": "log_operation",
      "kind": "function",
      "path": "src/main/python/database.py",
      "line": 505
    },
    {
      "symbol": "get_recent_logs",
      "kind": "function",
      "path": "src/main/python/database.py",
      "line": 510
    },
    {
      "symbol": "NotificationType",
      "kind": "class",
      "path": "src/main/python/notification.py",
      "line": 27
    },
    {
      "symbol": "NotificationPriority",
      "kind": "class",
      "path": "src/main/python/notification.py",
      "line": 36
    },
    {
      "symbol": "NotificationMessage",
      "kind": "class",
      "path": "src/main/python/notification.py",
      "line": 44
    },
    {
      "symbol": "NotificationResult",
      "kind": "class",
      "path": "src/main/python/notification.py",
      "line": 63
    },
    {
      "symbol": "NotificationProvider",
      "kind": "class",
      "path": "src/main/python/notification.py",
      "line": 72
    },
    {
      "symbol": "EmailConfig",
      "kind": "class",
      "path": "src/main/python/notification.py",
      "line": 87
    },
    {
      "symbol": "EmailProvider",
      "kind": "class",
      "path": "src/main/python/notification.py",
      "line": 101
    },
    {
      "symbol": "SMSConfig",
      "kind": "class",
      "path": "src/main/python/notification.py",
      "line": 159
    },
    {
      "symbol": "SMSProvider",
      "kind": "class",
      "path": "src/main/python/notification.py",
      "line": 167
    },
    {
      "symbol": "PushConfig",
      "kind": "class",
      "path": "src/main/python/notification.py",
      "line": 229
    },
    {
      "symbol": "PushProvider",
      "kind": "class",
      "path": "src/main/python/notification.py",
      "line": 236
    },
    {
      "symbol": "NotificationTemplate",
      "kind": "class",
      "path": "src/main/python/notification.py",
      "line": 298
    },
    {
      "symbol": "NotificationManager",
      "kind": "class",
      "path": "src/main/python/notification.py",
      "line": 362
    },
    {
      "symbol": "get_notification_manager",
      "kind": "function",
      "path": "src/main/python/notification.py",
      "line": 489
    },
    {
      "symbol": "initialize_notifications",
      "kind": "function",
      "path": "src/main/python/notification.py",
      "line": 494
    },
    {
      "symbol": "send_welcome_email",
      "kind": "function",
      "path": "src/main/python/notification.py",
      "line": 518
    },
    {
      "symbol": "send_password_reset_email",
      "kind": "function",
      "path": "src/main/python/notification.py",
      "line": 528
    },
    {
      "symbol": "send_activity_notification",
      "kind": "function",
      "path": "src/main/python/notification.py",
      "line": 538
    },
    {
      "symbol": "queue_bulk_notifications",
      "kind": "function",
      "path": "src/main/python/notification.py",
      "line": 553
    },
    {
      "symbol": "__post_init__",
      "kind": "function",
      "path": "src/main/python/notification.py",
      "line": 55
    },
    {
      "symbol": "send_notification",
      "kind": "async_function",
      "path": "src/main/python/notification.py",
      "line": 76
    },
    {
      "symbol": "get_provider_name",
      "kind": "function",
      "path": "src/main/python/notification.py",
      "line": 81
    },
    {
      "symbol": "__post_init__",
      "kind": "function",
      "path": "src/main/python/notification.py",
      "line": 96
    },
    {
      "symbol": "__init__",
      "kind": "function",
      "path": "src/main/python/notification.py",
      "line": 104
    },
    {
      "symbol": "send_notification",
      "kind": "async_function",
      "path": "src/main/python/notification.py",
      "line": 107
    },
    {
      "symbol": "get_provider_name",
      "kind": "function",
      "path": "src/main/python/notification.py",
      "line": 154
    },
    {
      "symbol": "__init__",
      "kind": "function",
      "path": "src/main/python/notification.py",
      "line": 170
    },
    {
      "symbol": "send_notification",
      "kind": "async_function",
      "path": "src/main/python/notification.py",
      "line": 173
    },
    {
      "symbol": "get_provider_name",
      "kind": "function",
      "path": "src/main/python/notification.py",
      "line": 224
    },
    {
      "symbol": "__init__",
      "kind": "function",
      "path": "src/main/python/notification.py",
      "line": 239
    },
    {
      "symbol": "send_notification",
      "kind": "async_function",
      "path": "src/main/python/notification.py",
      "line": 242
    },
    {
      "symbol": "get_provider_name",
      "kind": "function",
      "path": "src/main/python/notification.py",
      "line": 294
    },
    {
      "symbol": "__init__",
      "kind": "function",
      "path": "src/main/python/notification.py",
      "line": 301
    },
    {
      "symbol": "_load_templates",
      "kind": "function",
      "path": "src/main/python/notification.py",
      "line": 304
    },
    {
      "symbol": "render_template",
      "kind": "function",
      "path": "src/main/python/notification.py",
      "line": 342
    },
    {
      "symbol": "_replace_variables",
      "kind": "function",
      "path": "src/main/python/notification.py",
      "line": 354
    },
    {
      "symbol": "__init__",
      "kind": "function",
      "path": "src/main/python/notification.py",
      "line": 365
    },
    {
      "symbol": "register_provider",
      "kind": "function",
      "path": "src/main/python/notification.py",
      "line": 373
    },
    {
      "symbol": "unregister_provider",
      "kind": "function",
      "path": "src/main/python/notification.py",
      "line": 378
    },
    {
      "symbol": "send_notification",
      "kind": "function",
      "path": "src/main/python/notification.py",
      "line": 384
    },
    {
      "symbol": "send_notification_async",
      "kind": "async_function",
      "path": "src/main/python/notification.py",
      "line": 402
    },
    {
      "symbol": "send_notification_from_template",
      "kind": "function",
      "path": "src/main/python/notification.py",
      "line": 413
    },
    {
      "symbol": "queue_notification",
      "kind": "function",
      "path": "src/main/python/notification.py",
      "line": 433
    },
    {
      "symbol": "start_worker",
      "kind": "function",
      "path": "src/main/python/notification.py",
      "line": 438
    },
    {
      "symbol": "stop_worker",
      "kind": "function",
      "path": "src/main/python/notification.py",
      "line": 449
    },
    {
      "symbol": "_process_queue",
      "kind": "function",
      "path": "src/main/python/notification.py",
      "line": 456
    },
    {
      "symbol": "get_queue_size",
      "kind": "function",
      "path": "src/main/python/notification.py",
      "line": 475
    },
    {
      "symbol": "get_registered_providers",
      "kind": "function",
      "path": "src/main/python/notification.py",
      "line": 479
    }
  ],
  "tool_iter": 1,
  "call_index": 2
}
```

### Think Reflection
Reflection recorded: The project appears to be a multi-language (Java and Python) system with a rich set of features. 

Key modules identified:
1.  **Caching**: `src/caching.py`, `src/main/java/com/example/CacheManager.java`. Supports multiple backends (Memory, Redis, SQLite, Distributed), serialization (Pickle, JSON), and strategies (LRU, LFU, FIFO).
2.  **Authentication & Security**: `src/authentication.py`, `src/main/java/com/example/PermissionManager.java`. Includes user management, session handling, token validation, 2FA, rate limiting, and audit logging.
3.  **Data Processing & Reporting**: `src/main/python/data_processor.py`, `src/main/java/com/example/DataProcessor.java`, `src/main/java/com/example/ReportGenerator.java`. Features data transformation, validation, statistical analysis, and report generation in various formats.
4.  **Database Management**: `src/main/python/database.py`. Supports SQLite, PostgreSQL, MySQL, and repository patterns for users, activities, and audits.
5.  **Notification System**: `src/main/python/notification.py`, `src/main/java/com/example/NotificationService.java`. Supports Email, SMS, and Push notifications with template rendering and queuing.
6.  **API Client**: `src/main/python/api_client.py`. Synchronous and asynchronous clients for external services, including user, notification, and analytics APIs.
7.  **Configuration Management**: `src/main/python/config.py`. Supports environment, file, and database-based configurations with encryption and watching capabilities.
8.  **Design Patterns & Infrastructure**: 
    *   **Command Pattern**: `src/main/java/com/example/CommandManager.java` (File, Data, User, System, Network commands).
    *   **Observer Pattern**: `src/main/java/com/example/ObserverManager.java`.
    *   **Strategy Pattern**: `src/main/java/com/example/StrategyManager.java`.
    *   **Adapter Pattern**: `src/main/java/com/example/AdapterManager.java`.
    *   **Decorator Pattern**: `src/main/java/com/example/DecoratorManager.java`.
    *   **Factory Pattern**: `src/main/java/com/example/FactoryManager.java`.
    *   **Event System**: `src/main/java/com/example/EventSystem.java`.
    *   **Utilities**: `src/main/java/com/example/AdvancedUtils.java` (Time, String, Math, Collection, Validation, Concurrency, etc.).

I have a good overview of the modules and their public interfaces. I'll do a quick check of `README.md` to see if there's a high-level summary that aligns with these findings. I'll also check `pom.xml` and `requirements.txt` to see external dependencies which might hint at more features.

### Call 3
```json
{
  "tool": "read_file_range_tool",
  "args": {
    "start_line": 1,
    "path": "/home/ran/Documents/work/VectorCode/mini_code_index/test_code_index_project/README.md",
    "end_line": 50
  },
  "result": {
    "content": "# Test Code Index Project\n\n这是一个用于测试代码索引功能的示例项目，包含 Java 和 Python 代码。\n\n## 项目结构\n\n- `src/main/java/com/example/` - Java 源代码\n- `src/main/python/` - Python 脚本\n- `pom.xml` - Maven 配置（Java）\n- `requirements.txt` - Python 依赖\n\n## 功能\n\n- Java 部分：用户管理服务\n- Python 部分：数据处理工具\n\n## 运行\n\n### Java\n```bash\nmvn compile\nmvn exec:java -Dexec.mainClass=\"com.example.UserService\"\n```\n\n### Python\n```bash\npython src/main/python/data_processor.py\n```"
  },
  "tool_iter": 3,
  "call_index": 1
}
```

### Call 4
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
  "tool_iter": 3,
  "call_index": 2
}
```

### Call 5
```json
{
  "tool": "read_file_range_tool",
  "args": {
    "path": "/home/ran/Documents/work/VectorCode/mini_code_index/test_code_index_project/pom.xml",
    "end_line": 50,
    "start_line": 1
  },
  "result": {
    "content": "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<project xmlns=\"http://maven.apache.org/POM/4.0.0\"\n         xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n         xsi:schemaLocation=\"http://maven.apache.org/POM/4.0.0\n         http://maven.apache.org/xsd/maven-4.0.0.xsd\">\n    <modelVersion>4.0.0</modelVersion>\n\n    <groupId>com.example</groupId>\n    <artifactId>test-code-index</artifactId>\n    <version>1.0-SNAPSHOT</version>\n\n    <properties>\n        <maven.compiler.source>11</maven.compiler.source>\n        <maven.compiler.target>11</maven.compiler.target>\n    </properties>\n\n    <dependencies>\n        <dependency>\n            <groupId>com.google.code.gson</groupId>\n            <artifactId>gson</artifactId>\n            <version>2.10.1</version>\n        </dependency>\n    </dependencies>\n</project>"
  },
  "tool_iter": 3,
  "call_index": 3
}
```

### Think Reflection
Reflection recorded: The README is very basic and doesn't provide much detail beyond what I've already found. The `requirements.txt` confirms `requests`, `pandas`, and `numpy`, which supports the API client and data processing findings. `pom.xml` shows `gson`, supporting JSON serialization in Java.

I have enough information to categorize the key features and capabilities based on the module names and public interfaces.

Categories:
1.  **User Management & Security**: Authentication, session management, 2FA, permissions, and audit logging.
2.  **Data Management & Processing**: Data transformation, validation, statistical analysis (using pandas/numpy), and multi-format report generation.
3.  **Infrastructure & Integration**: Multi-backend caching, database abstraction (SQL), API clients (sync/async), and notification services (Email, SMS, Push).
4.  **System Architecture & Design Patterns**: Extensive use of design patterns (Command, Observer, Strategy, Adapter, Decorator, Factory) and an event-driven system.
5.  **Configuration & Utilities**: Flexible configuration management and a comprehensive set of utility functions for common tasks.

I'll do one last check on `src/main/java/com/example/UserService.java` and `src/main/python/data_processor.py` to see if there are any other major public interfaces I missed. I'll also check `src/main/java/com/example/EventSystem.java` to see how it's used.

### Call 6
```json
{
  "tool": "read_file_range_tool",
  "args": {
    "end_line": 100,
    "path": "/home/ran/Documents/work/VectorCode/mini_code_index/test_code_index_project/src/main/java/com/example/UserService.java",
    "start_line": 1
  },
  "result": {
    "content": "package com.example;\n\nimport java.util.*;\nimport java.util.concurrent.ConcurrentHashMap;\nimport java.util.concurrent.locks.ReadWriteLock;\nimport java.util.concurrent.locks.ReentrantReadWriteLock;\nimport java.util.stream.Collectors;\nimport java.util.function.Predicate;\nimport java.util.function.Function;\nimport java.util.function.Consumer;\nimport java.time.LocalDateTime;\nimport java.time.temporal.ChronoUnit;\n\n/**\n * 用户服务类，提供用户管理的功能\n * 支持并发操作、缓存、审计日志等高级功能\n */\npublic class UserService {\n    private final Map<String, User> users;\n    private final ReadWriteLock lock;\n    private final Map<String, User> userCache;\n    private final List<UserServiceListener> listeners;\n    private final AuditLogger auditLogger;\n    private final UserValidator validator;\n    private final UserStatistics statistics;\n\n    // 常量\n    private static final int MAX_CACHE_SIZE = 1000;\n    private static final long CACHE_EXPIRY_MINUTES = 30;\n\n    // 枚举\n    public enum OperationType {\n        CREATE, READ, UPDATE, DELETE, SEARCH\n    }\n\n    // 内部类\n    public static class UserStatistics {\n        private int totalUsers;\n        private int activeUsers;\n        private Map<String, Integer> departmentCounts;\n        private Map<String, Integer> skillCounts;\n        private double averageAge;\n        private LocalDateTime lastUpdated;\n\n        public UserStatistics() {\n            this.departmentCounts = new HashMap<>();\n            this.skillCounts = new HashMap<>();\n            this.lastUpdated = LocalDateTime.now();\n        }\n\n        public synchronized void update(List<User> users) {\n            this.totalUsers = users.size();\n            this.activeUsers = (int) users.stream()\n                    .filter(user -> !user.getRoles().contains(\"inactive\"))\n                    .count();\n\n            this.departmentCounts = users.stream()\n                    .collect(Collectors.groupingBy(\n                            User::getDepartment,\n                            Collectors.summingInt(user -> 1)\n                    ));\n\n            this.skillCounts = users.stream()\n                    .flatMap(user -> user.getSkills().stream())\n                    .collect(Collectors.groupingBy(\n                            skill -> skill,\n                            Collectors.summingInt(skill -> 1)\n                    ));\n\n            this.averageAge = users.stream()\n                    .mapToInt(User::getAge)\n                    .average()\n                    .orElse(0.0);\n\n            this.lastUpdated = LocalDateTime.now();\n        }\n\n        // Getters\n        public int getTotalUsers() { return totalUsers; }\n        public int getActiveUsers() { return activeUsers; }\n        public Map<String, Integer> getDepartmentCounts() { return new HashMap<>(departmentCounts); }\n        public Map<String, Integer> getSkillCounts() { return new HashMap<>(skillCounts); }\n        public double getAverageAge() { return averageAge; }\n        public LocalDateTime getLastUpdated() { return lastUpdated; }\n    }\n\n    public static class AuditLogger {\n        private final List<AuditEntry> auditLog;\n\n        public AuditLogger() {\n            this.auditLog = new ArrayList<>();\n        }\n\n        public void log(OperationType operation, String userId, String details) {\n            AuditEntry entry = new AuditEntry(operation, userId, details, LocalDateTime.now());\n            synchronized (auditLog) {\n                auditLog.add(entry);\n                // 保持日志大小\n                if (auditLog.size() > 10000) {\n                    auditLog.remove(0);"
  },
  "tool_iter": 5,
  "call_index": 1
}
```

### Call 7
```json
{
  "tool": "read_file_range_tool",
  "args": {
    "path": "/home/ran/Documents/work/VectorCode/mini_code_index/test_code_index_project/src/main/python/data_processor.py",
    "start_line": 1,
    "end_line": 100
  },
  "result": {
    "content": "#!/usr/bin/env python3\n\"\"\"\n数据处理脚本\n用于处理和分析用户数据\n\"\"\"\n\nimport json\nimport pandas as pd\nimport numpy as np\nfrom typing import List, Dict, Any, Optional, Union, Callable\nimport logging\nimport asyncio\nimport threading\nfrom dataclasses import dataclass, field\nfrom abc import ABC, abstractmethod\nimport functools\nfrom collections import defaultdict, namedtuple\nimport re\nimport datetime\nimport random\nimport math\n\n\n# 配置日志\nlogging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')\nlogger = logging.getLogger(__name__)\n\n\n# 自定义异常\nclass DataProcessingError(Exception):\n    \"\"\"数据处理异常\"\"\"\n    pass\n\n\nclass ValidationError(DataProcessingError):\n    \"\"\"验证错误\"\"\"\n    pass\n\n\nclass ProcessingTimeoutError(DataProcessingError):\n    \"\"\"处理超时错误\"\"\"\n    pass\n\n\n# 数据类\n@dataclass\nclass UserData:\n    \"\"\"用户数据类\"\"\"\n    id: str\n    name: str\n    email: str\n    age: Optional[int] = None\n    department: str = \"general\"\n    skills: List[str] = field(default_factory=list)\n    metadata: Dict[str, Any] = field(default_factory=dict)\n    created_at: datetime.datetime = field(default_factory=datetime.datetime.now)\n    updated_at: datetime.datetime = field(default_factory=datetime.datetime.now)\n\n    def validate(self) -> None:\n        \"\"\"验证用户数据\"\"\"\n        if not self.id:\n            raise ValidationError(\"ID cannot be empty\")\n        if not re.match(r'^[^@]+@[^@]+\\.[^@]+$', self.email):\n            raise ValidationError(\"Invalid email format\")\n        if self.age is not None and (self.age < 0 or self.age > 150):\n            raise ValidationError(\"Invalid age\")\n\n    def to_dict(self) -> Dict[str, Any]:\n        \"\"\"转换为字典\"\"\"\n        return {\n            'id': self.id,\n            'name': self.name,\n            'email': self.email,\n            'age': self.age,\n            'department': self.department,\n            'skills': self.skills,\n            'metadata': self.metadata,\n            'created_at': self.created_at.isoformat(),\n            'updated_at': self.updated_at.isoformat()\n        }\n\n\n@dataclass\nclass ProcessingResult:\n    \"\"\"处理结果类\"\"\"\n    success: bool\n    data: Optional[pd.DataFrame] = None\n    errors: List[str] = field(default_factory=list)\n    stats: Dict[str, Any] = field(default_factory=dict)\n    processing_time: float = 0.0\n\n\n# 抽象基类\nclass DataTransformer(ABC):\n    \"\"\"数据转换器抽象基类\"\"\"\n\n    @abstractmethod\n    def transform(self, data: pd.DataFrame) -> pd.DataFrame:\n        \"\"\"转换数据\"\"\"\n        pass"
  },
  "tool_iter": 5,
  "call_index": 2
}
```

### Call 8
```json
{
  "tool": "read_file_range_tool",
  "args": {
    "start_line": 1,
    "end_line": 100,
    "path": "/home/ran/Documents/work/VectorCode/mini_code_index/test_code_index_project/src/main/java/com/example/EventSystem.java"
  },
  "result": {
    "content": "package com.example;\n\nimport java.util.*;\nimport java.util.concurrent.*;\nimport java.util.concurrent.atomic.*;\nimport java.util.function.*;\nimport java.util.stream.*;\n\n/**\n * 观察者模式实现\n * 事件驱动的系统架构\n */\npublic class EventSystem {\n\n    // 单例模式\n    private static volatile EventSystem instance;\n    private static final Object LOCK = new Object();\n\n    private final Map<String, List<EventListener<?>>> listeners;\n    private final Map<String, EventQueue> eventQueues;\n    private final ExecutorService executorService;\n    private final Map<String, EventFilter> filters;\n    private final Map<String, EventTransformer> transformers;\n\n    private EventSystem() {\n        this.listeners = new ConcurrentHashMap<>();\n        this.eventQueues = new ConcurrentHashMap<>();\n        this.executorService = Executors.newFixedThreadPool(10);\n        this.filters = new ConcurrentHashMap<>();\n        this.transformers = new ConcurrentHashMap<>();\n\n        initializeDefaultEvents();\n        startEventProcessor();\n    }\n\n    public static EventSystem getInstance() {\n        if (instance == null) {\n            synchronized (LOCK) {\n                if (instance == null) {\n                    instance = new EventSystem();\n                }\n            }\n        }\n        return instance;\n    }\n\n    /**\n     * 初始化默认事件\n     */\n    private void initializeDefaultEvents() {\n        // 用户相关事件\n        registerEventType(\"user.created\");\n        registerEventType(\"user.updated\");\n        registerEventType(\"user.deleted\");\n        registerEventType(\"user.login\");\n        registerEventType(\"user.logout\");\n\n        // 系统事件\n        registerEventType(\"system.startup\");\n        registerEventType(\"system.shutdown\");\n        registerEventType(\"system.error\");\n\n        // 数据事件\n        registerEventType(\"data.processed\");\n        registerEventType(\"data.exported\");\n        registerEventType(\"data.imported\");\n\n        // 安全事件\n        registerEventType(\"security.violation\");\n        registerEventType(\"security.login_failure\");\n        registerEventType(\"security.permission_denied\");\n\n        // 业务事件\n        registerEventType(\"business.transaction_completed\");\n        registerEventType(\"business.report_generated\");\n        registerEventType(\"business.notification_sent\");\n    }\n\n    /**\n     * 注册事件类型\n     */\n    public void registerEventType(String eventType) {\n        listeners.putIfAbsent(eventType, new CopyOnWriteArrayList<>());\n        eventQueues.putIfAbsent(eventType, new EventQueue(eventType));\n    }\n\n    /**\n     * 添加事件监听器\n     */\n    public <T> void addListener(String eventType, EventListener<T> listener) {\n        listeners.computeIfAbsent(eventType, k -> new CopyOnWriteArrayList<>()).add(listener);\n    }\n\n    /**\n     * 移除事件监听器\n     */\n    public <T> void removeListener(String eventType, EventListener<T> listener) {\n        List<EventListener<?>> eventListeners = listeners.get(eventType);\n        if (eventListeners != null) {\n            eventListeners.remove(listener);"
  },
  "tool_iter": 5,
  "call_index": 3
}
```

### Think Reflection
Reflection recorded: I have gathered sufficient evidence to summarize the core functionalities of the project. 

The project is a comprehensive system that integrates Java and Python to provide a wide range of features, from user management and security to advanced data processing and infrastructure services.

Key functionalities include:
1.  **User Management & Security**:
    *   Comprehensive user lifecycle management (CRUD, search, statistics).
    *   Robust authentication (sessions, tokens, 2FA, password hashing).
    *   Fine-grained authorization (permission rules, effects).
    *   Security monitoring (rate limiting, audit logging, security event tracking).

2.  **Data Processing & Analytics**:
    *   Data transformation and normalization (using pandas/numpy).
    *   Statistical analysis and metric calculation.
    *   Multi-format report generation (PDF, CSV, Excel, HTML, JSON).
    *   Asynchronous and parallel data processing.

3.  **Infrastructure & Integration**:
    *   Multi-backend caching system (Memory, Redis, SQLite, Distributed).
    *   Database abstraction layer supporting multiple SQL dialects.
    *   Multi-channel notification system (Email, SMS, Push) with template support.
    *   Synchronous and asynchronous API clients for external service integration.

4.  **System Architecture & Design Patterns**:
    *   Event-driven architecture with a centralized event system.
    *   Extensive use of design patterns (Command, Strategy, Adapter, Decorator, Factory, Observer).
    *   Flexible configuration management (Environment, File, Database).

5.  **Utilities & Cross-cutting Concerns**:
    *   Advanced utility classes for common operations (Time, String, Math, Crypto, Network).
    *   Circuit breaker and rate limiting for system resilience.
    *   Comprehensive logging and monitoring.

I am ready to call RetrievalComplete.

### Call 9
```json
{
  "tool": "RetrievalComplete",
  "args": {},
  "result": "Retrieval marked complete",
  "tool_iter": 7,
  "call_index": 1
}
```