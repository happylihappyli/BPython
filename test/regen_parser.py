#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
重新生成Python parser文件的脚本
使用--regen选项重新生成opcodes、grammar和tokens
"""

import os
import subprocess
import sys
import time

def regen_parser_files():
    """重新生成parser文件"""
    python_src_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src", "Python-3.12.2")
    pcbuild_dir = os.path.join(python_src_dir, "PCbuild")
    
    if not os.path.exists(pcbuild_dir):
        print("✗ PCbuild目录不存在")
        return False
    
    # 检查构建脚本
    build_bat = os.path.join(pcbuild_dir, "build.bat")
    if not os.path.exists(build_bat):
        print("✗ build.bat 不存在")
        return False
    
    print("开始重新生成parser文件...")
    start_time = time.time()
    
    try:
        # 使用--regen选项重新生成文件
        cmd = ["cmd", "/c", "build.bat", "--regen"]
        
        print(f"执行命令: {' '.join(cmd)}")
        # 使用字节模式捕获输出，避免编码问题
        result = subprocess.run(cmd, cwd=pcbuild_dir, capture_output=True)
        
        end_time = time.time()
        regen_time = end_time - start_time
        
        # 解码输出，处理可能的编码错误
        stdout = result.stdout.decode('utf-8', errors='replace')
        stderr = result.stderr.decode('utf-8', errors='replace')
        
        if result.returncode == 0:
            print(f"✓ 重新生成成功! 耗时: {regen_time:.2f}秒")
            print("输出:")
            print(stdout)
            
            # 检查parser.c文件是否已更新
            parser_c_file = os.path.join(python_src_dir, "Parser", "parser.c")
            if os.path.exists(parser_c_file):
                print(f"✓ parser.c 文件已更新")
                
                # 检查是否包含LBRACE_rule和RBRACE_rule
                with open(parser_c_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                if 'LBRACE_rule' in content and 'RBRACE_rule' in content:
                    print("✓ LBRACE_rule 和 RBRACE_rule 已生成")
                else:
                    print("⚠ LBRACE_rule 和 RBRACE_rule 可能未正确生成")
            
            return True
        else:
            print(f"✗ 重新生成失败! 耗时: {regen_time:.2f}秒")
            print("错误输出:")
            print(stderr)
            return False
            
    except Exception as e:
        print(f"重新生成过程中出错: {e}")
        return False

def check_parser_files():
    """检查parser文件状态"""
    python_src_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src", "Python-3.12.2")
    
    # 检查关键文件
    files_to_check = [
        "Parser/parser.c",
        "Parser/parser.h",
        "Include/token.h",
        "Grammar/Tokens"
    ]
    
    print("检查parser文件状态:")
    for file_path in files_to_check:
        full_path = os.path.join(python_src_dir, file_path)
        if os.path.exists(full_path):
            print(f"✓ {file_path} 存在")
            
            # 检查文件大小
            size = os.path.getsize(full_path)
            print(f"  大小: {size} 字节")
            
            # 检查是否包含LBRACE和RBRACE
            if file_path == "Parser/parser.c":
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                if 'LBRACE_rule' in content:
                    print("  ✓ 包含 LBRACE_rule")
                else:
                    print("  ✗ 不包含 LBRACE_rule")
                    
                if 'RBRACE_rule' in content:
                    print("  ✓ 包含 RBRACE_rule")
                else:
                    print("  ✗ 不包含 RBRACE_rule")
        else:
            print(f"✗ {file_path} 不存在")

def main():
    """主函数"""
    print("=" * 60)
    print("重新生成Python parser文件")
    print("=" * 60)
    
    # 首先检查当前状态
    check_parser_files()
    
    print("\n" + "=" * 60)
    
    # 重新生成parser文件
    if regen_parser_files():
        print("\n重新生成完成，检查结果:")
        check_parser_files()
        
        # 播放语音提示
        try:
            import pyttsx3
            engine = pyttsx3.init()
            engine.say("parser文件重新生成完毕，过来看看！")
            engine.runAndWait()
        except:
            print("语音提示不可用")
    else:
        print("重新生成失败")

if __name__ == "__main__":
    main()