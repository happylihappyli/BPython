
import re
import sys

file_path = r"E:\GitHub3\cpp\BPython\src\Python-3.12.2\Lib\encodings\aliases.py"

def normalize_encoding(encoding):
    chars = []
    punct = False
    for c in encoding:
        if c.isalnum() or c == '.':
            if punct and chars:
                chars.append('_')
            chars.append(c)
            punct = False
        else:
            punct = True
    return ''.join(chars)

with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    match = re.match(r"(\s*)'([^']+)': '([^']+)',", line)
    if match:
        indent = match.group(1)
        key = match.group(2)
        val = match.group(3)
        
        new_key = normalize_encoding(key)
        new_lines.append(f"{indent}'{new_key}': '{val}',\n")
    else:
        new_lines.append(line)

with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Fixed aliases.py")
