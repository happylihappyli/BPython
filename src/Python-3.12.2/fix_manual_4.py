
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

# Lib/tkinter/__init__.py: 121
replace_line('Lib/tkinter/__init__.py', 121, 'except AttributeError: pass')

# Lib/tokenize.py: 540
replace_line('Lib/tokenize.py', 540, '        if type(e) != SyntaxError:')

# Lib/turtle.py: 2286
replace_line('Lib/turtle.py', 2286, '            if color == self._fillcolor:')

# Lib/typing.py: 2859
replace_line('Lib/typing.py', 2859, '            for n, tp in own_annotations.items()}')

# Lib/unittest/mock.py: 583
replace_line('Lib/unittest/mock.py', 583, '        if (sf is not None and not callable(sf)')

# Lib/unittest/result.py: 93
replace_line('Lib/unittest/result.py', 93, '                    if error:')

# Lib/urllib/request.py: 661
replace_line('Lib/urllib/request.py', 661, '            or code in (301, 302, 303) and m == "POST"):')

# Lib/venv/__init__.py: 426
replace_line('Lib/venv/__init__.py', 426, "                if (os.name == 'nt' and f.startswith('python')")

# Lib/xml/dom/expatbuilder.py: 273
replace_line('Lib/xml/dom/expatbuilder.py', 273, '            if (  self._cdata_continue')

# Lib/xml/dom/minidom.py: 1843 and 1848
replace_line('Lib/xml/dom/minidom.py', 1843, '                if (  prefix == "xmlns"')
replace_line('Lib/xml/dom/minidom.py', 1848, '                if (  name == "xmlns"')

# Lib/zipfile/__init__.py: 716
replace_line('Lib/zipfile/__init__.py', 716, '}')

# Lib/tracemalloc.py: 443
replace_line('Lib/tracemalloc.py', 443, '            if not any(trace_filter._match(trace)')
