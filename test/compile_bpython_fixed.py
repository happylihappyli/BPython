#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复编译bpython.exe
"""

import os
import sys
import subprocess
import time

def compile_bpython():
    """编译bpython.exe"""
    
    # 获取Python源码目录
    python_src_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src", "Python-3.12.2")
    pcbuild_dir = os.path.join(python_src_dir, "PCbuild")
    
    print("============================================================")
    print("编译bpython.exe")
    print("============================================================")
    
    # 方法1: 尝试直接编译python项目
    print("方法1: 直接编译python项目...")
    
    start_time = time.time()
    
    # 使用MSBuild直接编译python.vcxproj
    python_project = os.path.join(pcbuild_dir, "python.vcxproj")
    
    if os.path.exists(python_project):
        print(f"找到python项目文件: {python_project}")
        
        # 编译python项目
        cmd = ["D:\\Code\\VS2019\\Community\\MSBuild\\Current\\Bin\\MSBuild.exe", 
               python_project, 
               "/t:Build", 
               "/m", 
               "/nologo", 
               "/v:m", 
               "/clp:summary", 
               "/p:Configuration=Release", 
               "/p:Platform=x64", 
               "/p:IncludeExternals=true", 
               "/p:IncludeCTypes=true", 
               "/p:IncludeSSL=true", 
               "/p:IncludeTkinter=true"]
        
        try:
            result = subprocess.run(cmd, cwd=pcbuild_dir, capture_output=True, text=True, encoding='utf-8', errors='replace')
            
            elapsed_time = time.time() - start_time
            
            if result.returncode == 0:
                print(f"✅ python项目编译成功! 耗时: {elapsed_time:.2f}秒")
                
                # 检查编译结果
                python_exe_path = os.path.join(pcbuild_dir, "x64", "python.exe")
                if os.path.exists(python_exe_path):
                    print(f"✅ 编译好的python.exe: {python_exe_path}")
                    
                    # 重命名为bpython.exe
                    bpython_exe_path = os.path.join(pcbuild_dir, "x64", "bpython.exe")
                    os.rename(python_exe_path, bpython_exe_path)
                    print(f"✅ 重命名为: {bpython_exe_path}")
                    
                    # 测试编译结果
                    print("测试编译结果...")
                    test_cmd = [bpython_exe_path, "-c", "print('Hello from bpython!')"]
                    result = subprocess.run(test_cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
                    
                    if result.returncode == 0:
                        print(f"✅ 测试成功! 输出: {result.stdout.strip()}")
                        return True
                    else:
                        print(f"❌ 测试失败! 错误: {result.stderr}")
                        return False
                else:
                    print("❌ 编译好的python.exe不存在")
                    return False
            else:
                print(f"❌ python项目编译失败! 耗时: {elapsed_time:.2f}秒")
                print(f"标准输出: {result.stdout}")
                print(f"错误输出: {result.stderr}")
                
                # 方法2: 尝试使用build.bat但跳过冻结模块
                print("\n方法2: 尝试跳过冻结模块编译...")
                
                # 修改_freeze_module.vcxproj跳过冻结模块
                freeze_module_file = os.path.join(pcbuild_dir, "_freeze_module.vcxproj")
                
                if os.path.exists(freeze_module_file):
                    print("临时禁用冻结模块...")
                    
                    # 备份原文件
                    backup_file = freeze_module_file + ".backup"
                    if not os.path.exists(backup_file):
                        import shutil
                        shutil.copy2(freeze_module_file, backup_file)
                        print(f"备份文件: {backup_file}")
                    
                    # 读取文件内容
                    with open(freeze_module_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # 注释掉_RebuildFrozen目标
                    if '<Target Name="_RebuildFrozen"' in content:
                        # 找到目标开始和结束位置
                        start_idx = content.find('<Target Name="_RebuildFrozen"')
                        end_idx = content.find('</Target>', start_idx) + len('</Target>')
                        
                        if start_idx != -1 and end_idx != -1:
                            # 注释掉整个目标
                            target_content = content[start_idx:end_idx]
                            commented_target = f"<!-- {target_content} -->"
                            content = content[:start_idx] + commented_target + content[end_idx:]
                            
                            # 写入修改后的内容
                            with open(freeze_module_file, 'w', encoding='utf-8') as f:
                                f.write(content)
                            
                            print("✅ 已临时禁用冻结模块")
                            
                            # 重新尝试编译
                            print("重新尝试编译...")
                            
                            cmd = ["cmd", "/c", "build.bat", "-p", "x64", "-c", "Release"]
                            result = subprocess.run(cmd, cwd=pcbuild_dir, capture_output=True, text=True, encoding='utf-8', errors='replace')
                            
                            if result.returncode == 0:
                                print(f"✅ 编译成功!")
                                
                                # 恢复原文件
                                shutil.copy2(backup_file, freeze_module_file)
                                print("✅ 已恢复冻结模块设置")
                                
                                # 重命名和测试
                                python_exe_path = os.path.join(pcbuild_dir, "x64", "python.exe")
                                bpython_exe_path = os.path.join(pcbuild_dir, "x64", "bpython.exe")
                                
                                if os.path.exists(python_exe_path):
                                    os.rename(python_exe_path, bpython_exe_path)
                                    print(f"✅ 重命名为: {bpython_exe_path}")
                                    
                                    # 测试
                                    test_cmd = [bpython_exe_path, "-c", "print('Hello from bpython!')"]
                                    result = subprocess.run(test_cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
                                    
                                    if result.returncode == 0:
                                        print(f"✅ 测试成功! 输出: {result.stdout.strip()}")
                                        return True
                                    else:
                                        print(f"❌ 测试失败! 错误: {result.stderr}")
                                        return False
                                else:
                                    print("❌ 编译好的python.exe不存在")
                                    return False
                            else:
                                print(f"❌ 编译失败!")
                                print(f"标准输出: {result.stdout}")
                                print(f"错误输出: {result.stderr}")
                                
                                # 恢复原文件
                                shutil.copy2(backup_file, freeze_module_file)
                                print("✅ 已恢复冻结模块设置")
                                return False
                        else:
                            print("❌ 无法找到_RebuildFrozen目标")
                            return False
                    else:
                        print("❌ 未找到_RebuildFrozen目标")
                        return False
                else:
                    print("❌ _freeze_module.vcxproj不存在")
                    return False
                    
        except Exception as e:
            print(f"❌ 编译过程出现异常: {e}")
            return False
    else:
        print("❌ python.vcxproj不存在")
        return False

if __name__ == "__main__":
    if compile_bpython():
        print("\n🎉 bpython.exe编译完成!")
    else:
        print("\n💥 bpython.exe编译失败!")