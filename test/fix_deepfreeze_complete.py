#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建完整的deepfreeze.c占位符文件
包含所有必需的符号定义
"""

import os

def create_complete_deepfreeze_c():
    """创建完整的deepfreeze.c占位符文件"""
    
    python_src_dir = r"e:\GitHub3\cpp\BPython\src\Python-3.12.2"
    deepfreeze_dir = os.path.join(python_src_dir, "Python", "deepfreeze")
    
    # 确保目录存在
    os.makedirs(deepfreeze_dir, exist_ok=True)
    
    # 所有必需的符号列表（根据编译错误和原始文件）
    required_symbols = [
        # 原始文件中已有的符号
        "importlib__bootstrap_toplevel",
        "importlib__bootstrap_external_toplevel", 
        "zipimport_toplevel",
        "abc_toplevel",
        "codecs_toplevel",
        "io_toplevel",
        "_collections_abc_toplevel",
        "getpath_toplevel",
        
        # 编译错误中缺失的符号
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
    
    # 生成完整的deepfreeze.c内容
    deepfreeze_content = '''/*
 * Deepfreeze modules - 完整的占位符文件
 * 
 * 这个文件用于解决链接器错误，包含所有必需的_Py_get_*符号
 * 使用简单的实现来避免编译错误
 */

#include "Python.h"

/* 简单的空代码对象定义 */
static PyObject empty_code_object = {
    .ob_refcnt = 1,
    .ob_type = &PyCode_Type,
};

'''
    
    # 为每个必需的符号生成函数
    for symbol in required_symbols:
        function_name = f"_Py_get_{symbol}"
        deepfreeze_content += f'''PyObject *
{function_name}(void)
{{
    /* 占位符函数 - 返回空代码对象 */
    Py_INCREF(&empty_code_object);
    return &empty_code_object;
}}

'''
    
    # 添加全局变量
    deepfreeze_content += '''
/* 必需的全局变量 */
uint32_t _Py_next_func_version = 9;
'''
    
    # 添加初始化函数
    deepfreeze_content += '''
/* Deepfreeze初始化函数 */
void _Py_Deepfreeze_Init(void) {
    /* 占位符函数 */
}

void _Py_Deepfreeze_Fini(void) {
    /* 占位符函数 */
}
'''
    
    # 写入文件
    deepfreeze_file = os.path.join(deepfreeze_dir, "deepfreeze.c")
    
    # 备份原文件
    if os.path.exists(deepfreeze_file):
        backup_file = deepfreeze_file + ".backup3"
        os.rename(deepfreeze_file, backup_file)
        print(f"✓ 已备份原文件: {backup_file}")
    
    with open(deepfreeze_file, 'w', encoding='utf-8') as f:
        f.write(deepfreeze_content)
    
    print(f"✅ 已创建包含{len(required_symbols)}个符号的完整deepfreeze.c文件")
    print(f"📁 文件位置: {deepfreeze_file}")
    
    return True

def main():
    """主函数"""
    print("🚀 开始创建完整的deepfreeze.c占位符文件...")
    
    try:
        if create_complete_deepfreeze_c():
            print("🎉 完整的deepfreeze.c文件创建完成!")
            print("📝 现在可以尝试重新编译bpython.exe")
        else:
            print("❌ 文件创建失败")
    except Exception as e:
        print(f"❌ 创建过程中出错: {e}")

if __name__ == "__main__":
    main()