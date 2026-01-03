import module_py
import module_bpy

def main():
    print("Testing imports from .py file:")
    module_py.hello_from_py()
    module_bpy.hello_from_bpy()

if __name__ == "__main__":
    main()
