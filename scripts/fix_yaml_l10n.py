import re

def fix_yaml_value(line):
    if ': ' not in line:
        return line
    
    parts = line.split(': ', 1)
    key = parts[0]
    value = parts[1].strip()
    
    if not value or value == '|-':
        return line
    
    # If the value contains ZEUS and looks suspicious (unbalanced quotes or colons)
    if 'ZEUS' in value:
        # Remove trailing single/double quotes if they are unbalanced
        if (value.endswith("'") and value.count("'") % 2 != 0):
             value = value[:-1]
        if (value.endswith('"') and value.count('"') % 2 != 0):
             value = value[:-1]
             
        # If it doesn't start with a quote but has spaces or colons or internal quotes
        if not (value.startswith("'") and value.endswith("'")) and not (value.startswith('"') and value.endswith('"')):
            # Escape single quotes and wrap in single quotes
            value = value.replace("'", "''")
            value = f"'{value}'"
            
    # Reconstruct the line with correct indentation
    indent = line[:line.find(key)]
    return f"{indent}{key}: {value}\n"

with open('pkg/harvester/l10n/en-us.yaml', 'r') as f:
    lines = f.readlines()

fixed_lines = [fix_yaml_value(line) for line in lines]

with open('pkg/harvester/l10n/en-us.yaml', 'w') as f:
    f.writelines(fixed_lines)
