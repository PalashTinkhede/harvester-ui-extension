import sys

with open('pkg/harvester/l10n/en-us.yaml', 'r') as f:
    for i, line in enumerate(f, 1):
        if ': ' in line:
            key, value = line.split(': ', 1)
            value = value.strip()
            if not value:
                continue
            
            # Check for unbalanced single quotes
            if value.count("'") % 2 != 0:
                print(f"Unbalanced single quote at line {i}: {line.strip()}")
            
            # Check for unbalanced double quotes
            if value.count('"') % 2 != 0:
                print(f"Unbalanced double quote at line {i}: {line.strip()}")
            
            # Check for colons in unquoted values
            if ':' in value and not (value.startswith("'") and value.endswith("'")) and not (value.startswith('"') and value.endswith('"')):
                 print(f"Unquoted colon in value at line {i}: {line.strip()}")
