
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

# Lib/textwrap.py: 332
replace_line('Lib/textwrap.py', 332, '                            if (len(prev_line) + len(self.placeholder) <=')

# Lib/tomllib/_parser.py: 651
replace_line('Lib/tomllib/_parser.py', 651, 'def suffixed_err(src: str, pos: Pos, msg: str) -> TOMLDecodeError:')

# Lib/turtle.py: 2250
replace_line('Lib/turtle.py', 2250, '            if color == self._pencolor:')

# Lib/typing.py: 1770
replace_line('Lib/typing.py', 1770, "    'contextlib': ['AbstractContextManager', 'AbstractAsyncContextManager'],}")

# Lib/unittest/mock.py: 583
replace_line('Lib/unittest/mock.py', 583, '    if (sf is not None and not callable(sf)')

# Lib/urllib/request.py: 660
replace_line('Lib/urllib/request.py', 660, '    if (not (code in (301, 302, 303, 307, 308) and m in ("GET", "HEAD"))')

# Lib/venv/__init__.py: 426
replace_line('Lib/venv/__init__.py', 426, "    if (os.name == 'nt' and f.startswith('python')")

# Lib/xml/dom/expatbuilder.py: 273
replace_line('Lib/xml/dom/expatbuilder.py', 273, '    if (  self._cdata_continue')

# Lib/xml/dom/minidom.py: 1843
replace_line('Lib/xml/dom/minidom.py', 1843, '    if (  prefix == "xmlns"')

# Lib/xml/dom/xmlbuilder.py: 149 and 159
replace_line('Lib/xml/dom/xmlbuilder.py', 149, '            ("cdata_sections", 0),')
replace_line('Lib/xml/dom/xmlbuilder.py', 159, '            ("namespaces", 1)],}')

# Lib/xml/etree/ElementPath.py: 396
replace_line('Lib/xml/etree/ElementPath.py', 396, '    for select in selector:')

# Lib/zipfile/__init__.py: 253
replace_line('Lib/zipfile/__init__.py', 253, '    if sig != stringEndArchive64Locator:')

# Lib/zipimport.py: 818 (indent)
replace_line('Lib/zipimport.py', 818, '        if import_error:')

# Lib/tracemalloc.py: 443
replace_line('Lib/tracemalloc.py', 443, '    if not any(trace_filter._match(trace)')

# Lib/tkinter/__init__.py: 99 (unindent)
replace_line('Lib/tkinter/__init__.py', 99, 'except AttributeError: pass')
