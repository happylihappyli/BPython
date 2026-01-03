#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证importlib._bootstrap.py语法正确性
"""

import os
import sys

def verify_bootstrap_syntax():
    """验证importlib._bootstrap.py语法"""
    
    # 获取Python源码目录
    python_src_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src", "Python-3.12.2")
    bootstrap_file = os.path.join(python_src_dir, "Lib", "importlib", "_bootstrap.py")
    
    print(f"正在验证文件: {bootstrap_file}")
    
    # 读取文件内容
    with open(bootstrap_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查括号匹配
    stack = []
    brace_stack = []
    line_num = 1
    char_count = 0
    
    for i, char in enumerate(content):
        if char == '\n':
            line_num += 1
            char_count = 0
        else:
            char_count += 1
        
        if char == '(':
            stack.append(('(', line_num, char_count))
        elif char == ')':
            if not stack or stack[-1][0] != '(':
                print(f"错误: 第{line_num}行第{char_count}列: 不匹配的右括号")
                return False
            stack.pop()
        elif char == '{':
            brace_stack.append(('{', line_num, char_count))
        elif char == '}':
            if not brace_stack or brace_stack[-1][0] != '{':
                print(f"错误: 第{line_num}行第{char_count}列: 不匹配的右大括号")
                return False
            brace_stack.pop()
    
    if stack:
        print(f"错误: 未闭合的左括号在: {stack}")
        return False
    
    if brace_stack:
        print(f"错误: 未闭合的左大括号在: {brace_stack}")
        return False
    
    print("语法验证通过: 所有括号和大括号都正确匹配")
    
    # 检查_find_and_load函数
    if "def _find_and_load(name, import_):" in content:
        print("_find_and_load函数存在")
        
        # 检查if语句
        if "if (module is _NEEDS_LOADING or (" in content:
            print("if语句存在")
            
            # 检查括号匹配
            start_idx = content.find("if (module is _NEEDS_LOADING or (")
            if start_idx != -1:
                # 查找对应的右括号
                paren_count = 0
                brace_count = 0
                for i in range(start_idx, min(start_idx + 500, len(content))):
                    if content[i] == '(':
                        paren_count += 1
                    elif content[i] == ')':
                        paren_count -= 1
                        if paren_count == 0:
                            # 检查后面是否有冒号
                            j = i + 1
                            while j < len(content) and content[j] in ' \t\n':
                                j += 1
                            if j < len(content) and content[j] == ':':
                                print("if语句语法正确")
                                break
                            else:
                                print("错误: if语句缺少冒号")
                                return False
                
                if paren_count != 0:
                    print("错误: if语句括号不匹配")
                    return False
    
    return True

if __name__ == "__main__":
    if verify_bootstrap_syntax():
        print("✅ importlib._bootstrap.py语法验证通过")
    else:
        print("❌ importlib._bootstrap.py语法验证失败")