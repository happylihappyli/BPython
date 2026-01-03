#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查编译环境和依赖
"""

import os
import sys
import subprocess
import platform

def check_visual_studio():
    """检查Visual Studio安装"""
    vs_path = "D:\\Code\\VS2022\\Community"
    if os.path.exists(vs_path):
        print(f"✓ Visual Studio 2022 已安装: {vs_path}")
        
        # 检查VCVARSALL
        vcvarsall = os.path.join(vs_path, "VC", "Auxiliary", "Build", "vcvarsall.bat")
        if os.path.exists(vcvarsall):
            print(f"✓ vcvarsall.bat 存在: {vcvarsall}")
            return True
        else:
            print(f"✗ vcvarsall.bat 不存在")
            return False
    else:
        print(f"✗ Visual Studio 2022 未找到")
        return False

def check_build_tools():
    """检查构建工具"""
    tools_to_check = ["cl", "nmake", "msbuild"]
    
    for tool in tools_to_check:
        try:
            result = subprocess.run(["where", tool], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✓ {tool} 已安装")
            else:
                print(f"✗ {tool} 未找到")
        except Exception as e:
            print(f"✗ 检查 {tool} 时出错: {e}")

def check_python_dependencies():
    """检查Python编译依赖"""
    python_src_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src", "Python-3.12.2")
    
    # 检查必要的文件
    required_files = [
        "PCbuild\build.bat",
        "PCbuild\pcbuild.sln",
        "configure",
        "Makefile"
    ]
    
    for file in required_files:
        file_path = os.path.join(python_src_dir, file)
        if os.path.exists(file_path):
            print(f"✓ {file} 存在")
        else:
            print(f"✗ {file} 不存在")

def check_system_info():
    """检查系统信息"""
    print(f"操作系统: {platform.system()} {platform.release()}")
    print(f"系统版本: {platform.version()}")
    print(f"处理器: {platform.processor()}")
    print(f"Python版本: {sys.version}")

def main():
    """主函数"""
    print("=== 编译环境检查 ===")
    
    # 检查系统信息
    print("\n1. 系统信息:")
    check_system_info()
    
    # 检查Visual Studio
    print("\n2. Visual Studio 检查:")
    vs_ok = check_visual_studio()
    
    # 检查构建工具
    print("\n3. 构建工具检查:")
    check_build_tools()
    
    # 检查Python依赖
    print("\n4. Python源码依赖检查:")
    check_python_dependencies()
    
    # 总结
    print("\n=== 检查结果 ===")
    if vs_ok:
        print("✓ 编译环境基本满足要求")
        print("可以开始编译Python")
    else:
        print("✗ 编译环境不完整")
        print("请确保Visual Studio 2022正确安装")

if __name__ == "__main__":
    main()