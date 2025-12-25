# Awesome-crawl4AI 开发工具配置指南

本文档详细说明了项目中所有开发工具配置文件的作用和使用方法。

## 📋 目录

- [配置文件概览](#配置文件概览)
- [快速开始](#快速开始)
- [配置文件详解](#配置文件详解)
- [常用命令](#常用命令)
- [工作流程](#工作流程)
- [故障排除](#故障排除)

## 配置文件概览

| 文件 | 作用 | 工具 |
|------|------|------|
| `pyproject.toml` | 主配置文件（现代标准） | 所有工具 |
| `setup.cfg` | 传统配置备份 | setuptools 等 |
| `.pre-commit-config.yaml` | Git 预提交钩子 | pre-commit |
| `Makefile` | 快捷命令 | make |
| `.gitignore` | Git 忽略规则 | git |
| `requirements.txt` | 生产依赖 | pip |
| `requirements-dev.txt` | 开发依赖 | pip |

## 快速开始

### 1. 环境准备

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 安装开发依赖
pip install --upgrade pip
pip install -r requirements-dev.txt
pip install -e .
```

### 2. 安装预提交钩子

```bash
# 安装 Git 预提交钩子
pre-commit install

# 手动运行所有钩子
pre-commit run --all-files
```

### 3. 验证配置

```bash
# 快速检查
make check

# 运行测试
make test

# 查看所有可用命令
make help
```

## 配置文件详解

### 1. pyproject.toml

这是项目的主配置文件，采用 TOML 格式，符合 PEP 518 标准。

#### 项目元数据

```toml
[project]
name = "awesome-crawl4ai"
version = "0.1.0-alpha"
description = "智能化网页数据采集框架，专为 AI 应用优化"
```

#### 依赖配置

```toml
dependencies = [
    "httpx>=0.25.0",
    "beautifulsoup4>=4.12.0",
    # ... 其他依赖
]

[project.optional-dependencies]
dev = ["pytest", "black", ...]
playwright = ["playwright>=1.40.0"]
```

#### 工具配置

**Black（代码格式化）**
```toml
[tool.black]
line-length = 100              # 最大行长度
target-version = ["py39", ...] # 目标 Python 版本
```

**isort（导入排序）**
```toml
[tool.isort]
profile = "black"              # 与 black 兼容
line_length = 100
```

**pytest（测试框架）**
```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = ["-ra", "--strict-markers", ...]
markers = ["slow", "integration", ...]
```

**mypy（类型检查）**
```toml
[tool.mypy]
python_version = "3.9"
disallow_untyped_defs = true
strict_equality = true
```

**coverage（覆盖率）**
```toml
[tool.coverage.run]
source = ["packages"]
branch = true
```

### 2. setup.cfg

传统配置文件，作为 pyproject.toml 的补充和备份。

```ini
[flake8]
max-line-length = 100
extend-ignore = E203,W503

[tool:pytest]
testpaths = tests
addopts = -ra --strict-markers
```

### 3. .pre-commit-config.yaml

Git 预提交钩子配置，确保代码质量。

#### 钩子列表

| 钩子 | 作用 | 工具 |
|------|------|------|
| trailing-whitespace | 移除行尾空格 | pre-commit-hooks |
| end-of-file-fixer | 确保文件末尾有换行 | pre-commit-hooks |
| check-yaml | 检查 YAML 语法 | pre-commit-hooks |
| check-json | 检查 JSON 语法 | pre-commit-hooks |
| black | 代码格式化 | black |
| isort | 导入排序 | isort |
| flake8 | 代码风格检查 | flake8 |
| mypy | 类型检查 | mypy |
| bandit | 安全检查 | bandit |

#### 安装和使用

```bash
# 安装钩子
pre-commit install

# 运行所有钩子
pre-commit run --all-files

# 运行特定钩子
pre-commit run black --all-files

# 跳过钩子（不推荐）
git commit --no-verify -m "message"
```

### 4. Makefile

提供快捷命令，简化常见操作。

#### 主要命令

```bash
# 安装
make install           # 安装生产依赖
make install-dev       # 安装开发依赖

# 代码质量
make format            # 格式化代码
make lint              # 运行代码检查
make typecheck         # 运行类型检查
make check             # 快速检查（格式 + 类型）

# 测试
make test              # 运行所有测试
make test-cov          # 测试 + 覆盖率
make test-html         # HTML 覆盖率报告

# 清理
make clean             # 清理临时文件
make clean-all         # 深度清理

# 其他
make docs              # 构建文档
make build             # 构建分发包
make help              # 显示所有命令
```

### 5. .gitignore

指定 Git 应该忽略的文件和目录。

#### 主要类别

- **Python 相关**：`__pycache__/`, `*.pyc`, `.venv/`
- **构建产物**：`build/`, `dist/`, `*.egg-info/`
- **IDE 配置**：`.vscode/`, `.idea/`
- **测试和覆盖率**：`.pytest_cache/`, `.coverage`, `htmlcov/`
- **敏感信息**：`.env`, `*.key`, `*.pem`

### 6. requirements.txt & requirements-dev.txt

**requirements.txt** - 生产环境依赖：
```
httpx>=0.25.0
beautifulsoup4>=4.12.0
# ... 核心依赖
```

**requirements-dev.txt** - 开发环境依赖：
```
pytest>=7.4.0
black>=23.0.0
mypy>=1.5.0
# ... 开发工具
```

## 常用命令

### 代码格式化

```bash
# 手动格式化
black packages/ tests/
isort packages/ tests/

# 使用 make
make format

# 检查格式
black --check packages/
isort --check-only packages/
```

### 代码检查

```bash
# flake8 检查
flake8 packages/ tests/

# 类型检查
mypy packages/

# 安全检查
bandit -r packages/

# 使用 make
make lint
make typecheck
make security
```

### 测试

```bash
# 运行所有测试
pytest

# 运行特定测试
pytest tests/unit/test_crawler.py

# 带覆盖率
pytest --cov=packages --cov-report=html

# 并行运行
pytest -n auto

# 使用 make
make test
make test-cov
```

### 依赖管理

```bash
# 更新依赖
pip install --upgrade -r requirements-dev.txt

# 查看依赖树
pipdeptree

# 审计安全性
pip audit
```

## 工作流程

### 日常开发流程

1. **创建功能分支**
   ```bash
   git checkout -b feature/my-feature
   ```

2. **开发代码**
   - 编写代码
   - 定期运行测试：`make test`
   - 格式化代码：`make format`

3. **提交前检查**
   ```bash
   # 运行预提交钩子（自动运行）
   git add .
   git commit -m "feat: add my feature"

   # 或手动运行
   make check
   ```

4. **推送到远程**
   ```bash
   git push origin feature/my-feature
   ```

### 完整检查流程

在创建 Pull Request 前运行：

```bash
# 1. 格式化代码
make format

# 2. 运行所有检查
make lint
make typecheck
make security

# 3. 运行测试
make test-cov

# 4. 构建文档
make docs

# 或一键运行
make ci
```

## 故障排除

### 常见问题

**1. Black 和 flake8 冲突**

症状：black 格式化后 flake8 仍报错

解决方案：确保配置一致
```toml
# pyproject.toml
[tool.black]
line-length = 100

[tool.flake8]
max-line-length = 100
extend-ignore = E203,W503
```

**2. 类型检查失败**

症状：mypy 报告类型错误

解决方案：
```bash
# 查看详细错误
mypy packages/ --show-error-codes

# 安装类型存根
pip install types-requests types-PyYAML
```

**3. 测试失败**

症状：pytest 运行失败

解决方案：
```bash
# 详细输出
pytest -vvs

# 进入调试模式
pytest --pdb

# 只运行失败的测试
pytest --lf
```

**4. 预提交钩子失败**

症状：git commit 被阻止

解决方案：
```bash
# 查看哪个钩子失败
pre-commit run --all-files

# 跳过钩子（不推荐）
git commit --no-verify
```

**5. 导入顺序问题**

症状：isort 和 black 冲突

解决方案：确保配置兼容
```toml
[tool.isort]
profile = "black"
line_length = 100
```

### 性能优化

**加速测试**
```bash
# 使用并行测试
pytest -n auto

# 只运行修改的文件
pytest --changed-only

# 跳过慢速测试
pytest -m "not slow"
```

**加速类型检查**
```bash
# 使用 mypy daemon
pip install mypy.dmypy
dmypy watch

# 只检查修改的文件
mypy packages/ --incremental
```

## 最佳实践

### 1. 代码提交前

```bash
# 总是运行
make format
make check
make test
```

### 2. 保持依赖更新

```bash
# 定期更新开发依赖
pip install --upgrade -r requirements-dev.txt

# 检查过时的包
pip list --outdated
```

### 3. 使用有意义的提交信息

```bash
# 好的提交信息
git commit -m "feat(crawler): add async support for data fetching"
git commit -m "fix(extractor): handle empty HTML gracefully"
git commit -m "docs: update installation guide"

# 避免的提交信息
git commit -m "update code"
git commit -m "fix bug"
```

### 4. 编写测试

```python
# tests/unit/test_crawler.py
import pytest

@pytest.mark.unit
def test_crawler_init():
    """测试爬虫初始化"""
    crawler = Crawler()
    assert crawler is not None

@pytest.mark.slow
def test_crawler_fetch():
    """测试爬虫数据获取（慢速测试）"""
    # ... 测试代码
```

## 配置调优

### 根据项目需求调整

**1. 严格程度**

如果项目需要更严格的检查：
```toml
[tool.mypy]
strict = true  # 启用所有严格检查

[tool.flake8]
max-complexity = 10  # 降低复杂度阈值
```

**2. 性能优先**

如果关注测试速度：
```toml
[tool.pytest.ini_options]
addopts = [
    "-ra",
    "-n auto",  # 并行运行
    "-m 'not slow'",  # 跳过慢速测试
]
```

**3. 文档要求**

如果重视文档：
```toml
[tool.pydocstyle]
convention = "google"
add-ignore = []  # 不忽略任何文档错误
```

## 相关资源

- [Black 文档](https://black.readthedocs.io/)
- [isort 文档](https://pycqa.github.io/isort/)
- [pytest 文档](https://docs.pytest.org/)
- [mypy 文档](https://mypy.readthedocs.io/)
- [pre-commit 文档](https://pre-commit.com/)
- [Make 教程](https://makefiletutorial.com/)

## 贡献指南

如果你发现配置问题或有改进建议：

1. 检查现有配置是否合理
2. 提出改进方案
3. 更新此文档
4. 提交 Pull Request

---

**版本**: 1.0.0
**最后更新**: 2025-12-25
