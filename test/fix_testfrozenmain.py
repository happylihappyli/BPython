#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复_RegenTestFrozenmain目标
修改regen.targets文件，跳过测试冻结模块的再生步骤
"""

import os

def fix_testfrozenmain_target():
    """修复_RegenTestFrozenmain目标"""
    
    regen_targets_file = r"e:\GitHub3\cpp\BPython\src\Python-3.12.2\PCbuild\regen.targets"
    
    # 读取文件内容
    with open(regen_targets_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 备份原文件
    backup_file = regen_targets_file + ".backup_testfrozenmain"
    with open(backup_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✓ 已备份原文件: {backup_file}")
    
    # 查找_RegenTestFrozenmain目标
    target_name = "_RegenTestFrozenmain"
    start_marker = f'<Target Name="{target_name}"'
    end_marker = '</Target>'
    
    start_idx = content.find(start_marker)
    if start_idx == -1:
        print(f"❌ 未找到{target_name}目标")
        return False
    
    # 找到目标结束位置
    target_start = content.find('>', start_idx) + 1
    target_end = content.find(end_marker, target_start)
    
    if target_end == -1:
        print(f"❌ 未找到{target_name}目标结束位置")
        return False
    
    # 替换目标内容
    old_target = content[start_idx:target_end + len(end_marker)]
    new_target = f'''<Target Name="{target_name}"
          Inputs="@(_TestFrozenSources)" Outputs="@(_TestFrozenOutputs)"
          Condition="($(Platform) == 'Win32' or $(Platform) == 'x64') and
                     $(Configuration) != 'PGInstrument' and $(Configuration) != 'PGUpdate'">
    <Message Text="跳过{target_name}重新生成 - 使用现有文件" Importance="high" />
    <!-- 跳过重新生成，直接使用现有文件 -->
    <Exec Command="echo 跳过{target_name}重新生成" />
  </Target>'''
    
    content = content.replace(old_target, new_target)
    
    # 写入修改后的内容
    with open(regen_targets_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ 已修复{target_name}目标")
    print(f"📁 文件位置: {regen_targets_file}")
    
    return True

def main():
    """主函数"""
    print("🚀 开始修复_RegenTestFrozenmain目标...")
    
    try:
        if fix_testfrozenmain_target():
            print("🎉 _RegenTestFrozenmain目标修复完成!")
            print("📝 现在可以尝试重新编译bpython.exe")
        else:
            print("❌ 目标修复失败")
    except Exception as e:
        print(f"❌ 修复过程中出错: {e}")

if __name__ == "__main__":
    main()