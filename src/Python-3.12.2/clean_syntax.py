import os
import re
import sys

def clean_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    modified = False
    for line in lines:
        original = line
        stripped = line.strip()
        
        # Skip comments
        if stripped.startswith('#'):
            new_lines.append(line)
            continue
            
        # 1. def/class/if/elif/while/for/with/try/except statement ending with {
        # Check if it starts with a keyword
        if re.match(r'^\s*(def|class|if|elif|while|for|with|try|except)\b', line):
            if stripped.endswith('{'):
                # Replace { with : if : is missing, or just remove { if : is present?
                # Usually in C-style, { replaces :.
                # But in compileall.py, 'if ... ( {' -> 'if ... ('
                
                # If it ends with '): {', replace with '):'
                if stripped.endswith('): {'):
                    line = line.replace('): {', '):')
                    modified = True
                elif stripped.endswith(') {'):
                    line = line.replace(') {', '):')
                    modified = True
                elif stripped.endswith(' {') and not stripped.endswith('= {'):
                    # Check if : is already there
                    if ':' in stripped[:-1]:
                        line = line.replace(' {', '')
                    else:
                        line = line.replace(' {', ':')
                    modified = True
        
        # 2. else { -> else:
        if re.match(r'^\s*else\s*\{\s*$', line):
            line = line.replace('{', ':')
            modified = True
            
        # 3. Argument lists or expressions ending with {
        # e.g. 'def foo(a, {' -> 'def foo(a,'
        # e.g. 'call(a, {' -> 'call(a,'
        # e.g. 'if ( {' -> 'if ('
        if stripped.endswith(', {') or stripped.endswith('( {') or stripped.endswith('({'):
             # But watch out for dicts: 'func({' is valid start of dict.
             # 'func( {' is valid.
             # 'func, {' is NOT valid dict start usually (unless tuple).
             
             # In compileall.py: 'compile_file(..., {'
             # In argparse.py: 'def __init__(self, {'
             
             # If it is 'def ... (..., {' -> remove {
             if 'def ' in line and stripped.endswith('{'):
                 line = line.replace('{', '')
                 modified = True
             elif stripped.endswith(', {') and not stripped.endswith(' = {') and not stripped.endswith(':{'):
                 # Assuming it's an argument list error
                 line = line.replace(', {', ',')
                 modified = True
             elif stripped.endswith('({'):
                 # Could be dict. Check next line?
                 # If next line is indented and has 'key: val' or 'val', it might be dict.
                 # But in our context, it's likely error.
                 # Let's be conservative. Only fix if it looks like the compileall patterns.
                 pass
             elif stripped.endswith('( {'):
                 line = line.replace('( {', '(')
                 modified = True
        
        # 4. 'if ... and ( {' -> 'if ... and ('
        if re.search(r'\(\s*\{$', stripped):
             # This matches '( {' and '({'
             # compileall.py had 'if ... ( {'
             if 'if ' in line or 'while ' in line:
                 line = line.replace('{', '')
                 modified = True
                 
        new_lines.append(line)

    if modified:
        print(f"Modifying {filepath}")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)

def main():
    root_dir = 'Lib'
    for root, dirs, files in os.walk(root_dir):
        if 'test' in dirs:
            dirs.remove('test')  # Skip test directories
        if 'tests' in dirs:
            dirs.remove('tests')

        for file in files:
            if file.endswith('.py'):
                try:
                    clean_file(os.path.join(root, file))
                except Exception as e:
                    print(f"Error processing {file}: {e}")

if __name__ == '__main__':
    main()
