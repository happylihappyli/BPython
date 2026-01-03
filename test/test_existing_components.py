#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试现有编译组件的脚本
"""

import os
import subprocess
from pathlib import Path

def test_freeze_module():
    """测试 _freeze_module.exe"""
    print("=== 测试 _freeze_module.exe ===")
    
    freeze_exe = Path("src/Python-3.12.2/PCbuild/amd64/_freeze_module.exe")
    
    if freeze_exe.exists():
        print(f"找到 _freeze_module.exe: {freeze_exe}")
        
        # 测试 _freeze_module.exe 是否可以运行
        try:
            result = subprocess.run([
                str(freeze_exe), "--help"
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                print("✓ _freeze_module.exe 可以运行")
                print("输出:")
                print(result.stdout)
            else:
                print("✗ _freeze_module.exe 运行失败")
                print("错误输出:")
                print(result.stderr)
                
        except subprocess.TimeoutExpired:
            print("✗ 测试超时")
        except Exception as e:
            print(f"✗ 测试过程中出错: {e}")
    else:
        print("✗ _freeze_module.exe 不存在")

def test_python_dll():
    """测试 Python 动态库"""
    print("\n=== 测试 Python 动态库 ===")
    
    python_dll = Path("src/Python-3.12.2/PCbuild/amd64/python3.dll")
    
    if python_dll.exists():
        print(f"✓ Python 动态库存在: {python_dll}")
        
        # 检查文件大小
        size = python_dll.stat().st_size
        print(f"文件大小: {size:,} 字节")
        
        # 检查是否可以加载
        try:
            import ctypes
            dll = ctypes.WinDLL(str(python_dll))
            print("✓ 可以加载 Python 动态库")
        except Exception as e:
            print(f"✗ 加载 Python 动态库失败: {e}")
    else:
        print("✗ Python 动态库不存在")

def check_grammar_file():
    """检查语法文件状态"""
    print("\n=== 检查语法文件状态 ===")
    
    grammar_file = Path("src/Python-3.12.2/Grammar/python.gram")
    
    if grammar_file.exists():
        with open(grammar_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查关键修改
        checks = [
            ("LBRACE", "左大括号令牌"),
            ("RBRACE", "右大括号令牌"), 
            ("'{'", "左大括号字符"),
            ("'}'", "右大括号字符"),
            ("INDENT", "缩进令牌"),
            ("DEDENT", "取消缩进令牌")
        ]
        
        for pattern, description in checks:
            if pattern in content:
                print(f"✓ {description}: 存在")
            else:
                print(f"✗ {description}: 不存在")
    else:
        print("✗ 语法文件不存在")

def suggest_fixes():
    """建议修复方案"""
    print("\n=== 建议修复方案 ===")
    
    print("1. 重新应用语法修改:")
    print("   - 运行 'python test/modify_python_grammar.py'")
    print("   - 运行 'python test/modify_tokenizer.py'")
    
    print("\n2. 重新生成解析器:")
    print("   - 运行 'python test/regen_parser.py'")
    
    print("\n3. 尝试简化编译:")
    print("   - 运行 'python test/build_bpython_comprehensive.py'")
    print("   - 或运行 'python test/compile_step_by_step.py'")
    
    print("\n4. 检查 deepfreeze 过程:")
    print("   - 运行 'python test/generate_real_deepfreeze.py'")
    print("   - 检查 deepfreeze.py 脚本")

def main():
    """主测试函数"""
    print("现有组件测试")
    print("=" * 50)
    
    test_freeze_module()
    test_python_dll()
    check_grammar_file()
    suggest_fixes()
    
    print("\n" + "=" * 50)
    print("测试完成")

if __name__ == "__main__":
    main()