import colorsys
import re
import json


def clean_data(raw_data):
    # Matches JSON strings with escaped characters
    quoted_strings = re.findall(r'"(?:\\.|[^"\\])*"', raw_data)
    
    placeholder_map = {}
    for i, quote in enumerate(quoted_strings):
        placeholder = f"__PLACEHOLDER_{i}__"
        placeholder_map[placeholder] = quote
        raw_data = raw_data.replace(quote, placeholder)
    
    # Remove comments from the data
    # Matches single-line and multi-line comments
    no_comments_data = re.sub(r'//.*?$|/\*[\s\S]*?\*/', '', raw_data, flags=re.DOTALL | re.MULTILINE)
    
    for placeholder, quote in placeholder_map.items():
        no_comments_data = no_comments_data.replace(placeholder, quote)
    
    cleaned_data = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', no_comments_data)

    return cleaned_data


def extract_colors(theme_file_path):
    with open(theme_file_path, 'r', encoding='utf-8') as file:
        raw_data = file.read()
    
    cleaned_data = clean_data(raw_data)
    color_set = set()
    color_pattern = re.compile(r'#(?:[0-9a-fA-F]{3}){1,2}(?:[0-9a-fA-F]{2})?$')

    try:
        theme_data = json.loads(cleaned_data)
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON: {e}")
        return color_set

    def find_colors(obj):
        if isinstance(obj, dict):
            for value in obj.values():
                find_colors(value)
        elif isinstance(obj, list):
            for item in obj:
                find_colors(item)
        elif isinstance(obj, str) and color_pattern.match(obj):
            color_set.add(obj)

    find_colors(theme_data)
    
    return color_set


def create_palette_json(colors):
    palette = []
    
    for color in colors:
        palette.append({
            "hex": color,
            "name": "",
            "purpose": ""
        })
    
    return palette


def hex_to_hsv(hex_color):
    hex_color = hex_color.lstrip('#')
    r, g, b = tuple(int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4))
    hsv = colorsys.rgb_to_hsv(r, g, b)
    
    return hsv

def sort_colors_by_spectrum(colors):
    colors_with_hsv = [(color, hex_to_hsv(color)[0]) for color in colors]
    colors_with_hsv.sort(key=lambda x: (x[1], x[0]), reverse=True)
    
    return [color for color, _ in colors_with_hsv]



theme_file_path = './themes/Patinhooh\'s Theme-color-theme.json'

colors = extract_colors(theme_file_path)
sorted_colors = sort_colors_by_spectrum(colors)

if sorted_colors:
    palette_json = create_palette_json(sorted_colors)

    output_file_path = './palette/palette.json'
    with open(output_file_path, 'w', encoding='utf-8') as outfile:
        outfile.write(json.dumps(palette_json, indent=4))

    print(f"Palette JSON has been created and saved to {output_file_path}")
