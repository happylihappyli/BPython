#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成所有缺失的frozen模块头文件
"""

import os
import sys
import marshal
import importlib.util

# 设置路径
python_src_dir = r"e:\GitHub3\cpp\BPython\src\Python-3.12.2"
stdlib_dir = os.path.join(python_src_dir, "Lib")
frozen_modules_dir = os.path.join(python_src_dir, "Python", "frozen_modules")

# 需要生成的模块列表
modules_to_generate = [
    "importlib._bootstrap",
    "importlib._bootstrap_external", 
    "zipimport",
    "abc",
    "codecs",
    "io",
    "_collections_abc"
]

def compile_python_file(file_path):
    """编译Python文件并返回marshal后的字节码"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            source_code = f.read()
        
        # 编译代码
        filename = f"<frozen {os.path.basename(file_path)}>"
        code = compile(source_code, filename, "exec", optimize=0, dont_inherit=True)
        
        # 转换为marshal格式
        marshalled = marshal.dumps(code)
        return marshalled
    except Exception as e:
        print(f"❌ 编译文件 {file_path} 时出错: {e}")
        return None

def generate_frozen_header(module_name, marshalled_data, output_dir):
    """生成frozen模块头文件"""
    # 生成头文件名
    header_filename = module_name.replace('.', '_') + ".h"
    header_file = os.path.join(output_dir, header_filename)
    
    # 生成数组名
    array_name = "_Py_M_" + module_name.replace('.', '_')
    
    # 生成头文件内容
    header_content = f"/* Auto-generated frozen module header for {module_name} */\n"
    header_content += f"const unsigned char {array_name}[] = {{\n"
    
    # 写入marshal数据
    data_size = len(marshalled_data)
    for n in range(0, data_size, 16):
        header_content += "    "
        header_content += ",".join(str(i) for i in marshalled_data[n : n + 16])
        header_content += ",\n"
    
    header_content += "};\n"
    
    # 写入文件
    with open(header_file, 'w', encoding='utf-8') as f:
        f.write(header_content)
    
    print(f"✅ 已生成 {header_filename}")
    return header_file

def find_module_file(module_name, search_dir):
    """查找模块对应的Python文件"""
    # 将模块名转换为文件路径
    if module_name == "importlib._bootstrap":
        file_path = os.path.join(search_dir, "importlib", "_bootstrap.py")
    elif module_name == "importlib._bootstrap_external":
        file_path = os.path.join(search_dir, "importlib", "_bootstrap_external.py")
    else:
        file_path = os.path.join(search_dir, module_name.replace('.', os.sep) + ".py")
    
    if os.path.exists(file_path):
        return file_path
    
    # 如果没找到，尝试其他可能的路径
    alternative_paths = [
        os.path.join(search_dir, module_name + ".py"),
        os.path.join(search_dir, module_name.replace('_', '') + ".py"),
    ]
    
    for path in alternative_paths:
        if os.path.exists(path):
            return path
    
    return None

def main():
    """主函数"""
    print("🚀 开始生成所有缺失的frozen模块头文件...")
    
    # 确保输出目录存在
    os.makedirs(frozen_modules_dir, exist_ok=True)
    
    generated_count = 0
    
    for module_name in modules_to_generate:
        print(f"\n📦 处理模块: {module_name}")
        
        # 查找模块文件
        module_file = find_module_file(module_name, stdlib_dir)
        if not module_file:
            print(f"⚠️  找不到模块文件: {module_name}")
            continue
        
        print(f"📄 找到文件: {module_file}")
        
        # 编译文件
        marshalled_data = compile_python_file(module_file)
        if not marshalled_data:
            print(f"❌ 编译失败: {module_name}")
            continue
        
        # 生成头文件
        generate_frozen_header(module_name, marshalled_data, frozen_modules_dir)
        generated_count += 1
    
    print(f"\n🎉 完成! 成功生成 {generated_count}/{len(modules_to_generate)} 个frozen模块头文件")
    
    # 检查是否所有文件都已生成
    print("\n📋 检查生成的文件:")
    for module_name in modules_to_generate:
        header_filename = module_name.replace('.', '_') + ".h"
        header_file = os.path.join(frozen_modules_dir, header_filename)
        if os.path.exists(header_file):
            print(f"✅ {header_filename}")
        else:
            print(f"❌ {header_filename} (缺失)")

if __name__ == "__main__":
    main()