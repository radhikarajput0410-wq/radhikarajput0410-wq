import numpy as np
import re
from PIL import Image, ImageDraw

def create_dithered_dot_logo(draw_func, width=280, height=280):
    img = Image.new('L', (width, height), 255)
    draw = ImageDraw.Draw(img)
    draw_func(draw, width, height)
    
    # Apply light Floyd-Steinberg dithering for stippling effect
    arr = np.array(img, dtype=np.float32)
    h_arr, w_arr = arr.shape
    
    for y in range(h_arr):
        for x in range(w_arr):
            old_val = arr[y, x]
            new_val = 255 if old_val > 128 else 0
            arr[y, x] = new_val
            err = old_val - new_val
            if x + 1 < w_arr:
                arr[y, x + 1] += err * 0.4
            if y + 1 < h_arr:
                arr[y + 1, x] += err * 0.4
                
    path_runs = []
    cell = 1.3
    # Center inside VISUAL.MAP (x: 65, y: 150)
    for y in range(0, h_arr, 2):
        for x in range(0, w_arr, 2):
            if arr[y, x] < 128:
                px = round(70 + x * cell, 1)
                py = round(160 + y * cell, 1)
                path_runs.append(f"M {px} {py} h 2.2 v 2.2 h -2.2 z")
                
    return " ".join(path_runs)

# 1. High-Precision Python Logo
def draw_python_precise(draw, w, h):
    cx, cy = w // 2, h // 2
    # Upper head ring
    draw.rectangle([cx - 50, cy - 80, cx + 20, cy - 30], fill=0)
    draw.rectangle([cx - 80, cy - 50, cx + 50, cy - 10], fill=0)
    draw.ellipse([cx - 25, cy - 65, cx - 10, cy - 50], fill=255) # Eye
    
    # Lower tail ring
    draw.rectangle([cx - 20, cy + 30, cx + 50, cy + 80], fill=0)
    draw.rectangle([cx - 50, cy + 10, cx + 80, cy + 50], fill=0)
    draw.ellipse([cx + 10, cy + 50, cx + 25, cy + 65], fill=255) # Eye

# 2. High-Precision PyTorch Flame Logo
def draw_pytorch_precise(draw, w, h):
    cx, cy = w // 2, h // 2
    draw.ellipse([cx - 75, cy - 75, cx + 75, cy + 75], outline=0, width=16)
    draw.ellipse([cx - 15, cy - 15, cx + 15, cy + 15], fill=0) # Flame nucleus
    draw.polygon([(cx + 20, cy - 90), (cx + 65, cy - 35), (cx + 15, cy - 45)], fill=0) # Flame tip

# 3. High-Precision Hugging Face Logo
def draw_huggingface_precise(draw, w, h):
    cx, cy = w // 2, h // 2
    draw.ellipse([cx - 80, cy - 80, cx + 80, cy + 80], outline=0, width=14)
    # Eyes
    draw.ellipse([cx - 45, cy - 30, cx - 20, cy - 5], fill=0)
    draw.ellipse([cx + 20, cy - 30, cx + 45, cy - 5], fill=0)
    # Smile arc
    draw.arc([cx - 50, cy - 10, cx + 50, cy + 50], start=20, end=160, fill=0, width=12)

def update_crisp_dither_svgs():
    py_d = create_dithered_dot_logo(draw_python_precise)
    torch_d = create_dithered_dot_logo(draw_pytorch_precise)
    hf_d = create_dithered_dot_logo(draw_huggingface_precise)
    
    for filename, color in [("dark.svg", "#A78BFA"), ("light.svg", "#7C3AED")]:
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()
            
        content = re.sub(
            r'<g id="layer-python".*?</g>',
            f'''<g id="layer-python" opacity="0">
      <path shape-rendering="crispEdges" fill="{color}" d="{py_d}"/>
      <animate attributeName="opacity" dur="14.2s" repeatCount="indefinite"
        values="0; 0; 1; 1; 0; 0; 0; 0; 0"
        keyTimes="0; 0.21; 0.30; 0.44; 0.53; 0.67; 0.76; 0.90; 1.0"/>
      <animateTransform attributeName="transform" type="scale" dur="14.2s" repeatCount="indefinite"
        values="0.8; 0.8; 1; 1; 0.8; 0.8; 0.8; 0.8; 0.8"
        keyTimes="0; 0.21; 0.30; 0.44; 0.53; 0.67; 0.76; 0.90; 1.0" transform-origin="200 280"/>
    </g>''',
            content, flags=re.DOTALL
        )
        
        content = re.sub(
            r'<g id="layer-pytorch".*?</g>',
            f'''<g id="layer-pytorch" opacity="0">
      <path shape-rendering="crispEdges" fill="{color}" d="{torch_d}"/>
      <animate attributeName="opacity" dur="14.2s" repeatCount="indefinite"
        values="0; 0; 0; 0; 1; 1; 0; 0; 0"
        keyTimes="0; 0.21; 0.30; 0.44; 0.53; 0.67; 0.76; 0.90; 1.0"/>
      <animateTransform attributeName="transform" type="scale" dur="14.2s" repeatCount="indefinite"
        values="0.8; 0.8; 0.8; 0.8; 1; 1; 0.8; 0.8; 0.8"
        keyTimes="0; 0.21; 0.30; 0.44; 0.53; 0.67; 0.76; 0.90; 1.0" transform-origin="200 280"/>
    </g>''',
            content, flags=re.DOTALL
        )
        
        content = re.sub(
            r'<g id="layer-huggingface".*?</g>',
            f'''<g id="layer-huggingface" opacity="0">
      <path shape-rendering="crispEdges" fill="{color}" d="{hf_d}"/>
      <animate attributeName="opacity" dur="14.2s" repeatCount="indefinite"
        values="0; 0; 0; 0; 0; 0; 1; 1; 0"
        keyTimes="0; 0.21; 0.30; 0.44; 0.53; 0.67; 0.76; 0.90; 1.0"/>
      <animateTransform attributeName="transform" type="scale" dur="14.2s" repeatCount="indefinite"
        values="0.8; 0.8; 0.8; 0.8; 0.8; 0.8; 1; 1; 0.8"
        keyTimes="0; 0.21; 0.30; 0.44; 0.53; 0.67; 0.76; 0.90; 1.0" transform-origin="200 280"/>
    </g>''',
            content, flags=re.DOTALL
        )
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
            
    print("Crisp dithered point-cloud logos successfully generated!")

if __name__ == "__main__":
    update_crisp_dither_svgs()
