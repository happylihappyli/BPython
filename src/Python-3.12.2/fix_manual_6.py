
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

# Lib/tkinter/__init__.py: 3708
replace_line('Lib/tkinter/__init__.py', 3708, '        if not command:')

# Lib/turtle.py: 3434
replace_line('Lib/turtle.py', 3434, '        if not color:')

# Lib/unittest/mock.py: 1516
replace_line('Lib/unittest/mock.py', 1516, '                if (not _is_list(this_spec) and not')

# Lib/unittest/result.py: 201
replace_line('Lib/unittest/result.py', 201, '            if error:')

# Lib/urllib/request.py: 1280
replace_line('Lib/urllib/request.py', 1280, "            if (not request.has_header('Content-length')")

# Lib/xml/dom/expatbuilder.py: 507
replace_line('Lib/xml/dom/expatbuilder.py', 507, '    }')
