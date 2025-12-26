
import os
import difflib
import re

# Paths
literature_root = r"C:\Users\kryst\Workspace\Literature"
placeholders_source_dir = r"C:\Users\kryst\Workspace\Literature\the-kryssie-method-citations\sources"
placeholders_projects_dir = r"C:\Users\kryst\Workspace\Literature\the-kryssie-method-citations\projects"

# Helper to normalize strings for comparison
def normalize_string(s):
    # Lowercase, remove extension
    s = os.path.splitext(s)[0].lower()
    # Replace separators with spaces
    s = re.sub(r'[_\-\.]', ' ', s)
    # Remove non-alphanumeric chars (except spaces)
    s = re.sub(r'[^a-z0-9\s]', '', s)
    return " ".join(s.split())

# 1. Index all files in Literature (skipping the citations repo)
print("Indexing workspace files...")
file_index = []
excluded_dirs = ["the-kryssie-method-citations", ".git", ".gemini", "node_modules"]

for root, dirs, files in os.walk(literature_root):
    # Modify dirs in-place to skip excluded
    dirs[:] = [d for d in dirs if d not in excluded_dirs]
    
    for f in files:
        if f.endswith(".md") or f.endswith(".txt") or f.endswith(".pdf") or f.endswith(".jpg"):
            full_path = os.path.join(root, f)
            norm_name = normalize_string(f)
            file_index.append({
                "path": full_path,
                "name": f,
                "norm_name": norm_name
            })

print(f"Indexed {len(file_index)} candidate files.\n")

# 2. Match Placeholders
def audit_directory(placeholder_dir, label):
    print(f"## {label} Audit\n")
    if not os.path.exists(placeholder_dir):
        print(f"Directory not found: {placeholder_dir}")
        return

    placeholders = [p for p in os.listdir(placeholder_dir) if p.endswith(".md")]
    
    for p in placeholders:
        p_norm = normalize_string(p)
        
        # Find best match
        best_match = None
        best_score = 0.0
        
        for candidate in file_index:
            # Check for substring inclusion (strong indicator) or fuzzy match
            
            # 1. Exact normalized match
            if p_norm == candidate["norm_name"]:
                score = 1.0
            # 2. Substring match (candidate contains placeholder words)
            elif p_norm in candidate["norm_name"]:
                score = 0.9 # High confidence if placeholder is a subset
            elif candidate["norm_name"] in p_norm:
                score = 0.8 # High confidence if candidate is a subset (e.g. short filename)
            # 3. Fuzzy match
            else:
                score = difflib.SequenceMatcher(None, p_norm, candidate["norm_name"]).ratio()
            
            if score > best_score:
                best_score = score
                best_match = candidate

        rel_path = "N/A"
        if best_match:
             rel_path = os.path.relpath(best_match["path"], literature_root)

        if best_score > 0.6:
            print(f"MATCH: [{p}] matches [{rel_path}] (Score: {best_score:.2f})")
            # Generate a copy command or suggestion?
        else:
            print(f"MISS:  [{p}] - No confident match. Best was [{rel_path}] ({best_score:.2f})")

audit_directory(placeholders_source_dir, "Sources")
print("-" * 40)
audit_directory(placeholders_projects_dir, "Projects")
