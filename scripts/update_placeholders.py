import re
import os

file_path = r'c:\Users\kryst\Workspace\Literature\Literature Testing\kryssie-method.md'
sources_dir = r"C:\Users\kryst\Workspace\Literature\the-kryssie-method-citations\sources"
projects_dir = r"C:\Users\kryst\Workspace\Literature\the-kryssie-method-citations\projects"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find all citations (already normalized)
pattern = re.compile(r'\[cite:(.*?)\]')
matches = pattern.findall(content)
unique_citations = sorted(list(set(matches)))

print(f"Found {len(unique_citations)} unique normalized citations.")

created_count = 0
skipped_count = 0

for slug in unique_citations:
    slug = slug.strip()
    safe_slug = "".join([c for c in slug if c.isalpha() or c.isdigit() or c in ('_','-','.','&')]).strip()
    filename = safe_slug.lower() + ".md"
    
    if 'landing' in filename or 'project' in filename or 'toolman' in filename:
        target_path = os.path.join(projects_dir, filename)
        doc_type = "project_landing"
    else:
        target_path = os.path.join(sources_dir, filename)
        doc_type = "source_document"

    if not os.path.exists(target_path):
        with open(target_path, 'w', encoding='utf-8') as f:
            f.write(f"---\n")
            f.write(f"id: {slug}\n")
            f.write(f"type: {doc_type}\n")
            f.write(f"status: placeholder\n")
            f.write(f"---\n\n")
            f.write(f"# {slug.replace('_', ' ')}\n\n")
            f.write(f"Placeholder for {slug}.\n")
        print(f"Created: {filename}")
        created_count += 1
    else:
        skipped_count += 1

print(f"Created {created_count} new placeholders. Skipped {skipped_count} existing.")
