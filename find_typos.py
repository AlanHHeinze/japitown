import os
import re

search_dir = r"c:\Users\Alan\OneDrive\Desktop\Japitown\game\script"

def search_typos():
    results = []
    # common typo regex: anything that looks like an attempt at the mc name
    typos = [
        r'\[\s*(mcname|mc_nam|mcnombre|nombre|name|mc\s*name|player|mc)\s*\]',  # Wrong word in brackets
        r'\[\s+mc_name\s*\]|\[\s*mc_name\s+\]',  # Extra spaces inside brackets
        r'(?<!\[)mc_name(?!\])',  # mc_name without brackets
        r'\[mc_name(?=[\s\w.,!?¡¿])', # Missing closing bracket
        r'(?<=[\s\w.,!?¡¿])mc_name\]', # Missing opening bracket
    ]
    
    for root, _, files in os.walk(search_dir):
        for file in files:
            if file.endswith(".rpy"):
                path = os.path.join(root, file)
                with open(path, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                    
                for i, line in enumerate(lines):
                    # Only check lines with quotes (likely dialogue or strings)
                    if '"' in line:
                        for pattern in typos:
                            if re.search(pattern, line, re.IGNORECASE):
                                # Exclude legit python definitions like `define mc = Character("[mc_name]")`
                                # or python blocks like `$ mc_name = "..."`
                                if not line.strip().startswith('$') and not line.strip().startswith('default') and not line.strip().startswith('define'):
                                    results.append(f"{os.path.relpath(path, search_dir)}:{i+1}: {line.strip()}")
                                break
                                
    for r in results:
        print(r)

if __name__ == "__main__":
    search_typos()
