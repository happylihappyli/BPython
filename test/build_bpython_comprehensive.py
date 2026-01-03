#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全面构建bpython.exe - 分阶段编译
"""

import os
import sys
import subprocess
import time
import shutil

def build_bpython_comprehensive():
    """全面构建bpython.exe"""
    
    # 获取Python源码目录
    python_src_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src", "Python-3.12.2")
    pcbuild_dir = os.path.join(python_src_dir, "PCbuild")
    
    print("============================================================")
    print("全面构建bpython.exe")
    print("============================================================")
    
    # 阶段1: 准备环境
    print("阶段1: 准备编译环境...")
    
    # 备份原始的标准库文件
    lib_dir = os.path.join(python_src_dir, "Lib")
    backup_dir = os.path.join(lib_dir, "backup_original")
    
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
        print(f"创建备份目录: {backup_dir}")
    
    # 备份重要的标准库文件
    important_files = ["importlib/_bootstrap.py", "opcode.py"]
    
    for file_path in important_files:
        src_file = os.path.join(lib_dir, file_path)
        backup_file = os.path.join(backup_dir, file_path.replace("/", "_"))
        
        if os.path.exists(src_file) and not os.path.exists(backup_file):
            shutil.copy2(src_file, backup_file)
            print(f"备份: {src_file} -> {backup_file}")
    
    # 阶段2: 恢复原始语法的重要文件
    print("阶段2: 恢复原始语法的重要文件...")
    
    # 恢复opcode.py为原始语法（因为编译系统需要它）
    opcode_py = os.path.join(lib_dir, "opcode.py")
    if os.path.exists(opcode_py):
        # 读取当前内容
        with open(opcode_py, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否包含大括号语法
        if '{' in content and '}' in content:
            print("检测到opcode.py使用大括号语法，恢复为缩进语法...")
            
            # 简单的恢复：将大括号转换为缩进
            content = content.replace('{', '')
            content = content.replace('}', '')
            
            # 写入恢复后的内容
            with open(opcode_py, 'w', encoding='utf-8') as f:
                f.write(content)
            print("✅ opcode.py已恢复为缩进语法")
    
    # 阶段3: 编译基本Python解释器
    print("阶段3: 编译基本Python解释器...")
    
    start_time = time.time()
    
    # 使用build.bat编译基本版本
    cmd = ["cmd", "/c", "build.bat", "-p", "x64", "-c", "Release"]
    
    try:
        result = subprocess.run(cmd, cwd=pcbuild_dir, capture_output=True, text=True, encoding='utf-8', errors='replace')
        
        elapsed_time = time.time() - start_time
        
        if result.returncode == 0:
            print(f"✅ 基本Python解释器编译成功! 耗时: {elapsed_time:.2f}秒")
            
            # 检查编译结果
            python_exe_path = os.path.join(pcbuild_dir, "x64", "python.exe")
            if os.path.exists(python_exe_path):
                print(f"✅ 编译好的python.exe: {python_exe_path}")
                
                # 阶段4: 恢复大括号语法
                print("阶段4: 恢复大括号语法...")
                
                # 恢复importlib/_bootstrap.py的大括号语法
                bootstrap_file = os.path.join(lib_dir, "importlib", "_bootstrap.py")
                if os.path.exists(bootstrap_file):
                    # 读取备份的原始内容
                    backup_bootstrap = os.path.join(backup_dir, "importlib__bootstrap.py")
                    
                    if os.path.exists(backup_bootstrap):
                        with open(backup_bootstrap, 'r', encoding='utf-8') as f:
                            original_content = f.read()
                        
                        # 将缩进语法转换为大括号语法
                        converted_content = convert_to_braces(original_content)
                        
                        # 写入转换后的内容
                        with open(bootstrap_file, 'w', encoding='utf-8') as f:
                            f.write(converted_content)
                        
                        print("✅ importlib/_bootstrap.py已恢复为大括号语法")
                
                # 阶段5: 重命名为bpython.exe
                print("阶段5: 重命名为bpython.exe...")
                
                bpython_exe_path = os.path.join(pcbuild_dir, "x64", "bpython.exe")
                
                if os.path.exists(python_exe_path):
                    os.rename(python_exe_path, bpython_exe_path)
                    print(f"✅ 重命名为: {bpython_exe_path}")
                    
                    # 阶段6: 测试编译结果
                    print("阶段6: 测试编译结果...")
                    
                    # 测试基本功能
                    test_cmd = [bpython_exe_path, "-c", "print('Hello from bpython!')"]
                    result = subprocess.run(test_cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
                    
                    if result.returncode == 0:
                        print(f"✅ 基本测试成功! 输出: {result.stdout.strip()}")
                        
                        # 测试大括号语法
                        test_brace_code = '''
def test_brace_syntax() {\n    x = 5\n    if x > 3 {\n        print("大括号语法工作正常!")\n    }\n}\n\ntest_brace_syntax()'''
                        
                        # 写入测试文件
                        test_file = os.path.join(pcbuild_dir, "test_brace.py")
                        with open(test_file, 'w', encoding='utf-8') as f:
                            f.write(test_brace_code)
                        
                        # 运行测试
                        test_cmd = [bpython_exe_path, test_file]
                        result = subprocess.run(test_cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
                        
                        if result.returncode == 0:
                            print(f"✅ 大括号语法测试成功! 输出: {result.stdout.strip()}")
                            
                            # 清理测试文件
                            if os.path.exists(test_file):
                                os.remove(test_file)
                            
                            return True
                        else:
                            print(f"❌ 大括号语法测试失败! 错误: {result.stderr}")
                            return False
                    else:
                        print(f"❌ 基本测试失败! 错误: {result.stderr}")
                        return False
                else:
                    print("❌ 编译好的python.exe不存在")
                    return False
            else:
                print("❌ 编译好的python.exe不存在")
                return False
        else:
            print(f"❌ 基本Python解释器编译失败! 耗时: {elapsed_time:.2f}秒")
            print(f"标准输出: {result.stdout}")
            print(f"错误输出: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ 编译过程出现异常: {e}")
        return False

def convert_to_braces(content):
    """将缩进语法转换为大括号语法"""
    lines = content.split('\n')
    result = []
    indent_stack = []
    
    for line in lines:
        stripped = line.lstrip()
        if not stripped:
            result.append(line)
            continue
            
        indent_level = len(line) - len(stripped)
        
        # 处理缩进变化
        while indent_stack and indent_stack[-1] > indent_level:
            result.append(' ' * indent_stack.pop() + '}')
        
        if indent_stack and indent_stack[-1] < indent_level:
            # 增加缩进
            result.append(' ' * indent_stack[-1] + '{')
            indent_stack.append(indent_level)
        elif not indent_stack and indent_level > 0:
            # 第一个缩进
            result.append('{')
            indent_stack.append(indent_level)
        
        result.append(line)
    
    # 关闭所有剩余的缩进
    while indent_stack:
        result.append(' ' * indent_stack.pop() + '}')
    
    return '\n'.join(result)

if __name__ == "__main__":
    if build_bpython_comprehensive():
        print("\n🎉 bpython.exe构建完成!")
        
        # 播放语音提示
        try:
            import pyttsx3
            engine = pyttsx3.init()
            engine.say("任务运行完毕，过来看看！")
            engine.runAndWait()
        except:
            print("语音提示不可用")
    else:
        print("\n💥 bpython.exe构建失败!")