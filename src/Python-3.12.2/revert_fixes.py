import os

filepath = 'Lib/argparse.py'
with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Lines to revert (remove trailing colon)
# 294, 1648, 1879, 1880, 1884, 1885, 2115, 2177, 2178, 2426
# Note: Line numbers are 1-based. List index is 0-based.
lines_to_fix = [294, 1648, 1879, 1880, 1884, 1885, 2115, 2177, 2178, 2426]

for line_num in lines_to_fix:
    idx = line_num - 1
    if idx < len(lines):
        line = lines[idx]
        if line.strip().endswith(':'):
            print(f"Reverting line {line_num}: {line.strip()}")
            lines[idx] = line.rstrip()[:-1] + '\n' # Remove last char (:) and add newline

with open(filepath, 'w', encoding='utf-8') as f:
    f.writelines(lines)
