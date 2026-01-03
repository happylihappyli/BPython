import py_compile
import sys
import os

files = [
    r"E:\GitHub3\cpp\BPython\src\Python-3.12.2\Lib\textwrap.py",
    r"E:\GitHub3\cpp\BPython\src\Python-3.12.2\Lib\tokenize.py",
    r"E:\GitHub3\cpp\BPython\src\Python-3.12.2\Lib\unittest\mock.py",
]

for f in files:
    print(f"Compiling {f}...")
    try:
        py_compile.compile(f, doraise=True)
        print("Success")
    except Exception as e:
        print(f"Error: {e}")
