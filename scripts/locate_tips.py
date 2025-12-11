import re

target_file = "kryssie-method.md"
extracted_file = "extracted_tips.txt"

# Read Target
with open(target_file, "r", encoding="utf-8") as f:
    target_lines = [l.strip() for l in f.readlines()]

# Read Extracted Tips (Parser logic duplicated for simplicity, or just read the raw PTI for context)
# Actually, I'll just parse extracted_tips.txt since it's cleaner
with open(extracted_file, "r", encoding="utf-8") as f:
    raw_tips = f.read().split("--------------------")

locations = []

for i, raw_tip in enumerate(raw_tips):
    if not raw_tip.strip(): continue
    
    # Parse Context and Tip
    # Format is:
    # Line <num>
    # Context: ['line1', 'line2']
    # Tip: ...
    
    lines = raw_tip.strip().split('\n')
    tip_content = ""
    context_lines = []
    
    for l in lines:
        if l.startswith("Tip: "):
            tip_content = l[5:].strip()
        elif l.startswith("Context: "):
            # naive eval of list string
            try:
                context_str = l[len("Context: "):]
                context_lines = eval(context_str)
            except:
                pass

    if not context_lines or not tip_content:
        continue

    # Try to find context in target
    # We use the LAST line of context to find the insertion point
    last_context_line = context_lines[-1]
    
    # Normalize for matching (remove markdown bold/italic that might differ)
    def normalize(s):
        return re.sub(r'[\*\`]', '', s).strip()
    
    clean_context = normalize(last_context_line)
    
    found_line = -1
    for idx, tl in enumerate(target_lines):
        if clean_context in normalize(tl):
            found_line = idx + 1 # 1-indexed
            # Keep searching for best match? usually first is fine if unique enough
            # But let's assume unique enough
    
    locations.append({
        "id": i+1,
        "found_line": found_line,
        "tip_preview": tip_content[:30],
        "context_preview": clean_context[:30]
    })

print(f"Mapped {len(locations)} tips.")
for loc in locations:
    if loc['found_line'] != -1:
        print(f"Tip {loc['id']} -> Line {loc['found_line']}")
    else:
        print(f"Tip {loc['id']} -> NOT FOUND ({loc['context_preview']}...)")
