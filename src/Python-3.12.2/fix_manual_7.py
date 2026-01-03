
import os

def replace_line(filepath, line_num, new_content):
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return
    
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    if line_num - 1 < len(lines):
        lines[line_num - 1] = new_content + '\n'
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        print(f"Fixed {filepath} at line {line_num}")
    else:
        print(f"Error: Line {line_num} out of range for {filepath}")

# Lib/unittest/mock.py: 1994
replace_line('Lib/unittest/mock.py', 1994, '}')

# Lib/urllib/request.py: 2035
replace_line('Lib/urllib/request.py', 2035, '        if (not port')

# Lib/xml/dom/expatbuilder.py: 507 (Verify/Fix)
replace_line('Lib/xml/dom/expatbuilder.py', 507, '    }')
