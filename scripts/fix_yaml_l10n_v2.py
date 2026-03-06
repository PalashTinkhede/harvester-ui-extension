import re

def fix_yaml_line(line):
    if ': ' not in line:
        return line
    
    parts = line.split(': ', 1)
    key = parts[0]
    value = parts[1].strip()
    
    if not value or value == '|-':
        return line
    
    # Check for unbalanced quotes at the start/end
    starts_with_quote = value.startswith("'") or value.startswith('"')
    ends_with_quote = value.endswith("'") or value.endswith('"')
    
    # If it ends with a quote but doesn't start with one, or vice-versa
    if ends_with_quote and not starts_with_quote:
        value = value[:-1] # Remove trailing unbalanced quote
    elif starts_with_quote and not ends_with_quote:
        value = value[1:] # Remove leading unbalanced quote
        
    # Now, check if it NEEDS quotes (contains symbols like :, {, }, [, ], ,, &, *, #, ?, |, -, <, >, =, !, %, @, `)
    # or starts with a problematic character or has multiple spaces.
    needs_quotes = any(char in value for char in ":{}[]!\"'#&*|>?=-%@`") or '  ' in value or value == 'True' or value == 'False' or value == 'None'
    
    if needs_quotes:
        # Re-quote it properly. Escape single quotes if we use single quotes for wrapping.
        value = value.strip('"').strip("'")
        value = value.replace("'", "''")
        value = f"'{value}'"
        
    # Restore harvesterhci.io (if it was somehow broken further)
    value = value.replace('ZEUShci.io', 'harvesterhci.io')
    
    indent = line[:line.find(key)]
    return f"{indent}{key}: {value}\n"

with open('pkg/harvester/l10n/en-us.yaml', 'r') as f:
    lines = f.readlines()

fixed_lines = [fix_yaml_line(line) for line in lines]

with open('pkg/harvester/l10n/en-us.yaml', 'w') as f:
    f.writelines(fixed_lines)
