# 函数和类测试用例

# 测试函数和类
def calculate(a, b) {
    result = a + b
    if result > 10 {
        return "大于10"
    } else {
        return "小于等于10"
    }
}

class Person {
    def __init__(self, name) {
        self.name = name
    }
    
    def greet(self) {
        print(f"Hello, {self.name}!")
    }
}
