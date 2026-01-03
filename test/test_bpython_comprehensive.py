#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
综合测试 bpython 的脚本
包括语法验证、编译状态检查和功能测试
"""

import os
import sys
import subprocess
from pathlib import Path

def check_compilation_status():
    """检查编译状态"""
    print("=== 检查编译状态 ===")
    
    python_src_dir = Path("src/Python-3.12.2")
    pcbuild_dir = python_src_dir / "PCbuild"
    amd64_dir = pcbuild_dir / "amd64"
    
    # 检查关键文件是否存在
    key_files = [
        (amd64_dir / "python.exe", "Python 解释器"),
        (amd64_dir / "python3.dll", "Python 动态库"),
        (amd64_dir / "_freeze_module.exe", "冻结模块工具"),
        (pcbuild_dir / "python.bat", "Python 批处理文件")
    ]
    
    for file_path, description in key_files:
        if file_path.exists():
            print(f"✓ {description}: {file_path}")
        else:
            print(f"✗ {description}: 文件不存在")
    
    # 检查 bpython.exe
    bpython_exe = amd64_dir / "bpython.exe"
    if bpython_exe.exists():
        print(f"✓ bpython.exe: {bpython_exe}")
        return True
    else:
        print(f"✗ bpython.exe: 文件不存在")
        return False

def test_grammar_modifications():
    """测试语法修改"""
    print("\n=== 测试语法修改 ===")
    
    # 检查语法文件修改
    grammar_file = Path("src/Python-3.12.2/Grammar/python.gram")
    if grammar_file.exists():
        with open(grammar_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 检查是否包含大括号语法
        if 'LBRACE' in content or 'RBRACE' in content:
            print("✓ 语法文件已修改为使用大括号")
        else:
            print("✗ 语法文件未正确修改")
            
        # 检查是否移除了 INDENT/DEDENT
        if 'INDENT' not in content and 'DEDENT' not in content:
            print("✓ 已移除 INDENT/DEDENT")
        else:
            print("✗ INDENT/DEDENT 仍然存在")
    else:
        print("✗ 语法文件不存在")

def test_with_existing_python():
    """使用现有的 Python 解释器测试语法"""
    print("\n=== 使用现有 Python 测试语法 ===")
    
    # 测试脚本路径
    test_script = Path("test/test_bpython_syntax.py")
    
    if test_script.exists():
        print(f"测试脚本: {test_script}")
        
        # 尝试使用系统 Python 运行测试脚本
        try:
            result = subprocess.run([
                sys.executable, str(test_script)
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                print("✓ 测试脚本可以正常执行（使用标准 Python）")
                print("输出:")
                print(result.stdout)
            else:
                print("✗ 测试脚本执行失败")
                print("错误输出:")
                print(result.stderr)
                
        except subprocess.TimeoutExpired:
            print("✗ 测试脚本执行超时")
        except Exception as e:
            print(f"✗ 执行测试脚本时出错: {e}")
    else:
        print("✗ 测试脚本不存在")

def test_compiled_python():
    """测试已编译的 Python 解释器"""
    print("\n=== 测试已编译的 Python 解释器 ===")
    
    python_exe = Path("src/Python-3.12.2/PCbuild/amd64/python.exe")
    
    if python_exe.exists():
        print(f"找到已编译的 Python: {python_exe}")
        
        # 测试基本功能
        try:
            # 测试版本信息
            result = subprocess.run([
                str(python_exe), "--version"
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                print("✓ Python 解释器可以运行")
                print(f"版本信息: {result.stdout.strip()}")
                
                # 测试简单的 Python 代码
                test_code = "print('Hello from compiled Python!')"
                result = subprocess.run([
                    str(python_exe), "-c", test_code
                ], capture_output=True, text=True, timeout=10)
                
                if result.returncode == 0:
                    print("✓ 可以执行简单 Python 代码")
                    print(f"输出: {result.stdout.strip()}")
                else:
                    print("✗ 执行 Python 代码失败")
                    
            else:
                print("✗ Python 解释器无法运行")
                
        except subprocess.TimeoutExpired:
            print("✗ 测试超时")
        except Exception as e:
            print(f"✗ 测试过程中出错: {e}")
    else:
        print("✗ 已编译的 Python 解释器不存在")

def check_build_errors():
    """检查构建错误"""
    print("\n=== 检查构建错误 ===")
    
    # 检查构建日志或错误文件
    build_logs = [
        Path("build.log"),
        Path("src/Python-3.12.2/PCbuild/build.log"),
        Path("test/build_errors.txt")
    ]
    
    for log_file in build_logs:
        if log_file.exists():
            print(f"找到构建日志: {log_file}")
            try:
                with open(log_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # 检查常见错误
                errors = []
                if "error LNK" in content:
                    errors.append("链接器错误")
                if "syntax error" in content:
                    errors.append("语法错误")
                if "undefined symbol" in content:
                    errors.append("未定义符号")
                if "deepfreeze" in content.lower():
                    errors.append("deepfreeze 过程错误")
                    
                if errors:
                    print(f"发现错误: {', '.join(errors)}")
                else:
                    print("未发现明显错误")
                    
            except Exception as e:
                print(f"读取日志文件时出错: {e}")
            break
    else:
        print("未找到构建日志文件")

def suggest_next_steps():
    """建议下一步操作"""
    print("\n=== 建议下一步操作 ===")
    
    python_exe = Path("src/Python-3.12.2/PCbuild/amd64/python.exe")
    
    if python_exe.exists():
        print("1. 尝试使用已编译的 Python 解释器测试大括号语法")
        print("2. 检查 deepfreeze 过程的问题")
        print("3. 手动生成缺失的符号")
        print("4. 尝试简化编译配置")
    else:
        print("1. 重新编译 Python 源代码")
        print("2. 检查编译环境配置")
        print("3. 解决链接器错误")
        print("4. 确保所有依赖项正确安装")
    
    print("\n具体建议:")
    print("- 运行 'python test/build_bpython_comprehensive.py' 进行完整编译")
    print("- 检查 deepfreeze.py 脚本的执行")
    print("- 验证 _freeze_module.exe 是否可以正确运行")

def main():
    """主测试函数"""
    print("BPython 综合测试")
    print("=" * 60)
    
    # 检查编译状态
    bpython_available = check_compilation_status()
    
    # 测试语法修改
    test_grammar_modifications()
    
    # 使用现有 Python 测试语法
    test_with_existing_python()
    
    # 测试已编译的 Python
    test_compiled_python()
    
    # 检查构建错误
    check_build_errors()
    
    # 建议下一步操作
    suggest_next_steps()
    
    print("\n" + "=" * 60)
    
    if bpython_available:
        print("✓ bpython.exe 已生成，可以进行测试")
    else:
        print("✗ bpython.exe 尚未生成，需要解决编译问题")

if __name__ == "__main__":
    main()