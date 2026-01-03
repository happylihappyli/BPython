#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
下载Python最新稳定版源码
"""

import os
import sys
import urllib.request
import tarfile
import zipfile
import tempfile
import shutil

def download_python_source():
    """下载Python最新稳定版源码"""
    
    # Python官方源码下载地址（最新稳定版）
    python_version = "3.12.2"  # 当前最新稳定版
    download_url = f"https://www.python.org/ftp/python/{python_version}/Python-{python_version}.tgz"
    
    # 目标目录
    target_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src")
    
    # 创建目标目录
    os.makedirs(target_dir, exist_ok=True)
    
    print(f"开始下载Python {python_version} 源码...")
    
    # 临时文件路径
    temp_file = os.path.join(tempfile.gettempdir(), f"Python-{python_version}.tgz")
    
    try:
        # 下载文件
        print(f"下载地址: {download_url}")
        urllib.request.urlretrieve(download_url, temp_file)
        print("下载完成")
        
        # 解压文件
        print("开始解压...")
        with tarfile.open(temp_file, 'r:gz') as tar:
            tar.extractall(target_dir)
        print("解压完成")
        
        # 获取解压后的目录名
        extracted_dir = os.path.join(target_dir, f"Python-{python_version}")
        
        if os.path.exists(extracted_dir):
            print(f"Python源码已下载到: {extracted_dir}")
            
            # 检查Grammar目录是否存在
            grammar_dir = os.path.join(extracted_dir, "Grammar")
            if os.path.exists(grammar_dir):
                print("Grammar目录存在，准备进行语法修改")
                return extracted_dir
            else:
                print("警告: Grammar目录不存在")
                return extracted_dir
        else:
            print("错误: 解压目录不存在")
            return None
            
    except Exception as e:
        print(f"下载或解压过程中出现错误: {e}")
        return None
    finally:
        # 清理临时文件
        if os.path.exists(temp_file):
            os.remove(temp_file)

def main():
    """主函数"""
    print("=== Python源码下载工具 ===")
    
    result = download_python_source()
    
    if result:
        print(f"\n下载成功！源码位置: {result}")
        print("接下来可以开始修改语法文件")
    else:
        print("\n下载失败，请检查网络连接")
        sys.exit(1)

if __name__ == "__main__":
    main()