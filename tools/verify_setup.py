#!/usr/bin/env python3
"""
Awesome-crawl4AI - 开发环境验证脚本

此脚本用于验证开发环境是否正确配置，包括：
- Python 版本检查
- 依赖包安装检查
- 配置文件存在性检查
- 工具可用性检查

使用方法:
    python tools/verify_setup.py

退出码:
    0 - 所有检查通过
    1 - 部分检查失败
"""

import os
import sys
import subprocess
from pathlib import Path
from typing import List, Tuple, Dict

# ANSI 颜色代码
class Colors:
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BLUE = "\033[94m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"


def print_success(message: str) -> None:
    """打印成功消息"""
    print(f"{Colors.GREEN}[OK]{Colors.ENDC} {message}")


def print_warning(message: str) -> None:
    """打印警告消息"""
    print(f"{Colors.YELLOW}[WARN]{Colors.ENDC} {message}")


def print_error(message: str) -> None:
    """打印错误消息"""
    print(f"{Colors.RED}[FAIL]{Colors.ENDC} {message}")


def print_info(message: str) -> None:
    """打印信息消息"""
    print(f"{Colors.BLUE}[INFO]{Colors.ENDC} {message}")


def print_header(message: str) -> None:
    """打印标题"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'=' * 60}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.BLUE}{message.center(60)}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'=' * 60}{Colors.ENDC}\n")


def get_project_root() -> Path:
    """获取项目根目录"""
    # 从当前脚本向上查找项目根目录
    current = Path(__file__).resolve()
    while current != current.parent:
        if (current / "CLAUDE.md").exists():
            return current
        current = current.parent
    return Path.cwd()


def check_python_version() -> bool:
    """检查 Python 版本"""
    print_header("Python 版本检查")

    version = sys.version_info
    print_info(f"当前 Python 版本: {version.major}.{version.minor}.{version.micro}")

    if version.major == 3 and version.minor >= 9:
        print_success("Python 版本符合要求 (>= 3.9)")
        return True
    else:
        print_error("Python 版本过低，需要 3.9 或更高版本")
        return False


def check_config_files(root: Path) -> Dict[str, bool]:
    """检查配置文件是否存在"""
    print_header("配置文件检查")

    config_files = {
        "pyproject.toml": root / "pyproject.toml",
        "setup.cfg": root / "setup.cfg",
        ".pre-commit-config.yaml": root / ".pre-commit-config.yaml",
        "Makefile": root / "Makefile",
        "requirements.txt": root / "requirements.txt",
        "requirements-dev.txt": root / "requirements-dev.txt",
        ".editorconfig": root / ".editorconfig",
        ".gitignore": root / ".gitignore",
        ".vscode/settings.json": root / ".vscode" / "settings.json",
    }

    results = {}
    for name, path in config_files.items():
        if path.exists():
            print_success(f"{name} 存在")
            results[name] = True
        else:
            print_error(f"{name} 不存在")
            results[name] = False

    return results


def check_executables() -> Dict[str, bool]:
    """检查命令行工具是否可用"""
    print_header("命令行工具检查")

    tools = {
        "black": "black --version",
        "isort": "isort --version",
        "flake8": "flake8 --version",
        "mypy": "mypy --version",
        "pytest": "pytest --version",
        "pre-commit": "pre-commit --version",
    }

    results = {}
    for name, command in tools.items():
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                version = result.stdout.split('\n')[0]
                print_success(f"{name}: {version}")
                results[name] = True
            else:
                print_error(f"{name} 不可用")
                results[name] = False
        except (subprocess.TimeoutExpired, FileNotFoundError):
            print_error(f"{name} 未安装")
            results[name] = False

    return results


def check_python_packages() -> Dict[str, bool]:
    """检查 Python 包是否已安装"""
    print_header("Python 包检查")

    packages = [
        "httpx",
        "beautifulsoup4",
        "aiohttp",
        "pydantic",
        "pytest",
        "black",
        "isort",
        "flake8",
        "mypy",
        "pre-commit",
    ]

    results = {}
    for package in packages:
        try:
            __import__(package)
            print_success(f"{package} 已安装")
            results[package] = True
        except ImportError:
            print_warning(f"{package} 未安装")
            results[package] = False

    return results


def check_directory_structure(root: Path) -> Dict[str, bool]:
    """检查项目目录结构"""
    print_header("目录结构检查")

    directories = {
        "packages": root / "packages",
        "tests": root / "tests",
        "docs": root / "docs",
        "examples": root / "examples",
        "tools": root / "tools",
        ".vscode": root / ".vscode",
    }

    results = {}
    for name, path in directories.items():
        if path.exists() and path.is_dir():
            print_success(f"{name}/ 目录存在")
            results[name] = True
        else:
            print_warning(f"{name}/ 目录不存在")
            results[name] = False

    return results


def run_quick_tests() -> bool:
    """运行快速测试"""
    print_header("快速功能测试")

    # 测试 1: Black 格式化检查
    print_info("测试 Black 配置...")
    try:
        result = subprocess.run(
            ["black", "--check", "--config", "pyproject.toml", "pyproject.toml"],
            capture_output=True,
            timeout=10
        )
        if result.returncode == 0:
            print_success("Black 配置正确")
        else:
            print_warning("Black 配置可能有问题")
    except Exception as e:
        print_warning(f"Black 测试失败: {e}")

    # 测试 2: pytest 可用性
    print_info("测试 pytest...")
    try:
        result = subprocess.run(
            ["pytest", "--version"],
            capture_output=True,
            timeout=5
        )
        if result.returncode == 0:
            print_success("pytest 可用")
        else:
            print_warning("pytest 不可用")
    except Exception as e:
        print_warning(f"pytest 测试失败: {e}")

    return True


def print_summary(results: Dict[str, Dict[str, bool]]) -> None:
    """打印检查摘要"""
    print_header("检查摘要")

    total_checks = 0
    passed_checks = 0

    for category, checks in results.items():
        category_passed = sum(checks.values())
        category_total = len(checks)
        total_checks += category_total
        passed_checks += category_passed

        status = f"{category_passed}/{category_total}"
        if category_passed == category_total:
            print_success(f"{category}: {status}")
        else:
            print_warning(f"{category}: {status}")

    print(f"\n总计: {passed_checks}/{total_checks} 检查通过")

    if passed_checks == total_checks:
        print(f"\n{Colors.GREEN}{Colors.BOLD}所有检查通过！开发环境已就绪。{Colors.ENDC}\n")
    else:
        print(f"\n{Colors.YELLOW}{Colors.BOLD}部分检查失败，请根据上述提示进行配置。{Colors.ENDC}\n")


def main() -> int:
    """主函数"""
    print(f"\n{Colors.BOLD}Awesome-crawl4AI - 开发环境验证{Colors.ENDC}")
    print(f"{Colors.BOLD}{'=' * 60}{Colors.ENDC}\n")

    results = {}

    # 1. Python 版本检查
    results["Python 版本"] = {"版本": check_python_version()}

    # 2. 配置文件检查
    root = get_project_root()
    results["配置文件"] = check_config_files(root)

    # 3. 命令行工具检查
    results["命令行工具"] = check_executables()

    # 4. Python 包检查
    results["Python 包"] = check_python_packages()

    # 5. 目录结构检查
    results["目录结构"] = check_directory_structure(root)

    # 6. 快速功能测试
    run_quick_tests()

    # 打印摘要
    print_summary(results)

    # 返回退出码
    all_passed = all(
        all(checks.values())
        for checks in results.values()
        if isinstance(checks, dict)
    )

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
