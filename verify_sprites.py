import os
import re

def parse_layered_images(script_dir):
    valid_attributes = {}
    
    # We want to find layeredimage blocks and their attributes
    layered_img_pattern = re.compile(r'^\s*layeredimage\s+([a-zA-Z0-9_]+):')
    attribute_pattern = re.compile(r'^\s*attribute\s+([a-zA-Z0-9_ñÑáéíóú]+)\s*(?:default)?\s*:?')
    
    for root, dirs, files in os.walk(script_dir):
        for f in files:
            if f.startswith('sprites_') and f.endswith('.rpy'):
                filepath = os.path.join(root, f)
                with open(filepath, 'r', encoding='utf-8') as file:
                    lines = file.readlines()
                
                current_image = None
                
                for line in lines:
                    img_match = layered_img_pattern.match(line)
                    if img_match:
                        current_image = img_match.group(1)
                        if current_image not in valid_attributes:
                            valid_attributes[current_image] = set()
                        continue
                        
                    if current_image:
                        attr_match = attribute_pattern.match(line)
                        if attr_match:
                            attr_name = attr_match.group(1)
                            valid_attributes[current_image].add(attr_name)
                            
    return valid_attributes

def scan_show_statements(script_dir, valid_attributes):
    errors = []
    
    # Matches 'show image_name attr1 attr2 ...'
    # Captures everything after 'show ' until the end of the line or a colon or 'with'
    show_pattern = re.compile(r'^\s*show\s+([a-zA-Z0-9_]+)(.*?)(?:with\s+[\w_]+|:|\s*$)', re.IGNORECASE)
    
    for root, dirs, files in os.walk(script_dir):
        for f in files:
            if f.endswith('.rpy'):
                filepath = os.path.join(root, f)
                with open(filepath, 'r', encoding='utf-8') as file:
                    lines = file.readlines()
                
                for i, line in enumerate(lines):
                    line_clean = line.strip()
                    if line_clean.startswith('show '):
                        # Special case: showing a screen rather than an image
                        if "screen " in line_clean.lower() or "text " in line_clean.lower():
                            continue
                            
                        # Handle basic show commands
                        # split the line, remove 'show', any 'with', 'at', 'behind', etc.
                        parts = line_clean.split()
                        if len(parts) < 2:
                            continue
                        
                        img_name = parts[1]
                        
                        # Some shows might be just simple images not layered images
                        if img_name not in valid_attributes:
                            continue
                            
                        # Extract attributes
                        # Ignore keywords like 'at', 'with', 'behind', 'as'
                        attributes_used = []
                        skip_next = False
                        
                        for part in parts[2:]:
                            if skip_next:
                                skip_next = False
                                continue
                            if part in ['at', 'with', 'behind', 'as', 'zorder']:
                                skip_next = True
                                continue
                            if part == ':':
                                break
                            
                            # Clean up the part (might have colons or whatever attached)
                            clean_part = re.sub(r'[^a-zA-Z0-9_ñÑáéíóú]', '', part)
                            if clean_part:
                                attributes_used.append(clean_part)
                        
                        # Now check if attributes are valid
                        valid_attrs_for_img = valid_attributes[img_name]
                        
                        for attr in attributes_used:
                            if attr not in valid_attrs_for_img:
                                # Sometimes renpy transitions or other things slip in, let's filter obvious ones
                                if attr not in ['dissolve', 'fade', 'vpunch', 'hpunch']:
                                    errors.append({
                                        'file': filepath,
                                        'line_num': i + 1,
                                        'line_content': line_clean,
                                        'image': img_name,
                                        'invalid_attribute': attr
                                    })
                                
    return errors

if __name__ == "__main__":
    script_dir = r"c:/Users/Alan/OneDrive/Desktop/Japitown/game/script"
    
    print("Parsing layered images...")
    valid_attrs = parse_layered_images(script_dir)
    print(f"Found {len(valid_attrs)} layered images.")
    
    for img, attrs in valid_attrs.items():
        print(f" - {img}: {len(attrs)} attributes")
        
    print("\nScanning show statements...")
    errors = scan_show_statements(script_dir, valid_attrs)
    
    if errors:
        print(f"\nFound {len(errors)} potential invalid attributes in show statements:")
        for err in errors:
            print(f"File: {os.path.basename(err['file'])}:{err['line_num']}")
            print(f"  Line: {err['line_content']}")
            print(f"  ERROR: Attribute '{err['invalid_attribute']}' is not defined for layeredimage '{err['image']}'\n")
    else:
        print("\nAll sprite attributes in 'show' statements appear to be valid!")
