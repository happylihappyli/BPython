import os

filepath = 'Lib/argparse.py'
with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
modified = False
for i, line in enumerate(lines):
    stripped = line.strip()
    if (stripped.startswith('except ') or stripped == 'except') and not stripped.endswith(':') and not stripped.endswith('\\'):
        print(f"Fixing line {i+1}: {stripped}")
        line = line.rstrip() + ':\n'
        modified = True
    elif (stripped.startswith('if ') or stripped.startswith('elif ') or stripped.startswith('while ') or stripped.startswith('for ') or stripped.startswith('def ') or stripped.startswith('class ') or stripped == 'else' or stripped == 'try' or stripped == 'finally') and not stripped.endswith(':') and not stripped.endswith('\\'):
        # Check paren balance
        if stripped.count('(') == stripped.count(')'):
             print(f"Fixing line {i+1}: {stripped}")
             line = line.rstrip() + ':\n'
             modified = True
    new_lines.append(line)

if modified:
    print(f"Writing {filepath}")
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
else:
    print("No changes made.")
