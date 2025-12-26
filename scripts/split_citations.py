import re

file_path = r'c:\Users\kryst\Workspace\Literature\Literature Testing\kryssie-method.md'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Pattern to find citations with commas inside the bracket
# We reuse the logic: [cite: slug]
# We want to find cases where slug contains a comma
citation_pattern = re.compile(r'\[cite:(.*?)\]', re.DOTALL)

def split_composite_citations(match):
    full_match = match.group(0)
    inner = match.group(1)
    
    # Check for comma
    if ',' in inner:
        # Split by comma
        parts = [p.strip() for p in inner.split(',')]
        
        # specific fix for the one in screenshot which might have a newline
        # "Template,\n_NotebookLM..."
        
        normalized_parts = []
        for p in parts:
            # normalize each part individually
            clean_p = re.sub(r'\s+', ' ', p).strip() # collapse space
            clean_p = clean_p.replace(' ', '_')      # space to underscore
            # remove redundant underscores if any (e.g. from previous normalization)
            # actually previous normalization might have made it "A,_B"
            # so splitting by ',' is safe if we strip surrounding chars.
            
            # If the user script previously ran, "A, B" became "A,_B" or similar?
            # Wait, my previous script: `normalized_inner = inner.replace(' ', '_')`
            # So `A, B` became `A,_B`.
            # So I should look for `,_` or just `,` if underscore was missed?
            # Actually, `replace(' ', '_')` converts `A, B` to `A,_B`.
            # So the splitting char is likely `,_` or just `,`
            
            normalized_parts.append(f"[cite:{clean_p}]")
            
        return " ".join(normalized_parts)
    
    return full_match

# We need to handle the fact that they might already be normalized with underscores.
# e.g. [cite:Foo,_Bar]
# The user's screenshot showed `[cite: ...Template, _NotebookLM...]` (with a space or newline?).
# Wait, if I ran the script, it replaced spaces.
# So `Template, NotebookLM` became `Template,_NotebookLM`.
# So I should split on `,_` or `,`.

def refinement_sub(match):
    full_match = match.group(0)
    inner = match.group(1)
    
    # Heuristic: split on comma
    if ',' in inner:
        parts = inner.split(',')
        new_blocks = []
        for p in parts:
            p = p.strip()
            # clean leading/trailing underscores
            p = p.strip('_')
            if p:
                new_blocks.append(f"[cite:{p}]")
        
        print(f"Splitting: {full_match} -> {' '.join(new_blocks)}")
        return " ".join(new_blocks)
    return full_match

new_content, count = citation_pattern.subn(refinement_sub, content)

if count > 0:
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Refined {count} compound citations.")
else:
    print("No compound citations found to split.")
