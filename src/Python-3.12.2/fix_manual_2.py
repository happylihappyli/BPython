
import os

def replace_line(filepath, line_num, new_content):
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return
    
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    if line_num - 1 < len(lines):
        # Check if we are appending a brace to a line that already has content
        # For dictionary closing, we usually want to append '}' on a new line or at the end
        # But if the line ends with a comma, we might want to put '}' after it?
        # Or just replace the line with content + '}'?
        
        # Special handling for "append }" logic if new_content starts with special marker
        # But here I will provide the FULL new content for that line.
        
        current_content = lines[line_num - 1].rstrip('\n')
        # If I want to append '}', I should provide the full line with '}' appended
        # or replace with a block?
        # Let's just replace the line.
        
        lines[line_num - 1] = new_content + '\n'
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        print(f"Fixed {filepath} at line {line_num}")
    else:
        print(f"Error: Line {line_num} out of range for {filepath}")

# Lib/tkinter/__init__.py: line 99 except AttributeError: pass: -> except AttributeError: pass
replace_line('Lib/tkinter/__init__.py', 99, '    except AttributeError: pass')

# Lib/tkinter/colorchooser.py: line 75 if color -> if color:
replace_line('Lib/tkinter/colorchooser.py', 75, '    if color:')

# Lib/tokenize.py: line 540 if type(e) != SyntaxError -> if type(e) != SyntaxError:
replace_line('Lib/tokenize.py', 540, '    if type(e) != SyntaxError:')

# Lib/trace.py: append } to line 725
# Line 725 was: '                '__cached__': None,
replace_line('Lib/trace.py', 725, "                '__cached__': None,}")

# Lib/tracemalloc.py: line 443
replace_line('Lib/tracemalloc.py', 443, '    if not any(trace_filter._match(trace)):')

# Lib/turtledemo/clock.py: line 72
replace_line('Lib/turtledemo/clock.py', 72, '    for hand in second_hand, minute_hand, hour_hand:')

# Lib/types.py: line 169
replace_line('Lib/types.py', 169, '    except AttributeError:')

# Lib/typing.py: line 1088
replace_line('Lib/typing.py', 1088, '    if error:')

# Lib/unittest/mock.py: line 583
replace_line('Lib/unittest/mock.py', 583, '    if (sf is not None and not callable(sf)):')

# Lib/unittest/result.py: line 93
replace_line('Lib/unittest/result.py', 93, '    if error:')

# Lib/urllib/request.py: line 660
replace_line('Lib/urllib/request.py', 660, '    if (not (code in (301, 302, 303, 307, 308) and m in ("GET", "HEAD"))):')

# Lib/venv/__init__.py: line 426
replace_line('Lib/venv/__init__.py', 426, "    if (os.name == 'nt' and f.startswith('python')):")

# Lib/xml/dom/expatbuilder.py: line 273
replace_line('Lib/xml/dom/expatbuilder.py', 273, '    if (  self._cdata_continue):')

# Lib/xml/dom/minidom.py: line 1843
replace_line('Lib/xml/dom/minidom.py', 1843, '    if (  prefix == "xmlns"):')

# Lib/xml/dom/xmlbuilder.py: append } to line 149
# Line 149 was:             ("cdata_sections", 0),
replace_line('Lib/xml/dom/xmlbuilder.py', 149, '            ("cdata_sections", 0),}')

# Lib/xml/etree/ElementPath.py: append } to line 345
# Line 345 was:     "[": prepare_predicate,
replace_line('Lib/xml/etree/ElementPath.py', 345, '    "[": prepare_predicate,}')

# Lib/xml/etree/ElementTree.py: append } to line 997
# Line 997 was:     "http://purl.org/dc/elements/1.1/": "dc",
replace_line('Lib/xml/etree/ElementTree.py', 997, '    "http://purl.org/dc/elements/1.1/": "dc",}')

# Lib/zipfile/__init__.py: line 250
replace_line('Lib/zipfile/__init__.py', 250, '    if len(data) != sizeEndCentDir64Locator:')

# Lib/zipimport.py: line 818
replace_line('Lib/zipimport.py', 818, '    if import_error:')

# Lib/tomllib/_parser.py: line 49 ) -> })
replace_line('Lib/tomllib/_parser.py', 49, '})')

# Lib/turtle.py: append } to line 977
# Line 977 was:                    "blank" : Shape("image", self._blankimage())
replace_line('Lib/turtle.py', 977, '                   "blank" : Shape("image", self._blankimage())}')

# Lib/uuid.py: append } to line 742 and 748
# Line 742 was:        "uuid5": uuid5
replace_line('Lib/uuid.py', 742, '        "uuid5": uuid5}')
# Line 748 was:        "@x500": NAMESPACE_X500
replace_line('Lib/uuid.py', 748, '        "@x500": NAMESPACE_X500}')

