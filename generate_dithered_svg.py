import os
import numpy as np
from PIL import Image, ImageEnhance, ImageOps, ImageFilter

def process_portrait(image_path):
    img = Image.open(image_path).convert('L')
    w, h = img.size
    print(f"Original image size: {w}x{h}")
    
    # Head and shoulders crop: upper 48% height, centered horizontally
    crop_w = int(w * 0.55)
    crop_h = int(h * 0.45)
    left = int((w - crop_w) / 2)
    top = int(h * 0.08)
    right = left + crop_w
    bottom = top + crop_h
    
    cropped = img.crop((left, top, right, bottom))
    
    # Target grid resolution
    target_w, target_h = 280, 320
    resized = cropped.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    # Contrast 1.3x + autocontrast + UnsharpMask
    enhancer = ImageEnhance.Contrast(resized)
    enhanced = enhancer.enhance(1.3)
    auto_c = ImageOps.autocontrast(enhanced, cutoff=1)
    sharpened = auto_c.filter(ImageFilter.UnsharpMask(radius=3, percent=140))
    
    # Floyd-Steinberg Dithering
    arr = np.array(sharpened, dtype=np.float32)
    h_arr, w_arr = arr.shape
    
    output = np.zeros((h_arr, w_arr), dtype=np.uint8)
    
    for y in range(h_arr):
        # Serpentine direction
        x_range = range(w_arr) if y % 2 == 0 else range(w_arr - 1, -1, -1)
        for x in x_range:
            old_val = arr[y, x]
            new_val = 255 if old_val > 128 else 0
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
    # In dark mode, lit subject = black pixels in original image = dots drawn
    # Scale dots into VISUAL.MAP frame (x off: 45, y off: 110, scale: 1.1)
    
    path_runs = []
    cell_w, cell_h = 1.15, 1.3
    
    for y in range(h_arr):
        x = 0
        while x < w_arr:
            if output[y, x] == 0: # Dot present
                start_x = x
                while x < w_arr and output[y, x] == 0:
                    x += 1
                length = x - start_x
                
                px = round(45 + start_x * cell_w, 1)
                py = round(110 + y * cell_h, 1)
                pw = round(length * cell_w, 1)
                ph = round(cell_h, 1)
                
                path_runs.append(f"M {px} {py} h {pw} v {ph} h -{pw} z")
            else:
                x += 1
                
    d_attr = " ".join(path_runs)
    print(f"Generated d_attr with {len(path_runs)} path runs")
    return d_attr

def update_svg_files(d_attr):
    # Update dark.svg
    with open("dark.svg", "r", encoding="utf-8") as f:
        dark_content = f.read()
        
    # Replace portrait path
    import re
    # Match dither-layer group
    new_dark_layer = f'''<g class="dither-layer">
    <path shape-rendering="crispEdges" fill="url(#portraitGrad)" d="{d_attr}"/>
  </g>'''
    
    dark_updated = re.sub(r'<g class="dither-layer".*?</g>', new_dark_layer, dark_content, flags=re.DOTALL)
    
    with open("dark.svg", "w", encoding="utf-8") as f:
        f.write(dark_updated)
        
    # Update light.svg
    with open("light.svg", "r", encoding="utf-8") as f:
        light_content = f.read()
        
    new_light_layer = f'''<g class="dither-layer">
    <path shape-rendering="crispEdges" fill="url(#portraitGradLight)" d="{d_attr}"/>
  </g>'''
    
    light_updated = re.sub(r'<g class="dither-layer".*?</g>', new_light_layer, light_content, flags=re.DOTALL)
    
    with open("light.svg", "w", encoding="utf-8") as f:
        f.write(light_updated)
        
    print("Successfully updated dark.svg and light.svg with dithered portrait!")

if __name__ == "__main__":
    img_path = r"C:\Users\Radhika\AppData\Local\Temp\scoped_dir6160_1771263499\96988680703.png"
    d_attr = process_portrait(img_path)
    update_svg_files(d_attr)
