#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分步编译bpython.exe
"""

import os
import sys
import subprocess
import time

def compile_step_by_step():
    """分步编译bpython.exe"""
    
    # 获取Python源码目录
    python_src_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src", "Python-3.12.2")
    pcbuild_dir = os.path.join(python_src_dir, "PCbuild")
    
    print("============================================================")
    print("分步编译bpython.exe")
    print("============================================================")
    
    # 步骤1: 先编译一个基本的python.exe（不包含冻结模块）
    print("步骤1: 编译基本python.exe（不包含冻结模块）...")
    
    start_time = time.time()
    
    # 使用build.bat编译基本版本
    cmd = ["cmd", "/c", "build.bat", "-p", "x64", "-c", "Release", "python"]
    
    try:
        result = subprocess.run(cmd, cwd=pcbuild_dir, capture_output=True, text=True, encoding='utf-8', errors='replace')
        
        elapsed_time = time.time() - start_time
        
        if result.returncode == 0:
            print(f"✅ 基本python.exe编译成功! 耗时: {elapsed_time:.2f}秒")
            
            # 步骤2: 使用编译好的python.exe来构建冻结模块
            print("步骤2: 使用编译好的python.exe构建冻结模块...")
            
            # 首先检查编译好的python.exe是否存在
            python_exe_path = os.path.join(pcbuild_dir, "x64", "python.exe")
            if os.path.exists(python_exe_path):
                print(f"找到编译好的python.exe: {python_exe_path}")
                
                # 使用编译好的python.exe来运行deepfreeze.py
                deepfreeze_script = os.path.join(python_src_dir, "Tools", "build", "deepfreeze.py")
                
                if os.path.exists(deepfreeze_script):
                    print("运行deepfreeze.py生成冻结模块...")
                    
                    # 运行deepfreeze.py
                    cmd = [python_exe_path, deepfreeze_script]
                    result = subprocess.run(cmd, cwd=python_src_dir, capture_output=True, text=True, encoding='utf-8', errors='replace')
                    
                    if result.returncode == 0:
                        print("✅ 冻结模块生成成功!")
                        
                        # 步骤3: 完整编译Python
                        print("步骤3: 完整编译Python...")
                        
                        cmd = ["cmd", "/c", "build.bat", "-p", "x64", "-c", "Release"]
                        result = subprocess.run(cmd, cwd=pcbuild_dir, capture_output=True, text=True, encoding='utf-8', errors='replace')
                        
                        if result.returncode == 0:
                            print(f"✅ 完整Python编译成功!")
                            
                            # 步骤4: 重命名为bpython.exe
                            print("步骤4: 重命名为bpython.exe...")
                            
                            original_exe = os.path.join(pcbuild_dir, "x64", "python.exe")
                            new_exe = os.path.join(pcbuild_dir, "x64", "bpython.exe")
                            
                            if os.path.exists(original_exe):
                                os.rename(original_exe, new_exe)
                                print(f"✅ 重命名完成: {new_exe}")
                                
                                # 步骤5: 测试编译结果
                                print("步骤5: 测试编译结果...")
                                
                                test_cmd = [new_exe, "-c", "print('Hello from bpython!')"]
                                result = subprocess.run(test_cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
                                
                                if result.returncode == 0:
                                    print(f"✅ 测试成功! 输出: {result.stdout.strip()}")
                                    return True
                                else:
                                    print(f"❌ 测试失败! 错误: {result.stderr}")
                                    return False
                            else:
                                print("❌ 编译好的python.exe不存在")
                                return False
                        else:
                            print(f"❌ 完整Python编译失败!")
                            print(f"标准输出: {result.stdout}")
                            print(f"错误输出: {result.stderr}")
                            return False
                    else:
                        print(f"❌ 冻结模块生成失败!")
                        print(f"标准输出: {result.stdout}")
                        print(f"错误输出: {result.stderr}")
                        return False
                else:
                    print("❌ deepfreeze.py不存在")
                    return False
            else:
                print("❌ 编译好的python.exe不存在")
                return False
        else:
            print(f"❌ 基本python.exe编译失败! 耗时: {elapsed_time:.2f}秒")
            print(f"标准输出: {result.stdout}")
            print(f"错误输出: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ 编译过程出现异常: {e}")
        return False

if __name__ == "__main__":
    if compile_step_by_step():
        print("\n🎉 bpython.exe编译完成!")
    else:
        print("\n💥 bpython.exe编译失败!")