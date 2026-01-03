# 标准 Python 语法测试
# 预期：正常运行
def greet(name):
    if name:
        print(f"Hello, {name} from .py!")
    else:
        print("Hello from .py!")

class Greeter:
    def __init__(self):
        self.msg = "Standard Python Class"
    
    def say(self):
        print(self.msg)

if __name__ == "__main__":
    greet("哈哈")
    g = Greeter()
    g.say()
