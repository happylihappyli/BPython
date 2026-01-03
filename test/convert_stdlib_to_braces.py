#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将标准库中的Python文件转换为使用大括号语法
"""

import os
import re
import fnmatch

def convert_python_file(file_path):
    """将单个Python文件转换为大括号语法"""
    
    print(f"正在转换文件: {file_path}")
    
    try:
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 转换缩进为大括号
        # 基本思路：
        # 1. 找到所有函数定义、类定义、if/elif/else、for/while、try/except/finally等语句
        # 2. 在这些语句后面添加大括号
        # 3. 将缩进转换为大括号内的内容
        
        # 先处理简单的函数和类定义
        lines = content.split('\n')
        new_lines = []
        indent_stack = []  # 用于跟踪缩进级别
        current_indent = 0
        
        for i, line in enumerate(lines):
            stripped_line = line.lstrip()
            if not stripped_line:  # 空行
                new_lines.append(line)
                continue
                
            # 计算当前行的缩进级别
            indent_level = len(line) - len(stripped_line)
            
            # 检查是否需要添加结束大括号
            while indent_stack and indent_level <= indent_stack[-1]:
                new_lines.append(' ' * indent_stack.pop() + '}')
            
            # 检查当前行是否是块开始（函数、类、if、for等）
            if (stripped_line.startswith('def ') or 
                stripped_line.startswith('class ') or
                stripped_line.startswith('if ') or
                stripped_line.startswith('elif ') or
                stripped_line.startswith('else:') or
                stripped_line.startswith('for ') or
                stripped_line.startswith('while ') or
                stripped_line.startswith('try:') or
                stripped_line.startswith('except ') or
                stripped_line.startswith('finally:') or
                stripped_line.startswith('with ')):
                
                # 检查下一行是否有缩进（即是否有代码块）
                if i + 1 < len(lines):
                    next_line = lines[i + 1]
                    next_stripped = next_line.lstrip()
                    if next_stripped and len(next_line) - len(next_stripped) > indent_level:
                        # 有代码块，添加开始大括号
                        new_lines.append(line + ' {')
                        indent_stack.append(indent_level)
                        continue
            
            # 普通行，直接添加
            new_lines.append(line)
        
        # 添加剩余的大括号
        while indent_stack:
            new_lines.append(' ' * indent_stack.pop() + '}')
        
        new_content = '\n'.join(new_lines)
        
        # 写入转换后的内容
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"成功转换: {file_path}")
        return True
        
    except Exception as e:
        print(f"转换文件 {file_path} 时出错: {e}")
        return False

def convert_stdlib():
    """转换整个标准库"""
    
    # 获取Python源码目录
    python_src_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src", "Python-3.12.2")
    lib_dir = os.path.join(python_src_dir, "Lib")
    
    print(f"开始转换标准库: {lib_dir}")
    
    # 统计转换的文件数量
    converted_count = 0
    error_count = 0
    
    # 遍历Lib目录下的所有.py文件
    for root, dirs, files in os.walk(lib_dir):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                if convert_python_file(file_path):
                    converted_count += 1
                else:
                    error_count += 1
    
    print(f"转换完成! 成功: {converted_count}, 失败: {error_count}")
    return converted_count > 0

def main():
    """主函数"""
    print("开始转换标准库为使用大括号语法...")
    
    try:
        success = convert_stdlib()
        if success:
            print("转换完成！")
        else:
            print("转换失败")
    except Exception as e:
        print(f"转换过程中出现错误: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()