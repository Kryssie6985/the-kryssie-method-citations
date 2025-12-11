import re
import os

file_path = r'c:\Users\kryst\Workspace\Literature\Literature Testing\kryssie-method.md'
normalized_path = r'c:\Users\kryst\Workspace\Literature\Literature Testing\kryssie-method-normalized.md'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Pattern: [cite: content]
# We need to find these blocks, and within them, replace space with underscore
# Note: simple regex replacement might be hard if we want to ONLY target spaces inside the brackets.
# Better to use a callback function.

def normalize_match(match):
    full_match = match.group(0) # e.g. [cite: Some Title, Author]
    inner = match.group(1)      # e.g.  Some Title, Author
    
    # Replace spaces with underscores
    normalized_inner = inner.replace(' ', '_')
    
    new_citation = f"[cite:{normalized_inner}]"
    
    if full_match != new_citation:
        print(f"Normalizing: {full_match} -> {new_citation}")
        
    return new_citation

# Regex explanation:
# \[cite:  : Match literal [cite:
# (.*?)    : Match inner content non-greedily (group 1)
# \]       : Match literal ]
pattern = re.compile(r'\[cite:(.*?)\]')

new_content, count = pattern.subn(normalize_match, content)

print(f"\nTotal citations normalized: {count}")

if count > 0:
    with open(normalized_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Normalized content written to: {normalized_path}")
else:
    print("No changes needed or no citations found.")
