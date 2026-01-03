#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建简单的deepfreeze.c占位符文件
使用更简单的实现来避免编译错误
"""

import os

def create_simple_deepfreeze_c():
    """创建简单的deepfreeze.c占位符文件"""
    
    python_src_dir = r"e:\GitHub3\cpp\BPython\src\Python-3.12.2"
    deepfreeze_dir = os.path.join(python_src_dir, "Python", "deepfreeze")
    
    # 确保目录存在
    os.makedirs(deepfreeze_dir, exist_ok=True)
    
    # 缺失的符号列表（根据编译错误）
    missing_symbols = [
        "runpy_toplevel",
        "stat_toplevel", 
        "site_toplevel",
        "__phello___ham_toplevel",
        "ntpath_toplevel",
        "importlib_util_toplevel",
        "genericpath_toplevel",
        "__hello___toplevel",
        "__phello___ham_eggs_toplevel",
        "__phello___toplevel",
        "importlib_machinery_toplevel",
        "os_toplevel",
        "_sitebuiltins_toplevel",
        "posixpath_toplevel",
        "__phello___spam_toplevel",
        "frozen_only_toplevel"
    ]
    
    # 生成简单的deepfreeze.c内容
    deepfreeze_content = '''/*
 * Deepfreeze modules - 简单的占位符文件
 * 
 * 这个文件用于解决链接器错误，包含所有缺失的_Py_get_*符号
 * 使用简单的实现来避免编译错误
 */

#include "Python.h"

/* 简单的空代码对象定义 */
static PyObject empty_code_object = {
    .ob_refcnt = 1,
    .ob_type = &PyCode_Type,
};

'''
    
    # 为每个缺失的符号生成简单的函数
    for symbol in missing_symbols:
        function_name = f"_Py_get_{symbol}"
        deepfreeze_content += f'''PyObject *
{function_name}(void)
{{
    /* 简单的占位符函数 - 返回空代码对象 */
    Py_INCREF(&empty_code_object);
    return &empty_code_object;
}}

'''
    
    # 添加简单的初始化函数
    deepfreeze_content += '''
/* Deepfreeze初始化函数 */
void _Py_Deepfreeze_Init(void) {
    /* 简单的占位符函数 */
}

void _Py_Deepfreeze_Fini(void) {
    /* 简单的占位符函数 */
}
'''
    
    # 写入文件
    deepfreeze_file = os.path.join(deepfreeze_dir, "deepfreeze.c")
    
    # 备份原文件
    if os.path.exists(deepfreeze_file):
        backup_file = deepfreeze_file + ".backup2"
        os.rename(deepfreeze_file, backup_file)
        print(f"✓ 已备份原文件: {backup_file}")
    
    with open(deepfreeze_file, 'w', encoding='utf-8') as f:
        f.write(deepfreeze_content)
    
    print(f"✅ 已创建包含{len(missing_symbols)}个符号的简单deepfreeze.c文件")
    print(f"📁 文件位置: {deepfreeze_file}")
    
    return True

def main():
    """主函数"""
    print("🚀 开始创建简单的deepfreeze.c占位符文件...")
    
    try:
        if create_simple_deepfreeze_c():
            print("🎉 简单的deepfreeze.c文件创建完成!")
            print("📝 现在可以尝试重新编译bpython.exe")
        else:
            print("❌ 文件创建失败")
    except Exception as e:
        print(f"❌ 创建过程中出错: {e}")

if __name__ == "__main__":
    main()