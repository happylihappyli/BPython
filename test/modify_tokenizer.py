#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修改Python词法分析器，将缩进改为大括号处理
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

def modify_tokenizer_file(tokenizer_file):
    """修改Parser/tokenizer.c文件"""
    
    if not backup_file(tokenizer_file):
        return False
    
    with open(tokenizer_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 找到缩进处理的开始位置（Get indentation level注释之后）
    indent_start = content.find('    /* Get indentation level */')
    if indent_start == -1:
        print("错误: 未找到缩进处理代码")
        return False
    
    # 找到缩进处理的结束位置（Return pending indents/dedents之前）
    indent_end = content.find('    /* Return pending indents/dedents */', indent_start)
    if indent_end == -1:
        print("错误: 未找到缩进处理结束位置")
        return False
    
    # 创建新的处理逻辑
    new_indent_logic = '''    /* 大括号处理 - 替换缩进逻辑 */
    if (tok->atbol) {
        int c = tok_nextc(tok);
        tok_backup(tok, c);
        
        /* 检查是否为大括号 */
        if (c == '{') {
            /* 左大括号 - 相当于INDENT */
            if (tok->tok_extra_tokens) {
                p_start = tok->cur;
                p_end = tok->cur;
            }
            tok->pendin--;
            return MAKE_TOKEN(LBRACE);
        }
        else if (c == '}') {
            /* 右大括号 - 相当于DEDENT */
            if (tok->tok_extra_tokens) {
                p_start = tok->cur;
                p_end = tok->cur;
            }
            tok->pendin++;
            return MAKE_TOKEN(RBRACE);
        }
        else if (c == '\\n') {
            /* 保留换行处理，但跳过缩进检查 */
            tok->cont_line = 0;
            if (tok->tok_extra_tokens) {
                p_start = tok->cur;
                p_end = tok->cur;
            }
            tok_nextc(tok);
            return MAKE_TOKEN(NEWLINE);
        }
    }

    /* 跳过原有的缩进处理逻辑，直接进入字符处理 */
    tok->atbol = 0;  /* 标记不在行首 */
'''
    
    # 替换缩进处理代码
    new_content = content[:indent_start] + new_indent_logic + content[indent_end:]
    
    # 还需要修改pending indents/dedents的处理
    # 找到pending indents/dedents的处理部分
    pending_start = content.find('    /* Return pending indents/dedents */')
    if pending_start != -1:
        # 找到这个部分的结束位置
        pending_end = content.find('    /* Peek ahead at the next character */', pending_start)
        if pending_end != -1:
            # 修改pending处理逻辑
            new_pending_logic = '''    /* Return pending braces */
   if (tok->pendin != 0) {
        if (tok->pendin < 0) {
            /* 需要生成右大括号 */
            if (tok->tok_extra_tokens) {
                p_start = tok->cur;
                p_end = tok->cur;
            }
            tok->pendin++;
            return MAKE_TOKEN(RBRACE);
        }
        else {
            /* 需要生成左大括号 */
            if (tok->tok_extra_tokens) {
                p_start = tok->buf;
                p_end = tok->cur;
            }
            tok->pendin--;
            return MAKE_TOKEN(LBRACE);
        }
    }
'''
            new_content = new_content[:pending_start] + new_pending_logic + new_content[pending_end:]
    
    with open(tokenizer_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"已修改: {tokenizer_file}")
    return True

def main():
    """主函数"""
    print("=== Python词法分析器修改工具 ===")
    
    # Python源码目录
    python_src_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src", "Python-3.12.2")
    
    # 要修改的文件路径
    tokenizer_file = os.path.join(python_src_dir, "Parser", "tokenizer.c")
    
    print(f"Python源码目录: {python_src_dir}")
    
    # 检查文件是否存在
    if not os.path.exists(tokenizer_file):
        print(f"错误: 文件不存在: {tokenizer_file}")
        return
    
    # 修改词法分析器文件
    print("\n修改Parser/tokenizer.c...")
    if modify_tokenizer_file(tokenizer_file):
        print("✓ Tokenizer文件修改完成")
    else:
        print("✗ Tokenizer文件修改失败")
        return
    
    print("\n=== 修改完成 ===")
    print("Python词法分析器已修改为处理大括号")

if __name__ == "__main__":
    main()