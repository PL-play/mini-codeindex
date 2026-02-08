# Subtask Debug Report

**Title**: Scan for structural keywords
**Instruction**: Search the codebase for common design pattern naming conventions such as 'Factory', 'Singleton', 'Strategy', 'Adapter', 'Proxy', 'Observer', 'Builder', and 'Decorator'.

## Tool Calls
### Think Reflection
Reflection recorded: I will search for the specified design pattern keywords ('Factory', 'Singleton', 'Strategy', 'Adapter', 'Proxy', 'Observer', 'Builder', 'Decorator') across the codebase to identify structural patterns. I'll start with a broad text search for these terms.

### Call 1
```json
{
  "tool": "text_search_tool",
  "args": {
    "query": "Factory|Singleton|Strategy|Adapter|Proxy|Observer|Builder|Decorator",
    "is_regex": true,
    "root_dir": "/home/ran/Documents/work/VectorCode/mini_code_index/test_code_index_project"
  },
  "result": [
    {
      "path": "target/classes/com/example/AdapterManager$AdapterFactory.class",
      "line": 1,
      "col": 25,
      "snippet": "\u0000\u0000\u00007\u0000\u0013\u0007\u0000\u0002\u0001\u0000)com/example/AdapterManager$AdapterFactory\u0007\u0000\u0004\u0001\u0000\u0010java/lang/Object\u0001\u0000\u0006create\u0001\u00009([Ljava/lang/Object;)Lcom/example/AdapterManager$Adapter;\u0001\u0000\tSignature\u0001\u0000=([Ljava/lang/Object;)Lcom/example/AdapterManager$Adapter<**>;\u0001\u0000",
      "context_before": "",
      "context_after": "SourceFile\u0001\u0000\u0013AdapterManager.java\u0001\u0000\nInnerClasses\u0007\u0000"
    },
    {
      "path": "target/classes/com/example/AdapterManager$AdapterFactory.class",
      "line": 1,
      "col": 40,
      "snippet": "\u0000\u0000\u00007\u0000\u0013\u0007\u0000\u0002\u0001\u0000)com/example/AdapterManager$AdapterFactory\u0007\u0000\u0004\u0001\u0000\u0010java/lang/Object\u0001\u0000\u0006create\u0001\u00009([Ljava/lang/Object;)Lcom/example/AdapterManager$Adapter;\u0001\u0000\tSignature\u0001\u0000=([Ljava/lang/Object;)Lcom/example/AdapterManager$Adapter<**>;\u0001\u0000",
      "context_before": "",
      "context_after": "SourceFile\u0001\u0000\u0013AdapterManager.java\u0001\u0000\nInnerClasses\u0007\u0000"
    },
    {
      "path": "target/classes/com/example/AdapterManager$AdapterFactory.class",
      "line": 1,
      "col": 47,
      "snippet": "\u0000\u0000\u00007\u0000\u0013\u0007\u0000\u0002\u0001\u0000)com/example/AdapterManager$AdapterFactory\u0007\u0000\u0004\u0001\u0000\u0010java/lang/Object\u0001\u0000\u0006create\u0001\u00009([Ljava/lang/Object;)Lcom/example/AdapterManager$Adapter;\u0001\u0000\tSignature\u0001\u0000=([Ljava/lang/Object;)Lcom/example/AdapterManager$Adapter<**>;\u0001\u0000",
      "context_before": "",
      "context_after": "SourceFile\u0001\u0000\u0013AdapterManager.java\u0001\u0000\nInnerClasses\u0007\u0000"
    },
    {
      "path": "target/classes/com/example/AdapterManager$AdapterFactory.class",
      "line": 1,
      "col": 122,
      "snippet": "\u0000\u0000\u00007\u0000\u0013\u0007\u0000\u0002\u0001\u0000)com/example/AdapterManager$AdapterFactory\u0007\u0000\u0004\u0001\u0000\u0010java/lang/Object\u0001\u0000\u0006create\u0001\u00009([Ljava/lang/Object;)Lcom/example/AdapterManager$Adapter;\u0001\u0000\tSignature\u0001\u0000=([Ljava/lang/Object;)Lcom/example/AdapterManager$Adapter<**>;\u0001\u0000",
      "context_before": "",
      "context_after": "SourceFile\u0001\u0000\u0013AdapterManager.java\u0001\u0000\nInnerClasses\u0007\u0000"
    },
    {
      "path": "target/classes/com/example/AdapterManager$AdapterFactory.class",
      "line": 1,
      "col": 137,
      "snippet": "\u0000\u0000\u00007\u0000\u0013\u0007\u0000\u0002\u0001\u0000)com/example/AdapterManager$AdapterFactory\u0007\u0000\u0004\u0001\u0000\u0010java/lang/Object\u0001\u0000\u0006create\u0001\u00009([Ljava/lang/Object;)Lcom/example/AdapterManager$Adapter;\u0001\u0000\tSignature\u0001\u0000=([Ljava/lang/Object;)Lcom/example/AdapterManager$Adapter<**>;\u0001\u0000",
      "context_before": "",
      "context_after": "SourceFile\u0001\u0000\u0013AdapterManager.java\u0001\u0000\nInnerClasses\u0007\u0000"
    },
    {
      "path": "target/classes/com/example/AdapterManager$AdapterFactory.class",
      "line": 1,
      "col": 194,
      "snippet": "\u0000\u0000\u00007\u0000\u0013\u0007\u0000\u0002\u0001\u0000)com/example/AdapterManager$AdapterFactory\u0007\u0000\u0004\u0001\u0000\u0010java/lang/Object\u0001\u0000\u0006create\u0001\u00009([Ljava/lang/Object;)Lcom/example/AdapterManager$Adapter;\u0001\u0000\tSignature\u0001\u0000=([Ljava/lang/Object;)Lcom/example/AdapterManager$Adapter<**>;\u0001\u0000",
      "context_before": "",
      "context_after": "SourceFile\u0001\u0000\u0013AdapterManager.java\u0001\u0000\nInnerClasses\u0007\u0000"
    },
    {
      "path": "target/classes/com/example/AdapterManager$AdapterFactory.class",
      "line": 1,
      "col": 209,
      "snippet": "\u0000\u0000\u00007\u0000\u0013\u0007\u0000\u0002\u0001\u0000)com/example/AdapterManager$AdapterFactory\u0007\u0000\u0004\u0001\u0000\u0010java/lang/Object\u0001\u0000\u0006create\u0001\u00009([Ljava/lang/Object;)Lcom/example/AdapterManager$Adapter;\u0001\u0000\tSignature\u0001\u0000=([Ljava/lang/Object;)Lcom/example/AdapterManager$Adapter<**>;\u0001\u0000",
      "context_before": "",
      "context_after": "SourceFile\u0001\u0000\u0013AdapterManager.java\u0001\u0000\nInnerClasses\u0007\u0000"
    },
    {
      "path": "target/classes/com/example/AdapterManager$AdapterFactory.class",
      "line": 2,
      "col": 14,
      "snippet": "SourceFile\u0001\u0000\u0013AdapterManager.java\u0001\u0000",
      "context_before": "\u0000\u0000\u00007\u0000\u0013\u0007\u0000\u0002\u0001\u0000)com/example/AdapterManager$AdapterFactory\u0007\u0000\u0004\u0001\u0000\u0010java/lang/Object\u0001\u0000\u0006create\u0001\u00009([Ljava/lang/Object;)Lcom/example/AdapterManager$Adapter;\u0001\u0000\tSignature\u0001\u0000=([Ljava/lang/Object;)Lcom/example/AdapterManager$Adapter<**>;\u0001\u0000",
      "context_after": "InnerClasses\u0007\u0000\n\u0001\u0000\"com/example/AdapterManager$Adapter\u0007\u0000\u000f\u0001\u0000\u001acom/example/AdapterManager\u0001\u0000\u0007Adapter\u0001\u0000\u000eAdapterFactory\u0001\u0000\bNestHost\u0006\u0001\u0000\u0001\u0000\u0003\u0000\u0000\u0000\u0000\u0000\u0001\u0004\u0000\u0005\u0000\u0006\u0000\u0001\u0000\u0007\u0000\u0000\u0000\u0002\u0000\b\u0000\u0003\u0000\t\u0000\u0000\u0000\u0002\u0000"
    },
    {
      "path": "target/classes/com/example/AdapterManager$AdapterFactory.class",
      "line": 4,
      "col": 16,
      "snippet": "\u0001\u0000\"com/example/AdapterManager$Adapter\u0007\u0000\u000f\u0001\u0000\u001acom/example/AdapterManager\u0001\u0000\u0007Adapter\u0001\u0000\u000eAdapterFactory\u0001\u0000\bNestHost\u0006\u0001\u0000\u0001\u0000\u0003\u0000\u0000\u0000\u0000\u0000\u0001\u0004\u0000\u0005\u0000\u0006\u0000\u0001\u0000\u0007\u0000\u0000\u0000\u0002\u0000\b\u0000\u0003\u0000\t\u0000\u0000\u0000\u0002\u0000",
      "context_before": "SourceFile\u0001\u0000\u0013AdapterManager.java\u0001\u0000\nInnerClasses\u0007\u0000",
      "context_after": "\u0000\n\u0000\u0000\u0000\u0012\u0000\u0002\u0000"
    },
    {
      "path": "target/classes/com/example/AdapterManager$AdapterFactory.class",
      "line": 4,
      "col": 31,
      "snippet": "\u0001\u0000\"com/example/AdapterManager$Adapter\u0007\u0000\u000f\u0001\u0000\u001acom/example/AdapterManager\u0001\u0000\u0007Adapter\u0001\u0000\u000eAdapterFactory\u0001\u0000\bNestHost\u0006\u0001\u0000\u0001\u0000\u0003\u0000\u0000\u0000\u0000\u0000\u0001\u0004\u0000\u0005\u0000\u0006\u0000\u0001\u0000\u0007\u0000\u0000\u0000\u0002\u0000\b\u0000\u0003\u0000\t\u0000\u0000\u0000\u0002\u0000",
      "context_before": "SourceFile\u0001\u0000\u0013AdapterManager.java\u0001\u0000\nInnerClasses\u0007\u0000",
      "context_after": "\u0000\n\u0000\u0000\u0000\u0012\u0000\u0002\u0000"
    },
    {
      "path": "target/classes/com/example/AdapterManager$AdapterFactory.class",
      "line": 4,
      "col": 56,
      "snippet": "\u0001\u0000\"com/example/AdapterManager$Adapter\u0007\u0000\u000f\u0001\u0000\u001acom/example/AdapterManager\u0001\u0000\u0007Adapter\u0001\u0000\u000eAdapterFactory\u0001\u0000\bNestHost\u0006\u0001\u0000\u0001\u0000\u0003\u0000\u0000\u0000\u0000\u0000\u0001\u0004\u0000\u0005\u0000\u0006\u0000\u0001\u0000\u0007\u0000\u0000\u0000\u0002\u0000\b\u0000\u0003\u0000\t\u0000\u0000\u0000\u0002\u0000",
      "context_before": "SourceFile\u0001\u0000\u0013AdapterManager.java\u0001\u0000\nInnerClasses\u0007\u0000",
      "context_after": "\u0000\n\u0000\u0000\u0000\u0012\u0000\u0002\u0000"
    },
    {
      "path": "target/classes/com/example/AdapterManager$AdapterFactory.class",
      "line": 4,
      "col": 73,
      "snippet": "\u0001\u0000\"com/example/AdapterManager$Adapter\u0007\u0000\u000f\u0001\u0000\u001acom/example/AdapterManager\u0001\u0000\u0007Adapter\u0001\u0000\u000eAdapterFactory\u0001\u0000\bNestHost\u0006\u0001\u0000\u0001\u0000\u0003\u0000\u0000\u0000\u0000\u0000\u0001\u0004\u0000\u0005\u0000\u0006\u0000\u0001\u0000\u0007\u0000\u0000\u0000\u0002\u0000\b\u0000\u0003\u0000\t\u0000\u0000\u0000\u0002\u0000",
      "context_before": "SourceFile\u0001\u0000\u0013AdapterManager.java\u0001\u0000\nInnerClasses\u0007\u0000",
      "context_after": "\u0000\n\u0000\u0000\u0000\u0012\u0000\u0002\u0000"
    },
    {
      "path": "target/classes/com/example/AdapterManager$AdapterFactory.class",
      "line": 4,
      "col": 83,
      "snippet": "\u0001\u0000\"com/example/AdapterManager$Adapter\u0007\u0000\u000f\u0001\u0000\u001acom/example/AdapterManager\u0001\u0000\u0007Adapter\u0001\u0000\u000eAdapterFactory\u0001\u0000\bNestHost\u0006\u0001\u0000\u0001\u0000\u0003\u0000\u0000\u0000\u0000\u0000\u0001\u0004\u0000\u0005\u0000\u0006\u0000\u0001\u0000\u0007\u0000\u0000\u0000\u0002\u0000\b\u0000\u0003\u0000\t\u0000\u0000\u0000\u0002\u0000",
      "context_before": "SourceFile\u0001\u0000\u0013AdapterManager.java\u0001\u0000\nInnerClasses\u0007\u0000",
      "context_after": "\u0000\n\u0000\u0000\u0000\u0012\u0000\u0002\u0000"
    },
    {
      "path": "target/classes/com/example/AdapterManager$AdapterFactory.class",
      "line": 4,
      "col": 90,
      "snippet": "\u0001\u0000\"com/example/AdapterManager$Adapter\u0007\u0000\u000f\u0001\u0000\u001acom/example/AdapterManager\u0001\u0000\u0007Adapter\u0001\u0000\u000eAdapterFactory\u0001\u0000\bNestHost\u0006\u0001\u0000\u0001\u0000\u0003\u0000\u0000\u0000\u0000\u0000\u0001\u0004\u0000\u0005\u0000\u0006\u0000\u0001\u0000\u0007\u0000\u0000\u0000\u0002\u0000\b\u0000\u0003\u0000\t\u0000\u0000\u0000\u0002\u0000",
      "context_before": "SourceFile\u0001\u0000\u0013AdapterManager.java\u0001\u0000\nInnerClasses\u0007\u0000",
      "context_after": "\u0000\n\u0000\u0000\u0000\u0012\u0000\u0002\u0000"
    },
    {
      "path": "target/classes/com/example/DecoratorManager$LoggingDecorator.class",
      "line": 1,
      "col": 25,
      "snippet": "\u0000\u0000\u00007\u0000n\u0007\u0000\u0002\u0001\u0000-com/example/DecoratorManager$LoggingDecorator\u0007\u0000\u0004\u0001\u0000\u0010java/lang/Object\u0007\u0000\u0006\u0001\u0000&com/example/DecoratorManager$Decorator\u0001\u0000",
      "context_before": "",
      "context_after": "loggerName\u0001\u0000\u0012Ljava/lang/String;\u0001\u0000\u0006<init>\u0001\u0000\u0015(Ljava/lang/String;)V\u0001\u0000\u0004Code\n\u0000\u0003\u0000"
    },
    {
      "path": "target/classes/com/example/DecoratorManager$LoggingDecorator.class",
      "line": 1,
      "col": 49,
      "snippet": "\u0000\u0000\u00007\u0000n\u0007\u0000\u0002\u0001\u0000-com/example/DecoratorManager$LoggingDecorator\u0007\u0000\u0004\u0001\u0000\u0010java/lang/Object\u0007\u0000\u0006\u0001\u0000&com/example/DecoratorManager$Decorator\u0001\u0000",
      "context_before": "",
      "context_after": "loggerName\u0001\u0000\u0012Ljava/lang/String;\u0001\u0000\u0006<init>\u0001\u0000\u0015(Ljava/lang/String;)V\u0001\u0000\u0004Code\n\u0000\u0003\u0000"
    },
    {
      "path": "target/classes/com/example/DecoratorManager$LoggingDecorator.class",
      "line": 1,
      "col": 98,
      "snippet": "\u0000\u0000\u00007\u0000n\u0007\u0000\u0002\u0001\u0000-com/example/DecoratorManager$LoggingDecorator\u0007\u0000\u0004\u0001\u0000\u0010java/lang/Object\u0007\u0000\u0006\u0001\u0000&com/example/DecoratorManager$Decorator\u0001\u0000",
      "context_before": "",
      "context_after": "loggerName\u0001\u0000\u0012Ljava/lang/String;\u0001\u0000\u0006<init>\u0001\u0000\u0015(Ljava/lang/String;)V\u0001\u0000\u0004Code\n\u0000\u0003\u0000"
    },
    {
      "path": "target/classes/com/example/DecoratorManager$LoggingDecorator.class",
      "line": 1,
      "col": 115,
      "snippet": "\u0000\u0000\u00007\u0000n\u0007\u0000\u0002\u0001\u0000-com/example/DecoratorManager$LoggingDecorator\u0007\u0000\u0004\u0001\u0000\u0010java/lang/Object\u0007\u0000\u0006\u0001\u0000&com/example/DecoratorManager$Decorator\u0001\u0000",
      "context_before": "",
      "context_after": "loggerName\u0001\u0000\u0012Ljava/lang/String;\u0001\u0000\u0006<init>\u0001\u0000\u0015(Ljava/lang/String;)V\u0001\u0000\u0004Code\n\u0000\u0003\u0000"
    },
    {
      "path": "target/classes/com/example/DecoratorManager$LoggingDecorator.class",
      "line": 6,
      "col": 67,
      "snippet": "\u0000\u0007\u0000\b\u0001\u0000\u000fLineNumberTable\u0001\u0000\u0012LocalVariableTable\u0001\u0000\u0004this\u0001\u0000/Lcom/example/DecoratorManager$LoggingDecorator;\u0001\u0000\u0016LocalVariableTypeTable\u0001\u00004Lcom/example/DecoratorManager$LoggingDecorator<TT;>;\u0001\u0000\bdecorate\u0001\u0000&(Ljava/lang/Object;)Ljava/lang/Object;\u0001\u0000\tSignature\u0001\u0000\b(TT;)TT;\u0007\u0000",
      "context_before": "\n\u0000\t\u0000\u000e\u0001\u0000\u0003()V\t\u0000\u0001\u0000\u0010",
      "context_after": "\u0001\u0000\u001bjava/util/function/Function\u0012\u0000\u0000\u0000\n"
    },
    {
      "path": "target/classes/com/example/DecoratorManager$LoggingDecorator.class",
      "line": 6,
      "col": 91,
      "snippet": "\u0000\u0007\u0000\b\u0001\u0000\u000fLineNumberTable\u0001\u0000\u0012LocalVariableTable\u0001\u0000\u0004this\u0001\u0000/Lcom/example/DecoratorManager$LoggingDecorator;\u0001\u0000\u0016LocalVariableTypeTable\u0001\u00004Lcom/example/DecoratorManager$LoggingDecorator<TT;>;\u0001\u0000\bdecorate\u0001\u0000&(Ljava/lang/Object;)Ljava/lang/Object;\u0001\u0000\tSignature\u0001\u0000\b(TT;)TT;\u0007\u0000",
      "context_before": "\n\u0000\t\u0000\u000e\u0001\u0000\u0003()V\t\u0000\u0001\u0000\u0010",
      "context_after": "\u0001\u0000\u001bjava/util/function/Function\u0012\u0000\u0000\u0000\n"
    },
    {
      "path": "target/classes/com/example/DecoratorManager$LoggingDecorator.class",
      "line": 6,
      "col": 142,
      "snippet": "\u0000\u0007\u0000\b\u0001\u0000\u000fLineNumberTable\u0001\u0000\u0012LocalVariableTable\u0001\u0000\u0004this\u0001\u0000/Lcom/example/DecoratorManager$LoggingDecorator;\u0001\u0000\u0016LocalVariableTypeTable\u0001\u00004Lcom/example/DecoratorManager$LoggingDecorator<TT;>;\u0001\u0000\bdecorate\u0001\u0000&(Ljava/lang/Object;)Ljava/lang/Object;\u0001\u0000\tSignature\u0001\u0000\b(TT;)TT;\u0007\u0000",
      "context_before": "\n\u0000\t\u0000\u000e\u0001\u0000\u0003()V\t\u0000\u0001\u0000\u0010",
      "context_after": "\u0001\u0000\u001bjava/util/function/Function\u0012\u0000\u0000\u0000\n"
    },
    {
      "path": "target/classes/com/example/DecoratorManager$LoggingDecorator.class",
      "line": 6,
      "col": 166,
      "snippet": "\u0000\u0007\u0000\b\u0001\u0000\u000fLineNumberTable\u0001\u0000\u0012LocalVariableTable\u0001\u0000\u0004this\u0001\u0000/Lcom/example/DecoratorManager$LoggingDecorator;\u0001\u0000\u0016LocalVariableTypeTable\u0001\u00004Lcom/example/DecoratorManager$LoggingDecorator<TT;>;\u0001\u0000\bdecorate\u0001\u0000&(Ljava/lang/Object;)Ljava/lang/Object;\u0001\u0000\tSignature\u0001\u0000\b(TT;)TT;\u0007\u0000",
      "context_before": "\n\u0000\t\u0000\u000e\u0001\u0000\u0003()V\t\u0000\u0001\u0000\u0010",
      "context_after": "\u0001\u0000\u001bjava/util/function/Function\u0012\u0000\u0000\u0000\n"
    },
    {
      "path": "target/classes/com/example/DecoratorManager$LoggingDecorator.class",
      "line": 9,
      "col": 30,
      "snippet": "\u0000\u001f\u0000 \u0001\u0000\u0005apply\u0001\u0000k(Lcom/example/DecoratorManager$LoggingDecorator;Ljava/util/function/Function;)Ljava/util/function/Function;\u0001\u0000\u0006target\u0001\u0000\u0012Ljava/lang/Object;\u0001\u0000\bfunction\u0001\u0000",
      "context_before": "\u0001\u0000\u001bjava/util/function/Function\u0012\u0000\u0000\u0000\n",
      "context_after": "Ljava/util/function/Function;\u0001\u0000\u0011decoratedFunction\u0001\u0000\u0006result\u0001\u0000\u0003TT;\u0001\u0000CLjava/util/function/Function<Ljava/lang/Object;Ljava/lang/Object;>;\u0001\u0000\nStackMapTable\u0001\u0000\u0007getType\u0001\u0000\u0014()Ljava/lang/String;\b\u0000-\u0001\u0000\u0007logging\u0001\u0000\blambda$0\u0001\u0000C(Ljava/util/function/Function;Ljava/lang/Object;)Ljava/lang/Object;\t\u00001\u00003\u0007\u00002\u0001\u0000\u0010java/lang/System"
    },
    {
      "path": "target/classes/com/example/DecoratorManager$LoggingDecorator.class",
      "line": 9,
      "col": 54,
      "snippet": "\u0000\u001f\u0000 \u0001\u0000\u0005apply\u0001\u0000k(Lcom/example/DecoratorManager$LoggingDecorator;Ljava/util/function/Function;)Ljava/util/function/Function;\u0001\u0000\u0006target\u0001\u0000\u0012Ljava/lang/Object;\u0001\u0000\bfunction\u0001\u0000",
      "context_before": "\u0001\u0000\u001bjava/util/function/Function\u0012\u0000\u0000\u0000\n",
      "context_after": "Ljava/util/function/Function;\u0001\u0000\u0011decoratedFunction\u0001\u0000\u0006result\u0001\u0000\u0003TT;\u0001\u0000CLjava/util/function/Function<Ljava/lang/Object;Ljava/lang/Object;>;\u0001\u0000\nStackMapTable\u0001\u0000\u0007getType\u0001\u0000\u0014()Ljava/lang/String;\b\u0000-\u0001\u0000\u0007logging\u0001\u0000\blambda$0\u0001\u0000C(Ljava/util/function/Function;Ljava/lang/Object;)Ljava/lang/Object;\t\u00001\u00003\u0007\u00002\u0001\u0000\u0010java/lang/System"
    },
    {
      "path": "target/classes/com/example/DecoratorManager$LoggingDecorator.class",
      "line": 21,
      "col": 14,
      "snippet": "SourceFile\u0001\u0000\u0015DecoratorManager.java\u0001\u0000U<T:Ljava/lang/Object;>Ljava/lang/Object;Lcom/example/DecoratorManager$Decorator<TT;>;\u0001\u0000\u0010BootstrapMethods",
      "context_before": "\u0000\u001b\u0000F\n\u0000\u001f\u0000\u0018\u0012\u0000\u0002\u0000=\u0001\u0000\u0005input\u0001\u0000",
      "context_after": "\u0000N\u0000P\u0007\u0000O\u0001\u0000\"java/lang/invoke/LambdaMetafactory\n\u0000Q\u0000R\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/DecoratorManager$LoggingDecorator.class",
      "line": 21,
      "col": 91,
      "snippet": "SourceFile\u0001\u0000\u0015DecoratorManager.java\u0001\u0000U<T:Ljava/lang/Object;>Ljava/lang/Object;Lcom/example/DecoratorManager$Decorator<TT;>;\u0001\u0000\u0010BootstrapMethods",
      "context_before": "\u0000\u001b\u0000F\n\u0000\u001f\u0000\u0018\u0012\u0000\u0002\u0000=\u0001\u0000\u0005input\u0001\u0000",
      "context_after": "\u0000N\u0000P\u0007\u0000O\u0001\u0000\"java/lang/invoke/LambdaMetafactory\n\u0000Q\u0000R\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/DecoratorManager$LoggingDecorator.class",
      "line": 21,
      "col": 108,
      "snippet": "SourceFile\u0001\u0000\u0015DecoratorManager.java\u0001\u0000U<T:Ljava/lang/Object;>Ljava/lang/Object;Lcom/example/DecoratorManager$Decorator<TT;>;\u0001\u0000\u0010BootstrapMethods",
      "context_before": "\u0000\u001b\u0000F\n\u0000\u001f\u0000\u0018\u0012\u0000\u0002\u0000=\u0001\u0000\u0005input\u0001\u0000",
      "context_after": "\u0000N\u0000P\u0007\u0000O\u0001\u0000\"java/lang/invoke/LambdaMetafactory\n\u0000Q\u0000R\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/DecoratorManager$LoggingDecorator.class",
      "line": 27,
      "col": 40,
      "snippet": "\u0000Z\u0000\\\u0007\u0000[\u0001\u0000$java/lang/invoke/StringConcatFactory",
      "context_before": "\u0000\u0001\u0000V\n\u0000.\u0000/\u000f\u0007\u0000U\u0010\u0000\u0018",
      "context_after": "\u0000>\u0000]\u0001\u0000(Ljava/lang/invoke/MethodHandles$Lookup;Ljava/lang/String;Ljava/lang/invoke/MethodType;Ljava/lang/String;[Ljava/lang/Object;)Ljava/lang/invoke/CallSite;\u000f\u0006\u0000Y\b\u0000`\u0001\u0000\n[\u0001] Input: \u0001\b\u0000b\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/DecoratorManager$LoggingDecorator.class",
      "line": 32,
      "col": 13,
      "snippet": "com/example/DecoratorManager\u0001\u0000\tDecorator\u0001\u0000\u0010LoggingDecorator\u0007\u0000i\u0001\u0000%java/lang/invoke/MethodHandles$Lookup\u0007\u0000k\u0001\u0000",
      "context_before": "[\u0001] Output: \u0001\u0001\u0000\nInnerClasses\u0007\u0000e\u0001\u0000",
      "context_after": "java/lang/invoke/MethodHandles\u0001\u0000\u0006Lookup\u0001\u0000\bNestHost\u0000!\u0000\u0001\u0000\u0003\u0000\u0001\u0000\u0005\u0000\u0001\u0000\u0012\u0000\u0007\u0000\b\u0000\u0000\u0000\u0004\u0000\u0001\u0000\t\u0000\n\u0000\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/DecoratorManager$LoggingDecorator.class",
      "line": 32,
      "col": 32,
      "snippet": "com/example/DecoratorManager\u0001\u0000\tDecorator\u0001\u0000\u0010LoggingDecorator\u0007\u0000i\u0001\u0000%java/lang/invoke/MethodHandles$Lookup\u0007\u0000k\u0001\u0000",
      "context_before": "[\u0001] Output: \u0001\u0001\u0000\nInnerClasses\u0007\u0000e\u0001\u0000",
      "context_after": "java/lang/invoke/MethodHandles\u0001\u0000\u0006Lookup\u0001\u0000\bNestHost\u0000!\u0000\u0001\u0000\u0003\u0000\u0001\u0000\u0005\u0000\u0001\u0000\u0012\u0000\u0007\u0000\b\u0000\u0000\u0000\u0004\u0000\u0001\u0000\t\u0000\n\u0000\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/DecoratorManager$LoggingDecorator.class",
      "line": 32,
      "col": 51,
      "snippet": "com/example/DecoratorManager\u0001\u0000\tDecorator\u0001\u0000\u0010LoggingDecorator\u0007\u0000i\u0001\u0000%java/lang/invoke/MethodHandles$Lookup\u0007\u0000k\u0001\u0000",
      "context_before": "[\u0001] Output: \u0001\u0001\u0000\nInnerClasses\u0007\u0000e\u0001\u0000",
      "context_after": "java/lang/invoke/MethodHandles\u0001\u0000\u0006Lookup\u0001\u0000\bNestHost\u0000!\u0000\u0001\u0000\u0003\u0000\u0001\u0000\u0005\u0000\u0001\u0000\u0012\u0000\u0007\u0000\b\u0000\u0000\u0000\u0004\u0000\u0001\u0000\t\u0000\n\u0000\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/StrategyManager$PaymentStrategyFactory.class",
      "line": 1,
      "col": 24,
      "snippet": "\u0000\u0000\u00007\u0000\u0007\u0000\u0002\u0001\u00002com/example/StrategyManager$PaymentStrategyFactory\u0007\u0000\u0004\u0001\u0000\u0010java/lang/Object\u0007\u0000\u0006\u0001\u0000+com/example/StrategyManager$StrategyFactory\u0001\u0000\u0006<init>\u0001\u0000\u0003()V\u0001\u0000\u0004Code",
      "context_before": "",
      "context_after": "\u0000\u0003\u0000\n"
    },
    {
      "path": "target/classes/com/example/StrategyManager$PaymentStrategyFactory.class",
      "line": 1,
      "col": 47,
      "snippet": "\u0000\u0000\u00007\u0000\u0007\u0000\u0002\u0001\u00002com/example/StrategyManager$PaymentStrategyFactory\u0007\u0000\u0004\u0001\u0000\u0010java/lang/Object\u0007\u0000\u0006\u0001\u0000+com/example/StrategyManager$StrategyFactory\u0001\u0000\u0006<init>\u0001\u0000\u0003()V\u0001\u0000\u0004Code",
      "context_before": "",
      "context_after": "\u0000\u0003\u0000\n"
    },
    {
      "path": "target/classes/com/example/StrategyManager$PaymentStrategyFactory.class",
      "line": 1,
      "col": 55,
      "snippet": "\u0000\u0000\u00007\u0000\u0007\u0000\u0002\u0001\u00002com/example/StrategyManager$PaymentStrategyFactory\u0007\u0000\u0004\u0001\u0000\u0010java/lang/Object\u0007\u0000\u0006\u0001\u0000+com/example/StrategyManager$StrategyFactory\u0001\u0000\u0006<init>\u0001\u0000\u0003()V\u0001\u0000\u0004Code",
      "context_before": "",
      "context_after": "\u0000\u0003\u0000\n"
    },
    {
      "path": "target/classes/com/example/StrategyManager$PaymentStrategyFactory.class",
      "line": 1,
      "col": 102,
      "snippet": "\u0000\u0000\u00007\u0000\u0007\u0000\u0002\u0001\u00002com/example/StrategyManager$PaymentStrategyFactory\u0007\u0000\u0004\u0001\u0000\u0010java/lang/Object\u0007\u0000\u0006\u0001\u0000+com/example/StrategyManager$StrategyFactory\u0001\u0000\u0006<init>\u0001\u0000\u0003()V\u0001\u0000\u0004Code",
      "context_before": "",
      "context_after": "\u0000\u0003\u0000\n"
    },
    {
      "path": "target/classes/com/example/StrategyManager$PaymentStrategyFactory.class",
      "line": 1,
      "col": 118,
      "snippet": "\u0000\u0000\u00007\u0000\u0007\u0000\u0002\u0001\u00002com/example/StrategyManager$PaymentStrategyFactory\u0007\u0000\u0004\u0001\u0000\u0010java/lang/Object\u0007\u0000\u0006\u0001\u0000+com/example/StrategyManager$StrategyFactory\u0001\u0000\u0006<init>\u0001\u0000\u0003()V\u0001\u0000\u0004Code",
      "context_before": "",
      "context_after": "\u0000\u0003\u0000\n"
    },
    {
      "path": "target/classes/com/example/StrategyManager$PaymentStrategyFactory.class",
      "line": 1,
      "col": 126,
      "snippet": "\u0000\u0000\u00007\u0000\u0007\u0000\u0002\u0001\u00002com/example/StrategyManager$PaymentStrategyFactory\u0007\u0000\u0004\u0001\u0000\u0010java/lang/Object\u0007\u0000\u0006\u0001\u0000+com/example/StrategyManager$StrategyFactory\u0001\u0000\u0006<init>\u0001\u0000\u0003()V\u0001\u0000\u0004Code",
      "context_before": "",
      "context_after": "\u0000\u0003\u0000\n"
    },
    {
      "path": "target/classes/com/example/StrategyManager$PaymentStrategyFactory.class",
      "line": 4,
      "col": 67,
      "snippet": "\u0000\u0007\u0000\b\u0001\u0000\u000fLineNumberTable\u0001\u0000\u0012LocalVariableTable\u0001\u0000\u0004this\u0001\u00004Lcom/example/StrategyManager$PaymentStrategyFactory;\u0001\u0000\u0006create\u0001\u00009(Ljava/lang/String;[Ljava/lang/Object;)Ljava/lang/Object;",
      "context_before": "\u0000\u0003\u0000\n",
      "context_after": "\u0000\u0013\u0000\u0015\u0007\u0000\u0014\u0001\u0000\u0010java/lang/String\n\u0000\u0016\u0000\u0017\u0001\u0000\bhashCode\u0001\u0000\u0003()I\b\u0000\u0019\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/StrategyManager$PaymentStrategyFactory.class",
      "line": 4,
      "col": 90,
      "snippet": "\u0000\u0007\u0000\b\u0001\u0000\u000fLineNumberTable\u0001\u0000\u0012LocalVariableTable\u0001\u0000\u0004this\u0001\u00004Lcom/example/StrategyManager$PaymentStrategyFactory;\u0001\u0000\u0006create\u0001\u00009(Ljava/lang/String;[Ljava/lang/Object;)Ljava/lang/Object;",
      "context_before": "\u0000\u0003\u0000\n",
      "context_after": "\u0000\u0013\u0000\u0015\u0007\u0000\u0014\u0001\u0000\u0010java/lang/String\n\u0000\u0016\u0000\u0017\u0001\u0000\bhashCode\u0001\u0000\u0003()I\b\u0000\u0019\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/StrategyManager$PaymentStrategyFactory.class",
      "line": 4,
      "col": 98,
      "snippet": "\u0000\u0007\u0000\b\u0001\u0000\u000fLineNumberTable\u0001\u0000\u0012LocalVariableTable\u0001\u0000\u0004this\u0001\u00004Lcom/example/StrategyManager$PaymentStrategyFactory;\u0001\u0000\u0006create\u0001\u00009(Ljava/lang/String;[Ljava/lang/Object;)Ljava/lang/Object;",
      "context_before": "\u0000\u0003\u0000\n",
      "context_after": "\u0000\u0013\u0000\u0015\u0007\u0000\u0014\u0001\u0000\u0010java/lang/String\n\u0000\u0016\u0000\u0017\u0001\u0000\bhashCode\u0001\u0000\u0003()I\b\u0000\u0019\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/StrategyManager$PaymentStrategyFactory.class",
      "line": 13,
      "col": 33,
      "snippet": "\u0000$\u0000%\u0001\u0000\u0007execute\u0001\u0000(()Lcom/example/StrategyManager$Strategy;\u0012\u0000\u0001\u0000#\u0012\u0000\u0002\u0000#\u0007\u0000)\u0001\u0000\"java/lang/IllegalArgumentException\u0012\u0000\u0003\u0000+",
      "context_before": "\u0001\u0000\u0006equals\u0001\u0000\u0015(Ljava/lang/Object;)Z\b\u0000\u001f\u0001\u0000\u0006paypal\b\u0000!\u0001\u0000\ncredit_card\u0012\u0000\u0000\u0000#",
      "context_after": "\u0000,\u0000-\u0001\u0000\u0017makeConcatWithConstants\u0001\u0000&(Ljava/lang/String;)Ljava/lang/String;\n\u0000(\u0000/"
    },
    {
      "path": "target/classes/com/example/StrategyManager$PaymentStrategyFactory.class",
      "line": 13,
      "col": 49,
      "snippet": "\u0000$\u0000%\u0001\u0000\u0007execute\u0001\u0000(()Lcom/example/StrategyManager$Strategy;\u0012\u0000\u0001\u0000#\u0012\u0000\u0002\u0000#\u0007\u0000)\u0001\u0000\"java/lang/IllegalArgumentException\u0012\u0000\u0003\u0000+",
      "context_before": "\u0001\u0000\u0006equals\u0001\u0000\u0015(Ljava/lang/Object;)Z\b\u0000\u001f\u0001\u0000\u0006paypal\b\u0000!\u0001\u0000\ncredit_card\u0012\u0000\u0000\u0000#",
      "context_after": "\u0000,\u0000-\u0001\u0000\u0017makeConcatWithConstants\u0001\u0000&(Ljava/lang/String;)Ljava/lang/String;\n\u0000(\u0000/"
    },
    {
      "path": "target/classes/com/example/StrategyManager$PaymentStrategyFactory.class",
      "line": 18,
      "col": 42,
      "snippet": "StackMapTable\u0001\u0000\blambda$0\u0001\u0000V(Lcom/example/StrategyManager$PaymentData;)Lcom/example/StrategyManager$PaymentResult;\t\u00009\u0000;\u0007\u0000:\u0001\u0000'com/example/StrategyManager$PaymentData",
      "context_before": "\u0000\u0007\u00000\u0001\u0000\u0015(Ljava/lang/String;)V\u0001\u0000\nstrategyName\u0001\u0000\u0012Ljava/lang/String;\u0001\u0000\u0006params\u0001\u0000\u0013[Ljava/lang/Object;\u0001\u0000",
      "context_after": "\u0000<\u0000=\u0001\u0000\u0006amount\u0001\u0000\u0016Ljava/math/BigDecimal;\u0007\u0000?\u0001\u0000\u0014java/math/BigDecimal\b\u0000A\u0001\u0000\u000510000\n\u0000>\u0000/"
    },
    {
      "path": "target/classes/com/example/StrategyManager$PaymentStrategyFactory.class",
      "line": 18,
      "col": 84,
      "snippet": "StackMapTable\u0001\u0000\blambda$0\u0001\u0000V(Lcom/example/StrategyManager$PaymentData;)Lcom/example/StrategyManager$PaymentResult;\t\u00009\u0000;\u0007\u0000:\u0001\u0000'com/example/StrategyManager$PaymentData",
      "context_before": "\u0000\u0007\u00000\u0001\u0000\u0015(Ljava/lang/String;)V\u0001\u0000\nstrategyName\u0001\u0000\u0012Ljava/lang/String;\u0001\u0000\u0006params\u0001\u0000\u0013[Ljava/lang/Object;\u0001\u0000",
      "context_after": "\u0000<\u0000=\u0001\u0000\u0006amount\u0001\u0000\u0016Ljava/math/BigDecimal;\u0007\u0000?\u0001\u0000\u0014java/math/BigDecimal\b\u0000A\u0001\u0000\u000510000\n\u0000>\u0000/"
    },
    {
      "path": "target/classes/com/example/StrategyManager$PaymentStrategyFactory.class",
      "line": 18,
      "col": 137,
      "snippet": "StackMapTable\u0001\u0000\blambda$0\u0001\u0000V(Lcom/example/StrategyManager$PaymentData;)Lcom/example/StrategyManager$PaymentResult;\t\u00009\u0000;\u0007\u0000:\u0001\u0000'com/example/StrategyManager$PaymentData",
      "context_before": "\u0000\u0007\u00000\u0001\u0000\u0015(Ljava/lang/String;)V\u0001\u0000\nstrategyName\u0001\u0000\u0012Ljava/lang/String;\u0001\u0000\u0006params\u0001\u0000\u0013[Ljava/lang/Object;\u0001\u0000",
      "context_after": "\u0000<\u0000=\u0001\u0000\u0006amount\u0001\u0000\u0016Ljava/math/BigDecimal;\u0007\u0000?\u0001\u0000\u0014java/math/BigDecimal\b\u0000A\u0001\u0000\u000510000\n\u0000>\u0000/"
    },
    {
      "path": "target/classes/com/example/StrategyManager$PaymentStrategyFactory.class",
      "line": 22,
      "col": 63,
      "snippet": "\u0000E\u0000F\u0001\u0000\tcompareTo\u0001\u0000\u0019(Ljava/math/BigDecimal;)I\u0007\u0000H\u0001\u0000)com/example/StrategyManager$PaymentResult\b\u0000J\u0001\u0000\u0010Payment approved\b\u0000L\u0001\u0000\u0010Payment declined",
      "context_before": "\u0000>\u0000/\n\u0000>\u0000D",
      "context_after": "\u0000G\u0000N\n\u0000\u0007\u0000O\u0001\u0000\u0016(ZLjava/lang/String;)V\u0001\u0000\u0004data\u0001\u0000)Lcom/example/StrategyManager$PaymentData;\u0001\u0000\u0007success\u0001\u0000\u0001Z\u0001\u0000\blambda$1\b\u0000V\u0001\u0000\u00045000\b\u0000X\u0001\u0000\u0019PayPal payment successful\b\u0000Z\u0001\u0000\u0015PayPal payment failed\u0001\u0000\blambda$2\b\u0000]\u0001\u0000\u0017Bank transfer initiated\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/StrategyManager$PaymentStrategyFactory.class",
      "line": 24,
      "col": 53,
      "snippet": "\u0000\u0007\u0000O\u0001\u0000\u0016(ZLjava/lang/String;)V\u0001\u0000\u0004data\u0001\u0000)Lcom/example/StrategyManager$PaymentData;\u0001\u0000\u0007success\u0001\u0000\u0001Z\u0001\u0000\blambda$1\b\u0000V\u0001\u0000\u00045000\b\u0000X\u0001\u0000\u0019PayPal payment successful\b\u0000Z\u0001\u0000\u0015PayPal payment failed\u0001\u0000\blambda$2\b\u0000]\u0001\u0000\u0017Bank transfer initiated\u0001\u0000",
      "context_before": "\u0000E\u0000F\u0001\u0000\tcompareTo\u0001\u0000\u0019(Ljava/math/BigDecimal;)I\u0007\u0000H\u0001\u0000)com/example/StrategyManager$PaymentResult\b\u0000J\u0001\u0000\u0010Payment approved\b\u0000L\u0001\u0000\u0010Payment declined\n\u0000G\u0000N",
      "context_after": "SourceFile\u0001\u0000\u0014StrategyManager.java\u0001\u0000\u0010BootstrapMethods\n\u0000b\u0000d\u0007\u0000c\u0001\u0000\"java/lang/invoke/LambdaMetafactory"
    },
    {
      "path": "target/classes/com/example/StrategyManager$PaymentStrategyFactory.class",
      "line": 25,
      "col": 14,
      "snippet": "SourceFile\u0001\u0000\u0014StrategyManager.java\u0001\u0000\u0010BootstrapMethods",
      "context_before": "\u0000G\u0000N\n\u0000\u0007\u0000O\u0001\u0000\u0016(ZLjava/lang/String;)V\u0001\u0000\u0004data\u0001\u0000)Lcom/example/StrategyManager$PaymentData;\u0001\u0000\u0007success\u0001\u0000\u0001Z\u0001\u0000\blambda$1\b\u0000V\u0001\u0000\u00045000\b\u0000X\u0001\u0000\u0019PayPal payment successful\b\u0000Z\u0001\u0000\u0015PayPal payment failed\u0001\u0000\blambda$2\b\u0000]\u0001\u0000\u0017Bank transfer initiated\u0001\u0000",
      "context_after": "\u0000b\u0000d\u0007\u0000c\u0001\u0000\"java/lang/invoke/LambdaMetafactory\n\u0000e\u0000f\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/StrategyManager$PaymentStrategyFactory.class",
      "line": 35,
      "col": 40,
      "snippet": "\u0000y\u0000{\u0007\u0000z\u0001\u0000$java/lang/invoke/StringConcatFactory",
      "context_before": "\u0000\u0001\u0000u\n\u0000[\u00007\u000f\u0006\u0000t\u0010\u00007",
      "context_after": "\u0000,\u0000|\u0001\u0000(Ljava/lang/invoke/MethodHandles$Lookup;Ljava/lang/String;Ljava/lang/invoke/MethodType;Ljava/lang/String;[Ljava/lang/Object;)Ljava/lang/invoke/CallSite;\u000f\u0006\u0000x\b\u0000\u0001\u0000\u001bUnknown payment strategy: \u0001\u0001\u0000\nInnerClasses\u0007\u0000\u0001\u0000\u001bcom/example/StrategyManager\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/StrategyManager$PaymentStrategyFactory.class",
      "line": 37,
      "col": 30,
      "snippet": "InnerClasses\u0007\u0000\u0001\u0000\u001bcom/example/StrategyManager\u0001\u0000",
      "context_before": "\u0000y\u0000{\u0007\u0000z\u0001\u0000$java/lang/invoke/StringConcatFactory\n\u0000,\u0000|\u0001\u0000(Ljava/lang/invoke/MethodHandles$Lookup;Ljava/lang/String;Ljava/lang/invoke/MethodType;Ljava/lang/String;[Ljava/lang/Object;)Ljava/lang/invoke/CallSite;\u000f\u0006\u0000x\b\u0000\u0001\u0000\u001bUnknown payment strategy: \u0001\u0001\u0000",
      "context_after": "PaymentData\u0001\u0000\nPaymentResult\u0001\u0000\u0016PaymentStrategyFactory\u0001\u0000\u000fStrategyFactory\u0007\u0000\u0001\u0000%java/lang/invoke/MethodHandles$Lookup\u0007\u0000\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/StrategyManager$PaymentStrategyFactory.class",
      "line": 39,
      "col": 24,
      "snippet": "PaymentResult\u0001\u0000\u0016PaymentStrategyFactory\u0001\u0000\u000fStrategyFactory\u0007\u0000\u0001\u0000%java/lang/invoke/MethodHandles$Lookup\u0007\u0000\u0001\u0000",
      "context_before": "InnerClasses\u0007\u0000\u0001\u0000\u001bcom/example/StrategyManager\u0001\u0000\nPaymentData\u0001\u0000",
      "context_after": "java/lang/invoke/MethodHandles\u0001\u0000\u0006Lookup\u0001\u0000\bNestHost\u0000!\u0000\u0001\u0000\u0003\u0000\u0001\u0000\u0005\u0000\u0000\u0000\u0005\u0000\u0001\u0000\u0007\u0000\b\u0000\u0001\u0000\t\u0000\u0000\u0000/\u0000\u0001\u0000\u0001\u0000\u0000\u0000\u0005*\u0000\n\u0000\u0000\u0000\u0002\u0000"
    },
    {
      "path": "target/classes/com/example/StrategyManager$PaymentStrategyFactory.class",
      "line": 39,
      "col": 32,
      "snippet": "PaymentResult\u0001\u0000\u0016PaymentStrategyFactory\u0001\u0000\u000fStrategyFactory\u0007\u0000\u0001\u0000%java/lang/invoke/MethodHandles$Lookup\u0007\u0000\u0001\u0000",
      "context_before": "InnerClasses\u0007\u0000\u0001\u0000\u001bcom/example/StrategyManager\u0001\u0000\nPaymentData\u0001\u0000",
      "context_after": "java/lang/invoke/MethodHandles\u0001\u0000\u0006Lookup\u0001\u0000\bNestHost\u0000!\u0000\u0001\u0000\u0003\u0000\u0001\u0000\u0005\u0000\u0000\u0000\u0005\u0000\u0001\u0000\u0007\u0000\b\u0000\u0001\u0000\t\u0000\u0000\u0000/\u0000\u0001\u0000\u0001\u0000\u0000\u0000\u0005*\u0000\n\u0000\u0000\u0000\u0002\u0000"
    },
    {
      "path": "target/classes/com/example/StrategyManager$PaymentStrategyFactory.class",
      "line": 39,
      "col": 42,
      "snippet": "PaymentResult\u0001\u0000\u0016PaymentStrategyFactory\u0001\u0000\u000fStrategyFactory\u0007\u0000\u0001\u0000%java/lang/invoke/MethodHandles$Lookup\u0007\u0000\u0001\u0000",
      "context_before": "InnerClasses\u0007\u0000\u0001\u0000\u001bcom/example/StrategyManager\u0001\u0000\nPaymentData\u0001\u0000",
      "context_after": "java/lang/invoke/MethodHandles\u0001\u0000\u0006Lookup\u0001\u0000\bNestHost\u0000!\u0000\u0001\u0000\u0003\u0000\u0001\u0000\u0005\u0000\u0000\u0000\u0005\u0000\u0001\u0000\u0007\u0000\b\u0000\u0001\u0000\t\u0000\u0000\u0000/\u0000\u0001\u0000\u0001\u0000\u0000\u0000\u0005*\u0000\n\u0000\u0000\u0000\u0002\u0000"
    },
    {
      "path": "target/classes/com/example/StrategyManager$PaymentStrategyFactory.class",
      "line": 39,
      "col": 50,
      "snippet": "PaymentResult\u0001\u0000\u0016PaymentStrategyFactory\u0001\u0000\u000fStrategyFactory\u0007\u0000\u0001\u0000%java/lang/invoke/MethodHandles$Lookup\u0007\u0000\u0001\u0000",
      "context_before": "InnerClasses\u0007\u0000\u0001\u0000\u001bcom/example/StrategyManager\u0001\u0000\nPaymentData\u0001\u0000",
      "context_after": "java/lang/invoke/MethodHandles\u0001\u0000\u0006Lookup\u0001\u0000\bNestHost\u0000!\u0000\u0001\u0000\u0003\u0000\u0001\u0000\u0005\u0000\u0000\u0000\u0005\u0000\u0001\u0000\u0007\u0000\b\u0000\u0001\u0000\t\u0000\u0000\u0000/\u0000\u0001\u0000\u0001\u0000\u0000\u0000\u0005*\u0000\n\u0000\u0000\u0000\u0002\u0000"
    },
    {
      "path": "target/classes/com/example/AdapterManager$DatabaseAdapter.class",
      "line": 1,
      "col": 25,
      "snippet": "\u0000\u0000\u00007\u0000L\u0007\u0000\u0002\u0001\u0000*com/example/AdapterManager$DatabaseAdapter\u0007\u0000\u0004\u0001\u0000\u0010java/lang/Object\u0007\u0000\u0006\u0001\u0000\"com/example/AdapterManager$Adapter\u0001\u0000\u0006dbType\u0001\u0000\u0012Ljava/lang/String;\u0001\u0000\u0006<init>\u0001\u0000\u0015(Ljava/lang/String;)V\u0001\u0000\u0004Code",
      "context_before": "",
      "context_after": "\u0000\u0003\u0000\n"
    },
    {
      "path": "target/classes/com/example/AdapterManager$DatabaseAdapter.class",
      "line": 1,
      "col": 48,
      "snippet": "\u0000\u0000\u00007\u0000L\u0007\u0000\u0002\u0001\u0000*com/example/AdapterManager$DatabaseAdapter\u0007\u0000\u0004\u0001\u0000\u0010java/lang/Object\u0007\u0000\u0006\u0001\u0000\"com/example/AdapterManager$Adapter\u0001\u0000\u0006dbType\u0001\u0000\u0012Ljava/lang/String;\u0001\u0000\u0006<init>\u0001\u0000\u0015(Ljava/lang/String;)V\u0001\u0000\u0004Code",
      "context_before": "",
      "context_after": "\u0000\u0003\u0000\n"
    },
    {
      "path": "target/classes/com/example/AdapterManager$DatabaseAdapter.class",
      "line": 1,
      "col": 95,
      "snippet": "\u0000\u0000\u00007\u0000L\u0007\u0000\u0002\u0001\u0000*com/example/AdapterManager$DatabaseAdapter\u0007\u0000\u0004\u0001\u0000\u0010java/lang/Object\u0007\u0000\u0006\u0001\u0000\"com/example/AdapterManager$Adapter\u0001\u0000\u0006dbType\u0001\u0000\u0012Ljava/lang/String;\u0001\u0000\u0006<init>\u0001\u0000\u0015(Ljava/lang/String;)V\u0001\u0000\u0004Code",
      "context_before": "",
      "context_after": "\u0000\u0003\u0000\n"
    },
    {
      "path": "target/classes/com/example/AdapterManager$DatabaseAdapter.class",
      "line": 1,
      "col": 110,
      "snippet": "\u0000\u0000\u00007\u0000L\u0007\u0000\u0002\u0001\u0000*com/example/AdapterManager$DatabaseAdapter\u0007\u0000\u0004\u0001\u0000\u0010java/lang/Object\u0007\u0000\u0006\u0001\u0000\"com/example/AdapterManager$Adapter\u0001\u0000\u0006dbType\u0001\u0000\u0012Ljava/lang/String;\u0001\u0000\u0006<init>\u0001\u0000\u0015(Ljava/lang/String;)V\u0001\u0000\u0004Code",
      "context_before": "",
      "context_after": "\u0000\u0003\u0000\n"
    },
    {
      "path": "target/classes/com/example/AdapterManager$DatabaseAdapter.class",
      "line": 5,
      "col": 67,
      "snippet": "\u0000\u0007\u0000\b\u0001\u0000\u000fLineNumberTable\u0001\u0000\u0012LocalVariableTable\u0001\u0000\u0004this\u0001\u0000,Lcom/example/AdapterManager$DatabaseAdapter;\u0001\u0000\u0005adapt\u0001\u0000%(Ljava/util/Map;)Ljava/sql/ResultSet;\u0001\u0000\tSignature\u0001\u0000K(Ljava/util/Map<Ljava/lang/String;Ljava/lang/Object;>;)Ljava/sql/ResultSet;\t\u0000\u001a\u0000",
      "context_before": "\n\u0000\t\u0000\u000e\u0001\u0000\u0003()V\t\u0000\u0001\u0000\u0010",
      "context_after": "\u0007\u0000\u001b\u0001\u0000\u0010java/lang/System\n\u0000"
    },
    {
      "path": "target/classes/com/example/AdapterManager$DatabaseAdapter.class",
      "line": 5,
      "col": 90,
      "snippet": "\u0000\u0007\u0000\b\u0001\u0000\u000fLineNumberTable\u0001\u0000\u0012LocalVariableTable\u0001\u0000\u0004this\u0001\u0000,Lcom/example/AdapterManager$DatabaseAdapter;\u0001\u0000\u0005adapt\u0001\u0000%(Ljava/util/Map;)Ljava/sql/ResultSet;\u0001\u0000\tSignature\u0001\u0000K(Ljava/util/Map<Ljava/lang/String;Ljava/lang/Object;>;)Ljava/sql/ResultSet;\t\u0000\u001a\u0000",
      "context_before": "\n\u0000\t\u0000\u000e\u0001\u0000\u0003()V\t\u0000\u0001\u0000\u0010",
      "context_after": "\u0007\u0000\u001b\u0001\u0000\u0010java/lang/System\n\u0000"
    },
    {
      "path": "target/classes/com/example/AdapterManager$DatabaseAdapter.class",
      "line": 18,
      "col": 14,
      "snippet": "SourceFile\u0001\u0000\u0013AdapterManager.java\u0001\u0000Ljava/lang/Object;Lcom/example/AdapterManager$Adapter<Ljava/util/Map<Ljava/lang/String;Ljava/lang/Object;>;Ljava/sql/ResultSet;>;\u0001\u0000\u0010BootstrapMethods",
      "context_before": "\u0000\u0001\u00004\n\u0000\u0015\u0000\u0016\u0001\u0000",
      "context_after": "\u0000:\u0000<\u0007\u0000;\u0001\u0000$java/lang/invoke/StringConcatFactory\n\u0000!\u0000=\u0001\u0000(Ljava/lang/invoke/MethodHandles$Lookup;Ljava/lang/String;Ljava/lang/invoke/MethodType;Ljava/lang/String;[Ljava/lang/Object;)Ljava/lang/invoke/CallSite;\u000f\u0006\u00009\b\u0000@\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/AdapterManager$DatabaseAdapter.class",
      "line": 18,
      "col": 66,
      "snippet": "SourceFile\u0001\u0000\u0013AdapterManager.java\u0001\u0000Ljava/lang/Object;Lcom/example/AdapterManager$Adapter<Ljava/util/Map<Ljava/lang/String;Ljava/lang/Object;>;Ljava/sql/ResultSet;>;\u0001\u0000\u0010BootstrapMethods",
      "context_before": "\u0000\u0001\u00004\n\u0000\u0015\u0000\u0016\u0001\u0000",
      "context_after": "\u0000:\u0000<\u0007\u0000;\u0001\u0000$java/lang/invoke/StringConcatFactory\n\u0000!\u0000=\u0001\u0000(Ljava/lang/invoke/MethodHandles$Lookup;Ljava/lang/String;Ljava/lang/invoke/MethodType;Ljava/lang/String;[Ljava/lang/Object;)Ljava/lang/invoke/CallSite;\u000f\u0006\u00009\b\u0000@\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/AdapterManager$DatabaseAdapter.class",
      "line": 18,
      "col": 81,
      "snippet": "SourceFile\u0001\u0000\u0013AdapterManager.java\u0001\u0000Ljava/lang/Object;Lcom/example/AdapterManager$Adapter<Ljava/util/Map<Ljava/lang/String;Ljava/lang/Object;>;Ljava/sql/ResultSet;>;\u0001\u0000\u0010BootstrapMethods",
      "context_before": "\u0000\u0001\u00004\n\u0000\u0015\u0000\u0016\u0001\u0000",
      "context_after": "\u0000:\u0000<\u0007\u0000;\u0001\u0000$java/lang/invoke/StringConcatFactory\n\u0000!\u0000=\u0001\u0000(Ljava/lang/invoke/MethodHandles$Lookup;Ljava/lang/String;Ljava/lang/invoke/MethodType;Ljava/lang/String;[Ljava/lang/Object;)Ljava/lang/invoke/CallSite;\u000f\u0006\u00009\b\u0000@\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/AdapterManager$DatabaseAdapter.class",
      "line": 19,
      "col": 40,
      "snippet": "\u0000:\u0000<\u0007\u0000;\u0001\u0000$java/lang/invoke/StringConcatFactory",
      "context_before": "\u0000\u0015\u0000\u0016\u0001\u0000\nSourceFile\u0001\u0000\u0013AdapterManager.java\u0001\u0000Ljava/lang/Object;Lcom/example/AdapterManager$Adapter<Ljava/util/Map<Ljava/lang/String;Ljava/lang/Object;>;Ljava/sql/ResultSet;>;\u0001\u0000\u0010BootstrapMethods",
      "context_after": "\u0000!\u0000=\u0001\u0000(Ljava/lang/invoke/MethodHandles$Lookup;Ljava/lang/String;Ljava/lang/invoke/MethodType;Ljava/lang/String;[Ljava/lang/Object;)Ljava/lang/invoke/CallSite;\u000f\u0006\u00009\b\u0000@\u0001\u0000\nAdapting query for \u0001 database\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/AdapterManager$DatabaseAdapter.class",
      "line": 22,
      "col": 31,
      "snippet": "InnerClasses\u0007\u0000C\u0001\u0000\u001acom/example/AdapterManager\u0001\u0000\u0007Adapter\u0001\u0000\u000fDatabaseAdapter\u0007\u0000G\u0001\u0000%java/lang/invoke/MethodHandles$Lookup\u0007\u0000I\u0001\u0000",
      "context_before": "\u0000!\u0000=\u0001\u0000(Ljava/lang/invoke/MethodHandles$Lookup;Ljava/lang/String;Ljava/lang/invoke/MethodType;Ljava/lang/String;[Ljava/lang/Object;)Ljava/lang/invoke/CallSite;\u000f\u0006\u00009\b\u0000@\u0001\u0000\nAdapting query for \u0001 database\u0001\u0000",
      "context_after": "java/lang/invoke/MethodHandles\u0001\u0000\u0006Lookup\u0001\u0000\bNestHost\u0000!\u0000\u0001\u0000\u0003\u0000\u0001\u0000\u0005\u0000\u0001\u0000\u0012\u0000\u0007\u0000\b\u0000\u0000\u0000\u0004\u0000\u0001\u0000\t\u0000\n\u0000\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/AdapterManager$DatabaseAdapter.class",
      "line": 22,
      "col": 48,
      "snippet": "InnerClasses\u0007\u0000C\u0001\u0000\u001acom/example/AdapterManager\u0001\u0000\u0007Adapter\u0001\u0000\u000fDatabaseAdapter\u0007\u0000G\u0001\u0000%java/lang/invoke/MethodHandles$Lookup\u0007\u0000I\u0001\u0000",
      "context_before": "\u0000!\u0000=\u0001\u0000(Ljava/lang/invoke/MethodHandles$Lookup;Ljava/lang/String;Ljava/lang/invoke/MethodType;Ljava/lang/String;[Ljava/lang/Object;)Ljava/lang/invoke/CallSite;\u000f\u0006\u00009\b\u0000@\u0001\u0000\nAdapting query for \u0001 database\u0001\u0000",
      "context_after": "java/lang/invoke/MethodHandles\u0001\u0000\u0006Lookup\u0001\u0000\bNestHost\u0000!\u0000\u0001\u0000\u0003\u0000\u0001\u0000\u0005\u0000\u0001\u0000\u0012\u0000\u0007\u0000\b\u0000\u0000\u0000\u0004\u0000\u0001\u0000\t\u0000\n\u0000\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/AdapterManager$DatabaseAdapter.class",
      "line": 22,
      "col": 66,
      "snippet": "InnerClasses\u0007\u0000C\u0001\u0000\u001acom/example/AdapterManager\u0001\u0000\u0007Adapter\u0001\u0000\u000fDatabaseAdapter\u0007\u0000G\u0001\u0000%java/lang/invoke/MethodHandles$Lookup\u0007\u0000I\u0001\u0000",
      "context_before": "\u0000!\u0000=\u0001\u0000(Ljava/lang/invoke/MethodHandles$Lookup;Ljava/lang/String;Ljava/lang/invoke/MethodType;Ljava/lang/String;[Ljava/lang/Object;)Ljava/lang/invoke/CallSite;\u000f\u0006\u00009\b\u0000@\u0001\u0000\nAdapting query for \u0001 database\u0001\u0000",
      "context_after": "java/lang/invoke/MethodHandles\u0001\u0000\u0006Lookup\u0001\u0000\bNestHost\u0000!\u0000\u0001\u0000\u0003\u0000\u0001\u0000\u0005\u0000\u0001\u0000\u0012\u0000\u0007\u0000\b\u0000\u0000\u0000\u0004\u0000\u0001\u0000\t\u0000\n\u0000\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/FactoryManager$DataProcessorFactory.class",
      "line": 1,
      "col": 25,
      "snippet": "\u0000\u0000\u00007\u0000$\u0007\u0000\u0002\u0001\u0000/com/example/FactoryManager$DataProcessorFactory\u0007\u0000\u0004\u0001\u0000\u0010java/lang/Object\u0007\u0000\u0006\u0001\u0000(com/example/FactoryManager$ObjectFactory\u0001\u0000\u0006<init>\u0001\u0000\u0003()V\u0001\u0000\u0004Code",
      "context_before": "",
      "context_after": "\u0000\u0003\u0000\n"
    },
    {
      "path": "target/classes/com/example/FactoryManager$DataProcessorFactory.class",
      "line": 1,
      "col": 53,
      "snippet": "\u0000\u0000\u00007\u0000$\u0007\u0000\u0002\u0001\u0000/com/example/FactoryManager$DataProcessorFactory\u0007\u0000\u0004\u0001\u0000\u0010java/lang/Object\u0007\u0000\u0006\u0001\u0000(com/example/FactoryManager$ObjectFactory\u0001\u0000\u0006<init>\u0001\u0000\u0003()V\u0001\u0000\u0004Code",
      "context_before": "",
      "context_after": "\u0000\u0003\u0000\n"
    },
    {
      "path": "target/classes/com/example/FactoryManager$DataProcessorFactory.class",
      "line": 1,
      "col": 100,
      "snippet": "\u0000\u0000\u00007\u0000$\u0007\u0000\u0002\u0001\u0000/com/example/FactoryManager$DataProcessorFactory\u0007\u0000\u0004\u0001\u0000\u0010java/lang/Object\u0007\u0000\u0006\u0001\u0000(com/example/FactoryManager$ObjectFactory\u0001\u0000\u0006<init>\u0001\u0000\u0003()V\u0001\u0000\u0004Code",
      "context_before": "",
      "context_after": "\u0000\u0003\u0000\n"
    },
    {
      "path": "target/classes/com/example/FactoryManager$DataProcessorFactory.class",
      "line": 1,
      "col": 121,
      "snippet": "\u0000\u0000\u00007\u0000$\u0007\u0000\u0002\u0001\u0000/com/example/FactoryManager$DataProcessorFactory\u0007\u0000\u0004\u0001\u0000\u0010java/lang/Object\u0007\u0000\u0006\u0001\u0000(com/example/FactoryManager$ObjectFactory\u0001\u0000\u0006<init>\u0001\u0000\u0003()V\u0001\u0000\u0004Code",
      "context_before": "",
      "context_after": "\u0000\u0003\u0000\n"
    },
    {
      "path": "target/classes/com/example/FactoryManager$DataProcessorFactory.class",
      "line": 4,
      "col": 67,
      "snippet": "\u0000\u0007\u0000\b\u0001\u0000\u000fLineNumberTable\u0001\u0000\u0012LocalVariableTable\u0001\u0000\u0004this\u0001\u00001Lcom/example/FactoryManager$DataProcessorFactory;\u0001\u0000\u0006create\u0001\u00000([Ljava/lang/Object;)Lcom/example/DataProcessor;\u0007\u0000\u0013\u0001\u0000\u0019com/example/DataProcessor",
      "context_before": "\u0000\u0003\u0000\n",
      "context_after": "\u0000\u0012\u0000\n\u0001\u0000\u0004args\u0001\u0000\u0013[Ljava/lang/Object;\u0001\u0000'([Ljava/lang/Object;)Ljava/lang/Object;"
    },
    {
      "path": "target/classes/com/example/FactoryManager$DataProcessorFactory.class",
      "line": 4,
      "col": 95,
      "snippet": "\u0000\u0007\u0000\b\u0001\u0000\u000fLineNumberTable\u0001\u0000\u0012LocalVariableTable\u0001\u0000\u0004this\u0001\u00001Lcom/example/FactoryManager$DataProcessorFactory;\u0001\u0000\u0006create\u0001\u00000([Ljava/lang/Object;)Lcom/example/DataProcessor;\u0007\u0000\u0013\u0001\u0000\u0019com/example/DataProcessor",
      "context_before": "\u0000\u0003\u0000\n",
      "context_after": "\u0000\u0012\u0000\n\u0001\u0000\u0004args\u0001\u0000\u0013[Ljava/lang/Object;\u0001\u0000'([Ljava/lang/Object;)Ljava/lang/Object;"
    },
    {
      "path": "target/classes/com/example/FactoryManager$DataProcessorFactory.class",
      "line": 9,
      "col": 14,
      "snippet": "SourceFile\u0001\u0000\u0013FactoryManager.java\u0001\u0000\tSignature\u0001\u0000YLjava/lang/Object;Lcom/example/FactoryManager$ObjectFactory<Lcom/example/DataProcessor;>;\u0001\u0000",
      "context_before": "\u0000\u0001\u0000\u0019\n\u0000\u0010\u0000\u0011\u0001\u0000",
      "context_after": "InnerClasses\u0007\u0000 \u0001\u0000\u001acom/example/FactoryManager\u0001\u0000\u0014DataProcessorFactory\u0001\u0000\nObjectFactory\u0001\u0000\bNestHost\u0000!\u0000\u0001\u0000\u0003\u0000\u0001\u0000\u0005\u0000\u0000\u0000\u0003\u0000\u0001\u0000\u0007\u0000\b\u0000\u0001\u0000\t\u0000\u0000\u0000/\u0000\u0001\u0000\u0001\u0000\u0000\u0000\u0005*\u0000"
    },
    {
      "path": "target/classes/com/example/FactoryManager$DataProcessorFactory.class",
      "line": 9,
      "col": 79,
      "snippet": "SourceFile\u0001\u0000\u0013FactoryManager.java\u0001\u0000\tSignature\u0001\u0000YLjava/lang/Object;Lcom/example/FactoryManager$ObjectFactory<Lcom/example/DataProcessor;>;\u0001\u0000",
      "context_before": "\u0000\u0001\u0000\u0019\n\u0000\u0010\u0000\u0011\u0001\u0000",
      "context_after": "InnerClasses\u0007\u0000 \u0001\u0000\u001acom/example/FactoryManager\u0001\u0000\u0014DataProcessorFactory\u0001\u0000\nObjectFactory\u0001\u0000\bNestHost\u0000!\u0000\u0001\u0000\u0003\u0000\u0001\u0000\u0005\u0000\u0000\u0000\u0003\u0000\u0001\u0000\u0007\u0000\b\u0000\u0001\u0000\t\u0000\u0000\u0000/\u0000\u0001\u0000\u0001\u0000\u0000\u0000\u0005*\u0000"
    },
    {
      "path": "target/classes/com/example/FactoryManager$DataProcessorFactory.class",
      "line": 9,
      "col": 100,
      "snippet": "SourceFile\u0001\u0000\u0013FactoryManager.java\u0001\u0000\tSignature\u0001\u0000YLjava/lang/Object;Lcom/example/FactoryManager$ObjectFactory<Lcom/example/DataProcessor;>;\u0001\u0000",
      "context_before": "\u0000\u0001\u0000\u0019\n\u0000\u0010\u0000\u0011\u0001\u0000",
      "context_after": "InnerClasses\u0007\u0000 \u0001\u0000\u001acom/example/FactoryManager\u0001\u0000\u0014DataProcessorFactory\u0001\u0000\nObjectFactory\u0001\u0000\bNestHost\u0000!\u0000\u0001\u0000\u0003\u0000\u0001\u0000\u0005\u0000\u0000\u0000\u0003\u0000\u0001\u0000\u0007\u0000\b\u0000\u0001\u0000\t\u0000\u0000\u0000/\u0000\u0001\u0000\u0001\u0000\u0000\u0000\u0005*\u0000"
    },
    {
      "path": "target/classes/com/example/FactoryManager$DataProcessorFactory.class",
      "line": 10,
      "col": 31,
      "snippet": "InnerClasses\u0007\u0000 \u0001\u0000\u001acom/example/FactoryManager\u0001\u0000\u0014DataProcessorFactory\u0001\u0000",
      "context_before": "\u0000\u0010\u0000\u0011\u0001\u0000\nSourceFile\u0001\u0000\u0013FactoryManager.java\u0001\u0000\tSignature\u0001\u0000YLjava/lang/Object;Lcom/example/FactoryManager$ObjectFactory<Lcom/example/DataProcessor;>;\u0001\u0000",
      "context_after": "ObjectFactory\u0001\u0000\bNestHost\u0000!\u0000\u0001\u0000\u0003\u0000\u0001\u0000\u0005\u0000\u0000\u0000\u0003\u0000\u0001\u0000\u0007\u0000\b\u0000\u0001\u0000\t\u0000\u0000\u0000/\u0000\u0001\u0000\u0001\u0000\u0000\u0000\u0005*\u0000\n\u0000\u0000\u0000\u0002\u0000"
    },
    {
      "path": "target/classes/com/example/FactoryManager$DataProcessorFactory.class",
      "line": 10,
      "col": 61,
      "snippet": "InnerClasses\u0007\u0000 \u0001\u0000\u001acom/example/FactoryManager\u0001\u0000\u0014DataProcessorFactory\u0001\u0000",
      "context_before": "\u0000\u0010\u0000\u0011\u0001\u0000\nSourceFile\u0001\u0000\u0013FactoryManager.java\u0001\u0000\tSignature\u0001\u0000YLjava/lang/Object;Lcom/example/FactoryManager$ObjectFactory<Lcom/example/DataProcessor;>;\u0001\u0000",
      "context_after": "ObjectFactory\u0001\u0000\bNestHost\u0000!\u0000\u0001\u0000\u0003\u0000\u0001\u0000\u0005\u0000\u0000\u0000\u0003\u0000\u0001\u0000\u0007\u0000\b\u0000\u0001\u0000\t\u0000\u0000\u0000/\u0000\u0001\u0000\u0001\u0000\u0000\u0000\u0005*\u0000\n\u0000\u0000\u0000\u0002\u0000"
    },
    {
      "path": "target/classes/com/example/FactoryManager$DataProcessorFactory.class",
      "line": 11,
      "col": 7,
      "snippet": "ObjectFactory\u0001\u0000\bNestHost\u0000!\u0000\u0001\u0000\u0003\u0000\u0001\u0000\u0005\u0000\u0000\u0000\u0003\u0000\u0001\u0000\u0007\u0000\b\u0000\u0001\u0000\t\u0000\u0000\u0000/\u0000\u0001\u0000\u0001\u0000\u0000\u0000\u0005*\u0000",
      "context_before": "SourceFile\u0001\u0000\u0013FactoryManager.java\u0001\u0000\tSignature\u0001\u0000YLjava/lang/Object;Lcom/example/FactoryManager$ObjectFactory<Lcom/example/DataProcessor;>;\u0001\u0000\nInnerClasses\u0007\u0000 \u0001\u0000\u001acom/example/FactoryManager\u0001\u0000\u0014DataProcessorFactory\u0001\u0000",
      "context_after": "\u0000\u0000\u0000\u0002\u0000\n\u0000\u0000\u0000\u0006\u0000\u0001\u0000\u0000\u0000\u0000"
    },
    {
      "path": "target/classes/com/example/AdapterManager$PaymentAdapterFactory.class",
      "line": 1,
      "col": 25,
      "snippet": "\u0000\u0000\u00007\u0000.\u0007\u0000\u0002\u0001\u00000com/example/AdapterManager$PaymentAdapterFactory\u0007\u0000\u0004\u0001\u0000\u0010java/lang/Object\u0007\u0000\u0006\u0001\u0000)com/example/AdapterManager$AdapterFactory\u0001\u0000\u0006<init>\u0001\u0000\u0003()V\u0001\u0000\u0004Code",
      "context_before": "",
      "context_after": "\u0000\u0003\u0000\n"
    },
    {
      "path": "target/classes/com/example/AdapterManager$PaymentAdapterFactory.class",
      "line": 1,
      "col": 47,
      "snippet": "\u0000\u0000\u00007\u0000.\u0007\u0000\u0002\u0001\u00000com/example/AdapterManager$PaymentAdapterFactory\u0007\u0000\u0004\u0001\u0000\u0010java/lang/Object\u0007\u0000\u0006\u0001\u0000)com/example/AdapterManager$AdapterFactory\u0001\u0000\u0006<init>\u0001\u0000\u0003()V\u0001\u0000\u0004Code",
      "context_before": "",
      "context_after": "\u0000\u0003\u0000\n"
    },
    {
      "path": "target/classes/com/example/AdapterManager$PaymentAdapterFactory.class",
      "line": 1,
      "col": 54,
      "snippet": "\u0000\u0000\u00007\u0000.\u0007\u0000\u0002\u0001\u00000com/example/AdapterManager$PaymentAdapterFactory\u0007\u0000\u0004\u0001\u0000\u0010java/lang/Object\u0007\u0000\u0006\u0001\u0000)com/example/AdapterManager$AdapterFactory\u0001\u0000\u0006<init>\u0001\u0000\u0003()V\u0001\u0000\u0004Code",
      "context_before": "",
      "context_after": "\u0000\u0003\u0000\n"
    },
    {
      "path": "target/classes/com/example/AdapterManager$PaymentAdapterFactory.class",
      "line": 1,
      "col": 101,
      "snippet": "\u0000\u0000\u00007\u0000.\u0007\u0000\u0002\u0001\u00000com/example/AdapterManager$PaymentAdapterFactory\u0007\u0000\u0004\u0001\u0000\u0010java/lang/Object\u0007\u0000\u0006\u0001\u0000)com/example/AdapterManager$AdapterFactory\u0001\u0000\u0006<init>\u0001\u0000\u0003()V\u0001\u0000\u0004Code",
      "context_before": "",
      "context_after": "\u0000\u0003\u0000\n"
    },
    {
      "path": "target/classes/com/example/AdapterManager$PaymentAdapterFactory.class",
      "line": 1,
      "col": 116,
      "snippet": "\u0000\u0000\u00007\u0000.\u0007\u0000\u0002\u0001\u00000com/example/AdapterManager$PaymentAdapterFactory\u0007\u0000\u0004\u0001\u0000\u0010java/lang/Object\u0007\u0000\u0006\u0001\u0000)com/example/AdapterManager$AdapterFactory\u0001\u0000\u0006<init>\u0001\u0000\u0003()V\u0001\u0000\u0004Code",
      "context_before": "",
      "context_after": "\u0000\u0003\u0000\n"
    },
    {
      "path": "target/classes/com/example/AdapterManager$PaymentAdapterFactory.class",
      "line": 1,
      "col": 123,
      "snippet": "\u0000\u0000\u00007\u0000.\u0007\u0000\u0002\u0001\u00000com/example/AdapterManager$PaymentAdapterFactory\u0007\u0000\u0004\u0001\u0000\u0010java/lang/Object\u0007\u0000\u0006\u0001\u0000)com/example/AdapterManager$AdapterFactory\u0001\u0000\u0006<init>\u0001\u0000\u0003()V\u0001\u0000\u0004Code",
      "context_before": "",
      "context_after": "\u0000\u0003\u0000\n"
    },
    {
      "path": "target/classes/com/example/AdapterManager$PaymentAdapterFactory.class",
      "line": 4,
      "col": 67,
      "snippet": "\u0000\u0007\u0000\b\u0001\u0000\u000fLineNumberTable\u0001\u0000\u0012LocalVariableTable\u0001\u0000\u0004this\u0001\u00002Lcom/example/AdapterManager$PaymentAdapterFactory;\u0001\u0000\u0006create\u0001\u00009([Ljava/lang/Object;)Lcom/example/AdapterManager$Adapter;\u0001\u0000\tSignature\u0001\u0000=([Ljava/lang/Object;)Lcom/example/AdapterManager$Adapter<**>;\u0007\u0000\u0015\u0001\u0000\u0010java/lang/String\b\u0000\u0017\u0001\u0000\u0006stripe\u0007\u0000\u0019\u0001\u0000)com/example/AdapterManager$PaymentAdapter",
      "context_before": "\u0000\u0003\u0000\n",
      "context_after": "\u0000\u0018\u0000\u001b\n\u0000\u0007\u0000"
    },
    {
      "path": "target/classes/com/example/AdapterManager$PaymentAdapterFactory.class",
      "line": 4,
      "col": 89,
      "snippet": "\u0000\u0007\u0000\b\u0001\u0000\u000fLineNumberTable\u0001\u0000\u0012LocalVariableTable\u0001\u0000\u0004this\u0001\u00002Lcom/example/AdapterManager$PaymentAdapterFactory;\u0001\u0000\u0006create\u0001\u00009([Ljava/lang/Object;)Lcom/example/AdapterManager$Adapter;\u0001\u0000\tSignature\u0001\u0000=([Ljava/lang/Object;)Lcom/example/AdapterManager$Adapter<**>;\u0007\u0000\u0015\u0001\u0000\u0010java/lang/String\b\u0000\u0017\u0001\u0000\u0006stripe\u0007\u0000\u0019\u0001\u0000)com/example/AdapterManager$PaymentAdapter",
      "context_before": "\u0000\u0003\u0000\n",
      "context_after": "\u0000\u0018\u0000\u001b\n\u0000\u0007\u0000"
    },
    {
      "path": "target/classes/com/example/AdapterManager$PaymentAdapterFactory.class",
      "line": 4,
      "col": 96,
      "snippet": "\u0000\u0007\u0000\b\u0001\u0000\u000fLineNumberTable\u0001\u0000\u0012LocalVariableTable\u0001\u0000\u0004this\u0001\u00002Lcom/example/AdapterManager$PaymentAdapterFactory;\u0001\u0000\u0006create\u0001\u00009([Ljava/lang/Object;)Lcom/example/AdapterManager$Adapter;\u0001\u0000\tSignature\u0001\u0000=([Ljava/lang/Object;)Lcom/example/AdapterManager$Adapter<**>;\u0007\u0000\u0015\u0001\u0000\u0010java/lang/String\b\u0000\u0017\u0001\u0000\u0006stripe\u0007\u0000\u0019\u0001\u0000)com/example/AdapterManager$PaymentAdapter",
      "context_before": "\u0000\u0003\u0000\n",
      "context_after": "\u0000\u0018\u0000\u001b\n\u0000\u0007\u0000"
    },
    {
      "path": "target/classes/com/example/AdapterManager$PaymentAdapterFactory.class",
      "line": 4,
      "col": 150,
      "snippet": "\u0000\u0007\u0000\b\u0001\u0000\u000fLineNumberTable\u0001\u0000\u0012LocalVariableTable\u0001\u0000\u0004this\u0001\u00002Lcom/example/AdapterManager$PaymentAdapterFactory;\u0001\u0000\u0006create\u0001\u00009([Ljava/lang/Object;)Lcom/example/AdapterManager$Adapter;\u0001\u0000\tSignature\u0001\u0000=([Ljava/lang/Object;)Lcom/example/AdapterManager$Adapter<**>;\u0007\u0000\u0015\u0001\u0000\u0010java/lang/String\b\u0000\u0017\u0001\u0000\u0006stripe\u0007\u0000\u0019\u0001\u0000)com/example/AdapterManager$PaymentAdapter",
      "context_before": "\u0000\u0003\u0000\n",
      "context_after": "\u0000\u0018\u0000\u001b\n\u0000\u0007\u0000"
    },
    {
      "path": "target/classes/com/example/AdapterManager$PaymentAdapterFactory.class",
      "line": 4,
      "col": 165,
      "snippet": "\u0000\u0007\u0000\b\u0001\u0000\u000fLineNumberTable\u0001\u0000\u0012LocalVariableTable\u0001\u0000\u0004this\u0001\u00002Lcom/example/AdapterManager$PaymentAdapterFactory;\u0001\u0000\u0006create\u0001\u00009([Ljava/lang/Object;)Lcom/example/AdapterManager$Adapter;\u0001\u0000\tSignature\u0001\u0000=([Ljava/lang/Object;)Lcom/example/AdapterManager$Adapter<**>;\u0007\u0000\u0015\u0001\u0000\u0010java/lang/String\b\u0000\u0017\u0001\u0000\u0006stripe\u0007\u0000\u0019\u0001\u0000)com/example/AdapterManager$PaymentAdapter",
      "context_before": "\u0000\u0003\u0000\n",
      "context_after": "\u0000\u0018\u0000\u001b\n\u0000\u0007\u0000"
    },
    {
      "path": "target/classes/com/example/AdapterManager$PaymentAdapterFactory.class",
      "line": 4,
      "col": 222,
      "snippet": "\u0000\u0007\u0000\b\u0001\u0000\u000fLineNumberTable\u0001\u0000\u0012LocalVariableTable\u0001\u0000\u0004this\u0001\u00002Lcom/example/AdapterManager$PaymentAdapterFactory;\u0001\u0000\u0006create\u0001\u00009([Ljava/lang/Object;)Lcom/example/AdapterManager$Adapter;\u0001\u0000\tSignature\u0001\u0000=([Ljava/lang/Object;)Lcom/example/AdapterManager$Adapter<**>;\u0007\u0000\u0015\u0001\u0000\u0010java/lang/String\b\u0000\u0017\u0001\u0000\u0006stripe\u0007\u0000\u0019\u0001\u0000)com/example/AdapterManager$PaymentAdapter",
      "context_before": "\u0000\u0003\u0000\n",
      "context_after": "\u0000\u0018\u0000\u001b\n\u0000\u0007\u0000"
    },
    {
      "path": "target/classes/com/example/AdapterManager$PaymentAdapterFactory.class",
      "line": 4,
      "col": 237,
      "snippet": "\u0000\u0007\u0000\b\u0001\u0000\u000fLineNumberTable\u0001\u0000\u0012LocalVariableTable\u0001\u0000\u0004this\u0001\u00002Lcom/example/AdapterManager$PaymentAdapterFactory;\u0001\u0000\u0006create\u0001\u00009([Ljava/lang/Object;)Lcom/example/AdapterManager$Adapter;\u0001\u0000\tSignature\u0001\u0000=([Ljava/lang/Object;)Lcom/example/AdapterManager$Adapter<**>;\u0007\u0000\u0015\u0001\u0000\u0010java/lang/String\b\u0000\u0017\u0001\u0000\u0006stripe\u0007\u0000\u0019\u0001\u0000)com/example/AdapterManager$PaymentAdapter",
      "context_before": "\u0000\u0003\u0000\n",
      "context_after": "\u0000\u0018\u0000\u001b\n\u0000\u0007\u0000"
    },
    {
      "path": "target/classes/com/example/AdapterManager$PaymentAdapterFactory.class",
      "line": 4,
      "col": 301,
      "snippet": "\u0000\u0007\u0000\b\u0001\u0000\u000fLineNumberTable\u0001\u0000\u0012LocalVariableTable\u0001\u0000\u0004this\u0001\u00002Lcom/example/AdapterManager$PaymentAdapterFactory;\u0001\u0000\u0006create\u0001\u00009([Ljava/lang/Object;)Lcom/example/AdapterManager$Adapter;\u0001\u0000\tSignature\u0001\u0000=([Ljava/lang/Object;)Lcom/example/AdapterManager$Adapter<**>;\u0007\u0000\u0015\u0001\u0000\u0010java/lang/String\b\u0000\u0017\u0001\u0000\u0006stripe\u0007\u0000\u0019\u0001\u0000)com/example/AdapterManager$PaymentAdapter",
      "context_before": "\u0000\u0003\u0000\n",
      "context_after": "\u0000\u0018\u0000\u001b\n\u0000\u0007\u0000"
    },
    {
      "path": "target/classes/com/example/AdapterManager$PaymentAdapterFactory.class",
      "line": 4,
      "col": 323,
      "snippet": "\u0000\u0007\u0000\b\u0001\u0000\u000fLineNumberTable\u0001\u0000\u0012LocalVariableTable\u0001\u0000\u0004this\u0001\u00002Lcom/example/AdapterManager$PaymentAdapterFactory;\u0001\u0000\u0006create\u0001\u00009([Ljava/lang/Object;)Lcom/example/AdapterManager$Adapter;\u0001\u0000\tSignature\u0001\u0000=([Ljava/lang/Object;)Lcom/example/AdapterManager$Adapter<**>;\u0007\u0000\u0015\u0001\u0000\u0010java/lang/String\b\u0000\u0017\u0001\u0000\u0006stripe\u0007\u0000\u0019\u0001\u0000)com/example/AdapterManager$PaymentAdapter",
      "context_before": "\u0000\u0003\u0000\n",
      "context_after": "\u0000\u0018\u0000\u001b\n\u0000\u0007\u0000"
    },
    {
      "path": "target/classes/com/example/AdapterManager$PaymentAdapterFactory.class",
      "line": 10,
      "col": 14,
      "snippet": "SourceFile\u0001\u0000\u0013AdapterManager.java\u0001\u0000",
      "context_before": "gatewayType\u0001\u0000\u0012Ljava/lang/String;\u0001\u0000\nStackMapTable\u0001\u0000",
      "context_after": "InnerClasses\u0007\u0000&\u0001\u0000\"com/example/AdapterManager$Adapter\u0007\u0000(\u0001\u0000\u001acom/example/AdapterManager\u0001\u0000\u0007Adapter\u0001\u0000\u000eAdapterFactory\u0001\u0000\u000ePaymentAdapter\u0001\u0000\u0015PaymentAdapterFactory\u0001\u0000\bNestHost\u0000!\u0000\u0001\u0000\u0003\u0000\u0001\u0000\u0005\u0000\u0000\u0000\u0002\u0000\u0001\u0000\u0007\u0000\b\u0000\u0001\u0000\t\u0000\u0000\u0000/\u0000\u0001\u0000\u0001\u0000\u0000\u0000\u0005*\u0000\n\u0000\u0000\u0000\u0002\u0000"
    },
    {
      "path": "target/classes/com/example/AdapterManager$PaymentAdapterFactory.class",
      "line": 11,
      "col": 31,
      "snippet": "InnerClasses\u0007\u0000&\u0001\u0000\"com/example/AdapterManager$Adapter\u0007\u0000(\u0001\u0000\u001acom/example/AdapterManager\u0001\u0000\u0007Adapter\u0001\u0000\u000eAdapterFactory\u0001\u0000\u000ePaymentAdapter\u0001\u0000\u0015PaymentAdapterFactory\u0001\u0000\bNestHost\u0000!\u0000\u0001\u0000\u0003\u0000\u0001\u0000\u0005\u0000\u0000\u0000\u0002\u0000\u0001\u0000\u0007\u0000\b\u0000\u0001\u0000\t\u0000\u0000\u0000/\u0000\u0001\u0000\u0001\u0000\u0000\u0000\u0005*\u0000",
      "context_before": "StackMapTable\u0001\u0000\nSourceFile\u0001\u0000\u0013AdapterManager.java\u0001\u0000",
      "context_after": "\u0000\u0000\u0000\u0002\u0000\n\u0000\u0000\u0000\u0006\u0000\u0001\u0000\u0000\u00016\u0000"
    },
    {
      "path": "target/classes/com/example/AdapterManager$PaymentAdapterFactory.class",
      "line": 11,
      "col": 46,
      "snippet": "InnerClasses\u0007\u0000&\u0001\u0000\"com/example/AdapterManager$Adapter\u0007\u0000(\u0001\u0000\u001acom/example/AdapterManager\u0001\u0000\u0007Adapter\u0001\u0000\u000eAdapterFactory\u0001\u0000\u000ePaymentAdapter\u0001\u0000\u0015PaymentAdapterFactory\u0001\u0000\bNestHost\u0000!\u0000\u0001\u0000\u0003\u0000\u0001\u0000\u0005\u0000\u0000\u0000\u0002\u0000\u0001\u0000\u0007\u0000\b\u0000\u0001\u0000\t\u0000\u0000\u0000/\u0000\u0001\u0000\u0001\u0000\u0000\u0000\u0005*\u0000",
      "context_before": "StackMapTable\u0001\u0000\nSourceFile\u0001\u0000\u0013AdapterManager.java\u0001\u0000",
      "context_after": "\u0000\u0000\u0000\u0002\u0000\n\u0000\u0000\u0000\u0006\u0000\u0001\u0000\u0000\u00016\u0000"
    },
    {
      "path": "target/classes/com/example/AdapterManager$PaymentAdapterFactory.class",
      "line": 11,
      "col": 71,
      "snippet": "InnerClasses\u0007\u0000&\u0001\u0000\"com/example/AdapterManager$Adapter\u0007\u0000(\u0001\u0000\u001acom/example/AdapterManager\u0001\u0000\u0007Adapter\u0001\u0000\u000eAdapterFactory\u0001\u0000\u000ePaymentAdapter\u0001\u0000\u0015PaymentAdapterFactory\u0001\u0000\bNestHost\u0000!\u0000\u0001\u0000\u0003\u0000\u0001\u0000\u0005\u0000\u0000\u0000\u0002\u0000\u0001\u0000\u0007\u0000\b\u0000\u0001\u0000\t\u0000\u0000\u0000/\u0000\u0001\u0000\u0001\u0000\u0000\u0000\u0005*\u0000",
      "context_before": "StackMapTable\u0001\u0000\nSourceFile\u0001\u0000\u0013AdapterManager.java\u0001\u0000",
      "context_after": "\u0000\u0000\u0000\u0002\u0000\n\u0000\u0000\u0000\u0006\u0000\u0001\u0000\u0000\u00016\u0000"
    },
    {
      "path": "target/classes/com/example/AdapterManager$PaymentAdapterFactory.class",
      "line": 11,
      "col": 88,
      "snippet": "InnerClasses\u0007\u0000&\u0001\u0000\"com/example/AdapterManager$Adapter\u0007\u0000(\u0001\u0000\u001acom/example/AdapterManager\u0001\u0000\u0007Adapter\u0001\u0000\u000eAdapterFactory\u0001\u0000\u000ePaymentAdapter\u0001\u0000\u0015PaymentAdapterFactory\u0001\u0000\bNestHost\u0000!\u0000\u0001\u0000\u0003\u0000\u0001\u0000\u0005\u0000\u0000\u0000\u0002\u0000\u0001\u0000\u0007\u0000\b\u0000\u0001\u0000\t\u0000\u0000\u0000/\u0000\u0001\u0000\u0001\u0000\u0000\u0000\u0005*\u0000",
      "context_before": "StackMapTable\u0001\u0000\nSourceFile\u0001\u0000\u0013AdapterManager.java\u0001\u0000",
      "context_after": "\u0000\u0000\u0000\u0002\u0000\n\u0000\u0000\u0000\u0006\u0000\u0001\u0000\u0000\u00016\u0000"
    },
    {
      "path": "target/classes/com/example/AdapterManager$PaymentAdapterFactory.class",
      "line": 11,
      "col": 98,
      "snippet": "InnerClasses\u0007\u0000&\u0001\u0000\"com/example/AdapterManager$Adapter\u0007\u0000(\u0001\u0000\u001acom/example/AdapterManager\u0001\u0000\u0007Adapter\u0001\u0000\u000eAdapterFactory\u0001\u0000\u000ePaymentAdapter\u0001\u0000\u0015PaymentAdapterFactory\u0001\u0000\bNestHost\u0000!\u0000\u0001\u0000\u0003\u0000\u0001\u0000\u0005\u0000\u0000\u0000\u0002\u0000\u0001\u0000\u0007\u0000\b\u0000\u0001\u0000\t\u0000\u0000\u0000/\u0000\u0001\u0000\u0001\u0000\u0000\u0000\u0005*\u0000",
      "context_before": "StackMapTable\u0001\u0000\nSourceFile\u0001\u0000\u0013AdapterManager.java\u0001\u0000",
      "context_after": "\u0000\u0000\u0000\u0002\u0000\n\u0000\u0000\u0000\u0006\u0000\u0001\u0000\u0000\u00016\u0000"
    },
    {
      "path": "target/classes/com/example/AdapterManager$PaymentAdapterFactory.class",
      "line": 11,
      "col": 105,
      "snippet": "InnerClasses\u0007\u0000&\u0001\u0000\"com/example/AdapterManager$Adapter\u0007\u0000(\u0001\u0000\u001acom/example/AdapterManager\u0001\u0000\u0007Adapter\u0001\u0000\u000eAdapterFactory\u0001\u0000\u000ePaymentAdapter\u0001\u0000\u0015PaymentAdapterFactory\u0001\u0000\bNestHost\u0000!\u0000\u0001\u0000\u0003\u0000\u0001\u0000\u0005\u0000\u0000\u0000\u0002\u0000\u0001\u0000\u0007\u0000\b\u0000\u0001\u0000\t\u0000\u0000\u0000/\u0000\u0001\u0000\u0001\u0000\u0000\u0000\u0005*\u0000",
      "context_before": "StackMapTable\u0001\u0000\nSourceFile\u0001\u0000\u0013AdapterManager.java\u0001\u0000",
      "context_after": "\u0000\u0000\u0000\u0002\u0000\n\u0000\u0000\u0000\u0006\u0000\u0001\u0000\u0000\u00016\u0000"
    },
    {
      "path": "target/classes/com/example/AdapterManager$PaymentAdapterFactory.class",
      "line": 11,
      "col": 122,
      "snippet": "InnerClasses\u0007\u0000&\u0001\u0000\"com/example/AdapterManager$Adapter\u0007\u0000(\u0001\u0000\u001acom/example/AdapterManager\u0001\u0000\u0007Adapter\u0001\u0000\u000eAdapterFactory\u0001\u0000\u000ePaymentAdapter\u0001\u0000\u0015PaymentAdapterFactory\u0001\u0000\bNestHost\u0000!\u0000\u0001\u0000\u0003\u0000\u0001\u0000\u0005\u0000\u0000\u0000\u0002\u0000\u0001\u0000\u0007\u0000\b\u0000\u0001\u0000\t\u0000\u0000\u0000/\u0000\u0001\u0000\u0001\u0000\u0000\u0000\u0005*\u0000",
      "context_before": "StackMapTable\u0001\u0000\nSourceFile\u0001\u0000\u0013AdapterManager.java\u0001\u0000",
      "context_after": "\u0000\u0000\u0000\u0002\u0000\n\u0000\u0000\u0000\u0006\u0000\u0001\u0000\u0000\u00016\u0000"
    },
    {
      "path": "target/classes/com/example/AdapterManager$PaymentAdapterFactory.class",
      "line": 11,
      "col": 139,
      "snippet": "InnerClasses\u0007\u0000&\u0001\u0000\"com/example/AdapterManager$Adapter\u0007\u0000(\u0001\u0000\u001acom/example/AdapterManager\u0001\u0000\u0007Adapter\u0001\u0000\u000eAdapterFactory\u0001\u0000\u000ePaymentAdapter\u0001\u0000\u0015PaymentAdapterFactory\u0001\u0000\bNestHost\u0000!\u0000\u0001\u0000\u0003\u0000\u0001\u0000\u0005\u0000\u0000\u0000\u0002\u0000\u0001\u0000\u0007\u0000\b\u0000\u0001\u0000\t\u0000\u0000\u0000/\u0000\u0001\u0000\u0001\u0000\u0000\u0000\u0005*\u0000",
      "context_before": "StackMapTable\u0001\u0000\nSourceFile\u0001\u0000\u0013AdapterManager.java\u0001\u0000",
      "context_after": "\u0000\u0000\u0000\u0002\u0000\n\u0000\u0000\u0000\u0006\u0000\u0001\u0000\u0000\u00016\u0000"
    },
    {
      "path": "target/classes/com/example/AdapterManager$PaymentAdapterFactory.class",
      "line": 11,
      "col": 146,
      "snippet": "InnerClasses\u0007\u0000&\u0001\u0000\"com/example/AdapterManager$Adapter\u0007\u0000(\u0001\u0000\u001acom/example/AdapterManager\u0001\u0000\u0007Adapter\u0001\u0000\u000eAdapterFactory\u0001\u0000\u000ePaymentAdapter\u0001\u0000\u0015PaymentAdapterFactory\u0001\u0000\bNestHost\u0000!\u0000\u0001\u0000\u0003\u0000\u0001\u0000\u0005\u0000\u0000\u0000\u0002\u0000\u0001\u0000\u0007\u0000\b\u0000\u0001\u0000\t\u0000\u0000\u0000/\u0000\u0001\u0000\u0001\u0000\u0000\u0000\u0005*\u0000",
      "context_before": "StackMapTable\u0001\u0000\nSourceFile\u0001\u0000\u0013AdapterManager.java\u0001\u0000",
      "context_after": "\u0000\u0000\u0000\u0002\u0000\n\u0000\u0000\u0000\u0006\u0000\u0001\u0000\u0000\u00016\u0000"
    },
    {
      "path": "target/classes/com/example/AdapterManager$AuthenticationAdapterFactory.class",
      "line": 1,
      "col": 25,
      "snippet": "\u0000\u0000\u00007\u0000.\u0007\u0000\u0002\u0001\u00007com/example/AdapterManager$AuthenticationAdapterFactory\u0007\u0000\u0004\u0001\u0000\u0010java/lang/Object\u0007\u0000\u0006\u0001\u0000)com/example/AdapterManager$AdapterFactory\u0001\u0000\u0006<init>\u0001\u0000\u0003()V\u0001\u0000\u0004Code",
      "context_before": "",
      "context_after": "\u0000\u0003\u0000\n"
    },
    {
      "path": "target/classes/com/example/AdapterManager$AuthenticationAdapterFactory.class",
      "line": 1,
      "col": 54,
      "snippet": "\u0000\u0000\u00007\u0000.\u0007\u0000\u0002\u0001\u00007com/example/AdapterManager$AuthenticationAdapterFactory\u0007\u0000\u0004\u0001\u0000\u0010java/lang/Object\u0007\u0000\u0006\u0001\u0000)com/example/AdapterManager$AdapterFactory\u0001\u0000\u0006<init>\u0001\u0000\u0003()V\u0001\u0000\u0004Code",
      "context_before": "",
      "context_after": "\u0000\u0003\u0000\n"
    },
    {
      "path": "target/classes/com/example/AdapterManager$AuthenticationAdapterFactory.class",
      "line": 1,
      "col": 61,
      "snippet": "\u0000\u0000\u00007\u0000.\u0007\u0000\u0002\u0001\u00007com/example/AdapterManager$AuthenticationAdapterFactory\u0007\u0000\u0004\u0001\u0000\u0010java/lang/Object\u0007\u0000\u0006\u0001\u0000)com/example/AdapterManager$AdapterFactory\u0001\u0000\u0006<init>\u0001\u0000\u0003()V\u0001\u0000\u0004Code",
      "context_before": "",
      "context_after": "\u0000\u0003\u0000\n"
    },
    {
      "path": "target/classes/com/example/AdapterManager$AuthenticationAdapterFactory.class",
      "line": 1,
      "col": 108,
      "snippet": "\u0000\u0000\u00007\u0000.\u0007\u0000\u0002\u0001\u00007com/example/AdapterManager$AuthenticationAdapterFactory\u0007\u0000\u0004\u0001\u0000\u0010java/lang/Object\u0007\u0000\u0006\u0001\u0000)com/example/AdapterManager$AdapterFactory\u0001\u0000\u0006<init>\u0001\u0000\u0003()V\u0001\u0000\u0004Code",
      "context_before": "",
      "context_after": "\u0000\u0003\u0000\n"
    },
    {
      "path": "target/classes/com/example/AdapterManager$AuthenticationAdapterFactory.class",
      "line": 1,
      "col": 123,
      "snippet": "\u0000\u0000\u00007\u0000.\u0007\u0000\u0002\u0001\u00007com/example/AdapterManager$AuthenticationAdapterFactory\u0007\u0000\u0004\u0001\u0000\u0010java/lang/Object\u0007\u0000\u0006\u0001\u0000)com/example/AdapterManager$AdapterFactory\u0001\u0000\u0006<init>\u0001\u0000\u0003()V\u0001\u0000\u0004Code",
      "context_before": "",
      "context_after": "\u0000\u0003\u0000\n"
    },
    {
      "path": "target/classes/com/example/AdapterManager$AuthenticationAdapterFactory.class",
      "line": 1,
      "col": 130,
      "snippet": "\u0000\u0000\u00007\u0000.\u0007\u0000\u0002\u0001\u00007com/example/AdapterManager$AuthenticationAdapterFactory\u0007\u0000\u0004\u0001\u0000\u0010java/lang/Object\u0007\u0000\u0006\u0001\u0000)com/example/AdapterManager$AdapterFactory\u0001\u0000\u0006<init>\u0001\u0000\u0003()V\u0001\u0000\u0004Code",
      "context_before": "",
      "context_after": "\u0000\u0003\u0000\n"
    },
    {
      "path": "target/classes/com/example/AdapterManager$AuthenticationAdapterFactory.class",
      "line": 4,
      "col": 67,
      "snippet": "\u0000\u0007\u0000\b\u0001\u0000\u000fLineNumberTable\u0001\u0000\u0012LocalVariableTable\u0001\u0000\u0004this\u0001\u00009Lcom/example/AdapterManager$AuthenticationAdapterFactory;\u0001\u0000\u0006create\u0001\u00009([Ljava/lang/Object;)Lcom/example/AdapterManager$Adapter;\u0001\u0000\tSignature\u0001\u0000=([Ljava/lang/Object;)Lcom/example/AdapterManager$Adapter<**>;\u0007\u0000\u0015\u0001\u0000\u0010java/lang/String\b\u0000\u0017\u0001\u0000\u0006oauth2\u0007\u0000\u0019\u0001\u00000com/example/AdapterManager$AuthenticationAdapter",
      "context_before": "\u0000\u0003\u0000\n",
      "context_after": "\u0000\u0018\u0000\u001b\n\u0000\u0007\u0000"
    },
    {
      "path": "target/classes/com/example/AdapterManager$AuthenticationAdapterFactory.class",
      "line": 4,
      "col": 96,
      "snippet": "\u0000\u0007\u0000\b\u0001\u0000\u000fLineNumberTable\u0001\u0000\u0012LocalVariableTable\u0001\u0000\u0004this\u0001\u00009Lcom/example/AdapterManager$AuthenticationAdapterFactory;\u0001\u0000\u0006create\u0001\u00009([Ljava/lang/Object;)Lcom/example/AdapterManager$Adapter;\u0001\u0000\tSignature\u0001\u0000=([Ljava/lang/Object;)Lcom/example/AdapterManager$Adapter<**>;\u0007\u0000\u0015\u0001\u0000\u0010java/lang/String\b\u0000\u0017\u0001\u0000\u0006oauth2\u0007\u0000\u0019\u0001\u00000com/example/AdapterManager$AuthenticationAdapter",
      "context_before": "\u0000\u0003\u0000\n",
      "context_after": "\u0000\u0018\u0000\u001b\n\u0000\u0007\u0000"
    },
    {
      "path": "target/classes/com/example/AdapterManager$AuthenticationAdapterFactory.class",
      "line": 4,
      "col": 103,
      "snippet": "\u0000\u0007\u0000\b\u0001\u0000\u000fLineNumberTable\u0001\u0000\u0012LocalVariableTable\u0001\u0000\u0004this\u0001\u00009Lcom/example/AdapterManager$AuthenticationAdapterFactory;\u0001\u0000\u0006create\u0001\u00009([Ljava/lang/Object;)Lcom/example/AdapterManager$Adapter;\u0001\u0000\tSignature\u0001\u0000=([Ljava/lang/Object;)Lcom/example/AdapterManager$Adapter<**>;\u0007\u0000\u0015\u0001\u0000\u0010java/lang/String\b\u0000\u0017\u0001\u0000\u0006oauth2\u0007\u0000\u0019\u0001\u00000com/example/AdapterManager$AuthenticationAdapter",
      "context_before": "\u0000\u0003\u0000\n",
      "context_after": "\u0000\u0018\u0000\u001b\n\u0000\u0007\u0000"
    },
    {
      "path": "target/classes/com/example/AdapterManager$AuthenticationAdapterFactory.class",
      "line": 4,
      "col": 157,
      "snippet": "\u0000\u0007\u0000\b\u0001\u0000\u000fLineNumberTable\u0001\u0000\u0012LocalVariableTable\u0001\u0000\u0004this\u0001\u00009Lcom/example/AdapterManager$AuthenticationAdapterFactory;\u0001\u0000\u0006create\u0001\u00009([Ljava/lang/Object;)Lcom/example/AdapterManager$Adapter;\u0001\u0000\tSignature\u0001\u0000=([Ljava/lang/Object;)Lcom/example/AdapterManager$Adapter<**>;\u0007\u0000\u0015\u0001\u0000\u0010java/lang/String\b\u0000\u0017\u0001\u0000\u0006oauth2\u0007\u0000\u0019\u0001\u00000com/example/AdapterManager$AuthenticationAdapter",
      "context_before": "\u0000\u0003\u0000\n",
      "context_after": "\u0000\u0018\u0000\u001b\n\u0000\u0007\u0000"
    },
    {
      "path": "target/classes/com/example/AdapterManager$AuthenticationAdapterFactory.class",
      "line": 4,
      "col": 172,
      "snippet": "\u0000\u0007\u0000\b\u0001\u0000\u000fLineNumberTable\u0001\u0000\u0012LocalVariableTable\u0001\u0000\u0004this\u0001\u00009Lcom/example/AdapterManager$AuthenticationAdapterFactory;\u0001\u0000\u0006create\u0001\u00009([Ljava/lang/Object;)Lcom/example/AdapterManager$Adapter;\u0001\u0000\tSignature\u0001\u0000=([Ljava/lang/Object;)Lcom/example/AdapterManager$Adapter<**>;\u0007\u0000\u0015\u0001\u0000\u0010java/lang/String\b\u0000\u0017\u0001\u0000\u0006oauth2\u0007\u0000\u0019\u0001\u00000com/example/AdapterManager$AuthenticationAdapter",
      "context_before": "\u0000\u0003\u0000\n",
      "context_after": "\u0000\u0018\u0000\u001b\n\u0000\u0007\u0000"
    },
    {
      "path": "target/classes/com/example/AdapterManager$AuthenticationAdapterFactory.class",
      "line": 4,
      "col": 229,
      "snippet": "\u0000\u0007\u0000\b\u0001\u0000\u000fLineNumberTable\u0001\u0000\u0012LocalVariableTable\u0001\u0000\u0004this\u0001\u00009Lcom/example/AdapterManager$AuthenticationAdapterFactory;\u0001\u0000\u0006create\u0001\u00009([Ljava/lang/Object;)Lcom/example/AdapterManager$Adapter;\u0001\u0000\tSignature\u0001\u0000=([Ljava/lang/Object;)Lcom/example/AdapterManager$Adapter<**>;\u0007\u0000\u0015\u0001\u0000\u0010java/lang/String\b\u0000\u0017\u0001\u0000\u0006oauth2\u0007\u0000\u0019\u0001\u00000com/example/AdapterManager$AuthenticationAdapter",
      "context_before": "\u0000\u0003\u0000\n",
      "context_after": "\u0000\u0018\u0000\u001b\n\u0000\u0007\u0000"
    },
    {
      "path": "target/classes/com/example/AdapterManager$AuthenticationAdapterFactory.class",
      "line": 4,
      "col": 244,
      "snippet": "\u0000\u0007\u0000\b\u0001\u0000\u000fLineNumberTable\u0001\u0000\u0012LocalVariableTable\u0001\u0000\u0004this\u0001\u00009Lcom/example/AdapterManager$AuthenticationAdapterFactory;\u0001\u0000\u0006create\u0001\u00009([Ljava/lang/Object;)Lcom/example/AdapterManager$Adapter;\u0001\u0000\tSignature\u0001\u0000=([Ljava/lang/Object;)Lcom/example/AdapterManager$Adapter<**>;\u0007\u0000\u0015\u0001\u0000\u0010java/lang/String\b\u0000\u0017\u0001\u0000\u0006oauth2\u0007\u0000\u0019\u0001\u00000com/example/AdapterManager$AuthenticationAdapter",
      "context_before": "\u0000\u0003\u0000\n",
      "context_after": "\u0000\u0018\u0000\u001b\n\u0000\u0007\u0000"
    },
    {
      "path": "target/classes/com/example/AdapterManager$AuthenticationAdapterFactory.class",
      "line": 4,
      "col": 308,
      "snippet": "\u0000\u0007\u0000\b\u0001\u0000\u000fLineNumberTable\u0001\u0000\u0012LocalVariableTable\u0001\u0000\u0004this\u0001\u00009Lcom/example/AdapterManager$AuthenticationAdapterFactory;\u0001\u0000\u0006create\u0001\u00009([Ljava/lang/Object;)Lcom/example/AdapterManager$Adapter;\u0001\u0000\tSignature\u0001\u0000=([Ljava/lang/Object;)Lcom/example/AdapterManager$Adapter<**>;\u0007\u0000\u0015\u0001\u0000\u0010java/lang/String\b\u0000\u0017\u0001\u0000\u0006oauth2\u0007\u0000\u0019\u0001\u00000com/example/AdapterManager$AuthenticationAdapter",
      "context_before": "\u0000\u0003\u0000\n",
      "context_after": "\u0000\u0018\u0000\u001b\n\u0000\u0007\u0000"
    },
    {
      "path": "target/classes/com/example/AdapterManager$AuthenticationAdapterFactory.class",
      "line": 4,
      "col": 337,
      "snippet": "\u0000\u0007\u0000\b\u0001\u0000\u000fLineNumberTable\u0001\u0000\u0012LocalVariableTable\u0001\u0000\u0004this\u0001\u00009Lcom/example/AdapterManager$AuthenticationAdapterFactory;\u0001\u0000\u0006create\u0001\u00009([Ljava/lang/Object;)Lcom/example/AdapterManager$Adapter;\u0001\u0000\tSignature\u0001\u0000=([Ljava/lang/Object;)Lcom/example/AdapterManager$Adapter<**>;\u0007\u0000\u0015\u0001\u0000\u0010java/lang/String\b\u0000\u0017\u0001\u0000\u0006oauth2\u0007\u0000\u0019\u0001\u00000com/example/AdapterManager$AuthenticationAdapter",
      "context_before": "\u0000\u0003\u0000\n",
      "context_after": "\u0000\u0018\u0000\u001b\n\u0000\u0007\u0000"
    },
    {
      "path": "target/classes/com/example/AdapterManager$AuthenticationAdapterFactory.class",
      "line": 9,
      "col": 14,
      "snippet": "SourceFile\u0001\u0000\u0013AdapterManager.java\u0001\u0000",
      "context_before": "\u0001\u0000\u0015(Ljava/lang/String;)V\u0001\u0000\u0006params\u0001\u0000\u0013[Ljava/lang/Object;\u0001\u0000\bauthType\u0001\u0000\u0012Ljava/lang/String;\u0001\u0000\nStackMapTable\u0001\u0000",
      "context_after": "InnerClasses\u0007\u0000&\u0001\u0000\"com/example/AdapterManager$Adapter\u0007\u0000(\u0001\u0000\u001acom/example/AdapterManager\u0001\u0000\u0007Adapter\u0001\u0000\u000eAdapterFactory\u0001\u0000\u0015AuthenticationAdapter\u0001\u0000\nAuthenticationAdapterFactory\u0001\u0000\bNestHost\u0000!\u0000\u0001\u0000\u0003\u0000\u0001\u0000\u0005\u0000\u0000\u0000\u0002\u0000\u0001\u0000\u0007\u0000\b\u0000\u0001\u0000\t\u0000\u0000\u0000/\u0000\u0001\u0000\u0001\u0000\u0000\u0000\u0005*\u0000"
    },
    {
      "path": "target/classes/com/example/AdapterManager$AuthenticationAdapterFactory.class",
      "line": 10,
      "col": 31,
      "snippet": "InnerClasses\u0007\u0000&\u0001\u0000\"com/example/AdapterManager$Adapter\u0007\u0000(\u0001\u0000\u001acom/example/AdapterManager\u0001\u0000\u0007Adapter\u0001\u0000\u000eAdapterFactory\u0001\u0000\u0015AuthenticationAdapter\u0001\u0000",
      "context_before": "StackMapTable\u0001\u0000\nSourceFile\u0001\u0000\u0013AdapterManager.java\u0001\u0000",
      "context_after": "AuthenticationAdapterFactory\u0001\u0000\bNestHost\u0000!\u0000\u0001\u0000\u0003\u0000\u0001\u0000\u0005\u0000\u0000\u0000\u0002\u0000\u0001\u0000\u0007\u0000\b\u0000\u0001\u0000\t\u0000\u0000\u0000/\u0000\u0001\u0000\u0001\u0000\u0000\u0000\u0005*\u0000\n\u0000\u0000\u0000\u0002\u0000"
    },
    {
      "path": "target/classes/com/example/AdapterManager$AuthenticationAdapterFactory.class",
      "line": 10,
      "col": 46,
      "snippet": "InnerClasses\u0007\u0000&\u0001\u0000\"com/example/AdapterManager$Adapter\u0007\u0000(\u0001\u0000\u001acom/example/AdapterManager\u0001\u0000\u0007Adapter\u0001\u0000\u000eAdapterFactory\u0001\u0000\u0015AuthenticationAdapter\u0001\u0000",
      "context_before": "StackMapTable\u0001\u0000\nSourceFile\u0001\u0000\u0013AdapterManager.java\u0001\u0000",
      "context_after": "AuthenticationAdapterFactory\u0001\u0000\bNestHost\u0000!\u0000\u0001\u0000\u0003\u0000\u0001\u0000\u0005\u0000\u0000\u0000\u0002\u0000\u0001\u0000\u0007\u0000\b\u0000\u0001\u0000\t\u0000\u0000\u0000/\u0000\u0001\u0000\u0001\u0000\u0000\u0000\u0005*\u0000\n\u0000\u0000\u0000\u0002\u0000"
    },
    {
      "path": "target/classes/com/example/AdapterManager$AuthenticationAdapterFactory.class",
      "line": 10,
      "col": 71,
      "snippet": "InnerClasses\u0007\u0000&\u0001\u0000\"com/example/AdapterManager$Adapter\u0007\u0000(\u0001\u0000\u001acom/example/AdapterManager\u0001\u0000\u0007Adapter\u0001\u0000\u000eAdapterFactory\u0001\u0000\u0015AuthenticationAdapter\u0001\u0000",
      "context_before": "StackMapTable\u0001\u0000\nSourceFile\u0001\u0000\u0013AdapterManager.java\u0001\u0000",
      "context_after": "AuthenticationAdapterFactory\u0001\u0000\bNestHost\u0000!\u0000\u0001\u0000\u0003\u0000\u0001\u0000\u0005\u0000\u0000\u0000\u0002\u0000\u0001\u0000\u0007\u0000\b\u0000\u0001\u0000\t\u0000\u0000\u0000/\u0000\u0001\u0000\u0001\u0000\u0000\u0000\u0005*\u0000\n\u0000\u0000\u0000\u0002\u0000"
    },
    {
      "path": "target/classes/com/example/AdapterManager$AuthenticationAdapterFactory.class",
      "line": 10,
      "col": 88,
      "snippet": "InnerClasses\u0007\u0000&\u0001\u0000\"com/example/AdapterManager$Adapter\u0007\u0000(\u0001\u0000\u001acom/example/AdapterManager\u0001\u0000\u0007Adapter\u0001\u0000\u000eAdapterFactory\u0001\u0000\u0015AuthenticationAdapter\u0001\u0000",
      "context_before": "StackMapTable\u0001\u0000\nSourceFile\u0001\u0000\u0013AdapterManager.java\u0001\u0000",
      "context_after": "AuthenticationAdapterFactory\u0001\u0000\bNestHost\u0000!\u0000\u0001\u0000\u0003\u0000\u0001\u0000\u0005\u0000\u0000\u0000\u0002\u0000\u0001\u0000\u0007\u0000\b\u0000\u0001\u0000\t\u0000\u0000\u0000/\u0000\u0001\u0000\u0001\u0000\u0000\u0000\u0005*\u0000\n\u0000\u0000\u0000\u0002\u0000"
    },
    {
      "path": "target/classes/com/example/AdapterManager$AuthenticationAdapterFactory.class",
      "line": 10,
      "col": 98,
      "snippet": "InnerClasses\u0007\u0000&\u0001\u0000\"com/example/AdapterManager$Adapter\u0007\u0000(\u0001\u0000\u001acom/example/AdapterManager\u0001\u0000\u0007Adapter\u0001\u0000\u000eAdapterFactory\u0001\u0000\u0015AuthenticationAdapter\u0001\u0000",
      "context_before": "StackMapTable\u0001\u0000\nSourceFile\u0001\u0000\u0013AdapterManager.java\u0001\u0000",
      "context_after": "AuthenticationAdapterFactory\u0001\u0000\bNestHost\u0000!\u0000\u0001\u0000\u0003\u0000\u0001\u0000\u0005\u0000\u0000\u0000\u0002\u0000\u0001\u0000\u0007\u0000\b\u0000\u0001\u0000\t\u0000\u0000\u0000/\u0000\u0001\u0000\u0001\u0000\u0000\u0000\u0005*\u0000\n\u0000\u0000\u0000\u0002\u0000"
    },
    {
      "path": "target/classes/com/example/AdapterManager$AuthenticationAdapterFactory.class",
      "line": 10,
      "col": 105,
      "snippet": "InnerClasses\u0007\u0000&\u0001\u0000\"com/example/AdapterManager$Adapter\u0007\u0000(\u0001\u0000\u001acom/example/AdapterManager\u0001\u0000\u0007Adapter\u0001\u0000\u000eAdapterFactory\u0001\u0000\u0015AuthenticationAdapter\u0001\u0000",
      "context_before": "StackMapTable\u0001\u0000\nSourceFile\u0001\u0000\u0013AdapterManager.java\u0001\u0000",
      "context_after": "AuthenticationAdapterFactory\u0001\u0000\bNestHost\u0000!\u0000\u0001\u0000\u0003\u0000\u0001\u0000\u0005\u0000\u0000\u0000\u0002\u0000\u0001\u0000\u0007\u0000\b\u0000\u0001\u0000\t\u0000\u0000\u0000/\u0000\u0001\u0000\u0001\u0000\u0000\u0000\u0005*\u0000\n\u0000\u0000\u0000\u0002\u0000"
    },
    {
      "path": "target/classes/com/example/AdapterManager$AuthenticationAdapterFactory.class",
      "line": 10,
      "col": 129,
      "snippet": "InnerClasses\u0007\u0000&\u0001\u0000\"com/example/AdapterManager$Adapter\u0007\u0000(\u0001\u0000\u001acom/example/AdapterManager\u0001\u0000\u0007Adapter\u0001\u0000\u000eAdapterFactory\u0001\u0000\u0015AuthenticationAdapter\u0001\u0000",
      "context_before": "StackMapTable\u0001\u0000\nSourceFile\u0001\u0000\u0013AdapterManager.java\u0001\u0000",
      "context_after": "AuthenticationAdapterFactory\u0001\u0000\bNestHost\u0000!\u0000\u0001\u0000\u0003\u0000\u0001\u0000\u0005\u0000\u0000\u0000\u0002\u0000\u0001\u0000\u0007\u0000\b\u0000\u0001\u0000\t\u0000\u0000\u0000/\u0000\u0001\u0000\u0001\u0000\u0000\u0000\u0005*\u0000\n\u0000\u0000\u0000\u0002\u0000"
    },
    {
      "path": "target/classes/com/example/AdapterManager$AuthenticationAdapterFactory.class",
      "line": 11,
      "col": 15,
      "snippet": "AuthenticationAdapterFactory\u0001\u0000\bNestHost\u0000!\u0000\u0001\u0000\u0003\u0000\u0001\u0000\u0005\u0000\u0000\u0000\u0002\u0000\u0001\u0000\u0007\u0000\b\u0000\u0001\u0000\t\u0000\u0000\u0000/\u0000\u0001\u0000\u0001\u0000\u0000\u0000\u0005*\u0000",
      "context_before": "SourceFile\u0001\u0000\u0013AdapterManager.java\u0001\u0000\nInnerClasses\u0007\u0000&\u0001\u0000\"com/example/AdapterManager$Adapter\u0007\u0000(\u0001\u0000\u001acom/example/AdapterManager\u0001\u0000\u0007Adapter\u0001\u0000\u000eAdapterFactory\u0001\u0000\u0015AuthenticationAdapter\u0001\u0000",
      "context_after": "\u0000\u0000\u0000\u0002\u0000\n\u0000\u0000\u0000\u0006\u0000\u0001\u0000\u0000\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/AdapterManager$AuthenticationAdapterFactory.class",
      "line": 11,
      "col": 22,
      "snippet": "AuthenticationAdapterFactory\u0001\u0000\bNestHost\u0000!\u0000\u0001\u0000\u0003\u0000\u0001\u0000\u0005\u0000\u0000\u0000\u0002\u0000\u0001\u0000\u0007\u0000\b\u0000\u0001\u0000\t\u0000\u0000\u0000/\u0000\u0001\u0000\u0001\u0000\u0000\u0000\u0005*\u0000",
      "context_before": "SourceFile\u0001\u0000\u0013AdapterManager.java\u0001\u0000\nInnerClasses\u0007\u0000&\u0001\u0000\"com/example/AdapterManager$Adapter\u0007\u0000(\u0001\u0000\u001acom/example/AdapterManager\u0001\u0000\u0007Adapter\u0001\u0000\u000eAdapterFactory\u0001\u0000\u0015AuthenticationAdapter\u0001\u0000",
      "context_after": "\u0000\u0000\u0000\u0002\u0000\n\u0000\u0000\u0000\u0006\u0000\u0001\u0000\u0000\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/CommandManager$CommandFactory.class",
      "line": 1,
      "col": 47,
      "snippet": "\u0000\u0000\u00007\u0000\u0011\u0007\u0000\u0002\u0001\u0000)com/example/CommandManager$CommandFactory\u0007\u0000\u0004\u0001\u0000\u0010java/lang/Object\u0001\u0000\u0006create\u0001\u00009([Ljava/lang/Object;)Lcom/example/CommandManager$Command;\u0001\u0000",
      "context_before": "",
      "context_after": "SourceFile\u0001\u0000\u0013CommandManager.java\u0001\u0000\nInnerClasses\u0007\u0000"
    },
    {
      "path": "target/classes/com/example/CommandManager$CommandFactory.class",
      "line": 5,
      "col": 50,
      "snippet": "\u0001\u0000\u001acom/example/CommandManager\u0001\u0000\u0007Command\u0001\u0000\u000eCommandFactory\u0001\u0000\bNestHost\u0006\u0001\u0000\u0001\u0000\u0003\u0000\u0000\u0000\u0000\u0000\u0001\u0004\u0000\u0005\u0000\u0006\u0000\u0000\u0000\u0003\u0000\u0007\u0000\u0000\u0000\u0002\u0000\b\u0000\t\u0000\u0000\u0000\u0012\u0000\u0002\u0000",
      "context_before": "InnerClasses\u0007\u0000\n\u0001\u0000\"com/example/CommandManager$Command\u0007\u0000",
      "context_after": "\u0000\n\u0000\u000e\u0006\t\u0000\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/ObserverManager$ImmediateNotificationStrategy.class",
      "line": 1,
      "col": 25,
      "snippet": "\u0000\u0000\u00007\u0000*\u0007\u0000\u0002\u0001\u00009com/example/ObserverManager$ImmediateNotificationStrategy\u0007\u0000\u0004\u0001\u0000\u0010java/lang/Object\u0007\u0000\u0006\u0001\u00000com/example/ObserverManager$NotificationStrategy\u0001\u0000\u0006this$0\u0001\u0000",
      "context_before": "",
      "context_after": "Lcom/example/ObserverManager;\u0001\u0000\u0006<init>\u0001\u0000 (Lcom/example/ObserverManager;)V\u0001\u0000\u0004Code\t\u0000\u0001\u0000\n"
    },
    {
      "path": "target/classes/com/example/ObserverManager$ImmediateNotificationStrategy.class",
      "line": 1,
      "col": 62,
      "snippet": "\u0000\u0000\u00007\u0000*\u0007\u0000\u0002\u0001\u00009com/example/ObserverManager$ImmediateNotificationStrategy\u0007\u0000\u0004\u0001\u0000\u0010java/lang/Object\u0007\u0000\u0006\u0001\u00000com/example/ObserverManager$NotificationStrategy\u0001\u0000\u0006this$0\u0001\u0000",
      "context_before": "",
      "context_after": "Lcom/example/ObserverManager;\u0001\u0000\u0006<init>\u0001\u0000 (Lcom/example/ObserverManager;)V\u0001\u0000\u0004Code\t\u0000\u0001\u0000\n"
    },
    {
      "path": "target/classes/com/example/ObserverManager$ImmediateNotificationStrategy.class",
      "line": 1,
      "col": 110,
      "snippet": "\u0000\u0000\u00007\u0000*\u0007\u0000\u0002\u0001\u00009com/example/ObserverManager$ImmediateNotificationStrategy\u0007\u0000\u0004\u0001\u0000\u0010java/lang/Object\u0007\u0000\u0006\u0001\u00000com/example/ObserverManager$NotificationStrategy\u0001\u0000\u0006this$0\u0001\u0000",
      "context_before": "",
      "context_after": "Lcom/example/ObserverManager;\u0001\u0000\u0006<init>\u0001\u0000 (Lcom/example/ObserverManager;)V\u0001\u0000\u0004Code\t\u0000\u0001\u0000\n"
    },
    {
      "path": "target/classes/com/example/ObserverManager$ImmediateNotificationStrategy.class",
      "line": 1,
      "col": 138,
      "snippet": "\u0000\u0000\u00007\u0000*\u0007\u0000\u0002\u0001\u00009com/example/ObserverManager$ImmediateNotificationStrategy\u0007\u0000\u0004\u0001\u0000\u0010java/lang/Object\u0007\u0000\u0006\u0001\u00000com/example/ObserverManager$NotificationStrategy\u0001\u0000\u0006this$0\u0001\u0000",
      "context_before": "",
      "context_after": "Lcom/example/ObserverManager;\u0001\u0000\u0006<init>\u0001\u0000 (Lcom/example/ObserverManager;)V\u0001\u0000\u0004Code\t\u0000\u0001\u0000\n"
    },
    {
      "path": "target/classes/com/example/ObserverManager$ImmediateNotificationStrategy.class",
      "line": 2,
      "col": 14,
      "snippet": "Lcom/example/ObserverManager;\u0001\u0000\u0006<init>\u0001\u0000 (Lcom/example/ObserverManager;)V\u0001\u0000\u0004Code\t\u0000\u0001\u0000",
      "context_before": "\u0000\u0000\u00007\u0000*\u0007\u0000\u0002\u0001\u00009com/example/ObserverManager$ImmediateNotificationStrategy\u0007\u0000\u0004\u0001\u0000\u0010java/lang/Object\u0007\u0000\u0006\u0001\u00000com/example/ObserverManager$NotificationStrategy\u0001\u0000\u0006this$0\u0001\u0000",
      "context_after": "\n\u0000\u0007\u0000\b"
    },
    {
      "path": "target/classes/com/example/ObserverManager$ImmediateNotificationStrategy.class",
      "line": 2,
      "col": 56,
      "snippet": "Lcom/example/ObserverManager;\u0001\u0000\u0006<init>\u0001\u0000 (Lcom/example/ObserverManager;)V\u0001\u0000\u0004Code\t\u0000\u0001\u0000",
      "context_before": "\u0000\u0000\u00007\u0000*\u0007\u0000\u0002\u0001\u00009com/example/ObserverManager$ImmediateNotificationStrategy\u0007\u0000\u0004\u0001\u0000\u0010java/lang/Object\u0007\u0000\u0006\u0001\u00000com/example/ObserverManager$NotificationStrategy\u0001\u0000\u0006this$0\u0001\u0000",
      "context_after": "\n\u0000\u0007\u0000\b"
    },
    {
      "path": "target/classes/com/example/ObserverManager$ImmediateNotificationStrategy.class",
      "line": 6,
      "col": 73,
      "snippet": "\u0000\t\u0000\u0010\u0001\u0000\u0003()V\u0001\u0000\u000fLineNumberTable\u0001\u0000\u0012LocalVariableTable\u0001\u0000\u0004this\u0001\u0000;Lcom/example/ObserverManager$ImmediateNotificationStrategy;\u0001\u0000\u0006notify\u0001\u0000'(Ljava/lang/String;Ljava/lang/Object;)V",
      "context_before": "\u0000\u0007\u0000\b\n\u0000\u0003\u0000\u000f",
      "context_after": "\u0000\u0018\u0000\u001a\u0007\u0000\u0019\u0001\u0000\u001bcom/example/ObserverManager\n\u0000\u001b\u0000\u0016\u0001\u0000\u000fnotifyObservers\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/ObserverManager$ImmediateNotificationStrategy.class",
      "line": 6,
      "col": 110,
      "snippet": "\u0000\t\u0000\u0010\u0001\u0000\u0003()V\u0001\u0000\u000fLineNumberTable\u0001\u0000\u0012LocalVariableTable\u0001\u0000\u0004this\u0001\u0000;Lcom/example/ObserverManager$ImmediateNotificationStrategy;\u0001\u0000\u0006notify\u0001\u0000'(Ljava/lang/String;Ljava/lang/Object;)V",
      "context_before": "\u0000\u0007\u0000\b\n\u0000\u0003\u0000\u000f",
      "context_after": "\u0000\u0018\u0000\u001a\u0007\u0000\u0019\u0001\u0000\u001bcom/example/ObserverManager\n\u0000\u001b\u0000\u0016\u0001\u0000\u000fnotifyObservers\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/ObserverManager$ImmediateNotificationStrategy.class",
      "line": 7,
      "col": 23,
      "snippet": "\u0000\u0018\u0000\u001a\u0007\u0000\u0019\u0001\u0000\u001bcom/example/ObserverManager",
      "context_before": "\u0000\u0003\u0000\u000f\n\u0000\t\u0000\u0010\u0001\u0000\u0003()V\u0001\u0000\u000fLineNumberTable\u0001\u0000\u0012LocalVariableTable\u0001\u0000\u0004this\u0001\u0000;Lcom/example/ObserverManager$ImmediateNotificationStrategy;\u0001\u0000\u0006notify\u0001\u0000'(Ljava/lang/String;Ljava/lang/Object;)V",
      "context_after": "\u0000\u001b\u0000\u0016\u0001\u0000\u000fnotifyObservers\u0001\u0000\nsubjectName\u0001\u0000\u0012Ljava/lang/String;\u0001\u0000\u0004data\u0001\u0000\u0012Ljava/lang/Object;\u0001\u0000\u0007getName\u0001\u0000\u0014()Ljava/lang/String;\b\u0000#\u0001\u0000\timmediate\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/ObserverManager$ImmediateNotificationStrategy.class",
      "line": 8,
      "col": 14,
      "snippet": "\u0000\u001b\u0000\u0016\u0001\u0000\u000fnotifyObservers\u0001\u0000",
      "context_before": "\u0000\t\u0000\u0010\u0001\u0000\u0003()V\u0001\u0000\u000fLineNumberTable\u0001\u0000\u0012LocalVariableTable\u0001\u0000\u0004this\u0001\u0000;Lcom/example/ObserverManager$ImmediateNotificationStrategy;\u0001\u0000\u0006notify\u0001\u0000'(Ljava/lang/String;Ljava/lang/Object;)V\n\u0000\u0018\u0000\u001a\u0007\u0000\u0019\u0001\u0000\u001bcom/example/ObserverManager",
      "context_after": "subjectName\u0001\u0000\u0012Ljava/lang/String;\u0001\u0000\u0004data\u0001\u0000\u0012Ljava/lang/Object;\u0001\u0000\u0007getName\u0001\u0000\u0014()Ljava/lang/String;\b\u0000#\u0001\u0000\timmediate\u0001\u0000\nSourceFile\u0001\u0000\u0014ObserverManager.java\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/ObserverManager$ImmediateNotificationStrategy.class",
      "line": 10,
      "col": 14,
      "snippet": "SourceFile\u0001\u0000\u0014ObserverManager.java\u0001\u0000",
      "context_before": "\u0000\u001b\u0000\u0016\u0001\u0000\u000fnotifyObservers\u0001\u0000\nsubjectName\u0001\u0000\u0012Ljava/lang/String;\u0001\u0000\u0004data\u0001\u0000\u0012Ljava/lang/Object;\u0001\u0000\u0007getName\u0001\u0000\u0014()Ljava/lang/String;\b\u0000#\u0001\u0000\timmediate\u0001\u0000",
      "context_after": "InnerClasses\u0001\u0000\nImmediateNotificationStrategy\u0001\u0000\u0014NotificationStrategy\u0001\u0000\bNestHost\u0000!\u0000\u0001\u0000\u0003\u0000\u0001\u0000\u0005\u0000\u0001\u0010\u0010\u0000\u0007\u0000\b\u0000\u0000\u0000\u0003\u0000\u0001\u0000\t\u0000"
    },
    {
      "path": "target/classes/com/example/ObserverManager$ImmediateNotificationStrategy.class",
      "line": 12,
      "col": 22,
      "snippet": "ImmediateNotificationStrategy\u0001\u0000\u0014NotificationStrategy\u0001\u0000\bNestHost\u0000!\u0000\u0001\u0000\u0003\u0000\u0001\u0000\u0005\u0000\u0001\u0010\u0010\u0000\u0007\u0000\b\u0000\u0000\u0000\u0003\u0000\u0001\u0000\t\u0000",
      "context_before": "SourceFile\u0001\u0000\u0014ObserverManager.java\u0001\u0000\nInnerClasses\u0001\u0000",
      "context_after": "\u0000\u0001\u0000\n\u0000\u0000\u00004\u0000\u0002\u0000\u0002\u0000\u0000\u0000"
    },
    {
      "path": "target/classes/com/example/ObserverManager$ImmediateNotificationStrategy.class",
      "line": 12,
      "col": 45,
      "snippet": "ImmediateNotificationStrategy\u0001\u0000\u0014NotificationStrategy\u0001\u0000\bNestHost\u0000!\u0000\u0001\u0000\u0003\u0000\u0001\u0000\u0005\u0000\u0001\u0010\u0010\u0000\u0007\u0000\b\u0000\u0000\u0000\u0003\u0000\u0001\u0000\t\u0000",
      "context_before": "SourceFile\u0001\u0000\u0014ObserverManager.java\u0001\u0000\nInnerClasses\u0001\u0000",
      "context_after": "\u0000\u0001\u0000\n\u0000\u0000\u00004\u0000\u0002\u0000\u0002\u0000\u0000\u0000"
    },
    {
      "path": "target/classes/com/example/StrategyManager$LRUCacheStrategy$1.class",
      "line": 1,
      "col": 25,
      "snippet": "\u0000\u0000\u00007\u0000;\u0007\u0000\u0002\u0001\u0000.com/example/StrategyManager$LRUCacheStrategy$1\u0007\u0000\u0004\u0001\u0000\u0017java/util/LinkedHashMap\u0001\u0000\u0006this$1\u0001\u0000.Lcom/example/StrategyManager$LRUCacheStrategy;\u0001\u0000",
      "context_before": "",
      "context_after": "val$capacity\u0001\u0000\u0001I\u0001\u0000\u0006<init>\u0001\u00005(Lcom/example/StrategyManager$LRUCacheStrategy;IFZI)V\u0001\u0000\u0004Code\t\u0000\u0001\u0000\n"
    },
    {
      "path": "target/classes/com/example/StrategyManager$LRUCacheStrategy$1.class",
      "line": 1,
      "col": 49,
      "snippet": "\u0000\u0000\u00007\u0000;\u0007\u0000\u0002\u0001\u0000.com/example/StrategyManager$LRUCacheStrategy$1\u0007\u0000\u0004\u0001\u0000\u0017java/util/LinkedHashMap\u0001\u0000\u0006this$1\u0001\u0000.Lcom/example/StrategyManager$LRUCacheStrategy;\u0001\u0000",
      "context_before": "",
      "context_after": "val$capacity\u0001\u0000\u0001I\u0001\u0000\u0006<init>\u0001\u00005(Lcom/example/StrategyManager$LRUCacheStrategy;IFZI)V\u0001\u0000\u0004Code\t\u0000\u0001\u0000\n"
    },
    {
      "path": "target/classes/com/example/StrategyManager$LRUCacheStrategy$1.class",
      "line": 1,
      "col": 113,
      "snippet": "\u0000\u0000\u00007\u0000;\u0007\u0000\u0002\u0001\u0000.com/example/StrategyManager$LRUCacheStrategy$1\u0007\u0000\u0004\u0001\u0000\u0017java/util/LinkedHashMap\u0001\u0000\u0006this$1\u0001\u0000.Lcom/example/StrategyManager$LRUCacheStrategy;\u0001\u0000",
      "context_before": "",
      "context_after": "val$capacity\u0001\u0000\u0001I\u0001\u0000\u0006<init>\u0001\u00005(Lcom/example/StrategyManager$LRUCacheStrategy;IFZI)V\u0001\u0000\u0004Code\t\u0000\u0001\u0000\n"
    },
    {
      "path": "target/classes/com/example/StrategyManager$LRUCacheStrategy$1.class",
      "line": 1,
      "col": 137,
      "snippet": "\u0000\u0000\u00007\u0000;\u0007\u0000\u0002\u0001\u0000.com/example/StrategyManager$LRUCacheStrategy$1\u0007\u0000\u0004\u0001\u0000\u0017java/util/LinkedHashMap\u0001\u0000\u0006this$1\u0001\u0000.Lcom/example/StrategyManager$LRUCacheStrategy;\u0001\u0000",
      "context_before": "",
      "context_after": "val$capacity\u0001\u0000\u0001I\u0001\u0000\u0006<init>\u0001\u00005(Lcom/example/StrategyManager$LRUCacheStrategy;IFZI)V\u0001\u0000\u0004Code\t\u0000\u0001\u0000\n"
    },
    {
      "path": "target/classes/com/example/StrategyManager$LRUCacheStrategy$1.class",
      "line": 2,
      "col": 43,
      "snippet": "val$capacity\u0001\u0000\u0001I\u0001\u0000\u0006<init>\u0001\u00005(Lcom/example/StrategyManager$LRUCacheStrategy;IFZI)V\u0001\u0000\u0004Code\t\u0000\u0001\u0000",
      "context_before": "\u0000\u0000\u00007\u0000;\u0007\u0000\u0002\u0001\u0000.com/example/StrategyManager$LRUCacheStrategy$1\u0007\u0000\u0004\u0001\u0000\u0017java/util/LinkedHashMap\u0001\u0000\u0006this$1\u0001\u0000.Lcom/example/StrategyManager$LRUCacheStrategy;\u0001\u0000",
      "context_after": "\n\u0000\u0005\u0000\u0006\t\u0000\u0001\u0000\u000f"
    },
    {
      "path": "target/classes/com/example/StrategyManager$LRUCacheStrategy$1.class",
      "line": 2,
      "col": 67,
      "snippet": "val$capacity\u0001\u0000\u0001I\u0001\u0000\u0006<init>\u0001\u00005(Lcom/example/StrategyManager$LRUCacheStrategy;IFZI)V\u0001\u0000\u0004Code\t\u0000\u0001\u0000",
      "context_before": "\u0000\u0000\u00007\u0000;\u0007\u0000\u0002\u0001\u0000.com/example/StrategyManager$LRUCacheStrategy$1\u0007\u0000\u0004\u0001\u0000\u0017java/util/LinkedHashMap\u0001\u0000\u0006this$1\u0001\u0000.Lcom/example/StrategyManager$LRUCacheStrategy;\u0001\u0000",
      "context_after": "\n\u0000\u0005\u0000\u0006\t\u0000\u0001\u0000\u000f"
    },
    {
      "path": "target/classes/com/example/StrategyManager$LRUCacheStrategy$1.class",
      "line": 7,
      "col": 76,
      "snippet": "\u0000\t\u0000\u0012\u0001\u0000\u0006(IFZ)V\u0001\u0000\u000fLineNumberTable\u0001\u0000\u0012LocalVariableTable\u0001\u0000\u0004this\u0001\u00000Lcom/example/StrategyManager$LRUCacheStrategy$1;\u0001\u0000",
      "context_before": "\u0000\u0007\u0000\b\n\u0000\u0003\u0000\u0011",
      "context_after": "$anonymous0\u0001\u0000\n$anonymous1\u0001\u0000\u0001F\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/StrategyManager$LRUCacheStrategy$1.class",
      "line": 7,
      "col": 100,
      "snippet": "\u0000\t\u0000\u0012\u0001\u0000\u0006(IFZ)V\u0001\u0000\u000fLineNumberTable\u0001\u0000\u0012LocalVariableTable\u0001\u0000\u0004this\u0001\u00000Lcom/example/StrategyManager$LRUCacheStrategy$1;\u0001\u0000",
      "context_before": "\u0000\u0007\u0000\b\n\u0000\u0003\u0000\u0011",
      "context_after": "$anonymous0\u0001\u0000\n$anonymous1\u0001\u0000\u0001F\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/StrategyManager$LRUCacheStrategy$1.class",
      "line": 14,
      "col": 14,
      "snippet": "SourceFile\u0001\u0000\u0014StrategyManager.java\u0001\u0000?Ljava/util/LinkedHashMap<Ljava/lang/Object;Ljava/lang/Object;>;\u0001\u0000\u000fEnclosingMethod\u0007\u0000.\u0001\u0000,com/example/StrategyManager$LRUCacheStrategy",
      "context_before": "\u0000\"\u0000#\u0001\u0000\u0004size\u0001\u0000\u0003()I\u0001\u0000\u0006eldest\u0001\u0000\u0015Ljava/util/Map$Entry;\u0001\u0000\u0016LocalVariableTypeTable\u0001\u0000;Ljava/util/Map$Entry<Ljava/lang/Object;Ljava/lang/Object;>;\u0001\u0000\nStackMapTable\u0001\u0000",
      "context_after": "\u0000\t\u00000\u0001\u0000\u0004(I)V\u0001\u0000\nInnerClasses\u0007\u00003\u0001\u0000\u001bcom/example/StrategyManager\u0001\u0000\u0010LRUCacheStrategy\u0007\u00006\u0001\u0000\u0013java/util/Map$Entry\u0007\u00008\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/StrategyManager$LRUCacheStrategy$1.class",
      "line": 14,
      "col": 136,
      "snippet": "SourceFile\u0001\u0000\u0014StrategyManager.java\u0001\u0000?Ljava/util/LinkedHashMap<Ljava/lang/Object;Ljava/lang/Object;>;\u0001\u0000\u000fEnclosingMethod\u0007\u0000.\u0001\u0000,com/example/StrategyManager$LRUCacheStrategy",
      "context_before": "\u0000\"\u0000#\u0001\u0000\u0004size\u0001\u0000\u0003()I\u0001\u0000\u0006eldest\u0001\u0000\u0015Ljava/util/Map$Entry;\u0001\u0000\u0016LocalVariableTypeTable\u0001\u0000;Ljava/util/Map$Entry<Ljava/lang/Object;Ljava/lang/Object;>;\u0001\u0000\nStackMapTable\u0001\u0000",
      "context_after": "\u0000\t\u00000\u0001\u0000\u0004(I)V\u0001\u0000\nInnerClasses\u0007\u00003\u0001\u0000\u001bcom/example/StrategyManager\u0001\u0000\u0010LRUCacheStrategy\u0007\u00006\u0001\u0000\u0013java/util/Map$Entry\u0007\u00008\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/StrategyManager$LRUCacheStrategy$1.class",
      "line": 14,
      "col": 160,
      "snippet": "SourceFile\u0001\u0000\u0014StrategyManager.java\u0001\u0000?Ljava/util/LinkedHashMap<Ljava/lang/Object;Ljava/lang/Object;>;\u0001\u0000\u000fEnclosingMethod\u0007\u0000.\u0001\u0000,com/example/StrategyManager$LRUCacheStrategy",
      "context_before": "\u0000\"\u0000#\u0001\u0000\u0004size\u0001\u0000\u0003()I\u0001\u0000\u0006eldest\u0001\u0000\u0015Ljava/util/Map$Entry;\u0001\u0000\u0016LocalVariableTypeTable\u0001\u0000;Ljava/util/Map$Entry<Ljava/lang/Object;Ljava/lang/Object;>;\u0001\u0000\nStackMapTable\u0001\u0000",
      "context_after": "\u0000\t\u00000\u0001\u0000\u0004(I)V\u0001\u0000\nInnerClasses\u0007\u00003\u0001\u0000\u001bcom/example/StrategyManager\u0001\u0000\u0010LRUCacheStrategy\u0007\u00006\u0001\u0000\u0013java/util/Map$Entry\u0007\u00008\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/StrategyManager$LRUCacheStrategy$1.class",
      "line": 16,
      "col": 31,
      "snippet": "InnerClasses\u0007\u00003\u0001\u0000\u001bcom/example/StrategyManager\u0001\u0000\u0010LRUCacheStrategy\u0007\u00006\u0001\u0000\u0013java/util/Map$Entry\u0007\u00008\u0001\u0000",
      "context_before": "SourceFile\u0001\u0000\u0014StrategyManager.java\u0001\u0000?Ljava/util/LinkedHashMap<Ljava/lang/Object;Ljava/lang/Object;>;\u0001\u0000\u000fEnclosingMethod\u0007\u0000.\u0001\u0000,com/example/StrategyManager$LRUCacheStrategy\n\u0000\t\u00000\u0001\u0000\u0004(I)V\u0001\u0000",
      "context_after": "java/util/Map\u0001\u0000\u0005Entry\u0001\u0000\bNestHost\u0000 \u0000\u0001\u0000\u0003\u0000\u0000\u0000\u0002\u0010\u0010\u0000\u0005\u0000\u0006\u0000\u0000\u0010\u0012\u0000\u0007\u0000\b\u0000\u0000\u0000\u0002\u0000\u0000\u0000\t\u0000\n\u0000\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/StrategyManager$LRUCacheStrategy$1.class",
      "line": 16,
      "col": 57,
      "snippet": "InnerClasses\u0007\u00003\u0001\u0000\u001bcom/example/StrategyManager\u0001\u0000\u0010LRUCacheStrategy\u0007\u00006\u0001\u0000\u0013java/util/Map$Entry\u0007\u00008\u0001\u0000",
      "context_before": "SourceFile\u0001\u0000\u0014StrategyManager.java\u0001\u0000?Ljava/util/LinkedHashMap<Ljava/lang/Object;Ljava/lang/Object;>;\u0001\u0000\u000fEnclosingMethod\u0007\u0000.\u0001\u0000,com/example/StrategyManager$LRUCacheStrategy\n\u0000\t\u00000\u0001\u0000\u0004(I)V\u0001\u0000",
      "context_after": "java/util/Map\u0001\u0000\u0005Entry\u0001\u0000\bNestHost\u0000 \u0000\u0001\u0000\u0003\u0000\u0000\u0000\u0002\u0010\u0010\u0000\u0005\u0000\u0006\u0000\u0000\u0010\u0012\u0000\u0007\u0000\b\u0000\u0000\u0000\u0002\u0000\u0000\u0000\t\u0000\n\u0000\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/CommandManager$NetworkReceiveCommandFactory.class",
      "line": 1,
      "col": 61,
      "snippet": "\u0000\u0000\u00007\u00002\u0007\u0000\u0002\u0001\u00007com/example/CommandManager$NetworkReceiveCommandFactory\u0007\u0000\u0004\u0001\u0000\u0010java/lang/Object\u0007\u0000\u0006\u0001\u0000)com/example/CommandManager$CommandFactory\u0001\u0000\u0006<init>\u0001\u0000\u0003()V\u0001\u0000\u0004Code",
      "context_before": "",
      "context_after": "\u0000\u0003\u0000\n"
    },
    {
      "path": "target/classes/com/example/CommandManager$NetworkReceiveCommandFactory.class",
      "line": 1,
      "col": 130,
      "snippet": "\u0000\u0000\u00007\u00002\u0007\u0000\u0002\u0001\u00007com/example/CommandManager$NetworkReceiveCommandFactory\u0007\u0000\u0004\u0001\u0000\u0010java/lang/Object\u0007\u0000\u0006\u0001\u0000)com/example/CommandManager$CommandFactory\u0001\u0000\u0006<init>\u0001\u0000\u0003()V\u0001\u0000\u0004Code",
      "context_before": "",
      "context_after": "\u0000\u0003\u0000\n"
    },
    {
      "path": "target/classes/com/example/CommandManager$NetworkReceiveCommandFactory.class",
      "line": 4,
      "col": 103,
      "snippet": "\u0000\u0007\u0000\b\u0001\u0000\u000fLineNumberTable\u0001\u0000\u0012LocalVariableTable\u0001\u0000\u0004this\u0001\u00009Lcom/example/CommandManager$NetworkReceiveCommandFactory;\u0001\u0000\u0006create\u0001\u00009([Ljava/lang/Object;)Lcom/example/CommandManager$Command;\u0007\u0000\u0013\u0001\u0000\u0010java/lang/String\u0007\u0000\u0015\u0001\u0000\u0011java/lang/Integer",
      "context_before": "\u0000\u0003\u0000\n",
      "context_after": "\u0000\u0014\u0000\u0017\n\u0000\u0018\u0000\u0019\u0001\u0000\bintValue\u0001\u0000\u0003()I\u0007\u0000\u001b\u0001\u00000com/example/CommandManager$NetworkReceiveCommand"
    },
    {
      "path": "target/classes/com/example/CommandManager$NetworkReceiveCommandFactory.class",
      "line": 15,
      "col": 105,
      "snippet": "InnerClasses\u0007\u0000*\u0001\u0000\"com/example/CommandManager$Command\u0007\u0000,\u0001\u0000\u001acom/example/CommandManager\u0001\u0000\u0007Command\u0001\u0000\u000eCommandFactory\u0001\u0000\u0015NetworkReceiveCommand\u0001\u0000",
      "context_before": "StackMapTable\u0001\u0000\nSourceFile\u0001\u0000\u0013CommandManager.java\u0001\u0000",
      "context_after": "NetworkReceiveCommandFactory\u0001\u0000\bNestHost\u0000!\u0000\u0001\u0000\u0003\u0000\u0001\u0000\u0005\u0000\u0000\u0000\u0002\u0000\u0001\u0000\u0007\u0000\b\u0000\u0001\u0000\t\u0000\u0000\u0000/\u0000\u0001\u0000\u0001\u0000\u0000\u0000\u0005*\u0000\n\u0000\u0000\u0000\u0002\u0000"
    },
    {
      "path": "target/classes/com/example/CommandManager$NetworkReceiveCommandFactory.class",
      "line": 16,
      "col": 22,
      "snippet": "NetworkReceiveCommandFactory\u0001\u0000\bNestHost\u0000!\u0000\u0001\u0000\u0003\u0000\u0001\u0000\u0005\u0000\u0000\u0000\u0002\u0000\u0001\u0000\u0007\u0000\b\u0000\u0001\u0000\t\u0000\u0000\u0000/\u0000\u0001\u0000\u0001\u0000\u0000\u0000\u0005*\u0000",
      "context_before": "SourceFile\u0001\u0000\u0013CommandManager.java\u0001\u0000\nInnerClasses\u0007\u0000*\u0001\u0000\"com/example/CommandManager$Command\u0007\u0000,\u0001\u0000\u001acom/example/CommandManager\u0001\u0000\u0007Command\u0001\u0000\u000eCommandFactory\u0001\u0000\u0015NetworkReceiveCommand\u0001\u0000",
      "context_after": "\u0000\u0000\u0000\u0002\u0000\n\u0000\u0000\u0000\u0006\u0000\u0001\u0000\u0000\u0004x\u0000"
    },
    {
      "path": "target/classes/com/example/ObserverManager.class",
      "line": 1,
      "col": 25,
      "snippet": "\u0000\u0000\u00007\u0001\u0005\u0007\u0000\u0002\u0001\u0000\u001bcom/example/ObserverManager\u0007\u0000\u0004\u0001\u0000\u0010java/lang/Object\u0001\u0000\binstance\u0001\u0000",
      "context_before": "",
      "context_after": "Lcom/example/ObserverManager;\u0001\u0000\u0004LOCK\u0001\u0000\u0012Ljava/lang/Object;\u0001\u0000\bsubjects\u0001\u0000\u000fLjava/util/Map;\u0001\u0000\tSignature\u0001\u0000HLjava/util/Map<Ljava/lang/String;Lcom/example/ObserverManager$Subject;>;\u0001\u0000\tobservers\u0001\u0000[Ljava/util/Map<Ljava/lang/String;Ljava/util/List<Lcom/example/ObserverManager$Observer;>;>;\u0001\u0000\u0014notificationExecutor\u0001\u0000&Ljava/util/concurrent/ExecutorService;\u0001\u0000\u0016notificationStrategies\u0001\u0000ULjava/util/Map<Ljava/lang/String;Lcom/example/ObserverManager$NotificationStrategy;>;\u0001\u0000\b<clinit>\u0001\u0000\u0003()V\u0001\u0000\u0004Code\n\u0000\u0003\u0000\u0017"
    },
    {
      "path": "target/classes/com/example/ObserverManager.class",
      "line": 2,
      "col": 14,
      "snippet": "Lcom/example/ObserverManager;\u0001\u0000\u0004LOCK\u0001\u0000\u0012Ljava/lang/Object;\u0001\u0000\bsubjects\u0001\u0000\u000fLjava/util/Map;\u0001\u0000\tSignature\u0001\u0000HLjava/util/Map<Ljava/lang/String;Lcom/example/ObserverManager$Subject;>;\u0001\u0000\tobservers\u0001\u0000[Ljava/util/Map<Ljava/lang/String;Ljava/util/List<Lcom/example/ObserverManager$Observer;>;>;\u0001\u0000\u0014notificationExecutor\u0001\u0000&Ljava/util/concurrent/ExecutorService;\u0001\u0000\u0016notificationStrategies\u0001\u0000ULjava/util/Map<Ljava/lang/String;Lcom/example/ObserverManager$NotificationStrategy;>;\u0001\u0000\b<clinit>\u0001\u0000\u0003()V\u0001\u0000\u0004Code",
      "context_before": "\u0000\u0000\u00007\u0001\u0005\u0007\u0000\u0002\u0001\u0000\u001bcom/example/ObserverManager\u0007\u0000\u0004\u0001\u0000\u0010java/lang/Object\u0001\u0000\binstance\u0001\u0000",
      "context_after": "\u0000\u0003\u0000\u0017\n\u0000\u0018\u0000\u0014\u0001\u0000\u0006<init>\t\u0000\u0001\u0000\u001a"
    },
    {
      "path": "target/classes/com/example/ObserverManager.class",
      "line": 2,
      "col": 148,
      "snippet": "Lcom/example/ObserverManager;\u0001\u0000\u0004LOCK\u0001\u0000\u0012Ljava/lang/Object;\u0001\u0000\bsubjects\u0001\u0000\u000fLjava/util/Map;\u0001\u0000\tSignature\u0001\u0000HLjava/util/Map<Ljava/lang/String;Lcom/example/ObserverManager$Subject;>;\u0001\u0000\tobservers\u0001\u0000[Ljava/util/Map<Ljava/lang/String;Ljava/util/List<Lcom/example/ObserverManager$Observer;>;>;\u0001\u0000\u0014notificationExecutor\u0001\u0000&Ljava/util/concurrent/ExecutorService;\u0001\u0000\u0016notificationStrategies\u0001\u0000ULjava/util/Map<Ljava/lang/String;Lcom/example/ObserverManager$NotificationStrategy;>;\u0001\u0000\b<clinit>\u0001\u0000\u0003()V\u0001\u0000\u0004Code",
      "context_before": "\u0000\u0000\u00007\u0001\u0005\u0007\u0000\u0002\u0001\u0000\u001bcom/example/ObserverManager\u0007\u0000\u0004\u0001\u0000\u0010java/lang/Object\u0001\u0000\binstance\u0001\u0000",
      "context_after": "\u0000\u0003\u0000\u0017\n\u0000\u0018\u0000\u0014\u0001\u0000\u0006<init>\t\u0000\u0001\u0000\u001a"
    },
    {
      "path": "target/classes/com/example/ObserverManager.class",
      "line": 2,
      "col": 251,
      "snippet": "Lcom/example/ObserverManager;\u0001\u0000\u0004LOCK\u0001\u0000\u0012Ljava/lang/Object;\u0001\u0000\bsubjects\u0001\u0000\u000fLjava/util/Map;\u0001\u0000\tSignature\u0001\u0000HLjava/util/Map<Ljava/lang/String;Lcom/example/ObserverManager$Subject;>;\u0001\u0000\tobservers\u0001\u0000[Ljava/util/Map<Ljava/lang/String;Ljava/util/List<Lcom/example/ObserverManager$Observer;>;>;\u0001\u0000\u0014notificationExecutor\u0001\u0000&Ljava/util/concurrent/ExecutorService;\u0001\u0000\u0016notificationStrategies\u0001\u0000ULjava/util/Map<Ljava/lang/String;Lcom/example/ObserverManager$NotificationStrategy;>;\u0001\u0000\b<clinit>\u0001\u0000\u0003()V\u0001\u0000\u0004Code",
      "context_before": "\u0000\u0000\u00007\u0001\u0005\u0007\u0000\u0002\u0001\u0000\u001bcom/example/ObserverManager\u0007\u0000\u0004\u0001\u0000\u0010java/lang/Object\u0001\u0000\binstance\u0001\u0000",
      "context_after": "\u0000\u0003\u0000\u0017\n\u0000\u0018\u0000\u0014\u0001\u0000\u0006<init>\t\u0000\u0001\u0000\u001a"
    },
    {
      "path": "target/classes/com/example/ObserverManager.class",
      "line": 2,
      "col": 267,
      "snippet": "Lcom/example/ObserverManager;\u0001\u0000\u0004LOCK\u0001\u0000\u0012Ljava/lang/Object;\u0001\u0000\bsubjects\u0001\u0000\u000fLjava/util/Map;\u0001\u0000\tSignature\u0001\u0000HLjava/util/Map<Ljava/lang/String;Lcom/example/ObserverManager$Subject;>;\u0001\u0000\tobservers\u0001\u0000[Ljava/util/Map<Ljava/lang/String;Ljava/util/List<Lcom/example/ObserverManager$Observer;>;>;\u0001\u0000\u0014notificationExecutor\u0001\u0000&Ljava/util/concurrent/ExecutorService;\u0001\u0000\u0016notificationStrategies\u0001\u0000ULjava/util/Map<Ljava/lang/String;Lcom/example/ObserverManager$NotificationStrategy;>;\u0001\u0000\b<clinit>\u0001\u0000\u0003()V\u0001\u0000\u0004Code",
      "context_before": "\u0000\u0000\u00007\u0001\u0005\u0007\u0000\u0002\u0001\u0000\u001bcom/example/ObserverManager\u0007\u0000\u0004\u0001\u0000\u0010java/lang/Object\u0001\u0000\binstance\u0001\u0000",
      "context_after": "\u0000\u0003\u0000\u0017\n\u0000\u0018\u0000\u0014\u0001\u0000\u0006<init>\t\u0000\u0001\u0000\u001a"
    },
    {
      "path": "target/classes/com/example/ObserverManager.class",
      "line": 2,
      "col": 418,
      "snippet": "Lcom/example/ObserverManager;\u0001\u0000\u0004LOCK\u0001\u0000\u0012Ljava/lang/Object;\u0001\u0000\bsubjects\u0001\u0000\u000fLjava/util/Map;\u0001\u0000\tSignature\u0001\u0000HLjava/util/Map<Ljava/lang/String;Lcom/example/ObserverManager$Subject;>;\u0001\u0000\tobservers\u0001\u0000[Ljava/util/Map<Ljava/lang/String;Ljava/util/List<Lcom/example/ObserverManager$Observer;>;>;\u0001\u0000\u0014notificationExecutor\u0001\u0000&Ljava/util/concurrent/ExecutorService;\u0001\u0000\u0016notificationStrategies\u0001\u0000ULjava/util/Map<Ljava/lang/String;Lcom/example/ObserverManager$NotificationStrategy;>;\u0001\u0000\b<clinit>\u0001\u0000\u0003()V\u0001\u0000\u0004Code",
      "context_before": "\u0000\u0000\u00007\u0001\u0005\u0007\u0000\u0002\u0001\u0000\u001bcom/example/ObserverManager\u0007\u0000\u0004\u0001\u0000\u0010java/lang/Object\u0001\u0000\binstance\u0001\u0000",
      "context_after": "\u0000\u0003\u0000\u0017\n\u0000\u0018\u0000\u0014\u0001\u0000\u0006<init>\t\u0000\u0001\u0000\u001a"
    },
    {
      "path": "target/classes/com/example/ObserverManager.class",
      "line": 2,
      "col": 446,
      "snippet": "Lcom/example/ObserverManager;\u0001\u0000\u0004LOCK\u0001\u0000\u0012Ljava/lang/Object;\u0001\u0000\bsubjects\u0001\u0000\u000fLjava/util/Map;\u0001\u0000\tSignature\u0001\u0000HLjava/util/Map<Ljava/lang/String;Lcom/example/ObserverManager$Subject;>;\u0001\u0000\tobservers\u0001\u0000[Ljava/util/Map<Ljava/lang/String;Ljava/util/List<Lcom/example/ObserverManager$Observer;>;>;\u0001\u0000\u0014notificationExecutor\u0001\u0000&Ljava/util/concurrent/ExecutorService;\u0001\u0000\u0016notificationStrategies\u0001\u0000ULjava/util/Map<Ljava/lang/String;Lcom/example/ObserverManager$NotificationStrategy;>;\u0001\u0000\b<clinit>\u0001\u0000\u0003()V\u0001\u0000\u0004Code",
      "context_before": "\u0000\u0000\u00007\u0001\u0005\u0007\u0000\u0002\u0001\u0000\u001bcom/example/ObserverManager\u0007\u0000\u0004\u0001\u0000\u0010java/lang/Object\u0001\u0000\binstance\u0001\u0000",
      "context_after": "\u0000\u0003\u0000\u0017\n\u0000\u0018\u0000\u0014\u0001\u0000\u0006<init>\t\u0000\u0001\u0000\u001a"
    },
    {
      "path": "target/classes/com/example/ObserverManager.class",
      "line": 24,
      "col": 30,
      "snippet": "getInstance\u0001\u0000\u001f()Lcom/example/ObserverManager;\t\u0000\u0001\u00008",
      "context_before": "\u0000\u0001\u00002\n\u00003\u0000\u0014\u0001\u0000 initializeNotificationStrategies\u0001\u0000\u0004this\u0001\u0000",
      "context_after": "\u0000\u0005\u0000\u0006\n\u0000\u0001\u0000\u0017\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/ObserverManager.class",
      "line": 31,
      "col": 50,
      "snippet": "createSubject\u0001\u00009(Ljava/lang/String;)Lcom/example/ObserverManager$Subject;\b\u0000D\u0001\u0000",
      "context_before": "\u0000\u0001\u0000@\n\u0000A\u0000B\u0001\u0000",
      "context_after": "user_logout\b\u0000F\u0001\u0000\u0011user_registration\b\u0000H\u0001\u0000\u0013user_profile_update\b\u0000J\u0001\u0000\u000esystem_startup\b\u0000L\u0001\u0000\u000fsystem_shutdown\b\u0000N\u0001\u0000\nsystem_error\b\u0000P\u0001\u0000\u0012system_maintenance\b\u0000R\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/ObserverManager.class",
      "line": 40,
      "col": 66,
      "snippet": "health_check\b\u0000h\u0001\u0000\u000eresource_usage\b\u0000j\u0001\u0000\timmediate\u0007\u0000l\u0001\u00009com/example/ObserverManager$ImmediateNotificationStrategy",
      "context_before": "order_created\b\u0000\\\u0001\u0000\u000forder_cancelled\b\u0000^\u0001\u0000\u0010payment_received\b\u0000`\u0001\u0000\ninventory_low\b\u0000b\u0001\u0000\u0011performance_alert\b\u0000d\u0001\u0000\u000esecurity_alert\b\u0000f\u0001\u0000",
      "context_after": "\u0000k\u0000n\n\u0000\u0018\u0000o\u0001\u0000 (Lcom/example/ObserverManager;)V"
    },
    {
      "path": "target/classes/com/example/ObserverManager.class",
      "line": 40,
      "col": 103,
      "snippet": "health_check\b\u0000h\u0001\u0000\u000eresource_usage\b\u0000j\u0001\u0000\timmediate\u0007\u0000l\u0001\u00009com/example/ObserverManager$ImmediateNotificationStrategy",
      "context_before": "order_created\b\u0000\\\u0001\u0000\u000forder_cancelled\b\u0000^\u0001\u0000\u0010payment_received\b\u0000`\u0001\u0000\ninventory_low\b\u0000b\u0001\u0000\u0011performance_alert\b\u0000d\u0001\u0000\u000esecurity_alert\b\u0000f\u0001\u0000",
      "context_after": "\u0000k\u0000n\n\u0000\u0018\u0000o\u0001\u0000 (Lcom/example/ObserverManager;)V"
    },
    {
      "path": "target/classes/com/example/ObserverManager.class",
      "line": 42,
      "col": 22,
      "snippet": "\u0000\u0018\u0000o\u0001\u0000 (Lcom/example/ObserverManager;)V",
      "context_before": "health_check\b\u0000h\u0001\u0000\u000eresource_usage\b\u0000j\u0001\u0000\timmediate\u0007\u0000l\u0001\u00009com/example/ObserverManager$ImmediateNotificationStrategy\n\u0000k\u0000n",
      "context_after": "\u0000\u0001\u0000q\n\u0000r\u0000s\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/ObserverManager.class",
      "line": 45,
      "col": 21,
      "snippet": "registerNotificationStrategy\u0001\u0000G(Ljava/lang/String;Lcom/example/ObserverManager$NotificationStrategy;)V\b\u0000u\u0001\u0000\u0005async\u0007\u0000w\u0001\u00005com/example/ObserverManager$AsyncNotificationStrategy",
      "context_before": "\u0000\u0001\u0000q\n\u0000r\u0000s\u0001\u0000",
      "context_after": "\u0000v\u0000n\b\u0000z\u0001\u0000\u0007batched\u0007\u0000|\u0001\u00007com/example/ObserverManager$BatchedNotificationStrategy\n\u0000{\u0000n\b\u0000\u0001\u0000\bfiltered\u0007\u0000\u0001\u00008com/example/ObserverManager$FilteredNotificationStrategy"
    },
    {
      "path": "target/classes/com/example/ObserverManager.class",
      "line": 45,
      "col": 64,
      "snippet": "registerNotificationStrategy\u0001\u0000G(Ljava/lang/String;Lcom/example/ObserverManager$NotificationStrategy;)V\b\u0000u\u0001\u0000\u0005async\u0007\u0000w\u0001\u00005com/example/ObserverManager$AsyncNotificationStrategy",
      "context_before": "\u0000\u0001\u0000q\n\u0000r\u0000s\u0001\u0000",
      "context_after": "\u0000v\u0000n\b\u0000z\u0001\u0000\u0007batched\u0007\u0000|\u0001\u00007com/example/ObserverManager$BatchedNotificationStrategy\n\u0000{\u0000n\b\u0000\u0001\u0000\bfiltered\u0007\u0000\u0001\u00008com/example/ObserverManager$FilteredNotificationStrategy"
    },
    {
      "path": "target/classes/com/example/ObserverManager.class",
      "line": 45,
      "col": 92,
      "snippet": "registerNotificationStrategy\u0001\u0000G(Ljava/lang/String;Lcom/example/ObserverManager$NotificationStrategy;)V\b\u0000u\u0001\u0000\u0005async\u0007\u0000w\u0001\u00005com/example/ObserverManager$AsyncNotificationStrategy",
      "context_before": "\u0000\u0001\u0000q\n\u0000r\u0000s\u0001\u0000",
      "context_after": "\u0000v\u0000n\b\u0000z\u0001\u0000\u0007batched\u0007\u0000|\u0001\u00007com/example/ObserverManager$BatchedNotificationStrategy\n\u0000{\u0000n\b\u0000\u0001\u0000\bfiltered\u0007\u0000\u0001\u00008com/example/ObserverManager$FilteredNotificationStrategy"
    },
    {
      "path": "target/classes/com/example/ObserverManager.class",
      "line": 45,
      "col": 132,
      "snippet": "registerNotificationStrategy\u0001\u0000G(Ljava/lang/String;Lcom/example/ObserverManager$NotificationStrategy;)V\b\u0000u\u0001\u0000\u0005async\u0007\u0000w\u0001\u00005com/example/ObserverManager$AsyncNotificationStrategy",
      "context_before": "\u0000\u0001\u0000q\n\u0000r\u0000s\u0001\u0000",
      "context_after": "\u0000v\u0000n\b\u0000z\u0001\u0000\u0007batched\u0007\u0000|\u0001\u00007com/example/ObserverManager$BatchedNotificationStrategy\n\u0000{\u0000n\b\u0000\u0001\u0000\bfiltered\u0007\u0000\u0001\u00008com/example/ObserverManager$FilteredNotificationStrategy"
    },
    {
      "path": "target/classes/com/example/ObserverManager.class",
      "line": 45,
      "col": 165,
      "snippet": "registerNotificationStrategy\u0001\u0000G(Ljava/lang/String;Lcom/example/ObserverManager$NotificationStrategy;)V\b\u0000u\u0001\u0000\u0005async\u0007\u0000w\u0001\u00005com/example/ObserverManager$AsyncNotificationStrategy",
      "context_before": "\u0000\u0001\u0000q\n\u0000r\u0000s\u0001\u0000",
      "context_after": "\u0000v\u0000n\b\u0000z\u0001\u0000\u0007batched\u0007\u0000|\u0001\u00007com/example/ObserverManager$BatchedNotificationStrategy\n\u0000{\u0000n\b\u0000\u0001\u0000\bfiltered\u0007\u0000\u0001\u00008com/example/ObserverManager$FilteredNotificationStrategy"
    },
    {
      "path": "target/classes/com/example/ObserverManager.class",
      "line": 46,
      "col": 36,
      "snippet": "\u0000v\u0000n\b\u0000z\u0001\u0000\u0007batched\u0007\u0000|\u0001\u00007com/example/ObserverManager$BatchedNotificationStrategy",
      "context_before": "\u0000r\u0000s\u0001\u0000\nregisterNotificationStrategy\u0001\u0000G(Ljava/lang/String;Lcom/example/ObserverManager$NotificationStrategy;)V\b\u0000u\u0001\u0000\u0005async\u0007\u0000w\u0001\u00005com/example/ObserverManager$AsyncNotificationStrategy",
      "context_after": "\u0000{\u0000n\b\u0000\u0001\u0000\bfiltered\u0007\u0000\u0001\u00008com/example/ObserverManager$FilteredNotificationStrategy\n\u0000\u0000n\b\u0000\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/ObserverManager.class",
      "line": 46,
      "col": 71,
      "snippet": "\u0000v\u0000n\b\u0000z\u0001\u0000\u0007batched\u0007\u0000|\u0001\u00007com/example/ObserverManager$BatchedNotificationStrategy",
      "context_before": "\u0000r\u0000s\u0001\u0000\nregisterNotificationStrategy\u0001\u0000G(Ljava/lang/String;Lcom/example/ObserverManager$NotificationStrategy;)V\b\u0000u\u0001\u0000\u0005async\u0007\u0000w\u0001\u00005com/example/ObserverManager$AsyncNotificationStrategy",
      "context_after": "\u0000{\u0000n\b\u0000\u0001\u0000\bfiltered\u0007\u0000\u0001\u00008com/example/ObserverManager$FilteredNotificationStrategy\n\u0000\u0000n\b\u0000\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/ObserverManager.class",
      "line": 47,
      "col": 36,
      "snippet": "\u0000{\u0000n\b\u0000\u0001\u0000\bfiltered\u0007\u0000\u0001\u00008com/example/ObserverManager$FilteredNotificationStrategy",
      "context_before": "registerNotificationStrategy\u0001\u0000G(Ljava/lang/String;Lcom/example/ObserverManager$NotificationStrategy;)V\b\u0000u\u0001\u0000\u0005async\u0007\u0000w\u0001\u00005com/example/ObserverManager$AsyncNotificationStrategy\n\u0000v\u0000n\b\u0000z\u0001\u0000\u0007batched\u0007\u0000|\u0001\u00007com/example/ObserverManager$BatchedNotificationStrategy",
      "context_after": "\u0000\u0000n\b\u0000\u0001\u0000\nprioritized\u0007\u0000\u0001\u0000;com/example/ObserverManager$PrioritizedNotificationStrategy"
    },
    {
      "path": "target/classes/com/example/ObserverManager.class",
      "line": 47,
      "col": 72,
      "snippet": "\u0000{\u0000n\b\u0000\u0001\u0000\bfiltered\u0007\u0000\u0001\u00008com/example/ObserverManager$FilteredNotificationStrategy",
      "context_before": "registerNotificationStrategy\u0001\u0000G(Ljava/lang/String;Lcom/example/ObserverManager$NotificationStrategy;)V\b\u0000u\u0001\u0000\u0005async\u0007\u0000w\u0001\u00005com/example/ObserverManager$AsyncNotificationStrategy\n\u0000v\u0000n\b\u0000z\u0001\u0000\u0007batched\u0007\u0000|\u0001\u00007com/example/ObserverManager$BatchedNotificationStrategy",
      "context_after": "\u0000\u0000n\b\u0000\u0001\u0000\nprioritized\u0007\u0000\u0001\u0000;com/example/ObserverManager$PrioritizedNotificationStrategy"
    },
    {
      "path": "target/classes/com/example/ObserverManager.class",
      "line": 49,
      "col": 29,
      "snippet": "prioritized\u0007\u0000\u0001\u0000;com/example/ObserverManager$PrioritizedNotificationStrategy",
      "context_before": "\u0000{\u0000n\b\u0000\u0001\u0000\bfiltered\u0007\u0000\u0001\u00008com/example/ObserverManager$FilteredNotificationStrategy\n\u0000\u0000n\b\u0000\u0001\u0000",
      "context_after": "\u0000\u0000n\u0007\u0000\u0001\u0000+com/example/ObserverManager$ConcreteSubject\n\u0000\u0000"
    },
    {
      "path": "target/classes/com/example/ObserverManager.class",
      "line": 49,
      "col": 68,
      "snippet": "prioritized\u0007\u0000\u0001\u0000;com/example/ObserverManager$PrioritizedNotificationStrategy",
      "context_before": "\u0000{\u0000n\b\u0000\u0001\u0000\bfiltered\u0007\u0000\u0001\u00008com/example/ObserverManager$FilteredNotificationStrategy\n\u0000\u0000n\b\u0000\u0001\u0000",
      "context_after": "\u0000\u0000n\u0007\u0000\u0001\u0000+com/example/ObserverManager$ConcreteSubject\n\u0000\u0000"
    },
    {
      "path": "target/classes/com/example/ObserverManager.class",
      "line": 50,
      "col": 21,
      "snippet": "\u0000\u0000n\u0007\u0000\u0001\u0000+com/example/ObserverManager$ConcreteSubject",
      "context_before": "\u0000\u0000n\b\u0000\u0001\u0000\nprioritized\u0007\u0000\u0001\u0000;com/example/ObserverManager$PrioritizedNotificationStrategy",
      "context_after": "\u0000\u0000\n\u0000\u0018\u0000\u0001\u00002(Lcom/example/ObserverManager;Ljava/lang/String;)V"
    },
    {
      "path": "target/classes/com/example/ObserverManager.class",
      "line": 52,
      "col": 21,
      "snippet": "\u0000\u0018\u0000\u0001\u00002(Lcom/example/ObserverManager;Ljava/lang/String;)V",
      "context_before": "\u0000\u0000n\u0007\u0000\u0001\u0000+com/example/ObserverManager$ConcreteSubject\n\u0000\u0000",
      "context_after": "\u0000\u0000\u0007\u0000\u0001\u0000\njava/util/Map"
    },
    {
      "path": "target/classes/com/example/ObserverManager.class",
      "line": 57,
      "col": 59,
      "snippet": "subjectName\u0001\u0000\u0012Ljava/lang/String;\u0001\u0000\u0007subject\u0001\u0000%Lcom/example/ObserverManager$Subject;\u0001\u0000",
      "context_before": "\u0000\u0000\u0001\u0000\u0003put\u0001\u00008(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;\u0007\u0000\u0001\u0000)java/util/concurrent/CopyOnWriteArrayList\n\u0000\u0000\u0017\u0001\u0000",
      "context_after": "getSubject\n\u0000\u0000"
    },
    {
      "path": "target/classes/com/example/ObserverManager.class",
      "line": 60,
      "col": 67,
      "snippet": "\u0000\u0000\u0001\u0000\u0003get\u0001\u0000&(Ljava/lang/Object;)Ljava/lang/Object;\u0007\u0000\u0001\u0000#com/example/ObserverManager$Subject\u0001\u0000\u0010registerObserver\u0001\u0000;(Ljava/lang/String;Lcom/example/ObserverManager$Observer;)V\u0007\u0000\u0001\u0000\u000ejava/util/List",
      "context_before": "getSubject\n\u0000\u0000",
      "context_after": "\u0000\u0000\n\u0000\u0000\u0001\u0000\u0003add\u0001\u0000\u0015(Ljava/lang/Object;)Z\u0001\u0000\bobserver\u0001\u0000&Lcom/example/ObserverManager$Observer;\u0001\u0000\u0010subjectObservers\u0001\u0000\u0010Ljava/util/List;\u0001\u0000\u0016LocalVariableTypeTable\u0001\u00008Ljava/util/List<Lcom/example/ObserverManager$Observer;>;\u0001\u0000\u0012unregisterObserver"
    },
    {
      "path": "target/classes/com/example/ObserverManager.class",
      "line": 60,
      "col": 101,
      "snippet": "\u0000\u0000\u0001\u0000\u0003get\u0001\u0000&(Ljava/lang/Object;)Ljava/lang/Object;\u0007\u0000\u0001\u0000#com/example/ObserverManager$Subject\u0001\u0000\u0010registerObserver\u0001\u0000;(Ljava/lang/String;Lcom/example/ObserverManager$Observer;)V\u0007\u0000\u0001\u0000\u000ejava/util/List",
      "context_before": "getSubject\n\u0000\u0000",
      "context_after": "\u0000\u0000\n\u0000\u0000\u0001\u0000\u0003add\u0001\u0000\u0015(Ljava/lang/Object;)Z\u0001\u0000\bobserver\u0001\u0000&Lcom/example/ObserverManager$Observer;\u0001\u0000\u0010subjectObservers\u0001\u0000\u0010Ljava/util/List;\u0001\u0000\u0016LocalVariableTypeTable\u0001\u00008Ljava/util/List<Lcom/example/ObserverManager$Observer;>;\u0001\u0000\u0012unregisterObserver"
    },
    {
      "path": "target/classes/com/example/ObserverManager.class",
      "line": 60,
      "col": 144,
      "snippet": "\u0000\u0000\u0001\u0000\u0003get\u0001\u0000&(Ljava/lang/Object;)Ljava/lang/Object;\u0007\u0000\u0001\u0000#com/example/ObserverManager$Subject\u0001\u0000\u0010registerObserver\u0001\u0000;(Ljava/lang/String;Lcom/example/ObserverManager$Observer;)V\u0007\u0000\u0001\u0000\u000ejava/util/List",
      "context_before": "getSubject\n\u0000\u0000",
      "context_after": "\u0000\u0000\n\u0000\u0000\u0001\u0000\u0003add\u0001\u0000\u0015(Ljava/lang/Object;)Z\u0001\u0000\bobserver\u0001\u0000&Lcom/example/ObserverManager$Observer;\u0001\u0000\u0010subjectObservers\u0001\u0000\u0010Ljava/util/List;\u0001\u0000\u0016LocalVariableTypeTable\u0001\u00008Ljava/util/List<Lcom/example/ObserverManager$Observer;>;\u0001\u0000\u0012unregisterObserver"
    },
    {
      "path": "target/classes/com/example/ObserverManager.class",
      "line": 60,
      "col": 160,
      "snippet": "\u0000\u0000\u0001\u0000\u0003get\u0001\u0000&(Ljava/lang/Object;)Ljava/lang/Object;\u0007\u0000\u0001\u0000#com/example/ObserverManager$Subject\u0001\u0000\u0010registerObserver\u0001\u0000;(Ljava/lang/String;Lcom/example/ObserverManager$Observer;)V\u0007\u0000\u0001\u0000\u000ejava/util/List",
      "context_before": "getSubject\n\u0000\u0000",
      "context_after": "\u0000\u0000\n\u0000\u0000\u0001\u0000\u0003add\u0001\u0000\u0015(Ljava/lang/Object;)Z\u0001\u0000\bobserver\u0001\u0000&Lcom/example/ObserverManager$Observer;\u0001\u0000\u0010subjectObservers\u0001\u0000\u0010Ljava/util/List;\u0001\u0000\u0016LocalVariableTypeTable\u0001\u00008Ljava/util/List<Lcom/example/ObserverManager$Observer;>;\u0001\u0000\u0012unregisterObserver"
    },
    {
      "path": "target/classes/com/example/ObserverManager.class",
      "line": 62,
      "col": 60,
      "snippet": "\u0000\u0000\u0001\u0000\u0003add\u0001\u0000\u0015(Ljava/lang/Object;)Z\u0001\u0000\bobserver\u0001\u0000&Lcom/example/ObserverManager$Observer;\u0001\u0000\u0010subjectObservers\u0001\u0000\u0010Ljava/util/List;\u0001\u0000\u0016LocalVariableTypeTable\u0001\u00008Ljava/util/List<Lcom/example/ObserverManager$Observer;>;\u0001\u0000\u0012unregisterObserver",
      "context_before": "\u0000\u0000\u0001\u0000\u0003get\u0001\u0000&(Ljava/lang/Object;)Ljava/lang/Object;\u0007\u0000\u0001\u0000#com/example/ObserverManager$Subject\u0001\u0000\u0010registerObserver\u0001\u0000;(Ljava/lang/String;Lcom/example/ObserverManager$Observer;)V\u0007\u0000\u0001\u0000\u000ejava/util/List\n\u0000\u0000",
      "context_after": "\u0000\u0000\n\u0000\u0000\u0001\u0000\u0006remove\u0001\u0000\u000fnotifyObservers\u0001\u0000'(Ljava/lang/String;Ljava/lang/Object;)V"
    },
    {
      "path": "target/classes/com/example/ObserverManager.class",
      "line": 62,
      "col": 76,
      "snippet": "\u0000\u0000\u0001\u0000\u0003add\u0001\u0000\u0015(Ljava/lang/Object;)Z\u0001\u0000\bobserver\u0001\u0000&Lcom/example/ObserverManager$Observer;\u0001\u0000\u0010subjectObservers\u0001\u0000\u0010Ljava/util/List;\u0001\u0000\u0016LocalVariableTypeTable\u0001\u00008Ljava/util/List<Lcom/example/ObserverManager$Observer;>;\u0001\u0000\u0012unregisterObserver",
      "context_before": "\u0000\u0000\u0001\u0000\u0003get\u0001\u0000&(Ljava/lang/Object;)Ljava/lang/Object;\u0007\u0000\u0001\u0000#com/example/ObserverManager$Subject\u0001\u0000\u0010registerObserver\u0001\u0000;(Ljava/lang/String;Lcom/example/ObserverManager$Observer;)V\u0007\u0000\u0001\u0000\u000ejava/util/List\n\u0000\u0000",
      "context_after": "\u0000\u0000\n\u0000\u0000\u0001\u0000\u0006remove\u0001\u0000\u000fnotifyObservers\u0001\u0000'(Ljava/lang/String;Ljava/lang/Object;)V"
    },
    {
      "path": "target/classes/com/example/ObserverManager.class",
      "line": 62,
      "col": 95,
      "snippet": "\u0000\u0000\u0001\u0000\u0003add\u0001\u0000\u0015(Ljava/lang/Object;)Z\u0001\u0000\bobserver\u0001\u0000&Lcom/example/ObserverManager$Observer;\u0001\u0000\u0010subjectObservers\u0001\u0000\u0010Ljava/util/List;\u0001\u0000\u0016LocalVariableTypeTable\u0001\u00008Ljava/util/List<Lcom/example/ObserverManager$Observer;>;\u0001\u0000\u0012unregisterObserver",
      "context_before": "\u0000\u0000\u0001\u0000\u0003get\u0001\u0000&(Ljava/lang/Object;)Ljava/lang/Object;\u0007\u0000\u0001\u0000#com/example/ObserverManager$Subject\u0001\u0000\u0010registerObserver\u0001\u0000;(Ljava/lang/String;Lcom/example/ObserverManager$Observer;)V\u0007\u0000\u0001\u0000\u000ejava/util/List\n\u0000\u0000",
      "context_after": "\u0000\u0000\n\u0000\u0000\u0001\u0000\u0006remove\u0001\u0000\u000fnotifyObservers\u0001\u0000'(Ljava/lang/String;Ljava/lang/Object;)V"
    },
    {
      "path": "target/classes/com/example/ObserverManager.class",
      "line": 62,
      "col": 180,
      "snippet": "\u0000\u0000\u0001\u0000\u0003add\u0001\u0000\u0015(Ljava/lang/Object;)Z\u0001\u0000\bobserver\u0001\u0000&Lcom/example/ObserverManager$Observer;\u0001\u0000\u0010subjectObservers\u0001\u0000\u0010Ljava/util/List;\u0001\u0000\u0016LocalVariableTypeTable\u0001\u00008Ljava/util/List<Lcom/example/ObserverManager$Observer;>;\u0001\u0000\u0012unregisterObserver",
      "context_before": "\u0000\u0000\u0001\u0000\u0003get\u0001\u0000&(Ljava/lang/Object;)Ljava/lang/Object;\u0007\u0000\u0001\u0000#com/example/ObserverManager$Subject\u0001\u0000\u0010registerObserver\u0001\u0000;(Ljava/lang/String;Lcom/example/ObserverManager$Observer;)V\u0007\u0000\u0001\u0000\u000ejava/util/List\n\u0000\u0000",
      "context_after": "\u0000\u0000\n\u0000\u0000\u0001\u0000\u0006remove\u0001\u0000\u000fnotifyObservers\u0001\u0000'(Ljava/lang/String;Ljava/lang/Object;)V"
    },
    {
      "path": "target/classes/com/example/ObserverManager.class",
      "line": 62,
      "col": 196,
      "snippet": "\u0000\u0000\u0001\u0000\u0003add\u0001\u0000\u0015(Ljava/lang/Object;)Z\u0001\u0000\bobserver\u0001\u0000&Lcom/example/ObserverManager$Observer;\u0001\u0000\u0010subjectObservers\u0001\u0000\u0010Ljava/util/List;\u0001\u0000\u0016LocalVariableTypeTable\u0001\u00008Ljava/util/List<Lcom/example/ObserverManager$Observer;>;\u0001\u0000\u0012unregisterObserver",
      "context_before": "\u0000\u0000\u0001\u0000\u0003get\u0001\u0000&(Ljava/lang/Object;)Ljava/lang/Object;\u0007\u0000\u0001\u0000#com/example/ObserverManager$Subject\u0001\u0000\u0010registerObserver\u0001\u0000;(Ljava/lang/String;Lcom/example/ObserverManager$Observer;)V\u0007\u0000\u0001\u0000\u000ejava/util/List\n\u0000\u0000",
      "context_after": "\u0000\u0000\n\u0000\u0000\u0001\u0000\u0006remove\u0001\u0000\u000fnotifyObservers\u0001\u0000'(Ljava/lang/String;Ljava/lang/Object;)V"
    },
    {
      "path": "target/classes/com/example/ObserverManager.class",
      "line": 62,
      "col": 220,
      "snippet": "\u0000\u0000\u0001\u0000\u0003add\u0001\u0000\u0015(Ljava/lang/Object;)Z\u0001\u0000\bobserver\u0001\u0000&Lcom/example/ObserverManager$Observer;\u0001\u0000\u0010subjectObservers\u0001\u0000\u0010Ljava/util/List;\u0001\u0000\u0016LocalVariableTypeTable\u0001\u00008Ljava/util/List<Lcom/example/ObserverManager$Observer;>;\u0001\u0000\u0012unregisterObserver",
      "context_before": "\u0000\u0000\u0001\u0000\u0003get\u0001\u0000&(Ljava/lang/Object;)Ljava/lang/Object;\u0007\u0000\u0001\u0000#com/example/ObserverManager$Subject\u0001\u0000\u0010registerObserver\u0001\u0000;(Ljava/lang/String;Lcom/example/ObserverManager$Observer;)V\u0007\u0000\u0001\u0000\u000ejava/util/List\n\u0000\u0000",
      "context_after": "\u0000\u0000\n\u0000\u0000\u0001\u0000\u0006remove\u0001\u0000\u000fnotifyObservers\u0001\u0000'(Ljava/lang/String;Ljava/lang/Object;)V"
    },
    {
      "path": "target/classes/com/example/ObserverManager.class",
      "line": 64,
      "col": 21,
      "snippet": "\u0000\u0000\u0001\u0000\u0006remove\u0001\u0000\u000fnotifyObservers\u0001\u0000'(Ljava/lang/String;Ljava/lang/Object;)V",
      "context_before": "\u0000\u0000\u0001\u0000\u0003add\u0001\u0000\u0015(Ljava/lang/Object;)Z\u0001\u0000\bobserver\u0001\u0000&Lcom/example/ObserverManager$Observer;\u0001\u0000\u0010subjectObservers\u0001\u0000\u0010Ljava/util/List;\u0001\u0000\u0016LocalVariableTypeTable\u0001\u00008Ljava/util/List<Lcom/example/ObserverManager$Observer;>;\u0001\u0000\u0012unregisterObserver\n\u0000\u0000",
      "context_after": "\u0000\u0000\n\u0000\u0000\u0001\u0000\u0015(Ljava/lang/Object;)V\u0001\u0000\u0004data\u0001\u0000"
    },
    {
      "path": "target/classes/com/example/ObserverManager.class",
      "line": 67,
      "col": 40,
      "snippet": "strategyName\u0001\u0000\bstrategy\u0001\u00002Lcom/example/ObserverManager$NotificationStrategy;\u0001\u0000\u0012notifyWithStrategy\u0001\u00009(Ljava/lang/String;Ljava/lang/String;Ljava/lang/Object;)V\u0007\u0000\u0001\u00000com/example/ObserverManager$NotificationStrategy",
      "context_before": "\u0000\u0000\n\u0000\u0000\u0001\u0000\u0015(Ljava/lang/Object;)V\u0001\u0000\u0004data\u0001\u0000",
      "context_after": "\u0000\u0000\n\u0000\u0000\u0001\u0000\u0006notify"
    }
  ],
  "tool_iter": 1,
  "call_index": 1
}
```

### Think Reflection
Reflection recorded: The initial search returned many results, but they are mostly from `.class` files in the `target/` directory, which are compiled binaries. I need to focus on the source code (`.java` files) to understand the implementation of these patterns. I will perform a new search specifically targeting `.java` files and then examine the relevant source files. I've seen mentions of 'Adapter', 'Decorator', 'Strategy', 'Factory', and 'Observer' in the class names. I'll also look for 'Singleton', 'Proxy', and 'Builder' which didn't immediately stand out in the binary snippets.

### Call 2
```json
{
  "tool": "text_search_tool",
  "args": {
    "query": "Factory|Singleton|Strategy|Adapter|Proxy|Observer|Builder|Decorator",
    "is_regex": true,
    "root_dir": "/home/ran/Documents/work/VectorCode/mini_code_index/test_code_index_project",
    "include_glob": "**/*.java"
  },
  "result": [
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 17,
      "col": 14,
      "snippet": "public class DecoratorManager {",
      "context_before": " * 为对象动态添加功能和行为的装饰器集合\n */",
      "context_after": "\n    // 单例模式"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 20,
      "col": 29,
      "snippet": "private static volatile DecoratorManager instance;",
      "context_before": "\n    // 单例模式",
      "context_after": "    private static final Object LOCK = new Object();\n"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 23,
      "col": 31,
      "snippet": "private final Map<String, DecoratorFactory> decoratorFactories;",
      "context_before": "    private static final Object LOCK = new Object();\n",
      "context_after": "    private final Map<String, List<Decorator<?>>> activeDecorators;\n"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 23,
      "col": 40,
      "snippet": "private final Map<String, DecoratorFactory> decoratorFactories;",
      "context_before": "    private static final Object LOCK = new Object();\n",
      "context_after": "    private final Map<String, List<Decorator<?>>> activeDecorators;\n"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 24,
      "col": 36,
      "snippet": "private final Map<String, List<Decorator<?>>> activeDecorators;",
      "context_before": "\n    private final Map<String, DecoratorFactory> decoratorFactories;",
      "context_after": "\n    private DecoratorManager() {"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 24,
      "col": 57,
      "snippet": "private final Map<String, List<Decorator<?>>> activeDecorators;",
      "context_before": "\n    private final Map<String, DecoratorFactory> decoratorFactories;",
      "context_after": "\n    private DecoratorManager() {"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 26,
      "col": 13,
      "snippet": "private DecoratorManager() {",
      "context_before": "    private final Map<String, List<Decorator<?>>> activeDecorators;\n",
      "context_after": "        this.decoratorFactories = new ConcurrentHashMap<>();\n        this.activeDecorators = new ConcurrentHashMap<>();"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 28,
      "col": 20,
      "snippet": "this.activeDecorators = new ConcurrentHashMap<>();",
      "context_before": "    private DecoratorManager() {\n        this.decoratorFactories = new ConcurrentHashMap<>();",
      "context_after": "        initializeDefaultDecorators();\n    }"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 29,
      "col": 26,
      "snippet": "initializeDefaultDecorators();",
      "context_before": "        this.decoratorFactories = new ConcurrentHashMap<>();\n        this.activeDecorators = new ConcurrentHashMap<>();",
      "context_after": "    }\n"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 32,
      "col": 19,
      "snippet": "public static DecoratorManager getInstance() {",
      "context_before": "    }\n",
      "context_after": "        if (instance == null) {\n            synchronized (LOCK) {"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 36,
      "col": 36,
      "snippet": "instance = new DecoratorManager();",
      "context_before": "            synchronized (LOCK) {\n                if (instance == null) {",
      "context_after": "                }\n            }"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 46,
      "col": 35,
      "snippet": "private void initializeDefaultDecorators() {",
      "context_before": "     * 初始化默认装饰器\n     */",
      "context_after": "        // 日志装饰器\n        registerDecorator(\"logging\", new LoggingDecoratorFactory());"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 48,
      "col": 17,
      "snippet": "registerDecorator(\"logging\", new LoggingDecoratorFactory());",
      "context_before": "    private void initializeDefaultDecorators() {\n        // 日志装饰器",
      "context_after": "\n        // 缓存装饰器"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 48,
      "col": 49,
      "snippet": "registerDecorator(\"logging\", new LoggingDecoratorFactory());",
      "context_before": "    private void initializeDefaultDecorators() {\n        // 日志装饰器",
      "context_after": "\n        // 缓存装饰器"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 48,
      "col": 58,
      "snippet": "registerDecorator(\"logging\", new LoggingDecoratorFactory());",
      "context_before": "    private void initializeDefaultDecorators() {\n        // 日志装饰器",
      "context_after": "\n        // 缓存装饰器"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 51,
      "col": 17,
      "snippet": "registerDecorator(\"caching\", new CachingDecoratorFactory());",
      "context_before": "\n        // 缓存装饰器",
      "context_after": "\n        // 验证装饰器"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 51,
      "col": 49,
      "snippet": "registerDecorator(\"caching\", new CachingDecoratorFactory());",
      "context_before": "\n        // 缓存装饰器",
      "context_after": "\n        // 验证装饰器"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 51,
      "col": 58,
      "snippet": "registerDecorator(\"caching\", new CachingDecoratorFactory());",
      "context_before": "\n        // 缓存装饰器",
      "context_after": "\n        // 验证装饰器"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 54,
      "col": 17,
      "snippet": "registerDecorator(\"validation\", new ValidationDecoratorFactory());",
      "context_before": "\n        // 验证装饰器",
      "context_after": "\n        // 性能监控装饰器"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 54,
      "col": 55,
      "snippet": "registerDecorator(\"validation\", new ValidationDecoratorFactory());",
      "context_before": "\n        // 验证装饰器",
      "context_after": "\n        // 性能监控装饰器"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 54,
      "col": 64,
      "snippet": "registerDecorator(\"validation\", new ValidationDecoratorFactory());",
      "context_before": "\n        // 验证装饰器",
      "context_after": "\n        // 性能监控装饰器"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 57,
      "col": 17,
      "snippet": "registerDecorator(\"performance\", new PerformanceDecoratorFactory());",
      "context_before": "\n        // 性能监控装饰器",
      "context_after": "\n        // 安全装饰器"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 57,
      "col": 57,
      "snippet": "registerDecorator(\"performance\", new PerformanceDecoratorFactory());",
      "context_before": "\n        // 性能监控装饰器",
      "context_after": "\n        // 安全装饰器"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 57,
      "col": 66,
      "snippet": "registerDecorator(\"performance\", new PerformanceDecoratorFactory());",
      "context_before": "\n        // 性能监控装饰器",
      "context_after": "\n        // 安全装饰器"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 60,
      "col": 17,
      "snippet": "registerDecorator(\"security\", new SecurityDecoratorFactory());",
      "context_before": "\n        // 安全装饰器",
      "context_after": "\n        // 重试装饰器"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 60,
      "col": 51,
      "snippet": "registerDecorator(\"security\", new SecurityDecoratorFactory());",
      "context_before": "\n        // 安全装饰器",
      "context_after": "\n        // 重试装饰器"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 60,
      "col": 60,
      "snippet": "registerDecorator(\"security\", new SecurityDecoratorFactory());",
      "context_before": "\n        // 安全装饰器",
      "context_after": "\n        // 重试装饰器"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 63,
      "col": 17,
      "snippet": "registerDecorator(\"retry\", new RetryDecoratorFactory());",
      "context_before": "\n        // 重试装饰器",
      "context_after": "\n        // 事务装饰器"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 63,
      "col": 45,
      "snippet": "registerDecorator(\"retry\", new RetryDecoratorFactory());",
      "context_before": "\n        // 重试装饰器",
      "context_after": "\n        // 事务装饰器"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 63,
      "col": 54,
      "snippet": "registerDecorator(\"retry\", new RetryDecoratorFactory());",
      "context_before": "\n        // 重试装饰器",
      "context_after": "\n        // 事务装饰器"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 66,
      "col": 17,
      "snippet": "registerDecorator(\"transaction\", new TransactionDecoratorFactory());",
      "context_before": "\n        // 事务装饰器",
      "context_after": "\n        // 异步装饰器"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 66,
      "col": 57,
      "snippet": "registerDecorator(\"transaction\", new TransactionDecoratorFactory());",
      "context_before": "\n        // 事务装饰器",
      "context_after": "\n        // 异步装饰器"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 66,
      "col": 66,
      "snippet": "registerDecorator(\"transaction\", new TransactionDecoratorFactory());",
      "context_before": "\n        // 事务装饰器",
      "context_after": "\n        // 异步装饰器"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 69,
      "col": 17,
      "snippet": "registerDecorator(\"async\", new AsyncDecoratorFactory());",
      "context_before": "\n        // 异步装饰器",
      "context_after": "\n        // 压缩装饰器"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 69,
      "col": 45,
      "snippet": "registerDecorator(\"async\", new AsyncDecoratorFactory());",
      "context_before": "\n        // 异步装饰器",
      "context_after": "\n        // 压缩装饰器"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 69,
      "col": 54,
      "snippet": "registerDecorator(\"async\", new AsyncDecoratorFactory());",
      "context_before": "\n        // 异步装饰器",
      "context_after": "\n        // 压缩装饰器"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 72,
      "col": 17,
      "snippet": "registerDecorator(\"compression\", new CompressionDecoratorFactory());",
      "context_before": "\n        // 压缩装饰器",
      "context_after": "\n        // 加密装饰器"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 72,
      "col": 57,
      "snippet": "registerDecorator(\"compression\", new CompressionDecoratorFactory());",
      "context_before": "\n        // 压缩装饰器",
      "context_after": "\n        // 加密装饰器"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 72,
      "col": 66,
      "snippet": "registerDecorator(\"compression\", new CompressionDecoratorFactory());",
      "context_before": "\n        // 压缩装饰器",
      "context_after": "\n        // 加密装饰器"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 75,
      "col": 17,
      "snippet": "registerDecorator(\"encryption\", new EncryptionDecoratorFactory());",
      "context_before": "\n        // 加密装饰器",
      "context_after": "    }\n"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 75,
      "col": 55,
      "snippet": "registerDecorator(\"encryption\", new EncryptionDecoratorFactory());",
      "context_before": "\n        // 加密装饰器",
      "context_after": "    }\n"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 75,
      "col": 64,
      "snippet": "registerDecorator(\"encryption\", new EncryptionDecoratorFactory());",
      "context_before": "\n        // 加密装饰器",
      "context_after": "    }\n"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 81,
      "col": 25,
      "snippet": "public void registerDecorator(String decoratorType, DecoratorFactory factory) {",
      "context_before": "     * 注册装饰器工厂\n     */",
      "context_after": "        decoratorFactories.put(decoratorType, factory);\n    }"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 81,
      "col": 57,
      "snippet": "public void registerDecorator(String decoratorType, DecoratorFactory factory) {",
      "context_before": "     * 注册装饰器工厂\n     */",
      "context_after": "        decoratorFactories.put(decoratorType, factory);\n    }"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 81,
      "col": 66,
      "snippet": "public void registerDecorator(String decoratorType, DecoratorFactory factory) {",
      "context_before": "     * 注册装饰器工厂\n     */",
      "context_after": "        decoratorFactories.put(decoratorType, factory);\n    }"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 89,
      "col": 16,
      "snippet": "public <T> Decorator<T> createDecorator(String decoratorType, Object... params) {",
      "context_before": "     */\n    @SuppressWarnings(\"unchecked\")",
      "context_after": "        DecoratorFactory factory = decoratorFactories.get(decoratorType);\n        if (factory == null) {"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 89,
      "col": 35,
      "snippet": "public <T> Decorator<T> createDecorator(String decoratorType, Object... params) {",
      "context_before": "     */\n    @SuppressWarnings(\"unchecked\")",
      "context_after": "        DecoratorFactory factory = decoratorFactories.get(decoratorType);\n        if (factory == null) {"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 90,
      "col": 9,
      "snippet": "DecoratorFactory factory = decoratorFactories.get(decoratorType);",
      "context_before": "    @SuppressWarnings(\"unchecked\")\n    public <T> Decorator<T> createDecorator(String decoratorType, Object... params) {",
      "context_after": "        if (factory == null) {\n            throw new IllegalArgumentException(\"Decorator type not found: \" + decoratorType);"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 90,
      "col": 18,
      "snippet": "DecoratorFactory factory = decoratorFactories.get(decoratorType);",
      "context_before": "    @SuppressWarnings(\"unchecked\")\n    public <T> Decorator<T> createDecorator(String decoratorType, Object... params) {",
      "context_after": "        if (factory == null) {\n            throw new IllegalArgumentException(\"Decorator type not found: \" + decoratorType);"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 92,
      "col": 49,
      "snippet": "throw new IllegalArgumentException(\"Decorator type not found: \" + decoratorType);",
      "context_before": "        DecoratorFactory factory = decoratorFactories.get(decoratorType);\n        if (factory == null) {",
      "context_after": "        }\n        return (Decorator<T>) factory.create(params);"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 94,
      "col": 17,
      "snippet": "return (Decorator<T>) factory.create(params);",
      "context_before": "            throw new IllegalArgumentException(\"Decorator type not found: \" + decoratorType);\n        }",
      "context_after": "    }\n"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 101,
      "col": 9,
      "snippet": "Decorator<T> decorator = createDecorator(decoratorType, params);",
      "context_before": "     */\n    public <T> T decorate(String decoratorType, T target, Object... params) {",
      "context_after": "        return decorator.decorate(target);\n    }"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 101,
      "col": 40,
      "snippet": "Decorator<T> decorator = createDecorator(decoratorType, params);",
      "context_before": "     */\n    public <T> T decorate(String decoratorType, T target, Object... params) {",
      "context_after": "        return decorator.decorate(target);\n    }"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 119,
      "col": 23,
      "snippet": "public <T> T applyDecoratorChain(T target, List<String> decoratorTypes,",
      "context_before": "     * 应用装饰器链\n     */",
      "context_after": "                                    List<Object[]> paramsList) {\n        T result = target;"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 133,
      "col": 17,
      "snippet": "public List<Decorator<?>> getActiveDecorators(String decoratorType) {",
      "context_before": "     * 获取活跃装饰器\n     */",
      "context_after": "        return activeDecorators.getOrDefault(decoratorType, new ArrayList<>());\n    }"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 133,
      "col": 40,
      "snippet": "public List<Decorator<?>> getActiveDecorators(String decoratorType) {",
      "context_before": "     * 获取活跃装饰器\n     */",
      "context_after": "        return activeDecorators.getOrDefault(decoratorType, new ArrayList<>());\n    }"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 134,
      "col": 22,
      "snippet": "return activeDecorators.getOrDefault(decoratorType, new ArrayList<>());",
      "context_before": "     */\n    public List<Decorator<?>> getActiveDecorators(String decoratorType) {",
      "context_after": "    }\n"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 138,
      "col": 22,
      "snippet": "public interface Decorator<T> {",
      "context_before": "\n    // 装饰器接口",
      "context_after": "        T decorate(T target);\n        String getType();"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 144,
      "col": 22,
      "snippet": "public interface DecoratorFactory {",
      "context_before": "\n    // 装饰器工厂接口",
      "context_after": "        Decorator<?> create(Object... params);\n    }"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 144,
      "col": 31,
      "snippet": "public interface DecoratorFactory {",
      "context_before": "\n    // 装饰器工厂接口",
      "context_after": "        Decorator<?> create(Object... params);\n    }"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 145,
      "col": 9,
      "snippet": "Decorator<?> create(Object... params);",
      "context_before": "    // 装饰器工厂接口\n    public interface DecoratorFactory {",
      "context_after": "    }\n"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 149,
      "col": 32,
      "snippet": "public static class LoggingDecoratorFactory implements DecoratorFactory {",
      "context_before": "\n    // 日志装饰器",
      "context_after": "        @Override\n        public Decorator<?> create(Object... params) {"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 149,
      "col": 41,
      "snippet": "public static class LoggingDecoratorFactory implements DecoratorFactory {",
      "context_before": "\n    // 日志装饰器",
      "context_after": "        @Override\n        public Decorator<?> create(Object... params) {"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 149,
      "col": 60,
      "snippet": "public static class LoggingDecoratorFactory implements DecoratorFactory {",
      "context_before": "\n    // 日志装饰器",
      "context_after": "        @Override\n        public Decorator<?> create(Object... params) {"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 149,
      "col": 69,
      "snippet": "public static class LoggingDecoratorFactory implements DecoratorFactory {",
      "context_before": "\n    // 日志装饰器",
      "context_after": "        @Override\n        public Decorator<?> create(Object... params) {"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 151,
      "col": 16,
      "snippet": "public Decorator<?> create(Object... params) {",
      "context_before": "    public static class LoggingDecoratorFactory implements DecoratorFactory {\n        @Override",
      "context_after": "            String loggerName = params.length > 0 ? (String) params[0] : \"Decorator\";\n            return new LoggingDecorator(loggerName);"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 152,
      "col": 75,
      "snippet": "String loggerName = params.length > 0 ? (String) params[0] : \"Decorator\";",
      "context_before": "        @Override\n        public Decorator<?> create(Object... params) {",
      "context_after": "            return new LoggingDecorator(loggerName);\n        }"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 153,
      "col": 31,
      "snippet": "return new LoggingDecorator(loggerName);",
      "context_before": "        public Decorator<?> create(Object... params) {\n            String loggerName = params.length > 0 ? (String) params[0] : \"Decorator\";",
      "context_after": "        }\n    }"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 157,
      "col": 32,
      "snippet": "public static class LoggingDecorator<T> implements Decorator<T> {",
      "context_before": "    }\n",
      "context_after": "        private final String loggerName;\n"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 157,
      "col": 56,
      "snippet": "public static class LoggingDecorator<T> implements Decorator<T> {",
      "context_before": "    }\n",
      "context_after": "        private final String loggerName;\n"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 160,
      "col": 23,
      "snippet": "public LoggingDecorator(String loggerName) {",
      "context_before": "        private final String loggerName;\n",
      "context_after": "            this.loggerName = loggerName;\n        }"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 189,
      "col": 32,
      "snippet": "public static class CachingDecoratorFactory implements DecoratorFactory {",
      "context_before": "\n    // 缓存装饰器",
      "context_after": "        @Override\n        public Decorator<?> create(Object... params) {"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 189,
      "col": 41,
      "snippet": "public static class CachingDecoratorFactory implements DecoratorFactory {",
      "context_before": "\n    // 缓存装饰器",
      "context_after": "        @Override\n        public Decorator<?> create(Object... params) {"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 189,
      "col": 60,
      "snippet": "public static class CachingDecoratorFactory implements DecoratorFactory {",
      "context_before": "\n    // 缓存装饰器",
      "context_after": "        @Override\n        public Decorator<?> create(Object... params) {"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 189,
      "col": 69,
      "snippet": "public static class CachingDecoratorFactory implements DecoratorFactory {",
      "context_before": "\n    // 缓存装饰器",
      "context_after": "        @Override\n        public Decorator<?> create(Object... params) {"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 191,
      "col": 16,
      "snippet": "public Decorator<?> create(Object... params) {",
      "context_before": "    public static class CachingDecoratorFactory implements DecoratorFactory {\n        @Override",
      "context_after": "            int capacity = params.length > 0 ? (Integer) params[0] : 100;\n            return new CachingDecorator(capacity);"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 193,
      "col": 31,
      "snippet": "return new CachingDecorator(capacity);",
      "context_before": "        public Decorator<?> create(Object... params) {\n            int capacity = params.length > 0 ? (Integer) params[0] : 100;",
      "context_after": "        }\n    }"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 197,
      "col": 32,
      "snippet": "public static class CachingDecorator<T> implements Decorator<T> {",
      "context_before": "    }\n",
      "context_after": "        private final Map<Object, Object> cache;\n        private final int capacity;"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 197,
      "col": 56,
      "snippet": "public static class CachingDecorator<T> implements Decorator<T> {",
      "context_before": "    }\n",
      "context_after": "        private final Map<Object, Object> cache;\n        private final int capacity;"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 201,
      "col": 23,
      "snippet": "public CachingDecorator(int capacity) {",
      "context_before": "        private final int capacity;\n",
      "context_after": "            this.capacity = capacity;\n            this.cache = new LinkedHashMap<Object, Object>(capacity, 0.75f, true) {"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 248,
      "col": 35,
      "snippet": "public static class ValidationDecoratorFactory implements DecoratorFactory {",
      "context_before": "\n    // 验证装饰器",
      "context_after": "        @Override\n        public Decorator<?> create(Object... params) {"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 248,
      "col": 44,
      "snippet": "public static class ValidationDecoratorFactory implements DecoratorFactory {",
      "context_before": "\n    // 验证装饰器",
      "context_after": "        @Override\n        public Decorator<?> create(Object... params) {"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 248,
      "col": 63,
      "snippet": "public static class ValidationDecoratorFactory implements DecoratorFactory {",
      "context_before": "\n    // 验证装饰器",
      "context_after": "        @Override\n        public Decorator<?> create(Object... params) {"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 248,
      "col": 72,
      "snippet": "public static class ValidationDecoratorFactory implements DecoratorFactory {",
      "context_before": "\n    // 验证装饰器",
      "context_after": "        @Override\n        public Decorator<?> create(Object... params) {"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 250,
      "col": 16,
      "snippet": "public Decorator<?> create(Object... params) {",
      "context_before": "    public static class ValidationDecoratorFactory implements DecoratorFactory {\n        @Override",
      "context_after": "            Predicate<Object> validator = params.length > 0 ?\n                (Predicate<Object>) params[0] : Objects::nonNull;"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 253,
      "col": 34,
      "snippet": "return new ValidationDecorator(validator);",
      "context_before": "            Predicate<Object> validator = params.length > 0 ?\n                (Predicate<Object>) params[0] : Objects::nonNull;",
      "context_after": "        }\n    }"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 257,
      "col": 35,
      "snippet": "public static class ValidationDecorator<T> implements Decorator<T> {",
      "context_before": "    }\n",
      "context_after": "        private final Predicate<Object> validator;\n"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 257,
      "col": 59,
      "snippet": "public static class ValidationDecorator<T> implements Decorator<T> {",
      "context_before": "    }\n",
      "context_after": "        private final Predicate<Object> validator;\n"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 260,
      "col": 26,
      "snippet": "public ValidationDecorator(Predicate<Object> validator) {",
      "context_before": "        private final Predicate<Object> validator;\n",
      "context_after": "            this.validator = validator;\n        }"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 289,
      "col": 36,
      "snippet": "public static class PerformanceDecoratorFactory implements DecoratorFactory {",
      "context_before": "\n    // 性能监控装饰器",
      "context_after": "        @Override\n        public Decorator<?> create(Object... params) {"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 289,
      "col": 45,
      "snippet": "public static class PerformanceDecoratorFactory implements DecoratorFactory {",
      "context_before": "\n    // 性能监控装饰器",
      "context_after": "        @Override\n        public Decorator<?> create(Object... params) {"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 289,
      "col": 64,
      "snippet": "public static class PerformanceDecoratorFactory implements DecoratorFactory {",
      "context_before": "\n    // 性能监控装饰器",
      "context_after": "        @Override\n        public Decorator<?> create(Object... params) {"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 289,
      "col": 73,
      "snippet": "public static class PerformanceDecoratorFactory implements DecoratorFactory {",
      "context_before": "\n    // 性能监控装饰器",
      "context_after": "        @Override\n        public Decorator<?> create(Object... params) {"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 291,
      "col": 16,
      "snippet": "public Decorator<?> create(Object... params) {",
      "context_before": "    public static class PerformanceDecoratorFactory implements DecoratorFactory {\n        @Override",
      "context_after": "            String metricName = params.length > 0 ? (String) params[0] : \"operation\";\n            return new PerformanceDecorator(metricName);"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 293,
      "col": 35,
      "snippet": "return new PerformanceDecorator(metricName);",
      "context_before": "        public Decorator<?> create(Object... params) {\n            String metricName = params.length > 0 ? (String) params[0] : \"operation\";",
      "context_after": "        }\n    }"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 297,
      "col": 36,
      "snippet": "public static class PerformanceDecorator<T> implements Decorator<T> {",
      "context_before": "    }\n",
      "context_after": "        private final String metricName;\n"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 297,
      "col": 60,
      "snippet": "public static class PerformanceDecorator<T> implements Decorator<T> {",
      "context_before": "    }\n",
      "context_after": "        private final String metricName;\n"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 300,
      "col": 27,
      "snippet": "public PerformanceDecorator(String metricName) {",
      "context_before": "        private final String metricName;\n",
      "context_after": "            this.metricName = metricName;\n        }"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 338,
      "col": 33,
      "snippet": "public static class SecurityDecoratorFactory implements DecoratorFactory {",
      "context_before": "\n    // 安全装饰器",
      "context_after": "        @Override\n        public Decorator<?> create(Object... params) {"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 338,
      "col": 42,
      "snippet": "public static class SecurityDecoratorFactory implements DecoratorFactory {",
      "context_before": "\n    // 安全装饰器",
      "context_after": "        @Override\n        public Decorator<?> create(Object... params) {"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 338,
      "col": 61,
      "snippet": "public static class SecurityDecoratorFactory implements DecoratorFactory {",
      "context_before": "\n    // 安全装饰器",
      "context_after": "        @Override\n        public Decorator<?> create(Object... params) {"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 338,
      "col": 70,
      "snippet": "public static class SecurityDecoratorFactory implements DecoratorFactory {",
      "context_before": "\n    // 安全装饰器",
      "context_after": "        @Override\n        public Decorator<?> create(Object... params) {"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 340,
      "col": 16,
      "snippet": "public Decorator<?> create(Object... params) {",
      "context_before": "    public static class SecurityDecoratorFactory implements DecoratorFactory {\n        @Override",
      "context_after": "            String requiredRole = params.length > 0 ? (String) params[0] : \"user\";\n            return new SecurityDecorator(requiredRole);"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 342,
      "col": 32,
      "snippet": "return new SecurityDecorator(requiredRole);",
      "context_before": "        public Decorator<?> create(Object... params) {\n            String requiredRole = params.length > 0 ? (String) params[0] : \"user\";",
      "context_after": "        }\n    }"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 346,
      "col": 33,
      "snippet": "public static class SecurityDecorator<T> implements Decorator<T> {",
      "context_before": "    }\n",
      "context_after": "        private final String requiredRole;\n"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 346,
      "col": 57,
      "snippet": "public static class SecurityDecorator<T> implements Decorator<T> {",
      "context_before": "    }\n",
      "context_after": "        private final String requiredRole;\n"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 349,
      "col": 24,
      "snippet": "public SecurityDecorator(String requiredRole) {",
      "context_before": "        private final String requiredRole;\n",
      "context_after": "            this.requiredRole = requiredRole;\n        }"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 402,
      "col": 30,
      "snippet": "public static class RetryDecoratorFactory implements DecoratorFactory {",
      "context_before": "\n    // 重试装饰器",
      "context_after": "        @Override\n        public Decorator<?> create(Object... params) {"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 402,
      "col": 39,
      "snippet": "public static class RetryDecoratorFactory implements DecoratorFactory {",
      "context_before": "\n    // 重试装饰器",
      "context_after": "        @Override\n        public Decorator<?> create(Object... params) {"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 402,
      "col": 58,
      "snippet": "public static class RetryDecoratorFactory implements DecoratorFactory {",
      "context_before": "\n    // 重试装饰器",
      "context_after": "        @Override\n        public Decorator<?> create(Object... params) {"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 402,
      "col": 67,
      "snippet": "public static class RetryDecoratorFactory implements DecoratorFactory {",
      "context_before": "\n    // 重试装饰器",
      "context_after": "        @Override\n        public Decorator<?> create(Object... params) {"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 404,
      "col": 16,
      "snippet": "public Decorator<?> create(Object... params) {",
      "context_before": "    public static class RetryDecoratorFactory implements DecoratorFactory {\n        @Override",
      "context_after": "            int maxRetries = params.length > 0 ? (Integer) params[0] : 3;\n            long delayMillis = params.length > 1 ? (Long) params[1] : 1000L;"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 407,
      "col": 29,
      "snippet": "return new RetryDecorator(maxRetries, delayMillis);",
      "context_before": "            int maxRetries = params.length > 0 ? (Integer) params[0] : 3;\n            long delayMillis = params.length > 1 ? (Long) params[1] : 1000L;",
      "context_after": "        }\n    }"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 411,
      "col": 30,
      "snippet": "public static class RetryDecorator<T> implements Decorator<T> {",
      "context_before": "    }\n",
      "context_after": "        private final int maxRetries;\n        private final long delayMillis;"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 411,
      "col": 54,
      "snippet": "public static class RetryDecorator<T> implements Decorator<T> {",
      "context_before": "    }\n",
      "context_after": "        private final int maxRetries;\n        private final long delayMillis;"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 415,
      "col": 21,
      "snippet": "public RetryDecorator(int maxRetries, long delayMillis) {",
      "context_before": "        private final long delayMillis;\n",
      "context_after": "            this.maxRetries = maxRetries;\n            this.delayMillis = delayMillis;"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 460,
      "col": 36,
      "snippet": "public static class TransactionDecoratorFactory implements DecoratorFactory {",
      "context_before": "\n    // 事务装饰器",
      "context_after": "        @Override\n        public Decorator<?> create(Object... params) {"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 460,
      "col": 45,
      "snippet": "public static class TransactionDecoratorFactory implements DecoratorFactory {",
      "context_before": "\n    // 事务装饰器",
      "context_after": "        @Override\n        public Decorator<?> create(Object... params) {"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 460,
      "col": 64,
      "snippet": "public static class TransactionDecoratorFactory implements DecoratorFactory {",
      "context_before": "\n    // 事务装饰器",
      "context_after": "        @Override\n        public Decorator<?> create(Object... params) {"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 460,
      "col": 73,
      "snippet": "public static class TransactionDecoratorFactory implements DecoratorFactory {",
      "context_before": "\n    // 事务装饰器",
      "context_after": "        @Override\n        public Decorator<?> create(Object... params) {"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 462,
      "col": 16,
      "snippet": "public Decorator<?> create(Object... params) {",
      "context_before": "    public static class TransactionDecoratorFactory implements DecoratorFactory {\n        @Override",
      "context_after": "            return new TransactionDecorator();\n        }"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 463,
      "col": 35,
      "snippet": "return new TransactionDecorator();",
      "context_before": "        @Override\n        public Decorator<?> create(Object... params) {",
      "context_after": "        }\n    }"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 467,
      "col": 36,
      "snippet": "public static class TransactionDecorator<T> implements Decorator<T> {",
      "context_before": "    }\n",
      "context_after": "        @Override\n        public T decorate(T target) {"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 467,
      "col": 60,
      "snippet": "public static class TransactionDecorator<T> implements Decorator<T> {",
      "context_before": "    }\n",
      "context_after": "        @Override\n        public T decorate(T target) {"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 498,
      "col": 30,
      "snippet": "public static class AsyncDecoratorFactory implements DecoratorFactory {",
      "context_before": "\n    // 异步装饰器",
      "context_after": "        @Override\n        public Decorator<?> create(Object... params) {"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 498,
      "col": 39,
      "snippet": "public static class AsyncDecoratorFactory implements DecoratorFactory {",
      "context_before": "\n    // 异步装饰器",
      "context_after": "        @Override\n        public Decorator<?> create(Object... params) {"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 498,
      "col": 58,
      "snippet": "public static class AsyncDecoratorFactory implements DecoratorFactory {",
      "context_before": "\n    // 异步装饰器",
      "context_after": "        @Override\n        public Decorator<?> create(Object... params) {"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 498,
      "col": 67,
      "snippet": "public static class AsyncDecoratorFactory implements DecoratorFactory {",
      "context_before": "\n    // 异步装饰器",
      "context_after": "        @Override\n        public Decorator<?> create(Object... params) {"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 500,
      "col": 16,
      "snippet": "public Decorator<?> create(Object... params) {",
      "context_before": "    public static class AsyncDecoratorFactory implements DecoratorFactory {\n        @Override",
      "context_after": "            Executor executor = params.length > 0 ?\n                (Executor) params[0] : Executors.newCachedThreadPool();"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 503,
      "col": 29,
      "snippet": "return new AsyncDecorator(executor);",
      "context_before": "            Executor executor = params.length > 0 ?\n                (Executor) params[0] : Executors.newCachedThreadPool();",
      "context_after": "        }\n    }"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 507,
      "col": 30,
      "snippet": "public static class AsyncDecorator<T> implements Decorator<T> {",
      "context_before": "    }\n",
      "context_after": "        private final Executor executor;\n"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 507,
      "col": 54,
      "snippet": "public static class AsyncDecorator<T> implements Decorator<T> {",
      "context_before": "    }\n",
      "context_after": "        private final Executor executor;\n"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 510,
      "col": 21,
      "snippet": "public AsyncDecorator(Executor executor) {",
      "context_before": "        private final Executor executor;\n",
      "context_after": "            this.executor = executor;\n        }"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 545,
      "col": 36,
      "snippet": "public static class CompressionDecoratorFactory implements DecoratorFactory {",
      "context_before": "\n    // 压缩装饰器",
      "context_after": "        @Override\n        public Decorator<?> create(Object... params) {"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 545,
      "col": 45,
      "snippet": "public static class CompressionDecoratorFactory implements DecoratorFactory {",
      "context_before": "\n    // 压缩装饰器",
      "context_after": "        @Override\n        public Decorator<?> create(Object... params) {"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 545,
      "col": 64,
      "snippet": "public static class CompressionDecoratorFactory implements DecoratorFactory {",
      "context_before": "\n    // 压缩装饰器",
      "context_after": "        @Override\n        public Decorator<?> create(Object... params) {"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 545,
      "col": 73,
      "snippet": "public static class CompressionDecoratorFactory implements DecoratorFactory {",
      "context_before": "\n    // 压缩装饰器",
      "context_after": "        @Override\n        public Decorator<?> create(Object... params) {"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 547,
      "col": 16,
      "snippet": "public Decorator<?> create(Object... params) {",
      "context_before": "    public static class CompressionDecoratorFactory implements DecoratorFactory {\n        @Override",
      "context_after": "            String algorithm = params.length > 0 ? (String) params[0] : \"gzip\";\n            return new CompressionDecorator(algorithm);"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 549,
      "col": 35,
      "snippet": "return new CompressionDecorator(algorithm);",
      "context_before": "        public Decorator<?> create(Object... params) {\n            String algorithm = params.length > 0 ? (String) params[0] : \"gzip\";",
      "context_after": "        }\n    }"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 553,
      "col": 36,
      "snippet": "public static class CompressionDecorator<T> implements Decorator<T> {",
      "context_before": "    }\n",
      "context_after": "        private final String algorithm;\n"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 553,
      "col": 60,
      "snippet": "public static class CompressionDecorator<T> implements Decorator<T> {",
      "context_before": "    }\n",
      "context_after": "        private final String algorithm;\n"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 556,
      "col": 27,
      "snippet": "public CompressionDecorator(String algorithm) {",
      "context_before": "        private final String algorithm;\n",
      "context_after": "            this.algorithm = algorithm;\n        }"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 590,
      "col": 35,
      "snippet": "public static class EncryptionDecoratorFactory implements DecoratorFactory {",
      "context_before": "\n    // 加密装饰器",
      "context_after": "        @Override\n        public Decorator<?> create(Object... params) {"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 590,
      "col": 44,
      "snippet": "public static class EncryptionDecoratorFactory implements DecoratorFactory {",
      "context_before": "\n    // 加密装饰器",
      "context_after": "        @Override\n        public Decorator<?> create(Object... params) {"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 590,
      "col": 63,
      "snippet": "public static class EncryptionDecoratorFactory implements DecoratorFactory {",
      "context_before": "\n    // 加密装饰器",
      "context_after": "        @Override\n        public Decorator<?> create(Object... params) {"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 590,
      "col": 72,
      "snippet": "public static class EncryptionDecoratorFactory implements DecoratorFactory {",
      "context_before": "\n    // 加密装饰器",
      "context_after": "        @Override\n        public Decorator<?> create(Object... params) {"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 592,
      "col": 16,
      "snippet": "public Decorator<?> create(Object... params) {",
      "context_before": "    public static class EncryptionDecoratorFactory implements DecoratorFactory {\n        @Override",
      "context_after": "            String key = params.length > 0 ? (String) params[0] : \"default_key\";\n            return new EncryptionDecorator(key);"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 594,
      "col": 34,
      "snippet": "return new EncryptionDecorator(key);",
      "context_before": "        public Decorator<?> create(Object... params) {\n            String key = params.length > 0 ? (String) params[0] : \"default_key\";",
      "context_after": "        }\n    }"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 598,
      "col": 35,
      "snippet": "public static class EncryptionDecorator<T> implements Decorator<T> {",
      "context_before": "    }\n",
      "context_after": "        private final String key;\n"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 598,
      "col": 59,
      "snippet": "public static class EncryptionDecorator<T> implements Decorator<T> {",
      "context_before": "    }\n",
      "context_after": "        private final String key;\n"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 601,
      "col": 26,
      "snippet": "public EncryptionDecorator(String key) {",
      "context_before": "        private final String key;\n",
      "context_after": "            this.key = key;\n        }"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 637,
      "col": 19,
      "snippet": "StringBuilder result = new StringBuilder();",
      "context_before": "            // 简单的凯撒密码加密（仅用于演示）\n            int shift = key.length() % 26;",
      "context_after": "            for (char c : data.toUpperCase().toCharArray()) {\n                if (Character.isLetter(c)) {"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 637,
      "col": 46,
      "snippet": "StringBuilder result = new StringBuilder();",
      "context_before": "            // 简单的凯撒密码加密（仅用于演示）\n            int shift = key.length() % 26;",
      "context_after": "            for (char c : data.toUpperCase().toCharArray()) {\n                if (Character.isLetter(c)) {"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 655,
      "col": 19,
      "snippet": "StringBuilder result = new StringBuilder();",
      "context_before": "            String data = encryptedData.substring(4);\n            int shift = key.length() % 26;",
      "context_after": "            for (char c : data.toCharArray()) {\n                if (Character.isLetter(c)) {"
    },
    {
      "path": "src/main/java/com/example/DecoratorManager.java",
      "line": 655,
      "col": 46,
      "snippet": "StringBuilder result = new StringBuilder();",
      "context_before": "            String data = encryptedData.substring(4);\n            int shift = key.length() % 26;",
      "context_after": "            for (char c : data.toCharArray()) {\n                if (Character.isLetter(c)) {"
    },
    {
      "path": "src/main/java/com/example/FactoryManager.java",
      "line": 12,
      "col": 14,
      "snippet": "public class FactoryManager {",
      "context_before": " * 负责创建各种对象和服务\n */",
      "context_after": "\n    // 单例模式实现"
    },
    {
      "path": "src/main/java/com/example/FactoryManager.java",
      "line": 15,
      "col": 29,
      "snippet": "private static volatile FactoryManager instance;",
      "context_before": "\n    // 单例模式实现",
      "context_after": "    private static final Object LOCK = new Object();\n"
    },
    {
      "path": "src/main/java/com/example/FactoryManager.java",
      "line": 18,
      "col": 37,
      "snippet": "private final Map<String, ObjectFactory<?>> factories;",
      "context_before": "    private static final Object LOCK = new Object();\n",
      "context_after": "    private final Map<String, ServiceRegistry> serviceRegistries;\n    private final Map<String, Object> singletonInstances;"
    },
    {
      "path": "src/main/java/com/example/FactoryManager.java",
      "line": 22,
      "col": 13,
      "snippet": "private FactoryManager() {",
      "context_before": "    private final Map<String, Object> singletonInstances;\n",
      "context_after": "        this.factories = new ConcurrentHashMap<>();\n        this.serviceRegistries = new ConcurrentHashMap<>();"
    },
    {
      "path": "src/main/java/com/example/FactoryManager.java",
      "line": 29,
      "col": 19,
      "snippet": "public static FactoryManager getInstance() {",
      "context_before": "    }\n",
      "context_after": "        if (instance == null) {\n            synchronized (LOCK) {"
    },
    {
      "path": "src/main/java/com/example/FactoryManager.java",
      "line": 33,
      "col": 36,
      "snippet": "instance = new FactoryManager();",
      "context_before": "            synchronized (LOCK) {\n                if (instance == null) {",
      "context_after": "                }\n            }"
    },
    {
      "path": "src/main/java/com/example/FactoryManager.java",
      "line": 45,
      "col": 17,
      "snippet": "registerFactory(\"user\", new UserFactory());",
      "context_before": "    private void initializeDefaultFactories() {\n        // 用户相关工厂",
      "context_after": "        registerFactory(\"userService\", new UserServiceFactory());\n        registerFactory(\"permissionManager\", new PermissionManagerFactory());"
    },
    {
      "path": "src/main/java/com/example/FactoryManager.java",
      "line": 45,
      "col": 41,
      "snippet": "registerFactory(\"user\", new UserFactory());",
      "context_before": "    private void initializeDefaultFactories() {\n        // 用户相关工厂",
      "context_after": "        registerFactory(\"userService\", new UserServiceFactory());\n        registerFactory(\"permissionManager\", new PermissionManagerFactory());"
    },
    {
      "path": "src/main/java/com/example/FactoryManager.java",
      "line": 46,
      "col": 17,
      "snippet": "registerFactory(\"userService\", new UserServiceFactory());",
      "context_before": "        // 用户相关工厂\n        registerFactory(\"user\", new UserFactory());",
      "context_after": "        registerFactory(\"permissionManager\", new PermissionManagerFactory());\n"
    },
    {
      "path": "src/main/java/com/example/FactoryManager.java",
      "line": 46,
      "col": 55,
      "snippet": "registerFactory(\"userService\", new UserServiceFactory());",
      "context_before": "        // 用户相关工厂\n        registerFactory(\"user\", new UserFactory());",
      "context_after": "        registerFactory(\"permissionManager\", new PermissionManagerFactory());\n"
    },
    {
      "path": "src/main/java/com/example/FactoryManager.java",
      "line": 47,
      "col": 17,
      "snippet": "registerFactory(\"permissionManager\", new PermissionManagerFactory());",
      "context_before": "        registerFactory(\"user\", new UserFactory());\n        registerFactory(\"userService\", new UserServiceFactory());",
      "context_after": "\n        // 数据处理工厂"
    },
    {
      "path": "src/main/java/com/example/FactoryManager.java",
      "line": 47,
      "col": 67,
      "snippet": "registerFactory(\"permissionManager\", new PermissionManagerFactory());",
      "context_before": "        registerFactory(\"user\", new UserFactory());\n        registerFactory(\"userService\", new UserServiceFactory());",
      "context_after": "\n        // 数据处理工厂"
    },
    {
      "path": "src/main/java/com/example/FactoryManager.java",
      "line": 50,
      "col": 17,
      "snippet": "registerFactory(\"dataProcessor\", new DataProcessorFactory());",
      "context_before": "\n        // 数据处理工厂",
      "context_after": "        registerFactory(\"reportGenerator\", new ReportGeneratorFactory());\n"
    },
    {
      "path": "src/main/java/com/example/FactoryManager.java",
      "line": 50,
      "col": 59,
      "snippet": "registerFactory(\"dataProcessor\", new DataProcessorFactory());",
      "context_before": "\n        // 数据处理工厂",
      "context_after": "        registerFactory(\"reportGenerator\", new ReportGeneratorFactory());\n"
    },
    {
      "path": "src/main/java/com/example/FactoryManager.java",
      "line": 51,
      "col": 17,
      "snippet": "registerFactory(\"reportGenerator\", new ReportGeneratorFactory());",
      "context_before": "        // 数据处理工厂\n        registerFactory(\"dataProcessor\", new DataProcessorFactory());",
      "context_after": "\n        // 工具类工厂"
    },
    {
      "path": "src/main/java/com/example/FactoryManager.java",
      "line": 51,
      "col": 63,
      "snippet": "registerFactory(\"reportGenerator\", new ReportGeneratorFactory());",
      "context_before": "        // 数据处理工厂\n        registerFactory(\"dataProcessor\", new DataProcessorFactory());",
      "context_after": "\n        // 工具类工厂"
    },
    {
      "path": "src/main/java/com/example/FactoryManager.java",
      "line": 54,
      "col": 17,
      "snippet": "registerFactory(\"auditLogger\", new AuditLoggerFactory());",
      "context_before": "\n        // 工具类工厂",
      "context_after": "        registerFactory(\"cacheManager\", new CacheManagerFactory());\n        registerFactory(\"notificationService\", new NotificationServiceFactory());"
    },
    {
      "path": "src/main/java/com/example/FactoryManager.java",
      "line": 54,
      "col": 55,
      "snippet": "registerFactory(\"auditLogger\", new AuditLoggerFactory());",
      "context_before": "\n        // 工具类工厂",
      "context_after": "        registerFactory(\"cacheManager\", new CacheManagerFactory());\n        registerFactory(\"notificationService\", new NotificationServiceFactory());"
    },
    {
      "path": "src/main/java/com/example/FactoryManager.java",
      "line": 55,
      "col": 17,
      "snippet": "registerFactory(\"cacheManager\", new CacheManagerFactory());",
      "context_before": "        // 工具类工厂\n        registerFactory(\"auditLogger\", new AuditLoggerFactory());",
      "context_after": "        registerFactory(\"notificationService\", new NotificationServiceFactory());\n"
    },
    {
      "path": "src/main/java/com/example/FactoryManager.java",
      "line": 55,
      "col": 57,
      "snippet": "registerFactory(\"cacheManager\", new CacheManagerFactory());",
      "context_before": "        // 工具类工厂\n        registerFactory(\"auditLogger\", new AuditLoggerFactory());",
      "context_after": "        registerFactory(\"notificationService\", new NotificationServiceFactory());\n"
    },
    {
      "path": "src/main/java/com/example/FactoryManager.java",
      "line": 56,
      "col": 17,
      "snippet": "registerFactory(\"notificationService\", new NotificationServiceFactory());",
      "context_before": "        registerFactory(\"auditLogger\", new AuditLoggerFactory());\n        registerFactory(\"cacheManager\", new CacheManagerFactory());",
      "context_after": "\n        // 服务注册表"
    },
    {
      "path": "src/main/java/com/example/FactoryManager.java",
      "line": 56,
      "col": 71,
      "snippet": "registerFactory(\"notificationService\", new NotificationServiceFactory());",
      "context_before": "        registerFactory(\"auditLogger\", new AuditLoggerFactory());\n        registerFactory(\"cacheManager\", new CacheManagerFactory());",
      "context_after": "\n        // 服务注册表"
    },
    {
      "path": "src/main/java/com/example/FactoryManager.java",
      "line": 67,
      "col": 29,
      "snippet": "public <T> void registerFactory(String name, ObjectFactory<T> factory) {",
      "context_before": "     * 注册工厂\n     */",
      "context_after": "        factories.put(name, factory);\n    }"
    },
    {
      "path": "src/main/java/com/example/FactoryManager.java",
      "line": 67,
      "col": 56,
      "snippet": "public <T> void registerFactory(String name, ObjectFactory<T> factory) {",
      "context_before": "     * 注册工厂\n     */",
      "context_after": "        factories.put(name, factory);\n    }"
    },
    {
      "path": "src/main/java/com/example/FactoryManager.java",
      "line": 76,
      "col": 15,
      "snippet": "ObjectFactory<T> factory = (ObjectFactory<T>) factories.get(name);",
      "context_before": "    @SuppressWarnings(\"unchecked\")\n    public <T> T create(String name, Object... args) {",
      "context_after": "        if (factory == null) {\n            throw new IllegalArgumentException(\"Factory not found: \" + name);"
    },
    {
      "path": "src/main/java/com/example/FactoryManager.java",
      "line": 76,
      "col": 43,
      "snippet": "ObjectFactory<T> factory = (ObjectFactory<T>) factories.get(name);",
      "context_before": "    @SuppressWarnings(\"unchecked\")\n    public <T> T create(String name, Object... args) {",
      "context_after": "        if (factory == null) {\n            throw new IllegalArgumentException(\"Factory not found: \" + name);"
    },
    {
      "path": "src/main/java/com/example/FactoryManager.java",
      "line": 78,
      "col": 49,
      "snippet": "throw new IllegalArgumentException(\"Factory not found: \" + name);",
      "context_before": "        ObjectFactory<T> factory = (ObjectFactory<T>) factories.get(name);\n        if (factory == null) {",
      "context_after": "        }\n        return factory.create(args);"
    },
    {
      "path": "src/main/java/com/example/FactoryManager.java",
      "line": 87,
      "col": 21,
      "snippet": "public <T> T getSingleton(String name, Object... args) {",
      "context_before": "     */\n    @SuppressWarnings(\"unchecked\")",
      "context_after": "        return (T) singletonInstances.computeIfAbsent(name, key -> create(key, args));\n    }"
    },
    {
      "path": "src/main/java/com/example/FactoryManager.java",
      "line": 121,
      "col": 28,
      "snippet": "public interface ObjectFactory<T> {",
      "context_before": "\n    // 工厂接口",
      "context_after": "        T create(Object... args);\n    }"
    },
    {
      "path": "src/main/java/com/example/FactoryManager.java",
      "line": 132,
      "col": 29,
      "snippet": "public static class UserFactory implements ObjectFactory<User> {",
      "context_before": "\n    // 具体工厂实现",
      "context_after": "        @Override\n        public User create(Object... args) {"
    },
    {
      "path": "src/main/java/com/example/FactoryManager.java",
      "line": 132,
      "col": 54,
      "snippet": "public static class UserFactory implements ObjectFactory<User> {",
      "context_before": "\n    // 具体工厂实现",
      "context_after": "        @Override\n        public User create(Object... args) {"
    },
    {
      "path": "src/main/java/com/example/FactoryManager.java",
      "line": 137,
      "col": 37,
      "snippet": "return new User.Builder()",
      "context_before": "            try {\n                if (args.length == 0) {",
      "context_after": "                        .id(\"default\")\n                        .name(\"default\")"
    },
    {
      "path": "src/main/java/com/example/FactoryManager.java",
      "line": 148,
      "col": 33,
      "snippet": "return new User.Builder()",
      "context_before": "                String email = (String) args[2];\n",
      "context_after": "                    .id(userId)\n                    .name(username)"
    },
    {
      "path": "src/main/java/com/example/FactoryManager.java",
      "line": 159,
      "col": 36,
      "snippet": "public static class UserServiceFactory implements ObjectFactory<UserService> {",
      "context_before": "    }\n",
      "context_after": "        @Override\n        public UserService create(Object... args) {"
    },
    {
      "path": "src/main/java/com/example/FactoryManager.java",
      "line": 159,
      "col": 61,
      "snippet": "public static class UserServiceFactory implements ObjectFactory<UserService> {",
      "context_before": "    }\n",
      "context_after": "        @Override\n        public UserService create(Object... args) {"
    },
    {
      "path": "src/main/java/com/example/FactoryManager.java",
      "line": 186,
      "col": 42,
      "snippet": "public static class PermissionManagerFactory implements ObjectFactory<PermissionManager> {",
      "context_before": "    }\n",
      "context_after": "        @Override\n        public PermissionManager create(Object... args) {"
    },
    {
      "path": "src/main/java/com/example/FactoryManager.java",
      "line": 186,
      "col": 67,
      "snippet": "public static class PermissionManagerFactory implements ObjectFactory<PermissionManager> {",
      "context_before": "    }\n",
      "context_after": "        @Override\n        public PermissionManager create(Object... args) {"
    },
    {
      "path": "src/main/java/com/example/FactoryManager.java",
      "line": 199,
      "col": 38,
      "snippet": "public static class DataProcessorFactory implements ObjectFactory<DataProcessor> {",
      "context_before": "    }\n",
      "context_after": "        @Override\n        public DataProcessor create(Object... args) {"
    },
    {
      "path": "src/main/java/com/example/FactoryManager.java",
      "line": 199,
      "col": 63,
      "snippet": "public static class DataProcessorFactory implements ObjectFactory<DataProcessor> {",
      "context_before": "    }\n",
      "context_after": "        @Override\n        public DataProcessor create(Object... args) {"
    },
    {
      "path": "src/main/java/com/example/FactoryManager.java",
      "line": 206,
      "col": 40,
      "snippet": "public static class ReportGeneratorFactory implements ObjectFactory<ReportGenerator> {",
      "context_before": "    }\n",
      "context_after": "        @Override\n        public ReportGenerator create(Object... args) {"
    },
    {
      "path": "src/main/java/com/example/FactoryManager.java",
      "line": 206,
      "col": 65,
      "snippet": "public static class ReportGeneratorFactory implements ObjectFactory<ReportGenerator> {",
      "context_before": "    }\n",
      "context_after": "        @Override\n        public ReportGenerator create(Object... args) {"
    },
    {
      "path": "src/main/java/com/example/FactoryManager.java",
      "line": 222,
      "col": 36,
      "snippet": "public static class AuditLoggerFactory implements ObjectFactory<AuditLogger> {",
      "context_before": "    }\n",
      "context_after": "        @Override\n        public AuditLogger create(Object... args) {"
    },
    {
      "path": "src/main/java/com/example/FactoryManager.java",
      "line": 222,
      "col": 61,
      "snippet": "public static class AuditLoggerFactory implements ObjectFactory<AuditLogger> {",
      "context_before": "    }\n",
      "context_after": "        @Override\n        public AuditLogger create(Object... args) {"
    },
    {
      "path": "src/main/java/com/example/FactoryManager.java",
      "line": 229,
      "col": 37,
      "snippet": "public static class CacheManagerFactory implements ObjectFactory<CacheManager> {",
      "context_before": "    }\n",
      "context_after": "        @Override\n        public CacheManager create(Object... args) {"
    },
    {
      "path": "src/main/java/com/example/FactoryManager.java",
      "line": 229,
      "col": 62,
      "snippet": "public static class CacheManagerFactory implements ObjectFactory<CacheManager> {",
      "context_before": "    }\n",
      "context_after": "        @Override\n        public CacheManager create(Object... args) {"
    }
  ],
  "tool_iter": 3,
  "call_index": 1
}
```

### Think Reflection
Reflection recorded: I have found several design patterns in the codebase:
- **Decorator**: `DecoratorManager.java` contains a `Decorator` interface, `DecoratorFactory` interface, and several concrete decorators (Logging, Caching, Validation, etc.). It also uses the **Singleton** pattern for `DecoratorManager`.
- **Factory**: `FactoryManager.java` contains an `ObjectFactory` interface and several concrete factories (UserFactory, UserServiceFactory, etc.). It also uses the **Singleton** pattern for `FactoryManager`.
- **Strategy**: `StrategyManager.java` (implied by the binary search, though I haven't read the source yet) likely contains strategy implementations.
- **Adapter**: `AdapterManager.java` (implied by the binary search) likely contains adapter implementations.
- **Observer**: `ObserverManager.java` (implied by the binary search) likely contains observer implementations.
- **Builder**: `User.java` (referenced in `FactoryManager.java`) uses a `Builder` pattern.
- **Singleton**: Found in `DecoratorManager.java` and `FactoryManager.java`.

I need to confirm the details for **Strategy**, **Adapter**, **Observer**, and **Proxy**. I'll also check for **Proxy** as it hasn't appeared yet. I'll read the source files for `StrategyManager.java`, `AdapterManager.java`, and `ObserverManager.java`. I'll also search for 'Proxy' specifically in `.java` files.

### Call 3
```json
{
  "tool": "text_search_tool",
  "args": {
    "root_dir": "/home/ran/Documents/work/VectorCode/mini_code_index/test_code_index_project",
    "include_glob": "**/*.java",
    "query": "Proxy"
  },
  "result": [],
  "tool_iter": 5,
  "call_index": 1
}
```

### Call 4
```json
{
  "tool": "path_glob_tool",
  "args": {
    "pattern": "src/main/java/com/example/*.java",
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
  "tool_iter": 6,
  "call_index": 1
}
```

### Call 5
```json
{
  "tool": "read_file_range_tool",
  "args": {
    "end_line": 50,
    "path": "/home/ran/Documents/work/VectorCode/mini_code_index/test_code_index_project/src/main/java/com/example/StrategyManager.java",
    "start_line": 1
  },
  "result": {
    "content": "package com.example;\n\nimport java.util.*;\nimport java.util.function.*;\nimport java.math.*;\nimport java.time.*;\nimport java.time.temporal.*;\nimport java.util.concurrent.*;\nimport java.util.stream.*;\n\n/**\n * 策略模式实现\n * 各种算法和业务逻辑的策略集合\n */\npublic class StrategyManager {\n\n    // 单例模式\n    private static volatile StrategyManager instance;\n    private static final Object LOCK = new Object();\n\n    private final Map<String, StrategyFactory> strategyFactories;\n    private final Map<String, Object> strategyCache;\n    private final Map<String, StrategySelector> selectors;\n\n    private StrategyManager() {\n        this.strategyFactories = new ConcurrentHashMap<>();\n        this.strategyCache = new ConcurrentHashMap<>();\n        this.selectors = new ConcurrentHashMap<>();\n        initializeDefaultStrategies();\n    }\n\n    public static StrategyManager getInstance() {\n        if (instance == null) {\n            synchronized (LOCK) {\n                if (instance == null) {\n                    instance = new StrategyManager();\n                }\n            }\n        }\n        return instance;\n    }\n\n    /**\n     * 初始化默认策略\n     */\n    private void initializeDefaultStrategies() {\n        // 排序策略\n        registerStrategy(\"sorting\", new SortingStrategyFactory());\n\n        // 搜索策略"
  },
  "tool_iter": 7,
  "call_index": 1
}
```