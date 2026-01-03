#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
恢复关键标准库文件到原始缩进语法
"""

import os
import re

def restore_file_to_indentation(file_path):
    """
    将文件从大括号语法恢复为缩进语法
    """
    print(f"正在恢复文件: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 备份原始文件
        backup_path = file_path + '.backup'
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # 替换大括号为缩进
        # 1. 替换函数定义中的大括号
        content = re.sub(r'(def\s+\w+\s*\([^)]*\)):\s*{', r'\1:', content)
        
        # 2. 替换类定义中的大括号
        content = re.sub(r'(class\s+\w+\s*(?:\([^)]*\))?):\s*{', r'\1:', content)
        
        # 3. 替换if/elif/else/for/while/try/except/finally/with语句中的大括号
        content = re.sub(r'(if|elif|else|for|while|try|except|finally|with)\s*([^:]*):\s*{', r'\1 \2:', content)
        
        # 4. 删除单独的右大括号（需要更智能的处理）
        # 先处理简单的缩进情况
        lines = content.split('\n')
        new_lines = []
        indent_level = 0
        
        for line in lines:
            stripped = line.strip()
            
            # 如果是右大括号，减少缩进级别
            if stripped == '}':
                indent_level = max(0, indent_level - 1)
                continue
            
            # 如果是左大括号，增加缩进级别
            if stripped.endswith('{') and not stripped.startswith('#'):
                # 移除左大括号
                line = line.rstrip().rstrip('{')
                new_lines.append('    ' * indent_level + line.strip())
                indent_level += 1
            else:
                # 普通行，保持当前缩进
                new_lines.append('    ' * indent_level + line.strip())
        
        content = '\n'.join(new_lines)
        
        # 5. 修复一些特殊情况
        # 修复字典字面量中的大括号
        content = re.sub(r'(\w+)\s*=\s*{', r'\1 = {', content)
        
        # 写入恢复后的内容
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"成功恢复: {file_path}")
        return True
        
    except Exception as e:
        print(f"恢复失败 {file_path}: {e}")
        return False

def main():
    """
    主函数：恢复关键标准库文件
    """
    # 需要恢复的关键文件列表
    critical_files = [
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
    
    # 基础路径
    base_dir = os.path.join(os.path.dirname(__file__), "..", "src", "Python-3.12.2", "Lib")
    
    success_count = 0
    failed_files = []
    
    for file_name in critical_files:
        file_path = os.path.join(base_dir, file_name)
        
        if not os.path.exists(file_path):
            print(f"文件不存在: {file_path}")
            failed_files.append(file_name)
            continue
        
        if restore_file_to_indentation(file_path):
            success_count += 1
        else:
            failed_files.append(file_name)
    
    print(f"\n恢复完成: 成功 {success_count}/{len(critical_files)}")
    if failed_files:
        print(f"失败的文件: {failed_files}")
    else:
        print("所有文件都已成功恢复！")

if __name__ == "__main__":
    main()