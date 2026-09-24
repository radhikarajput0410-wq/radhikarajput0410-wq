import os
import numpy as np
import xml.etree.ElementTree as ET
from PIL import Image, ImageEnhance, ImageOps, ImageFilter, ImageDraw

# 1. Process Radhika's Real Photo into Dithered Path (Upper Body Portrait Crop)
def build_portrait_dither_path(offset_x=85, offset_y=135):
    photo_path = r"C:\Users\Radhika\.gemini\antigravity-ide\brain\00e4fd71-44f1-47de-b4b8-d190be800f05\.user_uploaded\media_1790245433298.jpg"
    img = Image.open(photo_path).convert('L')
    w, h = img.size
    
    # Upper-body / Head & Shoulders crop (like somya-ctrl portrait)
    left, top = int(w * 0.18), int(h * 0.05)
    right, bottom = int(w * 0.82), int(h * 0.52)
    cropped = img.crop((left, top, right, bottom))
    
    # Target resolution for VISUAL.MAP box (160x180)
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
    cell_w, cell_h = 1.95, 2.15
    
    for y in range(h_arr):
        x = 0
        while x < w_arr:
            if output[y, x] == 0:
                start_x = x
                while x < w_arr and output[y, x] == 0: x += 1
                length = x - start_x
                px = round(offset_x + start_x * cell_w, 1)
                py = round(offset_y + y * cell_h, 1)
                pw = round(length * cell_w, 1)
                ph = round(cell_h, 1)
                path_runs.append(f"M {px} {py} h {pw} v {ph} h -{pw} z")
            else: x += 1
            
    return " ".join(path_runs)

# 2. Draw Stippled Tech Badge (like TS / PY / PT badge in somya-ctrl)
def create_dithered_badge_path(draw_func, offset_x=105, offset_y=160, width=240, height=240):
    img = Image.new('L', (width, height), 255)
    draw = ImageDraw.Draw(img)
    draw_func(draw, width, height)
    
    arr = np.array(img, dtype=np.float32)
    h_arr, w_arr = arr.shape
    
    for y in range(h_arr):
        for x in range(w_arr):
            old_val = arr[y, x]
            new_val = 255 if old_val > 128 else 0
            arr[y, x] = new_val
            err = old_val - new_val
            if x + 1 < w_arr: arr[y, x + 1] += err * 0.4
            if y + 1 < h_arr: arr[y + 1, x] += err * 0.4
                
    path_runs = []
    cell = 1.35
    for y in range(0, h_arr, 2):
        for x in range(0, w_arr, 2):
            if arr[y, x] < 128:
                px = round(offset_x + x * cell, 1)
                py = round(offset_y + y * cell, 1)
                path_runs.append(f"M {px} {py} h 2.2 v 2.2 h -2.2 z")
                
    return " ".join(path_runs)

# Badge 1: PY (Python Tech Badge)
def draw_badge_py(draw, w, h):
    cx, cy = w // 2, h // 2
    # Outer square stippled border
    b = 85
    draw.rectangle([cx - b, cy - b, cx + b, cy + b], fill=0)
    draw.rectangle([cx - b + 10, cy - b + 10, cx + b - 10, cy + b - 10], fill=255)
    
    # Letter P
    draw.rectangle([cx - 55, cy - 45, cx - 38, cy + 45], fill=0)
    draw.rectangle([cx - 55, cy - 45, cx - 10, cy], fill=0)
    draw.rectangle([cx - 38, cy - 30, cx - 10, cy - 15], fill=255)
    
    # Letter Y
    draw.polygon([(cx + 5, cy - 45), (cx + 22, cy - 45), (cx + 38, cy - 5), (cx + 38, cy + 45), (cx + 21, cy + 45), (cx + 21, cy - 5), (cx + 5, cy - 45)], fill=0)
    draw.polygon([(cx + 70, cy - 45), (cx + 53, cy - 45), (cx + 38, cy - 5)], fill=0)

# Badge 2: PT (PyTorch Tech Badge)
def draw_badge_pt(draw, w, h):
    cx, cy = w // 2, h // 2
    b = 85
    draw.rectangle([cx - b, cy - b, cx + b, cy + b], fill=0)
    draw.rectangle([cx - b + 10, cy - b + 10, cx + b - 10, cy + b - 10], fill=255)
    
    # Letter P
    draw.rectangle([cx - 58, cy - 45, cx - 41, cy + 45], fill=0)
    draw.rectangle([cx - 58, cy - 45, cx - 15, cy], fill=0)
    draw.rectangle([cx - 41, cy - 30, cx - 15, cy - 15], fill=255)
    
    # Letter T
    draw.rectangle([cx - 5, cy - 45, cx + 60, cy - 30], fill=0)
    draw.rectangle([cx + 18, cy - 45, cx + 36, cy + 45], fill=0)

# Badge 3: AI (Artificial Intelligence / LLM Badge)
def draw_badge_ai(draw, w, h):
    cx, cy = w // 2, h // 2
    b = 85
    draw.rectangle([cx - b, cy - b, cx + b, cy + b], fill=0)
    draw.rectangle([cx - b + 10, cy - b + 10, cx + b - 10, cy + b - 10], fill=255)
    
    # Letter A
    draw.polygon([(cx - 55, cy + 45), (cx - 38, cy + 45), (cx - 28, cy - 45), (cx - 45, cy - 45)], fill=0)
    draw.polygon([(cx - 5, cy + 45), (cx - 22, cy + 45), (cx - 28, cy - 45), (cx - 12, cy - 45)], fill=0)
    draw.rectangle([cx - 45, cy, cx - 15, cy + 14], fill=0)
    
    # Letter I
    draw.rectangle([cx + 10, cy - 45, cx + 60, cy - 31], fill=0)
    draw.rectangle([cx + 26, cy - 45, cx + 44, cy + 45], fill=0)
    draw.rectangle([cx + 10, cy + 31, cx + 60, cy + 45], fill=0)

def generate_banner_svg(filename, is_dark=True):
    bg_main     = "#0B101D" if is_dark else "#F1F5F9"
    window_bg   = "#111827" if is_dark else "#FFFFFF"
    border_col  = "#1F2937" if is_dark else "#CBD5E1"
    box_bg      = "#0D1424" if is_dark else "#F8FAFC"
    text_cyan   = "#22D3EE" if is_dark else "#0891B2"
    text_purple = "#A78BFA" if is_dark else "#7C3AED"
    text_main   = "#F3F4F6" if is_dark else "#0F172A"
    text_muted  = "#64748B" if is_dark else "#64748B"
    text_red    = "#EF4444" if is_dark else "#DC2626"
    dot_color   = "#334155" if is_dark else "#CBD5E1"
    
    portrait_d = build_portrait_dither_path(offset_x=85, offset_y=135)
    py_d       = create_dithered_badge_path(draw_badge_py, offset_x=105, offset_y=160)
    torch_d    = create_dithered_badge_path(draw_badge_pt, offset_x=105, offset_y=160)
    ai_d       = create_dithered_badge_path(draw_badge_ai, offset_x=105, offset_y=160)

    key_times   = "0; 0.1875; 0.25; 0.4375; 0.50; 0.6875; 0.75; 0.9375; 1.0"
    op_portrait = "1; 1; 0; 0; 0; 0; 0; 0; 1"
    op_py       = "0; 0; 1; 1; 0; 0; 0; 0; 0"
    op_torch    = "0; 0; 0; 0; 1; 1; 0; 0; 0"
    op_ai       = "0; 0; 0; 0; 0; 0; 1; 1; 0"

    svg_content = f'''<svg fill="none" viewBox="0 0 1180 610" width="100%" height="610" xmlns="http://www.w3.org/2000/svg">
  <style>
    .bg-canvas {{ fill: {bg_main}; }}
    .window-card {{ fill: {window_bg}; stroke: {border_col}; stroke-width: 1; }}
    .box-card {{ fill: {box_bg}; stroke: {border_col}; stroke-width: 1; }}
    
    .txt-title {{ font-family: ui-monospace, 'Fira Code', 'Cascadia Code', monospace; font-size: 13px; font-weight: 600; fill: {text_cyan}; letter-spacing: 1px; }}
    .txt-tag {{ font-family: ui-monospace, 'Fira Code', 'Cascadia Code', monospace; font-size: 13px; font-weight: 700; fill: {text_cyan}; }}
    .txt-key {{ font-family: ui-monospace, 'Fira Code', 'Cascadia Code', monospace; font-size: 12px; font-weight: 500; fill: {text_cyan}; }}
    .txt-val {{ font-family: ui-monospace, 'Fira Code', 'Cascadia Code', monospace; font-size: 12px; font-weight: 600; fill: {text_main}; }}
    .txt-dots {{ font-family: ui-monospace, 'Fira Code', 'Cascadia Code', monospace; font-size: 11px; fill: {dot_color}; letter-spacing: 1.5px; }}
    .txt-live {{ font-family: ui-monospace, 'Fira Code', 'Cascadia Code', monospace; font-size: 12px; font-weight: 700; fill: {text_red}; }}

    @keyframes pulseRed {{
      0% {{ opacity: 1; }}
      50% {{ opacity: 0.3; }}
      100% {{ opacity: 1; }}
    }}
    .live-dot {{ animation: pulseRed 1.8s infinite ease-in-out; }}
  </style>

  <!-- Canvas Background -->
  <rect width="1180" height="610" rx="14" class="bg-canvas"/>

  <!-- Outer Terminal Window Card -->
  <rect x="20" y="20" width="1140" height="570" rx="12" class="window-card"/>

  <!-- Mac OS Terminal Window Header -->
  <circle cx="50" cy="45" r="5.5" fill="#FF5F56"/>
  <circle cx="68" cy="45" r="5.5" fill="#FFBD2E"/>
  <circle cx="86" cy="45" r="5.5" fill="#27C93F"/>
  <text x="590" y="50" text-anchor="middle" class="txt-title">profile.sh --live</text>
  <line x1="20" y1="70" x2="1160" y2="70" stroke="{border_col}" stroke-width="1"/>

  <!-- LEFT BOX: VISUAL.MAP (Morphing Dither Animation) -->
  <rect x="45" y="90" width="390" height="475" rx="8" class="box-card"/>
  <text x="65" y="118" class="txt-title">VISUAL.MAP</text>
  
  <!-- Corner Ticks -->
  <path d="M 60 135 v -10 h 10" stroke="{text_cyan}" stroke-width="1.5" fill="none"/>
  <path d="M 420 135 v -10 h -10" stroke="{text_cyan}" stroke-width="1.5" fill="none"/>
  <path d="M 60 535 v 10 h 10" stroke="{text_cyan}" stroke-width="1.5" fill="none"/>
  <path d="M 420 535 v 10 h -10" stroke="{text_cyan}" stroke-width="1.5" fill="none"/>

  <!-- ANIMATED MORPH CONTAINER -->
  <g class="visual-morph-container">
    <!-- Frame 1: Radhika Dithered Photo Portrait -->
    <g id="layer-portrait">
      <path shape-rendering="crispEdges" fill="{text_purple}" d="{portrait_d}">
        <animate attributeName="opacity" dur="16s" repeatCount="indefinite" keyTimes="{key_times}" values="{op_portrait}"/>
      </path>
    </g>

    <!-- Frame 2: PY (Python) Stippled Tech Badge -->
    <g id="layer-python">
      <path shape-rendering="crispEdges" fill="{text_purple}" d="{py_d}">
        <animate attributeName="opacity" dur="16s" repeatCount="indefinite" keyTimes="{key_times}" values="{op_py}"/>
      </path>
    </g>

    <!-- Frame 3: PT (PyTorch) Stippled Tech Badge -->
    <g id="layer-pytorch">
      <path shape-rendering="crispEdges" fill="{text_purple}" d="{torch_d}">
        <animate attributeName="opacity" dur="16s" repeatCount="indefinite" keyTimes="{key_times}" values="{op_torch}"/>
      </path>
    </g>

    <!-- Frame 4: AI (Artificial Intelligence) Stippled Tech Badge -->
    <g id="layer-huggingface">
      <path shape-rendering="crispEdges" fill="{text_purple}" d="{ai_d}">
        <animate attributeName="opacity" dur="16s" repeatCount="indefinite" keyTimes="{key_times}" values="{op_ai}"/>
      </path>
    </g>
  </g>

  <!-- RIGHT BOX: SYSTEM.INFO (Terminal Key-Value Table) -->
  <rect x="455" y="90" width="680" height="475" rx="8" class="box-card"/>
  <text x="480" y="118" class="txt-title">SYSTEM.INFO</text>

  <!-- Right Header Tags -->
  <text x="480" y="145" class="txt-tag">@radhikarajput0410-wq</text>
  <circle cx="1085" cy="141" r="4" fill="{text_red}" class="live-dot"/>
  <text x="1095" y="145" class="txt-live">&#x25CF; LIVE</text>

  <line x1="480" y1="158" x2="1110" y2="158" stroke="{border_col}" stroke-width="1"/>

  <!-- Table Rows (Compact Spacing to prevent overflow) -->
  <g transform="translate(480, 180)">
    <!-- Row 1: Subject -->
    <text x="0" y="0" class="txt-key">Subject</text>
    <text x="65" y="0" class="txt-dots">.........................................................................</text>
    <text x="630" y="0" text-anchor="end" class="txt-val">RADHIKA RAJPUT</text>

    <!-- Row 2: Role -->
    <g transform="translate(0, 22)">
      <text x="0" y="0" class="txt-key">Role</text>
      <text x="45" y="0" class="txt-dots">...........................................................................</text>
      <text x="630" y="0" text-anchor="end" class="txt-val">Data Scientist &amp; AI/ML Engineer</text>
    </g>

    <!-- Row 3: Origin -->
    <g transform="translate(0, 44)">
      <text x="0" y="0" class="txt-key">Origin</text>
      <text x="55" y="0" class="txt-dots">..........................................................................</text>
      <text x="630" y="0" text-anchor="end" class="txt-val">Ghaziabad, India</text>
    </g>

    <!-- Row 4: Education -->
    <g transform="translate(0, 66)">
      <text x="0" y="0" class="txt-key">Education</text>
      <text x="80" y="0" class="txt-dots">.......................................................................</text>
      <text x="630" y="0" text-anchor="end" class="txt-val">B.Tech in CSE</text>
    </g>

    <!-- Row 5: Status -->
    <g transform="translate(0, 88)">
      <text x="0" y="0" class="txt-key">Status</text>
      <text x="55" y="0" class="txt-dots">..........................................................................</text>
      <text x="630" y="0" text-anchor="end" class="txt-val">Building Multi-Modal RAG &amp; CV</text>
    </g>

    <!-- Row 6: ToolChain -->
    <g transform="translate(0, 110)">
      <text x="0" y="0" class="txt-key">ToolChain</text>
      <text x="75" y="0" class="txt-dots">........................................................................</text>
      <text x="630" y="0" text-anchor="end" class="txt-val">Git, GitHub, VS Code, Docker, PyTorch</text>
    </g>

    <!-- Divider -->
    <line x1="0" y1="126" x2="630" y2="126" stroke="{border_col}" stroke-width="1"/>

    <!-- Row 7: Core.Lang -->
    <g transform="translate(0, 146)">
      <text x="0" y="0" class="txt-key">Core.Lang</text>
      <text x="80" y="0" class="txt-dots">.......................................................................</text>
      <text x="630" y="0" text-anchor="end" class="txt-val">Python, C++, SQL, R</text>
    </g>

    <!-- Row 8: Core.AI/ML -->
    <g transform="translate(0, 168)">
      <text x="0" y="0" class="txt-key">Core.AI/ML</text>
      <text x="85" y="0" class="txt-dots">......................................................................</text>
      <text x="630" y="0" text-anchor="end" class="txt-val">PyTorch, TensorFlow, Keras, HuggingFace</text>
    </g>

    <!-- Row 9: Core.CV/RAG -->
    <g transform="translate(0, 190)">
      <text x="0" y="0" class="txt-key">Core.CV/RAG</text>
      <text x="95" y="0" class="txt-dots">.....................................................................</text>
      <text x="630" y="0" text-anchor="end" class="txt-val">OpenCV, LangChain, Multi-Modal RAG</text>
    </g>

    <!-- Row 10: Core.Infra -->
    <g transform="translate(0, 212)">
      <text x="0" y="0" class="txt-key">Core.Infra</text>
      <text x="85" y="0" class="txt-dots">......................................................................</text>
      <text x="630" y="0" text-anchor="end" class="txt-val">AWS, Cloudflare, Docker, FastAPI, Streamlit</text>
    </g>

    <!-- Divider -->
    <line x1="0" y1="228" x2="630" y2="228" stroke="{border_col}" stroke-width="1"/>

    <!-- Row 11: Grid.Mail -->
    <g transform="translate(0, 248)">
      <text x="0" y="0" class="txt-key">Grid.Mail</text>
      <text x="75" y="0" class="txt-dots">........................................................................</text>
      <text x="630" y="0" text-anchor="end" class="txt-val">radhikarajput0410@gmail.com</text>
    </g>

    <!-- Row 12: Grid.LinkedIn -->
    <g transform="translate(0, 270)">
      <text x="0" y="0" class="txt-key">Grid.LinkedIn</text>
      <text x="95" y="0" class="txt-dots">.....................................................................</text>
      <text x="630" y="0" text-anchor="end" class="txt-val">linkedin.com/in/radhika-rajput-832524345</text>
    </g>

    <!-- Row 13: Grid.GitHub -->
    <g transform="translate(0, 292)">
      <text x="0" y="0" class="txt-key">Grid.GitHub</text>
      <text x="85" y="0" class="txt-dots">......................................................................</text>
      <text x="630" y="0" text-anchor="end" class="txt-val">github.com/radhikarajput0410-wq</text>
    </g>
  </g>
</svg>'''

    with open(filename, "w", encoding="utf-8") as f:
        f.write(svg_content)

    # Verify XML validity
    try:
        ET.fromstring(svg_content)
        print(f"SUCCESS: {filename} created & validated as 100% valid XML!")
    except Exception as e:
        print(f"XML ERROR in {filename}:", e)

if __name__ == "__main__":
    generate_banner_svg("dark.svg", is_dark=True)
    generate_banner_svg("light.svg", is_dark=False)
