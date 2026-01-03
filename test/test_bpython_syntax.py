#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试 bpython 大括号语法的脚本
这个脚本用于验证修改后的 Python 解释器是否正确处理大括号语法
"""

def test_basic_brace_syntax():
    """测试基本的大括号语法"""
    print("=== 测试基本大括号语法 ===")
    
    # 测试 if 语句
    x = 10
    if x > 5 {
        print("if 语句测试通过: x > 5")
    }
    
    # 测试 for 循环
    for i in range(3) {
        print(f"for 循环测试通过: i = {i}")
    }
    
    # 测试 while 循环
    count = 0
    while count < 3 {
        print(f"while 循环测试通过: count = {count}")
        count += 1
    }
    
    # 测试函数定义
def test_function() {
    print("函数定义测试通过")
    return "函数返回值"
}

result = test_function()
print(f"函数返回值: {result}")

def test_nested_braces():
    """测试嵌套的大括号"""
    print("\n=== 测试嵌套大括号 ===")
    
    for i in range(2) {
        if i == 0 {
            print("嵌套测试通过: i == 0")
        } else {
            print("嵌套测试通过: i != 0")
        }
    }

def test_class_definition():
    """测试类定义"""
    print("\n=== 测试类定义 ===")
    
    class TestClass {
        def __init__(self, name) {
            self.name = name
        }
        
        def greet(self) {
            print(f"类方法测试通过: Hello, {self.name}!")
        }
    }
    
    obj = TestClass("BPython")
    obj.greet()

def test_try_except():
    """测试异常处理"""
    print("\n=== 测试异常处理 ===")
    
    try {
        result = 10 / 0
    } except ZeroDivisionError {
        print("异常处理测试通过: 成功捕获除零错误")
    } finally {
        print("finally 块测试通过")
    }

def test_list_comprehension():
    """测试列表推导式"""
    print("\n=== 测试列表推导式 ===")
    
    # 测试列表推导式
    squares = [x*x for x in range(5)]
    print(f"列表推导式测试通过: {squares}")
    
    # 测试带条件的列表推导式
    even_squares = [x*x for x in range(10) if x % 2 == 0]
    print(f"带条件的列表推导式测试通过: {even_squares}")

def test_with_statement():
    """测试 with 语句"""
    print("\n=== 测试 with 语句 ===")
    
    # 创建一个简单的上下文管理器
    class SimpleContextManager {
        def __enter__(self) {
            print("进入上下文")
            return self
        }
        
        def __exit__(self, exc_type, exc_val, exc_tb) {
            print("退出上下文")
    }
    
    with SimpleContextManager() {
        print("with 语句测试通过")
    }

def main():
    """主测试函数"""
    print("开始测试 bpython 大括号语法")
    print("=" * 50)
    
    try:
        test_basic_brace_syntax()
        test_nested_braces()
        test_class_definition()
        test_try_except()
        test_list_comprehension()
        test_with_statement()
        
        print("\n" + "=" * 50)
        print("所有语法测试完成！")
        
    except Exception as e:
        print(f"测试过程中出现错误: {e}")
        print("这可能是由于 bpython.exe 尚未完全编译或语法修改存在问题")

if __name__ == "__main__" {
    main()
}