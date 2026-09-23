import re
import numpy as np
from PIL import Image, ImageDraw

def render_dithered_logo(draw_func, target_w=240, target_h=270):
    img = Image.new('L', (target_w, target_h), 255)
    draw = ImageDraw.Draw(img)
    draw_func(draw, target_w, target_h)
    
    arr = np.array(img, dtype=np.uint8)
    h_arr, w_arr = arr.shape
    
    path_runs = []
    cell_w, cell_h = 1.35, 1.6
    
    for y in range(h_arr):
        x = 0
        while x < w_arr:
            if arr[y, x] < 128: # Logo pixel
                start_x = x
                while x < w_arr and arr[y, x] < 128:
                    x += 1
                length = x - start_x
                
                px = round(55 + start_x * cell_w, 1)
                py = round(125 + y * cell_h, 1)
                pw = round(length * cell_w, 1)
                ph = round(cell_h, 1)
                
                path_runs.append(f"M {px} {py} h {pw} v {ph} h -{pw} z")
            else:
                x += 1
                
    return " ".join(path_runs)

# 1. Python Logo Dithered Grid
def draw_python(draw, w, h):
    # Draw Python double snake outline/fill
    cx, cy = w // 2, h // 2
    # Upper head
    draw.rectangle([cx - 40, cy - 65, cx + 25, cy - 25], fill=0)
    draw.rectangle([cx - 65, cy - 40, cx + 40, cy - 10], fill=0)
    draw.ellipse([cx - 15, cy - 50, cx - 5, cy - 40], fill=255) # Eye
    
    # Lower tail
    draw.rectangle([cx - 25, cy + 25, cx + 40, cy + 65], fill=0)
    draw.rectangle([cx - 40, cy + 10, cx + 65, cy + 40], fill=0)
    draw.ellipse([cx + 5, cy + 40, cx + 15, cy + 50], fill=255) # Eye

# 2. PyTorch Flame Dithered Grid
def draw_pytorch(draw, w, h):
    cx, cy = w // 2, h // 2
    # PyTorch Flame & Circle
    draw.ellipse([cx - 50, cy - 60, cx + 50, cy + 60], fill=0)
    draw.ellipse([cx - 25, cy - 35, cx + 25, cy + 35], fill=255) # Inner cutout
    draw.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=0) # Center flame dot
    draw.polygon([(cx + 15, cy - 70), (cx + 50, cy - 30), (cx + 10, cy - 40)], fill=0) # Flame tip

# 3. Hugging Face Dithered Grid
def draw_huggingface(draw, w, h):
    cx, cy = w // 2, h // 2
    # Hugging Face smiling head
    draw.ellipse([cx - 65, cy - 65, cx + 65, cy + 65], fill=0)
    # Eyes
    draw.ellipse([cx - 35, cy - 25, cx - 15, cy - 5], fill=255)
    draw.ellipse([cx + 15, cy - 25, cx + 35, cy - 5], fill=255)
    # Smile cutout
    draw.arc([cx - 40, cy - 10, cx + 40, cy + 40], start=0, end=180, fill=255, width=12)

def generate_all_dithered_svgs():
    py_d = render_dithered_logo(draw_python)
    torch_d = render_dithered_logo(draw_pytorch)
    hf_d = render_dithered_logo(draw_huggingface)
    
    for filename, grad in [("dark.svg", "url(#portraitGrad)"), ("light.svg", "url(#portraitGradLight)")]:
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Replace python layer
        content = re.sub(
            r'<g id="layer-python".*?</g>',
            f'''<g id="layer-python" opacity="0">
      <path shape-rendering="crispEdges" fill="{grad}" d="{py_d}"/>
      <animate attributeName="opacity" dur="14.2s" repeatCount="indefinite"
        values="0; 0; 1; 1; 0; 0; 0; 0; 0"
        keyTimes="0; 0.21; 0.30; 0.44; 0.53; 0.67; 0.76; 0.90; 1.0"/>
      <animateTransform attributeName="transform" type="scale" dur="14.2s" repeatCount="indefinite"
        values="0.7; 0.7; 1; 1; 0.7; 0.7; 0.7; 0.7; 0.7"
        keyTimes="0; 0.21; 0.30; 0.44; 0.53; 0.67; 0.76; 0.90; 1.0" transform-origin="200 250"/>
    </g>''',
            content, flags=re.DOTALL
        )
        
        # Replace pytorch layer
        content = re.sub(
            r'<g id="layer-pytorch".*?</g>',
            f'''<g id="layer-pytorch" opacity="0">
      <path shape-rendering="crispEdges" fill="{grad}" d="{torch_d}"/>
      <animate attributeName="opacity" dur="14.2s" repeatCount="indefinite"
        values="0; 0; 0; 0; 1; 1; 0; 0; 0"
        keyTimes="0; 0.21; 0.30; 0.44; 0.53; 0.67; 0.76; 0.90; 1.0"/>
      <animateTransform attributeName="transform" type="scale" dur="14.2s" repeatCount="indefinite"
        values="0.7; 0.7; 0.7; 0.7; 1; 1; 0.7; 0.7; 0.7"
        keyTimes="0; 0.21; 0.30; 0.44; 0.53; 0.67; 0.76; 0.90; 1.0" transform-origin="200 250"/>
    </g>''',
            content, flags=re.DOTALL
        )
        
        # Replace huggingface layer
        content = re.sub(
            r'<g id="layer-huggingface".*?</g>',
            f'''<g id="layer-huggingface" opacity="0">
      <path shape-rendering="crispEdges" fill="{grad}" d="{hf_d}"/>
      <animate attributeName="opacity" dur="14.2s" repeatCount="indefinite"
        values="0; 0; 0; 0; 0; 0; 1; 1; 0"
        keyTimes="0; 0.21; 0.30; 0.44; 0.53; 0.67; 0.76; 0.90; 1.0"/>
      <animateTransform attributeName="transform" type="scale" dur="14.2s" repeatCount="indefinite"
        values="0.7; 0.7; 0.7; 0.7; 0.7; 0.7; 1; 1; 0.7"
        keyTimes="0; 0.21; 0.30; 0.44; 0.53; 0.67; 0.76; 0.90; 1.0" transform-origin="200 250"/>
    </g>''',
            content, flags=re.DOTALL
        )
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
            
    print("Dithered logos generated with matching photo palette and grid style!")

if __name__ == "__main__":
    generate_all_dithered_svgs()
