import re
import os

file_path = r'c:\Users\kryst\Workspace\Literature\Literature Testing\kryssie-method.md'
# output_path = r'c:\Users\kryst\Workspace\Literature\Literature Testing\citation_map.md'

# Base URL for the github repo (user provided this structure)
# [cite:Slug]: https://github.com/kryssie6985/the-kryssie-method-citations/blob/main/sources/slug.md
# We will guess 'sources' vs 'projects' based on the name or just default to 'sources' for now, 
# or maybe map specific ones if we can.
# The user said: "You don't have to make the filename identical... But v0 you can do a small hand-built set."
# But for automation, let's just point them all to appropriate locations using a simple heuristic or just 'sources' for now.

BASE_URL = "https://github.com/kryssie6985/the-kryssie-method-citations/blob/main"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find all citations
pattern = re.compile(r'\[cite:(.*?)\]')
matches = pattern.findall(content)

# Deduplicate
unique_citations = sorted(list(set(matches)))

output_path = r'c:\Users\kryst\Workspace\Literature\Literature Testing\citation_map_block.md'

with open(output_path, 'w', encoding='utf-8') as f_out:
    f_out.write("\n\n## Citation References\n\n")

    for slug in unique_citations:
        # Heuristic: If it looks like a file extension is present, maybe map it?
        # Or just default everything to sources/slug.md (lowercased)
        
        # Clean slug for filename: lowercase
        # simple clean
        safe_slug = "".join([c for c in slug if c.isalpha() or c.isdigit() or c in ('_','-','.','&')]).strip()
        filename = safe_slug.lower() + ".md"
        
        # If the user wants specific mapping, we'd need a dictionary. 
        # For now, we'll generate the block and they can edit the URLs.
        # We will assume 'sources' directory for documents and concepts.
        
        url = f"{BASE_URL}/sources/{filename}"
    
    
    # Check if it looks like a project landing page
    if 'landing' in filename or 'project' in filename or 'toolman' in filename:
         url = f"{BASE_URL}/projects/{filename}.md"

    f_out.write(f"[cite:{slug}]: {url}\n")

print(f"Citation map written to {output_path}")
