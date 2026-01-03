import os

filepath = 'Lib/argparse.py'
with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    stripped = line.strip()
    if i + 1 == 404:
        print(f"Line 404 content: {repr(line)}")
        print(f"Stripped: {repr(stripped)}")
        print(f"startswith('except '): {stripped.startswith('except ')}")
        print(f"endswith(':'): {stripped.endswith(':')}")
        print(f"endswith('\\'): {stripped.endswith('\\')}")
        
        if (stripped.startswith('except ') or stripped == 'except') and not stripped.endswith(':') and not stripped.endswith('\\'):
             print("MATCHED!")
        else:
             print("NOT MATCHED!")
