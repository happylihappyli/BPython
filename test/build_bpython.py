#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
编译修改后的Python为bpython.exe
"""

import os
import sys
import subprocess
import time
import shutil

def setup_vs_environment():
    """设置Visual Studio环境变量"""
    vs_path = "D:\\Code\\VS2022\\Community"
    vcvarsall = os.path.join(vs_path, "VC", "Auxiliary", "Build", "vcvarsall.bat")
    
    if not os.path.exists(vcvarsall):
        print("错误: vcvarsall.bat 不存在")
        return False
    
    # 创建设置环境变量的批处理文件
    env_script = '''@echo off
call "{}" x64
python "{}" %*
'''.format(vcvarsall, os.path.abspath(__file__))
    
    env_bat = os.path.join(os.path.dirname(__file__), "setup_vs_env.bat")
    with open(env_bat, 'w') as f:
        f.write(env_script)
    
    print(f"✓ 已创建环境设置脚本: {env_bat}")
    return True

def check_grammar_modifications():
    """检查语法修改是否正确"""
    python_src_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src", "Python-3.12.2")
    grammar_file = os.path.join(python_src_dir, "Grammar", "python.gram")
    
    with open(grammar_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查是否包含大括号语法
    if "LBRACE" in content and "RBRACE" in content:
        print("✓ Grammar文件已正确修改")
        return True
    else:
        print("✗ Grammar文件修改不完整")
        return False

def build_with_pcbuild():
    """使用PCbuild编译Python"""
    python_src_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src", "Python-3.12.2")
    pcbuild_dir = os.path.join(python_src_dir, "PCbuild")
    
    if not os.path.exists(pcbuild_dir):
        print("错误: PCbuild目录不存在")
        return False
    
    # 检查构建脚本
    build_bat = os.path.join(pcbuild_dir, "build.bat")
    if not os.path.exists(build_bat):
        print("错误: build.bat 不存在")
        return False
    
    print("开始编译Python...")
    start_time = time.time()
    
    try:
        # 使用msbuild编译
        sln_file = os.path.join(pcbuild_dir, "pcbuild.sln")
        
        # 编译Release版本
        cmd = ["msbuild", sln_file, "/p:Configuration=Release", "/p:Platform=x64", "/m"]
        
        print(f"执行命令: {' '.join(cmd)}")
        # 使用字节模式捕获输出，避免编码问题
        result = subprocess.run(cmd, cwd=pcbuild_dir, capture_output=True)
        
        end_time = time.time()
        compile_time = end_time - start_time
        
        # 解码输出，处理可能的编码错误
        stdout = result.stdout.decode('utf-8', errors='replace')
        stderr = result.stderr.decode('utf-8', errors='replace')
        
        if result.returncode == 0:
            print(f"✓ 编译成功! 耗时: {compile_time:.2f}秒")
            print(stdout)
            return True
        else:
            print(f"✗ 编译失败! 耗时: {compile_time:.2f}秒")
            print("错误输出:")
            print(stderr)
            return False
            
    except Exception as e:
        print(f"编译过程中出错: {e}")
        return False

def rename_to_bpython():
    """重命名Python为bpython.exe"""
    python_src_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src", "Python-3.12.2")
    pcbuild_dir = os.path.join(python_src_dir, "PCbuild")
    
    # 查找编译生成的python.exe
    python_exe_path = os.path.join(pcbuild_dir, "amd64", "python.exe")
    if not os.path.exists(python_exe_path):
        # 尝试其他可能的路径
        python_exe_path = os.path.join(pcbuild_dir, "x64", "Release", "python.exe")
    
    if not os.path.exists(python_exe_path):
        print("错误: 未找到编译生成的python.exe")
        return False
    
    # 创建bin目录
    bin_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "bin")
    os.makedirs(bin_dir, exist_ok=True)
    
    # 重命名并复制到bin目录
    bpython_exe_path = os.path.join(bin_dir, "bpython.exe")
    
    try:
        shutil.copy2(python_exe_path, bpython_exe_path)
        print(f"✓ 已重命名为: {bpython_exe_path}")
        return True
    except Exception as e:
        print(f"重命名失败: {e}")
        return False

def test_bpython():
    """测试编译后的bpython.exe"""
    bin_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "bin")
    bpython_exe_path = os.path.join(bin_dir, "bpython.exe")
    
    if not os.path.exists(bpython_exe_path):
        print("错误: bpython.exe 不存在")
        return False
    
    print("测试bpython.exe...")
    
    try:
        # 测试版本信息
        result = subprocess.run([bpython_exe_path, "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ 版本测试成功: {result.stdout.strip()}")
        else:
            print(f"✗ 版本测试失败: {result.stderr}")
            return False
        
        # 测试简单Python代码
        test_code = "print('Hello from bpython!')"
        result = subprocess.run([bpython_exe_path, "-c", test_code], capture_output=True, text=True)
        if result.returncode == 0 and "Hello from bpython!" in result.stdout:
            print("✓ 代码执行测试成功")
        else:
            print(f"✗ 代码执行测试失败: {result.stderr}")
            return False
        
        return True
        
    except Exception as e:
        print(f"测试过程中出错: {e}")
        return False

def main():
    """主函数"""
    print("=== 编译bpython.exe ===")
    
    # 1. 检查语法修改
    print("\n1. 检查语法修改...")
    if not check_grammar_modifications():
        return
    
    # 2. 设置VS环境
    print("\n2. 设置Visual Studio环境...")
    if not setup_vs_environment():
        return
    
    # 3. 编译Python
    print("\n3. 编译Python源码...")
    if not build_with_pcbuild():
        print("编译失败，尝试备用编译方法...")
        # 这里可以添加备用编译方法
        return
    
    # 4. 重命名为bpython.exe
    print("\n4. 重命名为bpython.exe...")
    if not rename_to_bpython():
        return
    
    # 5. 测试编译结果
    print("\n5. 测试编译结果...")
    if not test_bpython():
        print("警告: 测试失败，但可执行文件已生成")
    
    print("\n=== 编译完成 ===")
    print("bpython.exe 已成功编译并放置在 bin 目录")
    
    # 播放完成提示
    try:
        import pyttsx3
        engine = pyttsx3.init()
        engine.say('bpython编译完毕，过来看看！')
        engine.runAndWait()
    except:
        print("TTS提示播放失败")

if __name__ == "__main__":
    main()