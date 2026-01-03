#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
恢复标准库文件为原始语法，以便编译能够继续
"""

import os
import shutil
import time

def restore_stdlib():
    """恢复标准库文件为原始语法"""
    
    # 获取Python源码目录
    python_src_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src", "Python-3.12.2")
    lib_dir = os.path.join(python_src_dir, "Lib")
    
    print("============================================================")
    print("恢复标准库文件为原始语法")
    print("============================================================")
    
    # 需要恢复的关键文件列表
    critical_files = [
        "importlib/_bootstrap.py",
        "importlib/_bootstrap_external.py", 
        "zipimport.py",
        "abc.py",
        "codecs.py",
        "io.py",
        "_collections_abc.py",
        "_sitebuiltins.py",
        "genericpath.py",
        "ntpath.py",
        "posixpath.py",
        "os.py",
        "site.py",
        "stat.py",
        "importlib/util.py",
        "importlib/machinery.py",
        "runpy.py"
    ]
    
    # 检查备份目录
    backup_dir = os.path.join(lib_dir, "backup_original")
    
    if not os.path.exists(backup_dir):
        print(f"❌ 备份目录不存在: {backup_dir}")
        print("无法恢复标准库文件")
        return False
    
    print(f"✅ 找到备份目录: {backup_dir}")
    
    # 恢复每个关键文件
    restored_count = 0
    for file_path in critical_files:
        src_file = os.path.join(lib_dir, file_path)
        backup_file = os.path.join(backup_dir, file_path.replace("/", "_"))
        
        if os.path.exists(backup_file):
            # 检查源文件是否包含大括号
            with open(src_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if '{' in content and '}' in content:
                # 使用备份文件恢复
                shutil.copy2(backup_file, src_file)
                print(f"✅ 恢复: {file_path}")
                restored_count += 1
            else:
                print(f"ℹ️  跳过: {file_path} (已经是原始语法)")
        else:
            print(f"❌ 备份文件不存在: {backup_file}")
    
    print(f"\n✅ 总共恢复了 {restored_count} 个文件")
    
    # 特别处理opcode.py，确保它是正确的
    opcode_file = os.path.join(lib_dir, "opcode.py")
    if os.path.exists(opcode_file):
        with open(opcode_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查并修复opcode.py中的语法错误
        if 'opmap = ' in content and 'opmap = {}' not in content:
            content = content.replace('opmap = ', 'opmap = {}')
            print("✅ 修复opcode.py中的opmap定义")
        
        if '_pseudo_ops = ' in content and '_pseudo_ops = {}' not in content:
            content = content.replace('_pseudo_ops = ', '_pseudo_ops = {}')
            print("✅ 修复opcode.py中的_pseudo_ops定义")
        
        if '_specializations = ' in content and '_specializations = {' not in content:
            content = content.replace('_specializations = ', '_specializations = {')
            # 找到_specializations字典的结束位置并添加}
            if '_specializations = {' in content and '}' not in content.split('_specializations = {')[1].split('_specialized_instructions')[0]:
                # 在_specialized_instructions之前添加}
                parts = content.split('_specialized_instructions')
                if len(parts) > 1:
                    content = parts[0] + '}\n\n_specialized_instructions' + parts[1]
                    print("✅ 修复opcode.py中的_specializations字典")
        
        if '_cache_format = ' in content and '_cache_format = {' not in content:
            content = content.replace('_cache_format = ', '_cache_format = {')
            # 找到_cache_format字典的结束位置并添加}
            if '_cache_format = {' in content and '}' not in content.split('_cache_format = {')[1].split('_inline_cache_entries')[0]:
                # 在_inline_cache_entries之前添加}
                parts = content.split('_inline_cache_entries')
                if len(parts) > 1:
                    content = parts[0] + '}\n\n_inline_cache_entries' + parts[1]
                    print("✅ 修复opcode.py中的_cache_format字典")
        
        # 写入修复后的内容
        with open(opcode_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ opcode.py语法检查完成")
    
    return True

if __name__ == "__main__":
    start_time = time.time()
    
    if restore_stdlib():
        elapsed_time = time.time() - start_time
        print(f"\n✅ 标准库恢复完成! 耗时: {elapsed_time:.2f}秒")
    else:
        print("\n❌ 标准库恢复失败!")