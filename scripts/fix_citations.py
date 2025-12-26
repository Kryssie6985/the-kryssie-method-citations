import re
import os

file_path = r'c:\Users\kryst\Workspace\Literature\Literature Testing\kryssie-method.md'
map_block_path = r'c:\Users\kryst\Workspace\Literature\Literature Testing\citation_map_block.md'

BASE_URL = "https://github.com/kryssie6985/the-kryssie-method-citations/blob/main"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Normalize Citations (Handle Multiline)
# Use DOTALL to match across lines
pattern = re.compile(r'\[cite:(.*?)\]', re.DOTALL)

def normalize_match(match):
    full_match = match.group(0)
    inner = match.group(1)
    
    # Collapse newlines and multiple spaces into single space first
    clean_inner = re.sub(r'\s+', ' ', inner).strip()
    
    # Then replace spaces with underscores
    normalized_inner = clean_inner.replace(' ', '_')
    
    return f"[cite:{normalized_inner}]"

new_content, count = pattern.subn(normalize_match, content)

print(f"Refined normalization count: {count}")

# 2. Generate Map
# Find the new normalized citations
matches = pattern.findall(new_content)
date_sorted_citations = sorted(list(set(matches)))

map_content = "\n\n## Citation References\n\n"

for slug in date_sorted_citations:
    # clean slug for filename (remove newlines if any remained, though they shouldn't)
    slug = slug.strip()
    # simple filename clean
    safe_slug = "".join([c for c in slug if c.isalpha() or c.isdigit() or c in ('_','-','.','&')]).strip()
    filename = safe_slug.lower() + ".md"
    
    url = f"{BASE_URL}/sources/{filename}"
    if 'landing' in filename or 'project' in filename or 'toolman' in filename:
         url = f"{BASE_URL}/projects/{filename}"
         
    map_content += f"[cite:{slug}]: {url}\n"

# 3. Write Updated File (Content + Map)
# First, remove any existing map if present (heuristic: "## Citation References")
if "## Citation References" in new_content:
    new_content = new_content.split("## Citation References")[0].strip()

# Write content back
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(new_content)
    f.write(map_content)

print(f"Updated {file_path} with {len(date_sorted_citations)} unique citations in map.")

# Also verify the count match
if len(date_sorted_citations) == 0:
    print("WARNING: No citations found!")
elif abs(len(date_sorted_citations) - 97) > 10:
     print(f"WARNING: Found {len(date_sorted_citations)} citations, user count was ~97.")

