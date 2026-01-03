#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成缺失的冻结模块头文件
"""

import os
import sys
import subprocess

def generate_frozen_module(module_name, output_header):
    """
    生成单个模块的冻结头文件
    """
    print(f"正在生成模块 {module_name} 的冻结头文件...")
    
    # 构建_freeze_module.exe的完整路径
    freeze_module_exe = os.path.join(os.path.dirname(__file__), "..", "src", "Python-3.12.2", "PCbuild", "win32", "_freeze_module.exe")
    
    if not os.path.exists(freeze_module_exe):
        print(f"错误: 找不到 _freeze_module.exe 在 {freeze_module_exe}")
        return False
    
    # 构建Python源文件路径
    if '.' in module_name:
        # 处理子模块，如 importlib.util
        parts = module_name.split('.')
        py_file = os.path.join(os.path.dirname(__file__), "..", "src", "Python-3.12.2", "Lib", *parts) + ".py"
    else:
        # 处理顶级模块
        py_file = os.path.join(os.path.dirname(__file__), "..", "src", "Python-3.12.2", "Lib", module_name + ".py")
    
    if not os.path.exists(py_file):
        print(f"错误: 找不到Python源文件 {py_file}")
        return False
    
    # 构建输出目录
    output_dir = os.path.dirname(output_header)
    os.makedirs(output_dir, exist_ok=True)
    
    # 运行_freeze_module.exe
    cmd = [freeze_module_exe, module_name, py_file, output_header]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=os.path.dirname(freeze_module_exe))
        if result.returncode == 0:
            print(f"成功生成 {output_header}")
            return True
        else:
            print(f"生成失败: {result.stderr}")
            return False
    except Exception as e:
        print(f"执行错误: {e}")
        return False

def main():
    """
    主函数：生成所有缺失的冻结模块头文件
    """
    # 缺失的模块列表（根据编译错误）
    missing_modules = [
        "_sitebuiltins",
        "genericpath", 
        "ntpath",
        "posixpath",
        "os",
        "site",
        "stat",
        "importlib.util",
        "importlib.machinery",
        "runpy",
        "__hello__",
        "__phello__",
        "__phello__.ham",
        "__phello__.ham.eggs",
        "__phello__.spam",
        "frozen_only"
    ]
    
    # 基础路径
    base_dir = os.path.join(os.path.dirname(__file__), "..", "src", "Python-3.12.2")
    frozen_modules_dir = os.path.join(base_dir, "Python", "frozen_modules")
    
    success_count = 0
    failed_modules = []
    
    for module_name in missing_modules:
        # 构建输出文件名
        header_name = module_name.replace('.', '_').replace('__', '_') + ".h"
        output_header = os.path.join(frozen_modules_dir, header_name)
        
        # 如果文件已经存在，跳过
        if os.path.exists(output_header):
            print(f"模块 {module_name} 的冻结头文件已存在，跳过")
            success_count += 1
            continue
        
        # 生成冻结头文件
        if generate_frozen_module(module_name, output_header):
            success_count += 1
        else:
            failed_modules.append(module_name)
    
    print(f"\n生成完成: 成功 {success_count}/{len(missing_modules)}")
    if failed_modules:
        print(f"失败的模块: {failed_modules}")
    else:
        print("所有模块都已成功生成！")

if __name__ == "__main__":
    main()