import re
import os

file_path = r'c:\Users\kryst\Workspace\Literature\Literature Testing\kryssie-method.md'

sources_dir = r"C:\Users\kryst\Workspace\Literature\the-kryssie-method-citations\sources"
projects_dir = r"C:\Users\kryst\Workspace\Literature\the-kryssie-method-citations\projects"

# Ensure directories exist (just in case user missed subdirs)
os.makedirs(sources_dir, exist_ok=True)
os.makedirs(projects_dir, exist_ok=True)

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find all citations
pattern = re.compile(r'\[cite:(.*?)\]')
matches = pattern.findall(content)
unique_citations = sorted(list(set(matches)))

created_count = 0

for slug in unique_citations:
    # Normalize slug to filename safe string just in case, though they should be underscores already
    # simple clean
    safe_slug = "".join([c for c in slug if c.isalpha() or c.isdigit() or c in ('_','-','.','&')]).strip()
    filename = safe_slug.lower() + ".md"
    
    # Determine target directory
    if 'landing' in filename or 'project' in filename or 'toolman' in filename:
        target_path = os.path.join(projects_dir, filename)
        doc_type = "project_landing"
    else:
        target_path = os.path.join(sources_dir, filename)
        doc_type = "source_document"

    # Only create if doesn't exist
    if not os.path.exists(target_path):
        with open(target_path, 'w', encoding='utf-8') as f:
            f.write(f"---\n")
            f.write(f"id: {slug}\n")
            f.write(f"type: {doc_type}\n")
            f.write(f"status: placeholder\n")
            f.write(f"---\n\n")
            f.write(f"# {slug.replace('_', ' ')}\n\n")
            f.write(f"Placeholder for {slug}.\n")
        created_count += 1

print(f"Created {created_count} placeholder files.")
