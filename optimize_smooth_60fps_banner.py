import os
import re
import numpy as np
from PIL import Image, ImageEnhance, ImageOps, ImageFilter

def build_optimized_portrait_d():
    photo_path = r"C:\Users\Radhika\.gemini\antigravity-ide\brain\d2e44bcc-91df-44ea-95fc-3fa90673e054\.user_uploaded\media_1790159577547.jpg"
    img = Image.open(photo_path).convert('L')
    w, h = img.size
    
    # Head & shoulders crop
    left, top = int(w * 0.22), int(h * 0.08)
    right, bottom = int(w * 0.78), int(h * 0.50)
    cropped = img.crop((left, top, right, bottom))
    
    # Grid resolution for 60fps performance (~160x180)
    target_w, target_h = 160, 180
    resized = cropped.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    enhancer = ImageEnhance.Contrast(resized)
    enhanced = enhancer.enhance(1.4)
    auto_c = ImageOps.autocontrast(enhanced, cutoff=1)
    sharpened = auto_c.filter(ImageFilter.UnsharpMask(radius=2, percent=150))
    
    arr = np.array(sharpened, dtype=np.float32)
    h_arr, w_arr = arr.shape
    output = np.zeros((h_arr, w_arr), dtype=np.uint8)
    
    for y in range(h_arr):
        x_range = range(w_arr) if y % 2 == 0 else range(w_arr - 1, -1, -1)
        for x in x_range:
            old_val = arr[y, x]
            new_val = 255 if old_val > 125 else 0
            output[y, x] = new_val
            err = old_val - new_val
            if y % 2 == 0:
                if x + 1 < w_arr: arr[y, x + 1] += err * (7 / 16)
                if y + 1 < h_arr:
                    if x - 1 >= 0: arr[y + 1, x - 1] += err * (3 / 16)
                    arr[y + 1, x] += err * (5 / 16)
                    if x + 1 < w_arr: arr[y + 1, x + 1] += err * (1 / 16)
            else:
                if x - 1 >= 0: arr[y, x - 1] += err * (7 / 16)
                if y + 1 < h_arr:
                    if x + 1 < w_arr: arr[y + 1, x + 1] += err * (3 / 16)
                    arr[y + 1, x] += err * (5 / 16)
                    if x - 1 >= 0: arr[y + 1, x - 1] += err * (1 / 16)
                    
    path_runs = []
    cell_w, cell_h = 2.0, 2.4
    
    for y in range(h_arr):
        x = 0
        while x < w_arr:
            if output[y, x] == 0:
                start_x = x
                while x < w_arr and output[y, x] == 0: x += 1
                length = x - start_x
                px = round(55 + start_x * cell_w, 1)
                py = round(125 + y * cell_h, 1)
                pw = round(length * cell_w, 1)
                ph = round(cell_h, 1)
                path_runs.append(f"M {px} {py} h {pw} v {ph} h -{pw} z")
            else: x += 1
            
    print(f"Optimized portrait path runs: {len(path_runs)}")
    return " ".join(path_runs)

def update_60fps_svg(filename, portrait_d, is_dark=True):
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()
        
    color = "#A78BFA" if is_dark else "#7C3AED"
    grad_id = "url(#portraitGrad)" if is_dark else "url(#portraitGradLight)"
    
    # Extract d attributes for Python, PyTorch, Hugging Face
    py_match = re.search(r'<g id="layer-python".*?<path.*?d="(.*?)".*?</g>', content, re.DOTALL)
    torch_match = re.search(r'<g id="layer-pytorch".*?<path.*?d="(.*?)".*?</g>', content, re.DOTALL)
    hf_match = re.search(r'<g id="layer-huggingface".*?<path.*?d="(.*?)".*?</g>', content, re.DOTALL)
    
    py_d = py_match.group(1) if py_match else ""
    torch_d = torch_match.group(1) if torch_match else ""
    hf_d = hf_match.group(1) if hf_match else ""
    
    # Perfectly aligned 16s keyframe timings (Linear smooth 1s cross-fade, 3s hold)
    # 0s..3s (Hold Photo), 3s..4s (Fade Photo -> Py), 4s..7s (Hold Py), 7s..8s (Fade Py -> Torch), 8s..11s (Hold Torch), 11s..12s (Fade Torch -> HF), 12s..15s (Hold HF), 15s..16s (Fade HF -> Photo)
    
    key_times = "0; 0.1875; 0.25; 0.4375; 0.50; 0.6875; 0.75; 0.9375; 1.0"
    
    op_portrait = "1; 1; 0; 0; 0; 0; 0; 0; 1"
    op_py       = "0; 0; 1; 1; 0; 0; 0; 0; 0"
    op_torch    = "0; 0; 0; 0; 1; 1; 0; 0; 0"
    op_hf       = "0; 0; 0; 0; 0; 0; 1; 1; 0"

    container_60fps = f'''<g class="visual-morph-container">
    <!-- Layer 1: Radhika Photo Portrait (Single Unified Path - Zero Lag) -->
    <g id="layer-portrait">
      <path shape-rendering="crispEdges" fill="{grad_id}" d="{portrait_d}">
        <animate attributeName="opacity" dur="16s" repeatCount="indefinite"
          keyTimes="{key_times}" values="{op_portrait}"/>
      </path>
    </g>

    <!-- Layer 2: Python Logo -->
    <g id="layer-python">
      <path shape-rendering="crispEdges" fill="{color}" d="{py_d}">
        <animate attributeName="opacity" dur="16s" repeatCount="indefinite"
          keyTimes="{key_times}" values="{op_py}"/>
      </path>
    </g>

    <!-- Layer 3: PyTorch Logo -->
    <g id="layer-pytorch">
      <path shape-rendering="crispEdges" fill="{color}" d="{torch_d}">
        <animate attributeName="opacity" dur="16s" repeatCount="indefinite"
          keyTimes="{key_times}" values="{op_torch}"/>
      </path>
    </g>

    <!-- Layer 4: Hugging Face Logo -->
    <g id="layer-huggingface">
      <path shape-rendering="crispEdges" fill="{color}" d="{hf_d}">
        <animate attributeName="opacity" dur="16s" repeatCount="indefinite"
          keyTimes="{key_times}" values="{op_hf}"/>
      </path>
    </g>
  </g>'''

    new_content = re.sub(r'<g class="visual-morph-container".*?</g>\s*</g>', container_60fps + "\n  </g>", content, flags=re.DOTALL)
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"Updated {filename} with 60fps single-path SVG architecture!")

if __name__ == "__main__":
    portrait_d = build_optimized_portrait_d()
    update_60fps_svg("dark.svg", portrait_d, is_dark=True)
    update_60fps_svg("light.svg", portrait_d, is_dark=False)
