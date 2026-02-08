# mini-codeindex

一个面向本地代码库的轻量级检索与向量索引实验工程，包含：
- 检索 Agent（基于 LangGraph 的规划-检索-合成流程）
- 可配置的向量化分块策略（支持 Tree-sitter 结构化分块与文本窗口分块）

本文重点说明两件事：**检索 Agent 的设计** 与 **向量化的 chunk 策略**。

## 核心亮点

1) **检索 Agent 设计（LangGraph）**
- 采用「规划 → 子任务检索 → 子任务合成 → 全局总结」的图结构
- 子任务检索是工具调用循环，支持多工具协同
- 合成阶段将“证据日志”转为结构化结果，再汇总为最终回答
- 适用于本地代码理解、定位入口、用途总结等场景

2) **向量化分块策略（Chunking）**
- 兼容 Tree-sitter 与纯文本两条路径
- 支持多种模式：`file` / `type` / `function` / `auto_ast`
- 记录 scope、范围、分块组信息，便于检索时关联语义与结构
- 内置过滤、合并注释/空白等策略，保证 chunk 更“语义完整”

## 检索 Agent 设计

### 1. 工作流结构
主流程（高层）：
```
planner -> run_subtasks -> summarize -> END
```

子任务流程（检索循环）：
```
task_agent -> task_tools -> (task_agent | synthesize) -> verify -> (task_agent | END)
```

### 2. 子任务检索（task_agent + task_tools）
`task_agent` 负责根据子任务决定下一步工具调用，`task_tools` 执行工具并将结果写回消息/notes。  
典型职责：
- 规划：识别本子任务需要的证据
- 执行：调用工具抓取证据
- 终止：满足证据覆盖后调用 `RetrievalComplete`

### 3. 工具集合（局部检索 + 向量检索）
内置工具覆盖常见检索需求（示意）：
- 结构：`tree_summary_tool`
- 路径：`path_glob_tool`
- 内容：`text_search_tool` / `read_file_range_tool`
- 符号：`symbol_index_tool` / `find_references_tool`
- 元数据：`file_metadata_tool` / `language_stats_tool`
- 语义：`code_vector_search_tool`

### 4. 证据 → 合成 → 总结
子任务会生成一份**可追溯的证据日志**（Markdown），随后：
- `synthesize_node` 基于证据日志生成结构化子结果
- `summarize_node` 将所有子任务结果合并为最终回答
- 支持对证据进行去重、归纳、合并

### 5. 典型输出格式（引用约定）
最终回答中若引用文件/代码片段，可使用统一格式：
```
[name:path:start_line?end_line?]
```
例如：
```
[README:README.md], [UserService:src/main/java/.../UserService.java:10-55]
```

### 6. 设计精妙之处与优势

- **分层职责清晰**：规划、检索、合成、总结各自独立，易于替换/扩展模型与策略  
- **证据优先**：所有输出基于工具证据，避免“纯语言模型幻觉”  
- **可回放与可追踪**：子任务会输出完整检索日志（Markdown），便于审计与复现  
- **可插拔工具**：工具接口统一，局部检索与向量检索自然协同  
- **错误隔离与收敛**：子任务内部循环可控，逐步收敛到 `RetrievalComplete`  
- **可观测性强**：日志包含工具调用、参数、返回值、循环状态，便于定位问题  
- **零向量依赖也可运行**：完全可不建向量索引，直接从文件/目录/符号检索入手完成任务（最大卖点）  

更细节的优势：
- **合成策略两段式**：先子任务合成，再全局总结，减少信息丢失  
- **结构化证据保留**：chunk 元信息与路径/行号可直接落入引用格式  
- **支持多语言项目**：工具与 chunk 策略覆盖 Java/Python 等典型工程  
- **可扩展边界**：可增加验证节点或质量评审节点，不破坏主流程  

## 向量化分块策略（Chunking）

### 1. Chunk 配置
`chunking.Config` 支持以下核心参数：
- `chunk_size`：单块最大长度
- `overlap_ratio`：相邻块重叠比例
- `mode`：`file` / `type` / `function` / `auto_ast`
- `chunk_filters`：按语言/模式过滤
- `force_merge_trivia` / `force_merge_comments`：合并碎片

### 2. Tree-sitter 优先，文本分块兜底
- **Tree-sitter 可用**：按结构块分割（类型/函数/AST 片段）
- **Tree-sitter 不可用**：退化为文本滑窗分块（StringChunker）

### 3. 结构化元信息
每个 chunk 会附带：
- 作用域路径（scope_path）
- 包含的内部作用域（contained_scopes）
- 起止行列（start/end）
- 分组标识（group_id/group_index）

这些元信息被写入向量索引，支持按“结构语义 + 位置”检索。

#### 元数据的作用（更细节）
- **scope_path / contained_scopes**：保留“文件 → 类型 → 函数”的层级关系，帮助定位上下文语义  
- **scope_start / scope_end**：标注作用域级别的范围，用于更精确的引用/对齐  
- **start / end**：chunk 本身的精确位置（行列），便于生成可点击引用  
- **group_id / group_index**：同一作用域被切成多个 chunk 时的分组与顺序，便于回拼  
- **chunk_kind / mode**：标记 chunk 类型与分块策略（code/comment/trivia 与 file/type/function/auto_ast）  
- **symbol_names / scope_depth**：利于快速过滤目标函数/类型并加速语义检索  

### 4. 文件过滤与文本检测
索引前会执行：
- 二进制扩展过滤
- NUL 字节检测
- 编码解码探测
- 控制字符占比阈值过滤

这使得向量化只覆盖“可能是文本”的文件。

## 快速开始（示意）

1) 配置环境变量（示例）
```
PLANNER_BASE_URL=...
PLANNER_API_KEY=...
PLANNER_MODEL=...

TASK_AGENT_BASE_URL=...
TASK_AGENT_API_KEY=...
TASK_AGENT_MODEL=...

SYNTHESIZER_BASE_URL=...
SYNTHESIZER_API_KEY=...
SYNTHESIZER_MODEL=...
```

2) 运行检索图（测试入口）
```
python -m pytest tests/test_retrieval_agent_graph.py -k test_batch_questions_write_md -s
```

3) 向量化索引（示意）
```
python -c "from mini_code_index.vectorise import IndexConfig, index_directory; index_directory(IndexConfig(root_dir='YOUR_REPO'))"
```

## 从测试入手（调试与运行）

### 1) 检索 Agent 测试
`tests/test_retrieval_agent_graph.py` 会批量提问并生成结果文件：
```
python -m pytest tests/test_retrieval_agent_graph.py -k test_batch_questions_write_md -s
```
输出文件示例：
- `tests/batch_retrieval_q1.md` ~ `tests/batch_retrieval_q5.md`

### 2) 分块与索引调试（捕获 chunks）
`tests/test_indexing_smoke.py::test_index_directory_capture_chunks_to_file`  
会把 chunk 输出到 `captured_chunks.txt`，便于检查分块策略：
```
python -m pytest tests/test_indexing_smoke.py -k test_index_directory_capture_chunks_to_file -s
```

### 3) 全流程索引（真实向量服务）
`tests/test_indexing_smoke.py::test_full_pipeline_with_real_services`  
需要配置 ChromaDB 与 embedding：
```
python -m pytest tests/test_indexing_smoke.py -k test_full_pipeline_with_real_services -s
```

## 环境变量（.env.example）

建议复制 `.env.example` 并补齐以下关键配置：
- **Embedding**：`EMBEDDING_MODEL`, `EMBEDDING_DIM`, `EMBEDDING_BINDING_HOST`, `EMBEDDING_BINDING_API_KEY`
- **ChromaDB**：`CHROMADB_HOST`
- **Planner**：`PLANNER_BASE_URL`, `PLANNER_API_KEY`, `PLANNER_MODEL`
- **Task Agent**：`TASK_AGENT_BASE_URL`, `TASK_AGENT_API_KEY`, `TASK_AGENT_MODEL`
- **Synthesizer**：`SYNTHESIZER_BASE_URL`, `SYNTHESIZER_API_KEY`, `SYNTHESIZER_MODEL`
- **(可选) 查询改写**：`REWRITE_*`
- **(可选) Web 搜索**：`TAVILY_SEARCH_API_KEY`
- **(可选) 网页摘要**：`SUMMARY_*`

## 项目结构（关键目录）
- `src/mini_code_index/retrieval/`：检索 Agent 图与工具
- `src/mini_code_index/chunking.py`：分块策略
- `src/mini_code_index/indexing.py`：向量化索引入口

## License
MIT