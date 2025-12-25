# 贡献指南

感谢你对 **Awesome-crawl4AI** 项目的关注！这是一个个人项目，但仍然欢迎任何形式的贡献。

---

## 🤝 如何贡献

### 1. Fork 仓库

点击 GitHub 页面右上角的 **Fork** 按钮

### 2. Clone 你的 Fork

```bash
git clone https://github.com/YOUR_USERNAME/Awesome-crawl4AI.git
cd Awesome-crawl4AI
```

### 3. 创建分支

```bash
git checkout -b feature/your-feature-name
```

### 4. 进行更改

- 编写代码
- 添加测试
- 确保代码通过测试

### 5. 提交更改

```bash
git add .
git commit -m "feat: description of your changes"
```

### 6. 推送到 Fork

```bash
git push origin feature/your-feature-name
```

### 7. 创建 Pull Request

访问你 Fork 的 GitHub 页面，点击 **New Pull Request**

---

## 📐 代码规范

### Python 代码

- 遵循 **PEP 8** 规范
- 使用 **Black** 格式化代码
- 添加**类型注解**
- 编写 **Docstring**（Google 风格）

### 前端代码

- 使用 **TypeScript** 严格模式
- 遵循 **Vue 3 Composition API** 最佳实践
- 使用 **ESLint + Prettier** 格式化

---

## ✍️ 提交规范

使用 [Conventional Commits](https://www.conventionalcommits.org/) 格式：

```
<type>: <subject>

<body>
```

**Type 类型：**
- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档更新
- `style`: 代码格式
- `refactor`: 重构
- `perf`: 性能优化
- `test`: 测试相关
- `chore`: 其他

**示例：**
```bash
feat: add new scenario template for blog crawling
fix: resolve timeout issue in crawler
docs: update API documentation
```

---

## 🐛 报告 Bug

在提 Issue 时，请提供：

- 清晰的标题和描述
- 复现步骤
- 预期行为 vs 实际行为
- 环境信息（OS、Python 版本等）
- 错误日志或截图

---

## 📚 开发环境设置

### 后端

```bash
cd backend

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 运行测试
pytest
```

### 前端

```bash
cd frontend

# 安装依赖
npm install

# 运行测试
npm run test
```

---

## 📧 联系方式

- **GitHub**: [kevin12369](https://github.com/kevin12369)
- **Issues**: [GitHub Issues](https://github.com/kevin12369/Awesome-crawl4AI/issues)

---

## 📄 许可证

通过贡献代码，你同意你的贡献将在与项目相同的 [MIT License](LICENSE) 下发布。

---

**再次感谢你的贡献！** 🎉
