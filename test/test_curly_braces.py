# 测试大括号语法
# 这个文件使用大括号语法来测试bpython.exe

# 测试if语句
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