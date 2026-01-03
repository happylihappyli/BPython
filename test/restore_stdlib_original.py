#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
恢复标准库文件为原始缩进语法
"""

import os
import shutil

# 设置路径
python_src_dir = r"e:\GitHub3\cpp\BPython\src\Python-3.12.2"
stdlib_dir = os.path.join(python_src_dir, "Lib")
backup_dir = os.path.join(python_src_dir, "Lib_backup")

# 需要恢复的关键文件列表
critical_files = [
    "importlib/_bootstrap.py",
    "importlib/_bootstrap_external.py",
    "zipimport.py",
    "abc.py",
    "codecs.py",
    "io.py",
    "_collections_abc.py",
    "opcode.py"
]

def restore_file(file_path):
    """恢复单个文件为原始语法"""
    try:
        # 检查备份文件是否存在
        backup_file = os.path.join(backup_dir, os.path.basename(file_path))
        if os.path.exists(backup_file):
            shutil.copy2(backup_file, file_path)
            print(f"✅ 从备份恢复: {file_path}")
            return True
        
        # 如果没有备份，尝试从原始Python源码下载
        print(f"⚠️  没有找到备份文件: {backup_file}")
        return False
        
    except Exception as e:
        print(f"❌ 恢复文件 {file_path} 时出错: {e}")
        return False

def convert_braces_to_indentation(file_path):
    """将大括号转换为缩进语法"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 简单的转换逻辑（需要根据实际情况调整）
        lines = content.split('\n')
        new_lines = []
        indent_level = 0
        
        for line in lines:
            stripped = line.strip()
            
            # 处理开括号 - 增加缩进
            if stripped.endswith('{') and not stripped.startswith('#'):
                new_lines.append('    ' * indent_level + line.rstrip(' {'))
                indent_level += 1
            # 处理闭括号 - 减少缩进
            elif stripped == '}' and not line.strip().startswith('#'):
                indent_level = max(0, indent_level - 1)
            else:
                new_lines.append('    ' * indent_level + line)
        
        # 写入文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_lines))
        
        print(f"✅ 转换语法: {file_path}")
        return True
        
    except Exception as e:
        print(f"❌ 转换文件 {file_path} 时出错: {e}")
        return False

def main():
    """主函数"""
    print("🚀 开始恢复标准库文件为原始缩进语法...")
    
    restored_count = 0
    converted_count = 0
    
    for file_rel_path in critical_files:
        file_path = os.path.join(stdlib_dir, file_rel_path)
        
        if not os.path.exists(file_path):
            print(f"⚠️  文件不存在: {file_path}")
            continue
        
        print(f"\n📄 处理文件: {file_rel_path}")
        
        # 首先尝试从备份恢复
        if restore_file(file_path):
            restored_count += 1
        else:
            # 如果没有备份，尝试转换语法
            if convert_braces_to_indentation(file_path):
                converted_count += 1
    
    print(f"\n🎉 完成! 成功恢复 {restored_count} 个文件，转换 {converted_count} 个文件")
    
    # 验证文件语法
    print("\n🔍 验证文件语法...")
    for file_rel_path in critical_files:
        file_path = os.path.join(stdlib_dir, file_rel_path)
        if os.path.exists(file_path):
            try:
                # 尝试编译文件来验证语法
                with open(file_path, 'r', encoding='utf-8') as f:
                    source_code = f.read()
                compile(source_code, file_path, 'exec')
                print(f"✅ 语法正确: {file_rel_path}")
            except SyntaxError as e:
                print(f"❌ 语法错误: {file_rel_path} - {e}")
            except Exception as e:
                print(f"⚠️  验证失败: {file_rel_path} - {e}")

if __name__ == "__main__":
    main()