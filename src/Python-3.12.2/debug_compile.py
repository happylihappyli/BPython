import os
import compileall
import sys

def compile_file(path):
    print(f"Compiling {path}...", flush=True)
    try:
        compileall.compile_file(path, force=True, quiet=1)
    except Exception as e:
        print(f"Error compiling {path}: {e}")

def walk_and_compile(dir_path):
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file.endswith('.py'):
                full_path = os.path.join(root, file)
                compile_file(full_path)

if __name__ == "__main__":
    walk_and_compile('Lib')
