# 异常处理测试用例

# 测试异常处理
try {
    file = open("test.txt", "r")
    content = file.read()
} except FileNotFoundError {
    print("文件不存在")
} except Exception as e {
    print(f"其他错误: {e}")
} finally {
    print("清理完成")
}
