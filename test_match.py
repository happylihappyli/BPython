
def test():
    x = 1
    match x:
        case 1:
            print("One")
        case _:
            print("Other")

if __name__ == "__main__":
    test()
