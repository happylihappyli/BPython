#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最终测试bpython.exe是否支持大括号语法
"""

import os
import subprocess
import tempfile

def test_bpython_braces():
    """测试bpython.exe是否支持大括号语法"""
    
    bpython_exe = r"e:\GitHub3\cpp\BPython\src\Python-3.12.2\PCbuild\amd64\bpython.exe"
    
    if not os.path.exists(bpython_exe):
        print("❌ bpython.exe 不存在")
        return False
    
    print(f"✅ 找到 bpython.exe: {bpython_exe}")
    
    # 创建测试代码（使用大括号语法）
    test_code = '''
# 测试大括号语法
if True {
    print("✅ if语句大括号语法工作正常")
}

# 测试函数定义
def test_function() {
    print("✅ 函数定义大括号语法工作正常")
    return "成功"
}

# 测试循环
for i in range(3) {
    print(f"循环迭代: {i}")
}

# 调用函数
result = test_function()
print(f"函数返回: {result}")

print("🎉 所有大括号语法测试通过!")
'''
    
    # 创建临时文件
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
        f.write(test_code)
        temp_file = f.name
    
    try:
        # 运行bpython.exe执行测试代码
        print("🚀 运行bpython.exe测试大括号语法...")
        
        result = subprocess.run([bpython_exe, temp_file], 
                              capture_output=True, text=True, encoding='utf-8', errors='replace')
        
        print("=== 标准输出 ===")
        print(result.stdout)
        
        if result.stderr:
            print("=== 标准错误 ===")
            print(result.stderr)
        
        if result.returncode == 0:
            print("✅ bpython.exe 执行成功!")
            
            # 检查输出是否包含预期的成功消息
            if "✅ if语句大括号语法工作正常" in result.stdout and "✅ 函数定义大括号语法工作正常" in result.stdout:
                print("🎉 bpython.exe 支持大括号语法!")
                return True
            else:
                print("⚠ bpython.exe 执行了代码，但输出不符合预期")
                return False
        else:
            print(f"❌ bpython.exe 执行失败，返回码: {result.returncode}")
            return False
            
    except Exception as e:
        print(f"❌ 测试过程中出错: {e}")
        return False
    
    finally:
        # 清理临时文件
        try:
            os.unlink(temp_file)
        except:
            pass

def test_bpython_interactive():
    """测试bpython.exe交互模式"""
    
    bpython_exe = r"e:\GitHub3\cpp\BPython\src\Python-3.12.2\PCbuild\amd64\bpython.exe"
    
    print("\n🚀 测试bpython.exe交互模式...")
    
    # 测试简单的交互命令
    test_commands = [
        "print('Hello, bPython!')",
        "2 + 2",
        "exit()"
    ]
    
    try:
        # 使用subprocess.Popen进行交互测试
        proc = subprocess.Popen([bpython_exe], 
                               stdin=subprocess.PIPE, 
                               stdout=subprocess.PIPE, 
                               stderr=subprocess.PIPE,
                               text=True, encoding='utf-8')
        
        # 发送测试命令
        for cmd in test_commands:
            proc.stdin.write(cmd + '\n')
            proc.stdin.flush()
        
        # 获取输出
        stdout, stderr = proc.communicate(timeout=10)
        
        print("=== 交互模式输出 ===")
        print(stdout)
        
        if stderr:
            print("=== 交互模式错误 ===")
            print(stderr)
        
        if proc.returncode == 0:
            print("✅ bpython.exe 交互模式工作正常!")
            return True
        else:
            print(f"❌ bpython.exe 交互模式失败，返回码: {proc.returncode}")
            return False
            
    except Exception as e:
        print(f"❌ 交互模式测试过程中出错: {e}")
        return False

def main():
    """主函数"""
    print("=" * 50)
    print("🚀 最终bpython.exe测试")
    print("=" * 50)
    
    # 测试大括号语法
    braces_success = test_bpython_braces()
    
    # 测试交互模式
    interactive_success = test_bpython_interactive()
    
    print("\n" + "=" * 50)
    print("📊 测试结果汇总")
    print("=" * 50)
    
    if braces_success and interactive_success:
        print("🎉 bpython.exe 编译和测试完全成功!")
        print("✅ 支持大括号语法")
        print("✅ 交互模式工作正常")
        print("\n🎊 项目成功完成!")
    else:
        print("⚠ bpython.exe 测试存在一些问题")
        if not braces_success:
            print("❌ 大括号语法测试失败")
        if not interactive_success:
            print("❌ 交互模式测试失败")

if __name__ == "__main__":
    main()