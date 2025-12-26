
import os
import difflib

# Paths
placeholders_dir = r"C:\Users\kryst\Workspace\Literature\the-kryssie-method-citations\sources"
projects_dir = r"C:\Users\kryst\Workspace\Literature\the-kryssie-method-citations\projects"
file_list_path = r"C:\Users\kryst\Workspace\Literature\Literature Testing\all_files_list.txt"
workspace_root = r"C:\Users\kryst\Workspace\Literature"

# Load candidate files
with open(file_list_path, "r", encoding="utf-8", errors="ignore") as f:
    all_files = [line.strip() for line in f.readlines()]

# Filter candidates (exclude the citations repo itself to avoid self-match)
candidates = [f for f in all_files if "the-kryssie-method-citations" not in f and os.path.isfile(f)]

def find_best_match(target_name, candidate_list):
    # normalize target: remove extension, replace underscores with spaces
    target_clean = os.path.splitext(target_name)[0].replace("_", " ").lower()
    
    best_match = None
    best_ratio = 0.0
    
    for cand in candidate_list:
        cand_name = os.path.basename(cand)
        cand_clean = os.path.splitext(cand_name)[0].replace("_", " ").replace("-", " ").lower()
        
        # Exact match check first (ignoring ext)
        if target_clean == cand_clean:
             return cand, 1.0

        # Fuzzy match
        ratio = difflib.SequenceMatcher(None, target_clean, cand_clean).ratio()
        if ratio > best_ratio:
            best_ratio = ratio
            best_match = cand
            
    return best_match, best_ratio

# Audit Sources
print("# Citation Hub Audit Report\n")
print("## Sources Mapping\n")

placeholders = os.listdir(placeholders_dir)
for p in placeholders:
    match, score = find_best_match(p, candidates)
    if score > 0.6: # Threshold
        print(f"- **{p}** matches `{os.path.relpath(match, workspace_root)}` (Confidence: {score:.2f})")
    else:
        print(f"- **{p}** - *No confident match found*")

print("\n## Projects Mapping\n")
project_placeholders = os.listdir(projects_dir)
for p in project_placeholders:
    match, score = find_best_match(p, candidates)
    if score > 0.6:
        print(f"- **{p}** matches `{os.path.relpath(match, workspace_root)}` (Confidence: {score:.2f})")
    else:
         print(f"- **{p}** - *No confident match found*")
