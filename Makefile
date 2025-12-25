# ================================
# Awesome-crawl4AI - Makefile
# ================================
# 常用开发命令的快捷方式
#
# 使用方法:
#   make help          # 显示所有可用命令
#   make install       # 安装项目依赖
#   make test          # 运行测试
#
# 注意:
#   - Windows 用户需要安装 Make 工具或使用等效命令
#   - 或者直接使用命令行中列出的原始命令

# ================================
# 项目配置
# ================================

# Python 解释器
PYTHON := python
PYTHON3 := python3

# 虚拟环境目录
VENV := venv
VENV_BIN := $(VENV)/Scripts
ifeq ($(OS),Windows_NT)
    VENV_BIN := $(VENV)/Scripts
else
    VENV_BIN := $(VENV)/bin
endif

# 项目源码目录
SRC_DIR := packages
TESTS_DIR := tests

# 颜色输出（用于终端）
BLUE := \033[0;34m
GREEN := \033[0;32m
RED := \033[0;31m
YELLOW := \033[0;33m
NC := \033[0m # No Color

# ================================
# 默认目标
# ================================

.PHONY: all
all: install lint test  # 默认执行安装、检查和测试

# ================================
# 帮助信息
# ================================

.PHONY: help
help:
	@echo "$(BLUE)Awesome-crawl4AI - 可用命令$(NC)"
	@echo ""
	@echo "$(GREEN)安装和环境:$(NC)"
	@echo "  make install       - 安装生产依赖"
	@echo "  make install-dev   - 安装开发依赖"
	@echo "  make venv          - 创建虚拟环境"
	@echo "  make clean         - 清理临时文件"
	@echo "  make clean-all     - 深度清理（包括虚拟环境）"
	@echo ""
	@echo "$(GREEN)代码质量:$(NC)"
	@echo "  make format        - 格式化代码（black + isort）"
	@echo "  make format-check  - 检查代码格式"
	@echo "  make lint          - 运行代码检查（flake8）"
	@echo "  make lint-all      - 运行所有代码检查工具"
	@echo "  make typecheck     - 运行类型检查（mypy）"
	@echo "  make security      - 运行安全检查（bandit）"
	@echo "  make pre-commit    - 运行预提交钩子"
	@echo "  make pre-commit-install - 安装预提交钩子"
	@echo ""
	@echo "$(GREEN)测试:$(NC)"
	@echo "  make test          - 运行所有测试"
	@echo "  make test-unit     - 运行单元测试"
	@echo "  make test-integ    - 运行集成测试"
	@echo "  make test-cov      - 运行测试并生成覆盖率报告"
	@echo "  make test-html     - 生成 HTML 覆盖率报告"
	@echo "  make test-watch    - 监视文件变化并自动运行测试"
	@echo ""
	@echo "$(GREEN)文档:$(NC)"
	@echo "  make docs          - 构建文档"
	@echo "  make docs-serve    - 启动文档服务器"
	@echo ""
	@echo "$(GREEN)发布:$(NC)"
	@echo "  make build         - 构建分发包"
	@echo "  make upload-test   - 上传到 TestPyPI"
	@echo "  make upload        - 上传到 PyPI"
	@echo ""
	@echo "$(GREEN)其他:$(NC)"
	@echo "  make deps          - 更新依赖关系图"
	@echo "  make check         - 快速检查（格式 + 类型检查）"

# ================================
# 安装和环境
# ================================

.PHONY: venv
venv:
	@echo "$(BLUE)创建虚拟环境...$(NC)"
	$(PYTHON) -m venv $(VENV)
	@echo "$(GREEN)虚拟环境创建完成: $(VENV)$(NC)"
	@echo "运行以下命令激活虚拟环境:"
	@echo "  Windows: $(VENV)/Scripts/activate"
	@echo "  Linux/Mac: source $(VENV)/bin/activate"

.PHONY: install
install:
	@echo "$(BLUE)安装生产依赖...$(NC)"
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -e .
	@echo "$(GREEN)生产依赖安装完成$(NC)"

.PHONY: install-dev
install-dev:
	@echo "$(BLUE)安装开发依赖...$(NC)"
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -e ".[dev]"
	$(PYTHON) -m pip install -r requirements-dev.txt
	@echo "$(GREEN)开发依赖安装完成$(NC)"

.PHONY: update-deps
update-deps:
	@echo "$(BLUE)更新依赖包到最新版本...$(NC)"
	$(PYTHON) -m pip install --upgrade -r requirements-dev.txt
	@echo "$(GREEN)依赖包更新完成$(NC)"

# ================================
# 清理
# ================================

.PHONY: clean
clean:
	@echo "$(BLUE)清理临时文件...$(NC)"
	find . -type f -name "*.py[cod]" -delete
	find . -type f -name "*.so" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".tox" -exec rm -rf {} +
	find . -type d -name ".coverage" -exec rm -rf {} +
	find . -type f -name ".coverage" -delete
	find . -type f -name "*.log" -delete
	rm -rf build/ dist/ htmlcov/ .pytest_cache/
	@echo "$(GREEN)清理完成$(NC)"

.PHONY: clean-all
clean-all: clean
	@echo "$(BLUE)深度清理...$(NC)"
	rm -rf $(VENV)
	rm -rf .venv
	rm -rf *.egg
	@echo "$(GREEN)深度清理完成$(NC)"

# ================================
# 代码格式化
# ================================

.PHONY: format
format:
	@echo "$(BLUE)格式化代码...$(NC)"
	@echo "$(YELLOW)运行 black...$(NC)"
	black $(SRC_DIR) $(TESTS_DIR)
	@echo "$(YELLOW)运行 isort...$(NC)"
	isort $(SRC_DIR) $(TESTS_DIR)
	@echo "$(GREEN)代码格式化完成$(NC)"

.PHONY: format-check
format-check:
	@echo "$(BLUE)检查代码格式...$(NC)"
	black --check $(SRC_DIR) $(TESTS_DIR)
	isort --check-only $(SRC_DIR) $(TESTS_DIR)

# ================================
# 代码检查
# ================================

.PHONY: lint
lint:
	@echo "$(BLUE)运行 flake8 检查...$(NC)"
	flake8 $(SRC_DIR) $(TESTS_DIR)

.PHONY: lint-all
lint-all:
	@echo "$(BLUE)运行所有代码检查工具...$(NC)"
	@echo "$(YELLOW)flake8...$(NC)"
	flake8 $(SRC_DIR) $(TESTS_DIR)
	@echo "$(YELLOW)pydocstyle...$(NC)"
	pydocstyle $(SRC_DIR)
	@echo "$(GREEN)所有检查完成$(NC)"

.PHONY: typecheck
typecheck:
	@echo "$(BLUE)运行 mypy 类型检查...$(NC)"
	mypy $(SRC_DIR)

.PHONY: security
security:
	@echo "$(BLUE)运行 bandit 安全检查...$(NC)"
	bandit -r $(SRC_DIR)

# ================================
# 快速检查
# ================================

.PHONY: check
check: format-check typecheck
	@echo "$(GREEN)快速检查完成$(NC)"

# ================================
# 测试
# ================================

.PHONY: test
test:
	@echo "$(BLUE)运行所有测试...$(NC)"
	pytest $(TESTS_DIR)

.PHONY: test-unit
test-unit:
	@echo "$(BLUE)运行单元测试...$(NC)"
	pytest $(TESTS_DIR)/unit -v

.PHONY: test-integ
test-integ:
	@echo "$(BLUE)运行集成测试...$(NC)"
	pytest $(TESTS_DIR)/integration -v

.PHONY: test-cov
test-cov:
	@echo "$(BLUE)运行测试并生成覆盖率报告...$(NC)"
	pytest $(TESTS_DIR) --cov=$(SRC_DIR) --cov-report=term-missing

.PHONY: test-html
test-html:
	@echo "$(BLUE)生成 HTML 覆盖率报告...$(NC)"
	pytest $(TESTS_DIR) --cov=$(SRC_DIR) --cov-report=html
	@echo "$(GREEN)HTML 报告已生成: htmlcov/index.html$(NC)"

.PHONY: test-watch
test-watch:
	@echo "$(BLUE)监视文件变化并自动运行测试...$(NC)"
	pytest-watch $(TESTS_DIR)

.PHONY: test-fast
test-fast:
	@echo "$(BLUE)运行快速测试（跳过慢速测试）...$(NC)"
	pytest $(TESTS_DIR) -m "not slow" -v

# ================================
# 预提交钩子
# ================================

.PHONY: pre-commit
pre-commit:
	@echo "$(BLUE)运行预提交钩子...$(NC)"
	pre-commit run --all-files

.PHONY: pre-commit-install
pre-commit-install:
	@echo "$(BLUE)安装预提交钩子...$(NC)"
	pre-commit install

.PHONY: pre-commit-update
pre-commit-update:
	@echo "$(BLUE)更新预提交钩子...$(NC)"
	pre-commit autoupdate

# ================================
# 文档
# ================================

.PHONY: docs
docs:
	@echo "$(BLUE)构建文档...$(NC)"
	mkdocs build

.PHONY: docs-serve
docs-serve:
	@echo "$(BLUE)启动文档服务器...$(NC)"
	mkdocs serve

.PHONY: docs-deploy
docs-deploy:
	@echo "$(BLUE)部署文档...$(NC)"
	mkdocs gh-deploy

# ================================
# 构建和发布
# ================================

.PHONY: build
build:
	@echo "$(BLUE)构建分发包...$(NC)"
	$(PYTHON) -m build
	@echo "$(GREEN)构建完成$(NC)"
	@ls -lh dist/

.PHONY: upload-test
upload-test: build
	@echo "$(BLUE)上传到 TestPyPI...$(NC)"
	$(PYTHON) -m twine upload --repository testpypi dist/*

.PHONY: upload
upload: build
	@echo "$(BLUE)上传到 PyPI...$(NC)"
	$(PYTHON) -m twine upload dist/*

# ================================
# 依赖分析
# ================================

.PHONY: deps
deps:
	@echo "$(BLUE)生成依赖关系图...$(NC)"
	$(PYTHON) -m pip install pipdeptree
	pipdeptree -p

.PHONY: deps-check
deps-check:
	@echo "$(BLUE)检查依赖更新...$(NC)"
	$(PYTHON) -m pip list --outdated

.PHONY: deps-audit
deps-audit:
	@echo "$(BLUE)审计依赖安全性...$(NC)"
	$(PYTHON) -m pip audit

# ================================
# 数据库和缓存（可选）
# ================================

.PHONY: db-reset
db-reset:
	@echo "$(YELLOW)重置数据库...$(NC)"
	# 根据实际数据库配置添加命令

.PHONY: cache-clear
cache-clear:
	@echo "$(YELLOW)清除缓存...$(NC)"
	find . -type d -name ".cache" -exec rm -rf {} +
	find . -type d -name "*.pyc" -exec rm -rf {} +

# ================================
# Docker（可选）
# ================================

.PHONY: docker-build
docker-build:
	@echo "$(BLUE)构建 Docker 镜像...$(NC)"
	docker build -t awesome-crawl4ai .

.PHONY: docker-run
docker-run:
	@echo "$(BLUE)运行 Docker 容器...$(NC)"
	docker run -it awesome-crawl4ai

# ================================
# CI/CD 辅助
# ================================

.PHONY: ci
ci: format-check lint typecheck test-cov security
	@echo "$(GREEN)CI 检查完成$(NC)"

.PHONY: ci-fast
ci-fast: format-check typecheck test-fast
	@echo "$(GREEN)快速 CI 检查完成$(NC)"

# ================================
# 信息显示
# ================================

.PHONY: info
info:
	@echo "$(BLUE)项目信息:$(NC)"
	@echo "  Python 版本: $$($(PYTHON) --version)"
	@echo "  pip 版本: $$($(PYTHON) -m pip --version)"
	@echo "  项目路径: $$(pwd)"
	@echo "  虚拟环境: $(VENV)"
	@if [ -d "$(VENV)" ]; then \
		echo "$(GREEN)✓ 虚拟环境已创建$(NC)"; \
	else \
		echo "$(RED)✗ 虚拟环境未创建$(NC)"; \
	fi

# ================================
# 快捷命令别名
# ================================

.PHONY: fmt
fmt: format

.PHONY: tc
tc: typecheck

.PHONY: tl
tl: test-lint

# ================================
# 注意事项
# ================================

# Windows 用户:
# 如果没有安装 Make，可以使用以下替代方案:
# 1. 安装 MinGW 或 Cygwin
# 2. 使用 PowerShell 脚本（可创建 Makefile.ps）
# 3. 直接运行命令（参考 help 输出）
#
# 示例:
#   make format   →  black . && isort .
#   make test     →  pytest
#   make install  →  pip install -e .
