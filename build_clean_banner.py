import os
import numpy as np
import xml.etree.ElementTree as ET
from PIL import Image, ImageEnhance, ImageOps, ImageFilter

def build_portrait_d():
    photo_path = r"C:\Users\Radhika\.gemini\antigravity-ide\brain\00e4fd71-44f1-47de-b4b8-d190be800f05\.user_uploaded\media_1790245433298.jpg"
    img = Image.open(photo_path).convert('L')
    w, h = img.size
    
    # Head & shoulders crop from real photo of Radhika
    left, top = int(w * 0.15), int(h * 0.05)
    right, bottom = int(w * 0.85), int(h * 0.55)
    cropped = img.crop((left, top, right, bottom))
    
    # Grid resolution (170x190)
    target_w, target_h = 170, 190
    resized = cropped.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    enhancer = ImageEnhance.Contrast(resized)
    enhanced = enhancer.enhance(1.4)
    auto_c = ImageOps.autocontrast(enhanced, cutoff=1)
    sharpened = auto_c.filter(ImageFilter.UnsharpMask(radius=2, percent=150))
    
    arr = np.array(sharpened, dtype=np.float32)
    h_arr, w_arr = arr.shape
    output = np.zeros((h_arr, w_arr), dtype=np.uint8)
    
    # Floyd-Steinberg Dithering
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
    cell_w, cell_h = 2.2, 2.5
    offset_x, offset_y = 770.0, 110.0
    
    for y in range(h_arr):
        x = 0
        while x < w_arr:
            if output[y, x] == 0: # Black / dark pixels
                start_x = x
                while x < w_arr and output[y, x] == 0: x += 1
                length = x - start_x
                px = round(offset_x + start_x * cell_w, 1)
                py = round(offset_y + y * cell_h, 1)
                pw = round(length * cell_w, 1)
                ph = round(cell_h, 1)
                path_runs.append(f"M {px} {py} h {pw} v {ph} h -{pw} z")
            else: x += 1
            
    print(f"Generated {len(path_runs)} path runs for Radhika portrait.")
    return " ".join(path_runs)

def create_svg(filename, portrait_d, is_dark=True):
    bg_color = "#0A101F" if is_dark else "#F8FAFC"
    card_bg  = "#111827" if is_dark else "#FFFFFF"
    border_c = "#1F2937" if is_dark else "#E2E8F0"
    text_primary = "#F9FAFB" if is_dark else "#0F172A"
    text_muted = "#9CA3AF" if is_dark else "#475569"
    accent_cyan = "#22D3EE" if is_dark else "#0891B2"
    accent_green = "#10B981" if is_dark else "#059669"
    portrait_color = "#A78BFA" if is_dark else "#7C3AED"

    svg_content = f'''<svg fill="none" viewBox="0 0 1180 610" width="100%" height="610" xmlns="http://www.w3.org/2000/svg">
  <style>
    .bg-main {{ fill: {bg_color}; }}
    .card-bg {{ fill: {card_bg}; stroke: {border_c}; stroke-width: 1; }}
    .text-title {{ font-family: ui-monospace, 'Fira Code', 'Cascadia Code', monospace; font-size: 26px; font-weight: 700; fill: {text_primary}; }}
    .text-subtitle {{ font-family: ui-monospace, 'Fira Code', 'Cascadia Code', monospace; font-size: 14px; font-weight: 600; fill: {accent_cyan}; letter-spacing: 2px; }}
    .text-label {{ font-family: ui-monospace, 'Fira Code', 'Cascadia Code', monospace; font-size: 14px; font-weight: 500; fill: {text_muted}; }}
    .text-value {{ font-family: ui-monospace, 'Fira Code', 'Cascadia Code', monospace; font-size: 15px; font-weight: 600; fill: {text_primary}; }}
    .text-green {{ font-family: ui-monospace, 'Fira Code', 'Cascadia Code', monospace; font-size: 14px; font-weight: 600; fill: {accent_green}; }}

    @keyframes pulseLive {{
      0% {{ opacity: 1; transform: scale(1); }}
      50% {{ opacity: 0.3; transform: scale(0.92); }}
      100% {{ opacity: 1; transform: scale(1); }}
    }}
    .live-dot {{ animation: pulseLive 1.8s infinite ease-in-out; transform-origin: 1100px 50px; }}

    @keyframes portraitFloat {{
      0% {{ transform: translateY(0px); }}
      50% {{ transform: translateY(-4px); }}
      100% {{ transform: translateY(0px); }}
    }}
    .portrait-group {{ animation: portraitFloat 4s infinite ease-in-out; }}
  </style>

  <!-- Background Canvas -->
  <rect width="1180" height="610" rx="16" class="bg-main"/>

  <!-- Terminal Header Chrome -->
  <rect x="25" y="25" width="1130" height="50" rx="10" class="card-bg"/>
  <circle cx="55" cy="50" r="6" fill="#EF4444"/>
  <circle cx="75" cy="50" r="6" fill="#F59E0B"/>
  <circle cx="95" cy="50" r="6" fill="#10B981"/>
  <text x="120" y="55" class="text-subtitle">RADHIKA RAJPUT // AI &amp; ML ENGINEER</text>

  <!-- LIVE Pulse Badge -->
  <rect x="1030" y="36" width="100" height="28" rx="14" fill="{card_bg}" stroke="{accent_green}" stroke-width="1"/>
  <circle cx="1050" cy="50" r="4" fill="{accent_green}" class="live-dot"/>
  <text x="1062" y="54" class="text-green">ONLINE</text>

  <!-- Left Column: Specs & Info Card -->
  <rect x="25" y="90" width="710" height="495" rx="12" class="card-bg"/>

  <g transform="translate(60, 135)">
    <!-- Title -->
    <text x="0" y="30" class="text-title">Radhika Rajput</text>
    <text x="0" y="58" class="text-subtitle">DATA SCIENTIST &amp; AI / ML ENGINEER</text>

    <!-- Divider Line -->
    <line x1="0" y1="80" x2="640" y2="80" stroke="{border_c}" stroke-width="1"/>

    <!-- Spec Items -->
    <g transform="translate(0, 115)">
      <text x="0" y="0" class="text-label">&gt; CORE FOCUS</text>
      <text x="0" y="24" class="text-value">Multi-Modal LLMs, RAG Engines &amp; Autonomous Agents</text>

      <text x="0" y="70" class="text-label">&gt; COMPUTER VISION</text>
      <text x="0" y="94" class="text-value">Real-Time OpenCV &amp; PyTorch Inference Pipelines</text>

      <text x="0" y="140" class="text-label">&gt; TECH STACK</text>
      <text x="0" y="164" class="text-value">Python, PyTorch, TensorFlow, Scikit-Learn, LangChain</text>

      <text x="0" y="210" class="text-label">&gt; STATUS</text>
      <text x="0" y="234" class="text-green">&#x25CF; Actively Seeking Data Scientist &amp; AI/ML Roles</text>
    </g>
  </g>

  <!-- Right Column: Dithered Photo Portrait Card -->
  <rect x="750" y="90" width="405" height="495" rx="12" class="card-bg"/>
  
  <g class="portrait-group">
    <!-- Radhika Portrait Dithered Single-Path -->
    <path shape-rendering="crispEdges" fill="{portrait_color}" d="{portrait_d}"/>
  </g>
</svg>'''

    with open(filename, "w", encoding="utf-8") as f:
        f.write(svg_content)
        
    # Verify XML parsing
    try:
        ET.fromstring(svg_content)
        print(f"SUCCESS: {filename} created cleanly & parsed as 100% valid XML!")
    except Exception as e:
        print(f"XML ERROR in {filename}:", e)

if __name__ == "__main__":
    portrait_d = build_portrait_d()
    create_svg("dark.svg", portrait_d, is_dark=True)
    create_svg("light.svg", portrait_d, is_dark=False)
