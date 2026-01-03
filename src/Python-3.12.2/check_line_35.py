import glob
import os

def check_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            if len(lines) >= 35:
                line35 = lines[34].strip()
                if ')' in line35 or '}' in line35 or '{' in line35:
                    print(f"{filepath}:35: {line35}")
    except Exception as e:
        pass

for root, dirs, files in os.walk("Lib"):
    for file in files:
        if file.endswith(".py"):
            check_file(os.path.join(root, file))
