# Processors 模块

[根目录](../../CLAUDE.md) > [packages](../) > **processors**

---

## 模块职责

Processors 模块负责对提取的数据进行后处理、清洗和转换，使其更适合 AI 应用使用。

### 核心功能

- **数据清洗**：去除噪音、规范化格式
- **文本处理**：分词、摘要、翻译
- **AI 优化**：为 LLM 准备的高质量数据
- **去重**：检测和去除重复内容
- **验证**：数据质量检查和验证
- **转换**：格式转换和标准化

## 入口和启动

### 文件结构

```
processors/
├── __init__.py            # 包入口
├── base.py                # 处理器基类
├── text_processor.py      # 文本处理
├── markdown_processor.py  # Markdown 优化
├── deduplication.py       # 去重处理
├── validator.py           # 数据验证
└── ai_processor.py        # AI 特定处理
```

### 核心类设计

```python
class BaseProcessor:
    """处理器基类"""

    async def process(self, data: ExtractResult) -> ProcessedResult:
        """处理数据的抽象方法"""

    def batch_process(self, data: List[ExtractResult]) -> List[ProcessedResult]:
        """批量处理"""
```

## 外部接口

### 文本清洗

```python
from crawl4ai.processors import TextProcessor

processor = TextProcessor(
    remove_extra_whitespace=True,
    normalize_unicode=True,
    remove_special_chars=False
)

result = await processor.process(extract_result)
print(result.cleaned_text)
```

### Markdown 优化

```python
from crawl4ai.processors import MarkdownProcessor

processor = MarkdownProcessor(
    optimize_for_llm=True,
    max_length=8000,
    preserve_structure=True
)

result = await processor.process(extract_result)
print(result.optimized_markdown)
```

### AI 数据准备

```python
from crawl4ai.processors import AIProcessor

processor = AIProcessor(
    target_model="gpt-4",
    include_metadata=True,
    format_instructions="markdown"
)

result = await processor.process(extract_result)
print(result.ai_ready_content)
```

## 关键依赖和配置

### 依赖项

- **nltk**（可选）：文本处理
- **langdetect**：语言检测
- **simhash**：去重算法
- **jsonschema**：JSON 验证

### 配置示例

```python
from crawl4ai.processors import ProcessorConfig

config = ProcessorConfig(
    # 文本处理
    min_text_length=100,
    max_text_length=100000,
    remove_duplicates=True,

    # 质量检查
    check_quality=True,
    min_quality_score=0.7,

    # AI 优化
    optimize_for_llm=True,
    chunk_size=4000,
    chunk_overlap=200
)
```

## 数据模型

### ProcessedResult

```python
class ProcessedResult(BaseModel):
    """处理结果"""

    original: ExtractResult         # 原始数据
    cleaned_text: str               # 清洗后的文本
    optimized_markdown: str         # 优化的 Markdown
    ai_ready_content: str           # AI 就绪内容
    quality_score: float            # 质量分数
    is_duplicate: bool = False      # 是否重复
    language: str = ""              # 检测的语言
    chunks: List[str] = []          # 文本分块
    processing_time: float = 0.0    # 处理耗时
```

### QualityMetrics

```python
class QualityMetrics(BaseModel):
    """数据质量指标"""

    text_length: int
    readability_score: float        # 可读性分数
    info_density: float             # 信息密度
    link_count: int
    image_count: int
    has_structure: bool             # 是否有结构
    overall_score: float            # 总体质量分数
```

## 测试和质量

### 测试结构

```
tests/unit/processors/
├── test_text_processor.py
├── test_markdown_processor.py
├── test_deduplication.py
├── test_validator.py
└── test_ai_processor.py
```

### 测试用例

- [ ] 文本清洗功能
- [ ] Unicode 规范化
- [ ] 重复内容检测
- [ ] 质量评分算法
- [ ] 语言检测准确性
- [ ] Markdown 优化
- [ ] 文本分块策略
- [ ] AI 格式转换

### 性能指标

- 文本处理速度：> 1000 docs/s
- 去重检查：< 1ms per doc
- 内存占用：< 200MB for 10000 docs

## 常见问题 (FAQ)

### Q1: 如何处理多语言内容？
**A:** 使用自动语言检测并应用相应的处理策略：
```python
processor = TextProcessor(detect_language=True)
```

### Q2: 去重算法有多准确？
**A:** 使用 SimHash 算法，可以检测 90% 以上的近似重复内容，支持自定义相似度阈值。

### Q3: 如何为特定 LLM 优化？
**A:** 可以配置目标模型，自动优化 token 使用和格式：
```python
processor = AIProcessor(
    target_model="gpt-4",
    max_tokens=8000,
    preserve_context=True
)
```

### Q4: 支持哪些文本分块策略？
**A:** 支持固定大小、段落边界、句子边界、语义分块等多种策略。

## 相关文件列表

### 核心文件
- `packages/processors/__init__.py`
- `packages/processors/base.py`
- `packages/processors/text_processor.py`
- `packages/processors/markdown_processor.py`
- `packages/processors/deduplication.py`
- `packages/processors/validator.py`
- `packages/processors/ai_processor.py`

### 测试文件
- `tests/unit/processors/test_text_processor.py`
- `tests/unit/processors/test_markdown_processor.py`
- `tests/unit/processors/test_deduplication.py`
- `tests/integration/test_processing_pipeline.py`

## 更改日志 (Change Log)

### 2025-12-25
- 初始化模块设计文档
- 定义处理器接口和数据模型
- 规划质量检查和去重功能
