# CI/CD 工作流指南

本文档详细说明 Awesome-crawl4AI 项目的持续集成/持续部署 (CI/CD) 配置和使用方法。

## 目录

- [概述](#概述)
- [工作流文件](#工作流文件)
- [徽章说明](#徽章说明)
- [配置说明](#配置说明)
- [使用指南](#使用指南)
- [最佳实践](#最佳实践)
- [故障排除](#故障排除)

---

## 概述

项目使用 GitHub Actions 作为 CI/CD 平台，实现了以下自动化流程：

### 工作流列表

| 工作流 | 文件 | 触发条件 | 用途 |
|--------|------|----------|------|
| CI | `.github/workflows/ci.yml` | Push/PR | 代码质量检查、测试、构建 |
| Code Quality | `.github/workflows/code-quality.yml` | 定期/PR | 代码复杂度分析、依赖健康检查 |
| Release | `.github/workflows/release.yml` | Tag/手动 | 自动发布到 PyPI 和 GitHub Releases |
| Dependabot | `.github/dependabot.yml` | 每周 | 自动依赖更新 |

---

## 工作流文件

### 1. CI 工作流 (ci.yml)

**功能**:
- ✅ 代码质量检查 (Black, isort, Flake8)
- 🔒 安全扫描 (Bandit, Safety)
- 🧪 多版本测试 (Python 3.10, 3.11, 3.12)
- 📊 测试覆盖率报告 (Codecov)
- 📦 构建包检查

**触发条件**:
- Push 到 `main` 或 `develop` 分支
- 针对 `main` 或 `develop` 的 Pull Request
- 手动触发 (workflow_dispatch)

**关键步骤**:

```yaml
lint:          # 代码质量检查
security:      # 安全扫描
test:          # 多版本测试
build:         # 构建检查
```

### 2. Code Quality 工作流 (code-quality.yml)

**功能**:
- 📊 代码复杂度分析 (Radon, Xenon)
- 📦 依赖健康检查 (pip-audit)
- 📚 文档覆盖率检查 (Interrogate)
- 🔁 代码重复检测 (pycpd)
- ⚡ 性能基准测试 (pytest-benchmark)

**触发条件**:
- 每周一 UTC 00:00
- Pull Request
- 手动触发

### 3. Release 工作流 (release.yml)

**功能**:
- ✅ 版本验证
- 🧪 完整测试套件
- 📦 构建发布包
- 🏷️ 创建 Git Tag
- 📤 发布到 PyPI
- 🎉 创建 GitHub Release

**触发条件**:
- 推送 tag (格式: `v*.*.*`)
- 手动触发 (可选择 patch/minor/major)

**发布流程**:

```
验证版本 → 运行测试 → 构建包 → 发布 PyPI → 创建 Release → 通知
```

### 4. Dependabot 配置 (dependabot.yml)

**功能**:
- 📦 每周自动检查依赖更新
- 🔄 自动创建 Pull Request
- 👥 自动分配审查者

**配置**:
- Python 依赖: 每周一检查
- GitHub Actions: 每周一检查
- Docker 基础镜像: 每周一检查

---

## 徽章说明

README.md 中的徽章及其含义：

| 徽章 | 说明 | 链接 |
|------|------|------|
| CI/CD | 持续集成状态 | Actions 页面 |
| Code Quality | 代码质量检查状态 | Actions 页面 |
| codecov | 测试覆盖率 | Codecov 报告 |
| PyPI version | PyPI 最新版本 | PyPI 页面 |
| Downloads | PyPI 下载量 | pepy.tech |
| Code style: black | 代码格式化工具 | Black 官网 |
| Imports: isort | 导入排序工具 | isort 官网 |
| Type checking: mypy | 类型检查工具 | mypy 官网 |
| Security: bandit | 安全检查工具 | bandit 官网 |

---

## 配置说明

### 必需的 GitHub Secrets

在 GitHub 仓库设置中配置以下 Secrets：

| Secret 名称 | 说明 | 获取方式 |
|------------|------|----------|
| `CODECOV_TOKEN` | Codecov 上传令牌 | 在 [Codecov](https://codecov.io) 获取 |
| `PYPI_API_TOKEN` | PyPI 发布令牌 | 在 [PyPI](https://pypi.org) 创建 API token |

**配置步骤**:

1. 访问仓库 Settings → Secrets and variables → Actions
2. 点击 "New repository secret"
3. 添加上述 secrets

### PyPI Trusted Publishing (推荐)

不使用 API token，而是使用可信发布：

1. 访问 [PyPI](https://pypi.org) → Account settings → Publishing
2. 添加新的发布配置：
   - GitHub repository URL
   - Workflow name: `release.yml`
   - Environment name: `pypi`

### 可选的第三方服务

#### Codecov

1. 访问 [https://codecov.io](https://codecov.io)
2. 使用 GitHub 账号登录
3. 添加 Awesome-crawl4AI 仓库
4. 获取 token 并添加到 GitHub Secrets

---

## 使用指南

### 本地开发工作流

#### 1. 安装 pre-commit hooks

```bash
# 安装 pre-commit
pip install pre-commit

# 安装 hooks
pre-commit install

# 手动运行所有检查
pre-commit run --all-files

# 跳过 hooks (不推荐)
git commit --no-verify -m "message"
```

#### 2. 代码质量检查

```bash
# 代码格式化
black .
isort .

# 代码风格检查
flake8 .

# 类型检查
mypy packages/

# 安全检查
bandit -r packages/

# 文档检查
pydocstyle packages/
```

#### 3. 运行测试

```bash
# 运行所有测试
pytest tests/

# 运行特定测试
pytest tests/test_crawler.py

# 带覆盖率报告
pytest tests/ --cov=packages --cov-report=html

# 查看覆盖率报告
open htmlcov/index.html  # Mac
start htmlcov/index.html  # Windows
```

### 提交规范

使用 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

```bash
# 功能
git commit -m "feat: add new extractor for JSON data"

# Bug 修复
git commit -m "fix: resolve timeout issue in async crawler"

# 文档
git commit -m "docs: update installation guide"

# 测试
git commit -m "test: add unit tests for HTML parser"

# 重构
git commit -m "refactor: simplify crawler initialization"
```

### Pull Request 流程

#### 1. 创建功能分支

```bash
git checkout develop
git pull upstream develop
git checkout -b feature/your-feature-name
```

#### 2. 开发和提交

```bash
# 进行开发
# ...

# 提交代码
git add .
git commit -m "feat: description of your feature"
```

#### 3. 推送并创建 PR

```bash
git push origin feature/your-feature-name
```

然后在 GitHub 上创建 Pull Request，使用提供的 PR 模板。

### 发布流程

#### 方法 1: 通过 Tag 发布

```bash
# 创建版本 tag
git tag -a v1.0.0 -m "Release v1.0.0"

# 推送 tag
git push origin v1.0.0
```

#### 方法 2: 通过手动触发

1. 访问 GitHub Actions 页面
2. 选择 "Release" 工作流
3. 点击 "Run workflow"
4. 选择版本增量类型 (patch/minor/major)
5. 点击 "Run workflow" 按钮

---

## 最佳实践

### 代码提交前检查

✅ **提交前检查清单**:

- [ ] 代码通过 `black` 格式化
- [ ] 代码通过 `isort` 排序
- [ ] 代码通过 `flake8` 检查
- [ ] 测试通过 (`pytest`)
- [ ] 测试覆盖率没有降低
- [ ] 文档已更新
- [ ] Commit message 遵循规范

### 分支管理

- `main`: 稳定发布版本
- `develop`: 开发主分支
- `feature/*`: 功能开发
- `bugfix/*`: Bug 修复
- `hotfix/*`: 紧急修复

### Issue 和 PR 管理

1. **创建 Issue**:
   - 使用适当的模板 (Bug/Feature/Question)
   - 提供详细的信息
   - 标记合适的 labels

2. **创建 PR**:
   - 链接相关的 Issue
   - 填写 PR 模板
   - 确保所有 CI 检查通过
   - 等待代码审查

### 版本发布

1. 更新 CHANGELOG.md
2. 创建 git tag (格式: `vX.Y.Z`)
3. 推送 tag 触发自动发布
4. 验证 PyPI 和 GitHub Release

---

## 故障排除

### 常见问题

#### 1. CI 检查失败

**问题**: 代码格式检查失败

```bash
# 解决方案：本地运行格式化
black .
isort .
git add .
git commit -m "style: fix code formatting"
```

**问题**: 测试失败

```bash
# 解决方案：本地运行测试查看详细输出
pytest tests/ -v -s

# 运行特定失败的测试
pytest tests/test_crawler.py::test_crawl_url -v
```

**问题**: 类型检查失败

```bash
# 解决方案：查看类型错误
mypy packages/

# 临时忽略特定错误
# type: ignore
```

#### 2. Pre-commit hooks 问题

**问题**: Pre-commit hook 失败

```bash
# 跳过 hooks (不推荐)
git commit --no-verify -m "message"

# 更新 hooks 到最新版本
pre-commit autoupdate
pre-commit run --all-files
```

#### 3. 发布失败

**问题**: PyPI 发布失败

- 检查 `PYPI_API_TOKEN` 是否正确配置
- 检查版本号是否已存在
- 检查包名是否已被占用

**问题**: GitHub Release 创建失败

- 检查 tag 格式是否正确 (`vX.Y.Z`)
- 检查 GitHub token 权限
- 查看 Actions 日志获取详细错误

#### 4. Dependabot 问题

**问题**: Dependabot 不创建 PR

- 检查 `.github/dependabot.yml` 配置
- 确保仓库启用了 Dependabot
- 检查仓库设置中的安全选项

---

## 相关资源

### 官方文档

- [GitHub Actions 文档](https://docs.github.com/en/actions)
- [Pre-commit 文档](https://pre-commit.com/)
- [Black 文档](https://black.readthedocs.io/)
- [pytest 文档](https://docs.pytest.org/)
- [Codecov 文档](https://docs.codecov.com/)

### 项目文档

- [CONTRIBUTING.md](../CONTRIBUTING.md) - 贡献指南
- [README.md](../README.md) - 项目说明
- [CHANGELOG.md](../CHANGELOG.md) - 变更日志

### 联系方式

- GitHub Issues: [提交问题](https://github.com/YOUR_USERNAME/Awesome-crawl4AI/issues)
- Discussions: [讨论区](https://github.com/YOUR_USERNAME/Awesome-crawl4AI/discussions)

---

**最后更新**: 2025-12-25
**维护者**: Awesome-crawl4AI Team
