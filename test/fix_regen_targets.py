#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复regen.targets文件，跳过解析器重新生成步骤
"""

import os
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

def fix_regen_targets():
    """修复regen.targets文件"""
    regen_file = "src/Python-3.12.2/PCbuild/regen.targets"
    
    if not backup_file(regen_file):
        return False
    
    with open(regen_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 需要修复的目标列表
    targets_to_fix = [
        "_RegenPegen",
        "_RegenKeywords",
        "_RegenAST_H",
        "_RegenTokens"
    ]
    
    for target_name in targets_to_fix:
        # 修改目标，跳过重新生成步骤
        start_marker = f'<Target Name="{target_name}"'
        end_marker = '</Target>'
        
        start_idx = content.find(start_marker)
        if start_idx == -1:
            print(f"警告: 未找到{target_name}目标")
            continue
        
        # 找到目标结束位置
        target_start = content.find('>', start_idx) + 1
        target_end = content.find(end_marker, target_start)
        
        if target_end == -1:
            print(f"警告: 未找到{target_name}目标结束位置")
            continue
        
        # 替换目标内容
        old_target = content[start_idx:target_end + len(end_marker)]
        new_target = f'''<Target Name="{target_name}"
          Inputs="@(_PegenSources)" Outputs="@(_PegenOutputs)"
          DependsOnTargets="FindPythonForBuild">
    <Message Text="跳过{target_name}重新生成 - 使用现有文件" Importance="high" />
    <!-- 跳过重新生成，直接使用现有文件 -->
    <Exec Command="echo 跳过{target_name}重新生成" />
  </Target>'''
        
        content = content.replace(old_target, new_target)
        print(f"✓ 已修复{target_name}目标")
    
    # 修改Regen目标，移除所有重新生成依赖
    regen_start = content.find('<Target Name="Regen"')
    if regen_start != -1:
        regen_end = content.find('</Target>', regen_start) + len('</Target>')
        regen_content = content[regen_start:regen_end]
        
        # 移除所有重新生成依赖
        new_regen_content = regen_content
        for target_name in targets_to_fix:
            new_regen_content = new_regen_content.replace(f'{target_name};', '')
        
        content = content.replace(regen_content, new_regen_content)
    
    with open(regen_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"已修改: {regen_file}")
    return True

def main():
    """主函数"""
    print("=== 修复regen.targets文件 ===")
    
    if fix_regen_targets():
        print("✓ regen.targets文件修复成功")
        return True
    else:
        print("✗ regen.targets文件修复失败")
        return False

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("\n🎉 修复完成!")
        else:
            print("\n❌ 修复失败!")
    except Exception as e:
        print(f"\n💥 修复过程中发生错误: {e}")