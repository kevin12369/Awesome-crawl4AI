# CI/CD 快速入门

这是一个简短的 CI/CD 配置检查清单，帮助你快速设置和使用项目的自动化工具。

## 📋 初始设置

### 1. GitHub Secrets 配置

在 GitHub 仓库中添加以下 Secrets（Settings → Secrets and variables → Actions）：

```
CODECOV_TOKEN=<你的 Codecov token>
PYPI_API_TOKEN=<你的 PyPI API token>
```

### 2. 本地开发环境

```bash
# 克隆仓库
git clone https://github.com/YOUR_USERNAME/Awesome-crawl4AI.git
cd Awesome-crawl4AI

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 安装 pre-commit hooks
pre-commit install
```

## 🚀 日常开发

### 提交代码前检查

```bash
# 1. 格式化代码
black .
isort .

# 2. 运行测试
pytest tests/ -v

# 3. 代码质量检查
flake8 .
mypy packages/

# 4. 提交代码
git add .
git commit -m "feat: add new feature"
```

### 创建 Pull Request

```bash
# 1. 切换到 develop 分支
git checkout develop
git pull upstream develop

# 2. 创建功能分支
git checkout -b feature/your-feature

# 3. 开发和提交
# ... 进行开发 ...
git add .
git commit -m "feat: description"

# 4. 推送并创建 PR
git push origin feature/your-feature
# 然后在 GitHub 上创建 PR
```

## 📦 发布流程

### 方法 1: 通过 Tag 发布

```bash
# 创建 tag
git tag -a v1.0.0 -m "Release v1.0.0"

# 推送 tag（触发自动发布）
git push origin v1.0.0
```

### 方法 2: 手动触发发布

1. 访问 GitHub Actions 页面
2. 选择 "Release" 工作流
3. 点击 "Run workflow"
4. 选择版本增量类型
5. 点击运行

## 🎯 Commit Message 规范

```bash
feat: 新功能
fix: Bug 修复
docs: 文档更新
style: 代码格式（不影响功能）
refactor: 重构
perf: 性能优化
test: 测试相关
chore: 构建/工具变更
ci: CI 配置变更
```

## 📊 CI 检查状态

检查 GitHub Actions 页面查看：
- ✅ CI 工作流状态
- 🔒 安全扫描结果
- 📊 代码质量报告
- 🧪 测试覆盖率

## 🆘 常见问题

### CI 失败怎么办？

1. 查看失败的 job 日志
2. 本地复现问题
3. 修复后推送新 commit

### Pre-commit 失败？

```bash
# 查看具体错误
pre-commit run --all-files

# 跳过 hooks（不推荐）
git commit --no-verify -m "message"
```

### 测试失败？

```bash
# 本地运行测试
pytest tests/ -v

# 运行特定测试
pytest tests/test_crawler.py::test_function -v
```

## 📚 更多信息

- [完整 CI/CD 指南](CI-CD-GUIDE.md)
- [贡献指南](../CONTRIBUTING.md)
- [项目文档](../README.md)

---

**快速提示**: 使用 `git commit --no-verify` 可以跳过 pre-commit hooks，但不推荐这样做！
