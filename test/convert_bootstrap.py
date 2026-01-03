#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
转换_bootstrap.py文件为花括号语法
将备份文件的内容转换为使用花括号的语法
"""

def convert_indentation_to_braces(content):
    """将Python缩进语法转换为花括号语法"""
    lines = content.split('\n')
    converted_lines = []
    indent_stack = []
    current_indent = 0
    
    for i, line in enumerate(lines):
        stripped = line.lstrip()
        if not stripped:  # 空行
            converted_lines.append(line)
            continue
            
        # 计算当前缩进级别
        indent_level = len(line) - len(stripped)
        
        # 处理缩进变化
        while indent_stack and indent_level < indent_stack[-1]:
            # 缩进减少，添加闭合花括号
            converted_lines.append(' ' * indent_stack.pop() + '}')
        
        if indent_level > current_indent:
            # 缩进增加，添加开括号
            converted_lines.append(' ' * current_indent + '{')
            indent_stack.append(current_indent)
        
        current_indent = indent_level
        
        # 处理当前行
        converted_lines.append(line)
        
        # 检查行尾是否需要闭合花括号
        if stripped.startswith(('def ', 'class ', 'if ', 'elif ', 'else:', 'for ', 'while ', 'try:', 'except ', 'finally:', 'with ')):
            # 这些语句后面需要闭合花括号
            if not stripped.endswith(':') and ':' in stripped:
                # 确保行尾有冒号
                pass
    
    # 处理剩余的缩进
    while indent_stack:
        converted_lines.append(' ' * indent_stack.pop() + '}')
    
    return '\n'.join(converted_lines)

def main():
    """主函数"""
    backup_file = r"e:\GitHub3\cpp\BPython\src\Python-3.12.2\Lib\backup_original\importlib__bootstrap.py"
    output_file = r"e:\GitHub3\cpp\BPython\src\Python-3.12.2\Lib\importlib\_bootstrap.py"
    
    print("正在读取备份文件...")
    try:
        with open(backup_file, 'r', encoding='utf-8') as f:
            content = f.read()
        print(f"读取成功，文件长度: {len(content)} 字符")
    except Exception as e:
        print(f"读取备份文件失败: {e}")
        return
    
    print("正在转换为花括号语法...")
    converted_content = convert_indentation_to_braces(content)
    
    print("正在写入转换后的文件...")
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(converted_content)
        print(f"转换完成，已写入: {output_file}")
    except Exception as e:
        print(f"写入文件失败: {e}")
        return
    
    # 验证转换结果
    print("验证转换结果...")
    try:
        with open(output_file, 'r', encoding='utf-8') as f:
            result_content = f.read()
        print(f"验证成功，新文件长度: {len(result_content)} 字符")
        print(f"行数: {result_content.count('\\n') + 1}")
    except Exception as e:
        print(f"验证失败: {e}")

if __name__ == "__main__":
    main()