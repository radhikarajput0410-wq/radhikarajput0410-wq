import os
import numpy as np
import re
from PIL import Image, ImageEnhance, ImageOps, ImageFilter

def process_radhika_photo(image_path):
    img = Image.open(image_path).convert('L')
    w, h = img.size
    print(f"Original photo size: {w}x{h}")
    
    # Head & shoulders crop box for Radhika's sitting photo (876x1024)
    # Head is near top center (x: 180 to 700, y: 90 to 520)
    left = int(w * 0.22)
    top = int(h * 0.08)
    right = int(w * 0.78)
    bottom = int(h * 0.50)
    
    cropped = img.crop((left, top, right, bottom))
    print(f"Cropped head-and-shoulders size: {cropped.size}")
    
    # Target grid resolution
    target_w, target_h = 240, 270
    resized = cropped.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    # Contrast 1.3x + autocontrast + UnsharpMask
    enhancer = ImageEnhance.Contrast(resized)
    enhanced = enhancer.enhance(1.35)
    auto_c = ImageOps.autocontrast(enhanced, cutoff=1)
    sharpened = auto_c.filter(ImageFilter.UnsharpMask(radius=3, percent=140))
    
    # Floyd-Steinberg Dithering
    arr = np.array(sharpened, dtype=np.float32)
    h_arr, w_arr = arr.shape
    
    output = np.zeros((h_arr, w_arr), dtype=np.uint8)
    
    for y in range(h_arr):
        x_range = range(w_arr) if y % 2 == 0 else range(w_arr - 1, -1, -1)
        for x in x_range:
            old_val = arr[y, x]
            new_val = 255 if old_val > 120 else 0
            output[y, x] = new_val
            err = old_val - new_val
            
            if y % 2 == 0:
                if x + 1 < w_arr:
                    arr[y, x + 1] += err * (7 / 16)
                if y + 1 < h_arr:
                    if x - 1 >= 0:
                        arr[y + 1, x - 1] += err * (3 / 16)
                    arr[y + 1, x] += err * (5 / 16)
                    if x + 1 < w_arr:
                        arr[y + 1, x + 1] += err * (1 / 16)
            else:
                if x - 1 >= 0:
                    arr[y, x - 1] += err * (7 / 16)
                if y + 1 < h_arr:
                    if x + 1 < w_arr:
                        arr[y + 1, x + 1] += err * (3 / 16)
                    arr[y + 1, x] += err * (5 / 16)
                    if x - 1 >= 0:
                        arr[y + 1, x - 1] += err * (1 / 16)
                        
    # Run-length encode path d attribute
    # Scale dots into VISUAL.MAP frame (x off: 55, y off: 125, cell_w: 1.35, cell_h: 1.6)
    path_runs = []
    cell_w, cell_h = 1.35, 1.6
    
    for y in range(h_arr):
        x = 0
        while x < w_arr:
            if output[y, x] == 0: # Dark pixel in dithered photo -> draw dot
                start_x = x
                while x < w_arr and output[y, x] == 0:
                    x += 1
                length = x - start_x
                
                px = round(55 + start_x * cell_w, 1)
                py = round(125 + y * cell_h, 1)
                pw = round(length * cell_w, 1)
                ph = round(cell_h, 1)
                
                path_runs.append(f"M {px} {py} h {pw} v {ph} h -{pw} z")
            else:
                x += 1
                
    d_attr = " ".join(path_runs)
    print(f"Generated {len(path_runs)} path runs for Radhika's portrait!")
    return d_attr

def update_svgs(d_attr):
    # Dark mode SVG
    with open("dark.svg", "r", encoding="utf-8") as f:
        dark_content = f.read()
        
    new_dark_layer = f'''<g class="dither-layer">
    <path shape-rendering="crispEdges" fill="url(#portraitGrad)" d="{d_attr}"/>
  </g>'''
    
    dark_updated = re.sub(r'<g class="dither-layer".*?</g>', new_dark_layer, dark_content, flags=re.DOTALL)
    
    with open("dark.svg", "w", encoding="utf-8") as f:
        f.write(dark_updated)
        
    # Light mode SVG
    with open("light.svg", "r", encoding="utf-8") as f:
        light_content = f.read()
        
    new_light_layer = f'''<g class="dither-layer">
    <path shape-rendering="crispEdges" fill="url(#portraitGradLight)" d="{d_attr}"/>
  </g>'''
    
    light_updated = re.sub(r'<g class="dither-layer".*?</g>', new_light_layer, light_content, flags=re.DOTALL)
    
    with open("light.svg", "w", encoding="utf-8") as f:
        f.write(light_updated)
        
    print("Updated dark.svg and light.svg with Radhika's real photo dither portrait!")

if __name__ == "__main__":
    photo_path = r"C:\Users\Radhika\.gemini\antigravity-ide\brain\d2e44bcc-91df-44ea-95fc-3fa90673e054\.user_uploaded\media_1790159577547.jpg"
    d_attr = process_radhika_photo(photo_path)
    update_svgs(d_attr)
