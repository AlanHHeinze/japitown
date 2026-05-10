import os
import re

def scan_rpy_files():
    script_dir = r"c:/Users/Alan/OneDrive/Desktop/Japitown/game/script"
    
    char_signatures = {
        'violet': ['violet_parada', 'sprites_violet'],
        'jasmine': ['jasmine_parada', 'jasmine_paradadeportiva', 'sprites_jasmine'],
        'monica': ['monica_parada', 'monica_perfume', 'sprites_monica'],
        'mc': ['mc_parado_base', 'mc_espalda_base', 'sprites_mc']
    }
    
    ambiguous = []
    
    pattern = re.compile(r'\b([ob]_[a-zA-ZñÑáéíóú]+)\b')
    
    for root, dirs, files in os.walk(script_dir):
        for f in files:
            if f.endswith('.rpy'):
                filepath = os.path.join(root, f)
                with open(filepath, 'r', encoding='utf-8') as file:
                    lines = file.readlines()
                
                for i, line in enumerate(lines):
                    matches = pattern.findall(line)
                    if matches:
                        # Find context
                        ctx = []
                        for char, sigs in char_signatures.items():
                            if any(sig in line.lower() for sig in sigs) or any(sig in filepath.lower() for sig in sigs):
                                ctx.append(char)
                        
                        if len(ctx) != 1:
                            ambiguous.append((filepath, i+1, line.strip(), matches, ctx))

    with open(r"c:\Users\Alan\OneDrive\Desktop\Japitown\ambiguous_tags.txt", "w", encoding='utf-8') as out:
        for a in ambiguous:
            out.write(f"{a[0]}:{a[1]} | Ctx: {a[4]} | {a[2]}\n")

if __name__ == "__main__":
    scan_rpy_files()
