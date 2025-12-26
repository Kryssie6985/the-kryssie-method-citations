
def split_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    mid = len(lines) // 2
    part1 = lines[:mid]
    part2 = lines[mid:]
    
    with open('part1.md', 'w', encoding='utf-8') as f:
        f.writelines(part1)
        
    with open('part2.md', 'w', encoding='utf-8') as f:
        f.writelines(part2)
        
    print(f"Split into part1.md ({len(part1)} lines) and part2.md ({len(part2)} lines)")

if __name__ == "__main__":
    split_file(r"C:\Users\kryst\Workspace\Literature\Literature Testing\kryssie-method-final.md")
