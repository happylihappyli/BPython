#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修改Python语法，将缩进改为大括号
"""

import os
import re
import shutil

def backup_file(file_path):
    """备份文件"""
    backup_path = file_path + ".backup"
    if os.path.exists(file_path):
        shutil.copy2(file_path, backup_path)
        print(f"已备份: {file_path} -> {backup_path}")
        return True
    else:
        print(f"错误: 文件不存在: {file_path}")
        return False

def modify_grammar_file(grammar_file):
    """修改Grammar/python.gram文件"""
    
    if not backup_file(grammar_file):
        return False
    
    with open(grammar_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 修改block规则：将NEWLINE INDENT ... DEDENT改为NEWLINE LBRACE ... RBRACE
    content = re.sub(
        r'NEWLINE\s+INDENT\s+(\w+)=statements\s+DEDENT',
        r'NEWLINE LBRACE \1=statements RBRACE',
        content
    )
    
    # 修改match_stmt规则
    content = re.sub(
        r"NEWLINE\s+INDENT\s+cases\[asdl_match_case_seq\*\]=case_block\+\s+DEDENT",
        r"NEWLINE LBRACE cases[asdl_match_case_seq*]=case_block+ RBRACE",
        content
    )
    
    # 修改func_type_comment规则
    content = re.sub(
        r'NEWLINE\s+TYPE_COMMENT\s+&\(NEWLINE\s+INDENT\)',
        r'NEWLINE TYPE_COMMENT &(NEWLINE LBRACE)',
        content
    )
    
    # 修改所有错误检查规则中的INDENT
    content = re.sub(
        r'!INDENT',
        r'!LBRACE',
        content
    )
    
    # 修改block规则中的simple_stmts选项
    content = re.sub(
        r'block\[asdl_stmt_seq\*\].*?simple_stmts',
        r'block[asdl_stmt_seq*] (memo):\n    | NEWLINE LBRACE a=statements RBRACE { a }\n    | simple_stmts\n    | invalid_block',
        content,
        flags=re.DOTALL
    )
    
    with open(grammar_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"已修改: {grammar_file}")
    return True

def modify_tokenizer_file(tokenizer_file):
    """修改Parser/tokenizer.c文件"""
    
    if not backup_file(tokenizer_file):
        return False
    
    with open(tokenizer_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 注释掉缩进处理逻辑，改为处理大括号
    # 找到缩进处理的相关代码段
    
    # 首先添加大括号处理逻辑
    brace_handling_code = '''\n    /* 大括号处理 - 替换缩进逻辑 */\n    if (c == '{') {\n        /* 左大括号 - 相当于INDENT */\n        if (tok->tok_extra_tokens) {\n            p_start = tok->cur;\n            p_end = tok->cur;\n        }\n        tok->pendin--;\n        tok_nextc(tok);  /* 消耗大括号 */\n        return MAKE_TOKEN(LBRACE);\n    }\n    else if (c == '}') {\n        /* 右大括号 - 相当于DEDENT */\n        if (tok->tok_extra_tokens) {\n            p_start = tok->cur;\n            p_end = tok->cur;\n        }\n        tok->pendin++;\n        tok_nextc(tok);  /* 消耗大括号 */\n        return MAKE_TOKEN(RBRACE);\n    }\n    else if (c == '\\n') {\n        /* 保留换行处理，但跳过缩进检查 */\n        tok->cont_line = 0;\n        if (tok->tok_extra_tokens) {\n            p_start = tok->cur;\n            p_end = tok->cur;\n        }\n        tok_nextc(tok);\n        return MAKE_TOKEN(NEWLINE);\n    }\n\n    /* 跳过原有的缩进处理逻辑 */\n    /*\n'''
    
    # 找到缩进处理的开始位置
    indent_start = content.find('    /* Check for indentation */')
    if indent_start == -1:
        print("警告: 未找到缩进处理代码")
        return False
    
    # 找到缩进处理的结束位置
    indent_end = content.find('    /* Peek ahead at the next character */', indent_start)
    if indent_end == -1:
        print("警告: 未找到缩进处理结束位置")
        return False
    
    # 替换缩进处理代码
    new_content = content[:indent_start] + brace_handling_code + content[indent_start:indent_end] + '    */\n' + content[indent_end:]
    
    with open(tokenizer_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"已修改: {tokenizer_file}")
    return True

def main():
    """主函数"""
    print("=== Python语法修改工具 ===")
    
    # Python源码目录
    python_src_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src", "Python-3.12.2")
    
    # 要修改的文件路径
    grammar_file = os.path.join(python_src_dir, "Grammar", "python.gram")
    tokenizer_file = os.path.join(python_src_dir, "Parser", "tokenizer.c")
    
    print(f"Python源码目录: {python_src_dir}")
    
    # 检查文件是否存在
    if not os.path.exists(grammar_file):
        print(f"错误: 文件不存在: {grammar_file}")
        return
    
    if not os.path.exists(tokenizer_file):
        print(f"错误: 文件不存在: {tokenizer_file}")
        return
    
    # 修改语法文件
    print("\n1. 修改Grammar/python.gram...")
    if modify_grammar_file(grammar_file):
        print("Grammar文件修改完成")
    else:
        print("Grammar文件修改失败")
        return
    
    # 修改词法分析器文件
    print("\n2. 修改Parser/tokenizer.c...")
    if modify_tokenizer_file(tokenizer_file):
        print("Tokenizer文件修改完成")
    else:
        print("Tokenizer文件修改失败")
        return
    
    print("\n=== 修改完成 ===")
    print("Python语法已从缩进改为大括号")
    print("注意: 这只是一个基础修改，可能需要进一步调整才能完全工作")

if __name__ == "__main__":
    main()