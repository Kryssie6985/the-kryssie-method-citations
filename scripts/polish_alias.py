
import re

file_path = r'c:\Users\kryst\Workspace\Literature\Literature Testing\kryssie-method.md'
base_url = "https://github.com/kryssie6985/the-kryssie-method-citations/blob/main/sources"

# The old ugly slug
old_slug = "_Chapter_3:The_AI_Teacher(Finalized)"
# The new pretty slug
new_slug = "AI_Teacher_Chapter_3"

# 1. Update the Map Definition
# We want to replace "[cite:_Chapter_3:The_AI_Teacher(Finalized)]: URL" 
# with "[cite:AI_Teacher_Chapter_3]: URL"

# 2. Update the Usage in Text
# We want to replace "[cite:_Chapter_3:The_AI_Teacher(Finalized)]"
# with "[cite:AI_Teacher_Chapter_3]"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace usage
if f"[cite:{old_slug}]" in content:
    content = content.replace(f"[cite:{old_slug}]", f"[cite:{new_slug}]")
    print("Replaced usage in text.")
else:
    print("Usage not found (or already replaced).")

# Replace map definition
# Find the line starting with [cite:{new_slug}] (if already done) or [cite:{old_slug}]
# We need to construct the URL line.
# The URL should point to .../sources/chapter_3_the_ai_teacher.md

# Let's search for the old definition line using regex to be safe about the URL part
old_pattern = re.compile(re.escape(f"[cite:{old_slug}]") + r":\s*(.*)")
match = old_pattern.search(content)

if match:
    # We found the old definition
    url = match.group(1) # Reuse existing URL if valid, or force the new correct one? 
    # Force correct one to be safe: sources/chapter_3_the_ai_teacher.md
    correct_url = f"{base_url}/chapter_3_the_ai_teacher.md"
    
    new_line = f"[cite:{new_slug}]: {correct_url}"
    content = old_pattern.sub(new_line, content)
    print(f"Updated map definition to: {new_line}")
else:
    # Maybe add it if missing?
    # Or maybe it has a trailing underscore in the file? 
    # Let's check for the version with trailing underscore: _Chapter_3:The_AI_Teacher(Finalized)_
    old_slug_2 = "_Chapter_3:The_AI_Teacher(Finalized)_"
    if f"[cite:{old_slug_2}]" in content:
         content = content.replace(f"[cite:{old_slug_2}]", f"[cite:{new_slug}]")
         print("Replaced usage (variant 2) in text.")
         
    old_pattern_2 = re.compile(re.escape(f"[cite:{old_slug_2}]") + r":\s*(.*)")
    if old_pattern_2.search(content):
        correct_url = f"{base_url}/chapter_3_the_ai_teacher.md"
        new_line = f"[cite:{new_slug}]: {correct_url}"
        content = old_pattern_2.sub(new_line, content)
        print(f"Updated map definition (variant 2).")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
