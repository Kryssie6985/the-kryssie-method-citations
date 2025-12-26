
def check_fences(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    fence_count = 0
    open_line = 0
    
    for i, line in enumerate(lines):
        # Look for triple backticks
        if line.strip().startswith('```'):
            fence_count += 1
            if fence_count % 2 != 0:
                open_line = i + 1
                curr_fence = line.strip()
            else:
                # Closed
                pass

    if fence_count % 2 != 0:
        print(f"ERROR: Unclosed code fence! Started at line {open_line}")
        print(f"Total fences found: {fence_count}")
    else:
        print(f"Code fences seem balanced. Total: {fence_count}")

if __name__ == "__main__":
    check_fences(r"C:\Users\kryst\Workspace\Literature\Literature Testing\kryssie-method-final.md")
