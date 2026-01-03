import os
import re

def fix_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Skipping {filepath}: {e}")
        return

    new_lines = []
    modified = False
    for line in lines:
        stripped = line.strip()
        
        # Generic fix for trailing colons on line continuations
        # patterns: "(:", ",:", "or:", "and:"
        
        if stripped.endswith('(:') or stripped.endswith(',:') or stripped.endswith('or:') or stripped.endswith('and:'):
             # Make sure it's not a valid usage (which is hard to imagine for these specific endings)
             # e.g. "if (a or b):" is valid, but "if (a or b or:" is not.
             # "def foo(a,:" is not valid.
             
             # Check if it is "if ... :" which is valid?
             # But "if ... (:" is NOT valid.
             # "if ... or:" is NOT valid.
             
             # Replace the last char
             line = line.rstrip()[:-1] + '\n'
             modified = True
             # print(f"Fixed line in {filepath}: {line.strip()}")

        # Fix missing colon in except clauses
        if (stripped.startswith('except ') or stripped == 'except') and not stripped.endswith(':') and not stripped.endswith('\\'):
             line = line.rstrip() + ':\n'
             modified = True
        
        # Fix missing colon in class definitions
        if stripped.startswith('class ') and not stripped.endswith(':') and not stripped.endswith('\\'):
             # Check if it looks complete (balanced parens)
             if stripped.count('(') == stripped.count(')'):
                 line = line.rstrip() + ':\n'
                 modified = True


        new_lines.append(line)

    if modified:
        print(f"Fixing {filepath}")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)

def main():
    fix_file('Lib/argparse.py')
    root_dir = 'Lib'
    for root, dirs, files in os.walk(root_dir):
        if 'test' in dirs:
            dirs.remove('test')
        if 'tests' in dirs:
            dirs.remove('tests')
            
        for file in files:
            if file.endswith('.py'):
                fix_file(os.path.join(root, file))

if __name__ == '__main__':
    main()
