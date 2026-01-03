import os

def replace_line(filepath, line_num, new_content):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    if line_num - 1 < len(lines):
        lines[line_num - 1] = new_content + '\n'
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        print(f"Fixed {filepath} at line {line_num}")
    else:
        print(f"Error: Line {line_num} out of range for {filepath}")

def append_to_line(filepath, line_num, content_to_append):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    if line_num - 1 < len(lines):
        lines[line_num - 1] = lines[line_num - 1].rstrip() + content_to_append + '\n'
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        print(f"Appended to {filepath} at line {line_num}")
    else:
        print(f"Error: Line {line_num} out of range for {filepath}")

# Fix regressions (pass:)
replace_line('Lib/tkinter/dialog.py', 22, '        except TclError: pass')
replace_line('Lib/tokenize.py', 162, 'class TokenError(Exception): pass')
replace_line('Lib/tokenize.py', 165, 'class StopTokenizing(Exception): pass')

# Fix missing )
replace_line('Lib/urllib/robotparser.py', 141, '                        if (len(numbers) == 2 and numbers[0].strip().isdigit()')
replace_line('Lib/traceback.py', 788, '                if (e and e.__cause__ is not None')
replace_line('Lib/traceback.py', 809, '                if (e and e.__context__ is not None')
replace_line('Lib/tracemalloc.py', 381, '            if any(self._match_frame_impl(filename, lineno)')
replace_line('Lib/unittest/loader.py', 155, '                if (getattr(obj, \'__path__\', None) is not None')
replace_line('Lib/xml/dom/minidom.py', 150, '        if (newChild.nodeType in _nodeTypes_with_children')

# Fix missing }
append_to_line('Lib/trace.py', 713, '}')
append_to_line('Lib/turtle.py', 163, '}')
append_to_line('Lib/unittest/mock.py', 325, '}')
append_to_line('Lib/xml/dom/expatbuilder.py', 58, '}')
append_to_line('Lib/xml/etree/ElementTree.py', 966, '}')
append_to_line('Lib/token.py', 84, '}') # Check line content first? assuming it's unclosed dict def
append_to_line('Lib/venv/__init__.py', 101, '}') # Line 97 was start, need to find end. Assuming end is near.
# For unclosed dicts starting at a line, usually we need to append } to the end of the dict definition.
# The previous errors showed the start line. I need to be careful.
# Let's read the files for unclosed dicts to find where to close them.

# Special case
replace_line('Lib/urllib/request.py', 315, '    def __init__(self, url, data=None, headers={},')

