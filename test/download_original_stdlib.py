#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从原始Python源码重新下载标准库文件
"""

import os
import urllib.request
import urllib.error

# 设置路径
python_src_dir = r"e:\GitHub3\cpp\BPython\src\Python-3.12.2"
stdlib_dir = os.path.join(python_src_dir, "Lib")

# 需要下载的文件列表（从GitHub原始仓库）
files_to_download = [
    ("importlib/_bootstrap_external.py", "https://raw.githubusercontent.com/python/cpython/3.12/Lib/importlib/_bootstrap_external.py"),
    ("zipimport.py", "https://raw.githubusercontent.com/python/cpython/3.12/Lib/zipimport.py"),
    ("opcode.py", "https://raw.githubusercontent.com/python/cpython/3.12/Lib/opcode.py"),
]

def download_file(url, local_path):
    """下载文件"""
    try:
        # 确保目录存在
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        
        # 下载文件
        urllib.request.urlretrieve(url, local_path)
        print(f"✅ 下载成功: {local_path}")
        return True
    except urllib.error.URLError as e:
        print(f"❌ 下载失败 {url}: {e}")
        return False
    except Exception as e:
        print(f"❌ 下载失败 {url}: {e}")
        return False

def verify_syntax(file_path):
    """验证文件语法"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            source_code = f.read()
        compile(source_code, file_path, 'exec')
        return True
    except SyntaxError as e:
        print(f"❌ 语法错误: {file_path} - {e}")
        return False
    except Exception as e:
        print(f"⚠️  验证失败: {file_path} - {e}")
        return False

def main():
    """主函数"""
    print("🚀 开始从原始源码重新下载标准库文件...")
    
    downloaded_count = 0
    
    for file_rel_path, url in files_to_download:
        file_path = os.path.join(stdlib_dir, file_rel_path)
        
        print(f"\n📄 下载文件: {file_rel_path}")
        
        # 备份原文件
        if os.path.exists(file_path):
            backup_path = file_path + ".backup"
            os.rename(file_path, backup_path)
            print(f"📋 已备份原文件到: {backup_path}")
        
        # 下载文件
        if download_file(url, file_path):
            # 验证语法
            if verify_syntax(file_path):
                print(f"✅ 语法验证通过: {file_rel_path}")
                downloaded_count += 1
            else:
                print(f"❌ 语法验证失败: {file_rel_path}")
                # 恢复备份
                if os.path.exists(file_path + ".backup"):
                    os.rename(file_path + ".backup", file_path)
                    print(f"↩️  已恢复备份文件")
        else:
            # 恢复备份
            if os.path.exists(file_path + ".backup"):
                os.rename(file_path + ".backup", file_path)
                print(f"↩️  已恢复备份文件")
    
    print(f"\n🎉 完成! 成功下载 {downloaded_count}/{len(files_to_download)} 个文件")

if __name__ == "__main__":
    main()