
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

# Lib/tkinter/__init__.py: 1654, 1664
replace_line('Lib/tkinter/__init__.py', 1654, '        except TclError: pass')
replace_line('Lib/tkinter/__init__.py', 1664, '        except TclError: pass')

# Lib/tracemalloc.py: 447
replace_line('Lib/tracemalloc.py', 447, '            if any(not trace_filter._match(trace)')

# Lib/turtle.py: 2399
replace_line('Lib/turtle.py', 2399, '                "tilt"          : self._tilt}')

# Lib/typing.py: 3395
replace_line('Lib/typing.py', 3395, '            "kwargs": kwargs,}')

# Lib/unittest/mock.py: 1086
replace_line('Lib/unittest/mock.py', 1086, '            if all([')

# Lib/unittest/result.py: 94, 95, 96
replace_line('Lib/unittest/result.py', 94, "                        if not error.endswith('\\n'):")
replace_line('Lib/unittest/result.py', 95, "                            error += '\\n'")
replace_line('Lib/unittest/result.py', 96, '                        self._original_stderr.write(STDERR_LINE % error)')

# Lib/urllib/request.py: 660 (indent correction)
replace_line('Lib/urllib/request.py', 660, '        if (not (code in (301, 302, 303, 307, 308) and m in ("GET", "HEAD"))')

# Lib/xml/dom/expatbuilder.py: 405
replace_line('Lib/xml/dom/expatbuilder.py', 405, '        if (self._options.whitespace_in_element_content')

# Lib/zipfile/__init__.py: 1204, 1216
replace_line('Lib/zipfile/__init__.py', 1204, '        if self._compressor:')
replace_line('Lib/zipfile/__init__.py', 1216, '            if self._compressor:')
