# 贡献指南

感谢你对 Awesome-crawl4AI 项目的关注！我们欢迎任何形式的贡献，包括但不限于：

- 🐛 报告 Bug
- 💡 提出新功能建议
- 📝 改进文档
- 🔧 提交代码修复
- ✨ 添加新功能
- 🧪 编写测试
- 🌍 帮助翻译

---

## 📋 目录

- [行为准则](#行为准则)
- [如何贡献](#如何贡献)
- [开发流程](#开发流程)
- [代码规范](#代码规范)
- [提交规范](#提交规范)
- [Pull Request 流程](#pull-request-流程)
- [问题反馈](#问题反馈)

---

## 🤝 行为准则

参与本项目即表示你同意遵守我们的行为准则：

- 尊重不同的观点和经验
- 使用包容和友好的语言
- 优雅地接受建设性批评
- 关注对社区最有利的事情
- 对其他社区成员表示同理心

---

## 🚀 如何贡献

### 1. 环境准备

#### Fork 仓库

点击 GitHub 页面右上角的 "Fork" 按钮，将项目 fork 到你的账户下。

#### Clone 你的 Fork

```bash
git clone https://github.com/YOUR_USERNAME/Awesome-crawl4AI.git
cd Awesome-crawl4AI
```

#### 添加上游远程仓库

```bash
git remote add upstream https://github.com/ORIGINAL_OWNER/Awesome-crawl4AI.git
```

#### 设置开发环境

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 安装 pre-commit hooks（可选但推荐）
pip install pre-commit
pre-commit install
```

### 2. 选择贡献方式

#### 报告 Bug

1. 在 [Issues](https://github.com/ORIGINAL_OWNER/Awesome-crawl4AI/issues) 中搜索是否已存在相同问题
2. 如果没有，点击 "New Issue"
3. 选择 "Bug 报告" 模板
4. 填写详细信息并提交

#### 提出新功能

1. 搜索现有的 Feature Requests
2. 如果没有，创建新 Issue
3. 选择 "功能请求" 模板
4. 描述你的功能想法
5. 等待维护者反馈

#### 提交代码

1. 在 Issue 中评论表明你想处理这个任务
2. 等待分配和确认
3. 创建分支进行开发
4. 提交 Pull Request

---

## 🔄 开发流程

### 分支策略

我们使用以下分支结构：

- `main`: 稳定发布版本
- `develop`: 开发主分支
- `feature/*`: 功能开发分支
- `bugfix/*`: Bug 修复分支
- `hotfix/*`: 紧急修复分支

### 创建功能分支

```bash
# 确保你的本地仓库是最新的
git checkout develop
git pull upstream develop

# 创建功能分支
git checkout -b feature/your-feature-name
```

### 进行开发

1. 编写代码
2. 添加测试
3. 运行代码检查

```bash
# 格式化代码
black .
isort .

# 代码风格检查
flake8 .

# 类型检查
mypy packages/

# 运行测试
pytest tests/ -v

# 测试覆盖率
pytest tests/ --cov=packages --cov-report=html
```

4. 提交代码（遵循 [提交规范](#提交规范)）

```bash
git add .
git commit -m "feat: add new feature for extracting markdown"
```

### 同步上游更新

```bash
# 获取上游更新
git fetch upstream

# 合并上游 develop 分支
git rebase upstream/develop
```

---

## 📐 代码规范

### Python 代码风格

我们遵循以下编码规范：

#### PEP 8

- 使用 4 个空格缩进
- 每行最多 88 个字符（Black 默认）
- 使用空格而不是 Tab

#### 命名规范

```python
# 类名：CapWords
class CrawlerEngine:
    pass

# 函数和变量：snake_case
def crawl_url(url: str) -> dict:
    result = {}
    return result

# 常量：UPPER_SNAKE_CASE
MAX_RETRIES = 3
DEFAULT_TIMEOUT = 30

# 私有成员：前导下划线
class MyClass:
    def __private_method(self):
        pass
```

#### 类型注解

```python
from typing import List, Dict, Optional

def process_data(
    urls: List[str],
    options: Optional[Dict[str, any]] = None
) -> Dict[str, str]:
    """处理数据并返回结果。

    Args:
        urls: 要处理的 URL 列表
        options: 可选的处理选项

    Returns:
        包含处理结果的字典
    """
    if options is None:
        options = {}
    # 实现代码...
    return {}
```

#### 文档字符串

使用 Google 风格的 docstring：

```python
def extract_content(html: str, selector: str) -> str:
    """从 HTML 中提取内容。

    Args:
        html: HTML 源码
        selector: CSS 选择器

    Returns:
        提取的文本内容

    Raises:
        ValueError: 当选择器无效时
        ParserError: 当 HTML 解析失败时

    Examples:
        >>> extract_content('<p>Hello</p>', 'p')
        'Hello'
    """
    # 实现代码...
```

### 导入顺序

```python
# 1. 标准库
import os
import sys
from typing import Dict, List

# 2. 第三方库
import requests
from bs4 import BeautifulSoup

# 3. 本地模块
from packages.crawler import Crawler
from packages.extractors import ContentExtractor
```

### 错误处理

```python
def safe_request(url: str) -> Optional[requests.Response]:
    """安全的请求函数，处理异常情况。"""
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response
    except requests.RequestException as e:
        logger.error(f"请求失败: {url}, 错误: {e}")
        return None
```

---

## ✍️ 提交规范

我们使用 [Conventional Commits](https://www.conventionalcommits.org/) 规范。

### 提交格式

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Type 类型

- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档更新
- `style`: 代码格式（不影响代码运行的变动）
- `refactor`: 重构（既不是新增功能，也不是修改 bug 的代码变动）
- `perf`: 性能优化
- `test`: 测试相关
- `chore`: 构建过程或辅助工具的变动
- `ci`: CI 配置文件和脚本的变动

### 示例

```bash
# 简单提交
feat: add markdown extraction support
fix: resolve timeout issue in crawler
docs: update installation guide

# 带范围的提交
feat(crawler): add JavaScript rendering support
fix(extractor): handle malformed HTML
test(parser): add unit tests for HTML parser

# 带详细说明的提交
feat(crawler): add proxy rotation support

添加代理池轮换功能以防止 IP 封禁：
- 支持多个代理源
- 自动故障转移
- 代理健康检查

Closes #123
```

---

## 📮 Pull Request 流程

### 1. 推送到你的 Fork

```bash
git push origin feature/your-feature-name
```

### 2. 创建 Pull Request

1. 访问你 Fork 的 GitHub 页面
2. 点击 "New Pull Request"
3. 选择你的功能分支
4. 点击 "Create Pull Request"

### 3. 填写 PR 模板

使用提供的 PR 模板，确保：

- 清晰描述变更内容
- 关联相关 Issue
- 添加截图或演示（如适用）
- 完成检查清单

### 4. 等待审查

- 维护者会审查你的代码
- 可能会要求修改
- 及时回应评论

### 5. 修改后的更新

如果需要修改：

```bash
# 在你的分支上进行修改
git add .
git commit -m "fix: address review comments"
git push origin feature/your-feature-name
```

### 6. 合并

- PR 通过审查后，维护者会合并代码
- 你的贡献将被记录在贡献者列表中

---

## 🐛 问题反馈

### 报告 Bug 时的信息

- 清晰的标题和描述
- 复现步骤
- 预期行为 vs 实际行为
- 环境信息（OS、Python 版本等）
- 错误日志或截图
- 最小化的复现代码

### 功能建议时的信息

- 清晰的功能描述
- 使用场景
- 期望的行为
- 可能的实现方案（可选）
- 是否愿意自己实现

---

## 📚 开发资源

### 有用的文档

- [项目 README](README.md)
- [快速开始指南](QUICKSTART.md)
- [API 文档](docs/)（待完善）

### 开发工具

- **代码格式化**: Black, isort
- **代码检查**: Flake8, pylint
- **类型检查**: mypy
- **测试框架**: pytest
- **覆盖率**: pytest-cov
- **文档生成**: Sphinx（待配置）

### 调试技巧

```bash
# 使用 pdb 调试
python -m pdb your_script.py

# 使用 pytest 的调试功能
pytest tests/ -pdb

# 查看详细日志
python -m logging
```

---

## 🎉 成为贡献者

所有贡献者都会被添加到项目的贡献者列表中。

### 贡献者级别

- 🌱 **新手贡献者**: 第一次贡献
- 🌿 **活跃贡献者**: 提交 3+ 个 PR
- 🌳 **核心贡献者**: 长期贡献且质量稳定
- 🏆 **杰出贡献者**: 对项目有重大影响

---

## ❓ 常见问题

### Q: 我的 PR 没有得到回复怎么办？

A: 通常我们会在一周内审查 PR。如果没有回复，可以：

1. 在 PR 中友好地提醒
2. 在相关的 Issue 中提及
3. 在讨论区发帖询问

### Q: 我的 PR 被拒绝了怎么办？

A: 不要灰心！：

1. 仔细阅读拒绝原因
2. 根据反馈进行修改
3. 重新提交

### Q: 我不会写代码，能贡献吗？

A: 当然可以！你可以：

- 改进文档
- 报告 Bug
- 分享使用经验
- 帮助其他用户
- 提出功能建议

### Q: 如何保持我的 Fork 与上游同步？

A:

```bash
# 添加上游仓库（如果还没有）
git remote add upstream https://github.com/ORIGINAL_OWNER/Awesome-crawl4AI.git

# 获取上游更新
git fetch upstream

# 合并到你的分支
git checkout develop
git merge upstream/develop

# 推送到你的 Fork
git push origin develop
```

---

## 📧 联系方式

如果你有任何问题：

- 在 GitHub 上提 Issue
- 加入我们的讨论社区（待创建）
- 发送邮件到维护者（待提供）

---

## 📄 许可证

通过贡献代码，你同意你的贡献将在与项目相同的 [许可证](LICENSE) 下发布。

---

**再次感谢你的贡献！** 🎉

你的每一个贡献都让这个项目变得更好。无论贡献大小，我们都非常感激！

---

**最后更新**: 2025-12-25
