
def split_part2(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    mid = len(lines) // 2
    part2a = lines[:mid]
    part2b = lines[mid:]
    
    with open('part2a.md', 'w', encoding='utf-8') as f:
        f.writelines(part2a)
        
    with open('part2b.md', 'w', encoding='utf-8') as f:
        f.writelines(part2b)
        
    print(f"Split part2.md into part2a.md ({len(part2a)} lines) and part2b.md ({len(part2b)} lines)")

if __name__ == "__main__":
    split_part2(r"C:\Users\kryst\Workspace\Literature\Literature Testing\part2.md")
