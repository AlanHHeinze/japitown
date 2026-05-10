import os
import re

mappings = {
    'violet': {
        'o': {
            'basemirando': 'base',
            'abajo': 'abajonm',
            'arriba': 'arribanm',
            'juzgando': 'juzgandonm',
            'bostezogrande': 'bostezograndenm',
            'abiertosmirando': 'abiertos',
            'contenta': 'felicesnm',
            'feliz': 'felices',
            'dormidamirando': 'dormidos',
            'enojadamirando': 'enojados',
            'guiñando': 'guiñando',
            'llorandomucho': 'llorandomuchonm',
            'tristesmirando': 'tristes',
            'sexymirando': 'sexys',
            'cerrados': 'cerrados'
        },
        'b': {
            'hablando': 'hablando',
            'hablandochica': 'hablandochica',
            'aburrida': 'aburrida',
            'gritandomucho': 'gritandomucho',
            'feliz': 'feliz',
            'contenta': 'contenta',
            'sonrisacerrada': 'sonrisacerrada',
            'sonrisacostado': 'sonrisacostado',
            'sonrisaleve': 'sonrisaleve',
            'sonrisapequeña': 'sonrisapequeña',
            'abiertachica': 'abiertachica',
            'cerradachica': 'cerradachica',
            'bostezogrande': 'bostezogrande',
            'triste': 'triste',
            'sexy': 'sexy',
            'mordiendo': 'mordiendo'
        }
    },
    'jasmine': {
        'o': {
            'basemirando': 'base',
            'abajo': 'abajonm',
            'abajosexy': 'sexysnm',
            'aburrida': 'aburridosnm',
            'aburridamirando': 'aburridos',
            'arriba': 'arribanm',
            'asustada': 'asustadosnm',
            'cerrados': 'cerrados',
            'enojados': 'enojadosnm',
            'lagrimas': 'lagrimasnm',
            'sorprendida': 'sorprendidosnm',
            'tristes': 'tristesnm'
        },
        'b': {
            'aburrida': 'aburrida',
            'asustada': 'asustada',
            'cachete': 'cachete',
            'feliz': 'feliz',
            'felizcerrada': 'felizcerrada',
            'hablando': 'hablando',
            'molesta': 'enojada',
            'sexy': 'sexy',
            'sorprendida': 'sorprendida',
            'triste': 'triste'
        }
    },
    'monica': {
        'o': {
            'basemirando': 'base',
            'abajo': 'abajonm',
            'aburrida': 'aburridosnm',
            'aburridamedio': 'aburridosmedionm',
            'arriba': 'arribanm',
            'bostezo': 'bostezonm',
            'enojada': 'enojadosnm',
            'lagrimas': 'lagrimasnm',
            'miedo': 'asustadosnm',
            'muyfeliz': 'muyfelicesnm',
            'feliz': 'felicesnm',
            'sexy': 'sexysnm',
            'dolor': 'dolornm'
        },
        'b': {
            'seria': 'seria',
            'bostezando': 'bostezando',
            'hablando': 'hablando',
            'hablandochica': 'hablandochica',
            'miedo': 'asustada',
            'molesta': 'enojada',
            'mordida': 'mordiendo',
            'muyfeliz': 'muyfeliz',
            'feliz': 'feliz',
            'sexy': 'sexy',
            'dolor': 'dolor',
            'sonrisacerrada': 'sonrisacerrada'
        }
    },
    'mc': {
        'o': {
            'aburridocentro': 'aburridosnm',
            'aburridomirando': 'aburridos',
            'alegrecentro': 'felicesnm',
            'alegremirando': 'felices',
            'asustadocentro': 'asustadosnm',
            'asustadomirando': 'asustados',
            'baseabajo': 'abajonm',
            'basearriba': 'arribanm',
            'basemirando': 'base',
            'cerrados': 'cerrados',
            'disgusto': 'disgustonm',
            'enojadocentro': 'enojadosnm',
            'enojadomirando': 'enojados',
            'feliz': 'felicescerrados',
            'molestocentro': 'molestosnm',
            'molestomirando': 'molestos',
            'seriocentro': 'seriosnm',
            'seriomirando': 'serios',
            'sorprendidocentro': 'sorprendidosnm',
            'sorprendidomirando': 'sorprendidos',
            'triste': 'tristesnm'
        },
        'b': {
            'abierta': 'abierta',
            'abiertachica': 'abiertachica',
            'aburrido': 'aburrida',
            'asustado': 'asustada',
            'disgusto': 'disgusto',
            'enojadacerrada': 'enojadacerrada',
            'felizabierta': 'felizabierta',
            'felizcerrada': 'felizcerrada',
            'hablando': 'hablando',
            'molesto': 'molesta',
            'serio': 'seria',
            'triste': 'triste'
        }
    }
}


def get_char(line, filename):
    line_lower = line.lower()
    for c in ['violet', 'jasmine', 'monica']:
        if f"show {c}" in line_lower or f"{c}_parada" in line_lower:
            return c
    if "show mc" in line_lower or "mc_" in line_lower:
        return 'mc'
        
    for c in ['violet', 'jasmine', 'monica']:
        if c in line_lower:
            return c
            
    if re.search(r'\bmc\b', line_lower):
        return 'mc'
        
    fname_lower = os.path.basename(filename).lower()
    for c in ['violet', 'jasmine', 'monica']:
        if c in fname_lower:
            return c
    if 'mc' in fname_lower:
        return 'mc'
        
    return None

def rename_images():
    img_dir = r"c:/Users/Alan/OneDrive/Desktop/Japitown/game/images/characters"
    renamed_count = 0
    for root, dirs, files in os.walk(img_dir):
        for f in files:
            if f.endswith('.png'):
                char = get_char(f, os.path.join(root, f))
                if not char:
                    # try folder name
                    for c in ['violet', 'jasmine', 'monica', 'mc']:
                        if c in root.lower().split(os.sep):
                            char = c
                            break
                            
                if not char:
                    continue
                
                new_f = f
                
                # Ojos
                for old_val, new_val in mappings[char]['o'].items():
                    target = f"_ojos_{old_val}.png"
                    if new_f.endswith(target):
                        new_f = new_f[:-len(target)] + f"_ojos_{new_val}.png"
                        break
                
                # Boca
                if new_f == f:
                    for old_val, new_val in mappings[char]['b'].items():
                        target = f"_boca_{old_val}.png"
                        if new_f.endswith(target):
                            new_f = new_f[:-len(target)] + f"_boca_{new_val}.png"
                            break

                if new_f != f:
                    old_path = os.path.join(root, f)
                    new_path = os.path.join(root, new_f)
                    print(f"Renaming {f} -> {new_f}")
                    os.rename(old_path, new_path)
                    renamed_count += 1
    print(f"Renamed {renamed_count} images.")

def update_scripts():
    script_dir = r"c:/Users/Alan/OneDrive/Desktop/Japitown/game/script"
    
    pattern_o = re.compile(r'\bo_([a-zA-ZñÑáéíóú]+)\b')
    pattern_b = re.compile(r'\bb_([a-zA-ZñÑáéíóú]+)\b')
    pattern_img_o = re.compile(r'_ojos_([a-zA-ZñÑáéíóú]+)\.png')
    pattern_img_b = re.compile(r'_boca_([a-zA-ZñÑáéíóú]+)\.png')
    updated_files = 0
    
    for root, dirs, files in os.walk(script_dir):
        for f in files:
            if f.endswith('.rpy'):
                filepath = os.path.join(root, f)
                with open(filepath, 'r', encoding='utf-8') as file:
                    content = file.read()
                
                lines = content.split('\n')
                new_lines = []
                changed = False
                
                for line in lines:
                    new_line = line
                    
                    if pattern_o.search(line) or pattern_b.search(line) or \
                       pattern_img_o.search(line) or pattern_img_b.search(line):
                           
                        char = get_char(line, f)
                        if char:
                            def repl_o(m):
                                old_val = m.group(1)
                                if old_val in mappings[char]['o']:
                                    return 'o_' + mappings[char]['o'][old_val]
                                return m.group(0)
                            
                            def repl_b(m):
                                old_val = m.group(1)
                                if old_val in mappings[char]['b']:
                                    return 'b_' + mappings[char]['b'][old_val]
                                return m.group(0)

                            def repl_img_o(m):
                                old_val = m.group(1)
                                if old_val in mappings[char]['o']:
                                    return '_ojos_' + mappings[char]['o'][old_val] + '.png'
                                return m.group(0)

                            def repl_img_b(m):
                                old_val = m.group(1)
                                if old_val in mappings[char]['b']:
                                    return '_boca_' + mappings[char]['b'][old_val] + '.png'
                                return m.group(0)
                            
                            nl1 = pattern_o.sub(repl_o, new_line)
                            nl2 = pattern_b.sub(repl_b, nl1)
                            nl3 = pattern_img_o.sub(repl_img_o, nl2)
                            nl4 = pattern_img_b.sub(repl_img_b, nl3)
                            new_line = nl4
                            
                    if new_line != line:
                        changed = True
                    new_lines.append(new_line)
                
                if changed:
                    print(f"Updated {f}")
                    with open(filepath, 'w', encoding='utf-8') as out:
                        out.write('\n'.join(new_lines))
                    updated_files += 1
    print(f"Updated {updated_files} script files.")

if __name__ == "__main__":
    rename_images()
    update_scripts()
    print("ALL DONE")
