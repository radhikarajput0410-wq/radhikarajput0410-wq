import re

def create_tech_logo_paths():
    # Centered inside VISUAL.MAP panel (x offset: 70, y offset: 130, width: 260, height: 260)
    
    # 1. Python Logo Path
    python_logo = (
        "M 195 140 c -40 0 -60 15 -60 35 v 20 h 60 v 10 h -80 c -25 0 -45 20 -45 50 "
        "c 0 30 20 50 45 50 h 20 v -25 c 0 -20 15 -35 35 -35 h 50 c 20 0 35 -15 35 -35 "
        "v -35 c 0 -20 -20 -35 -60 -35 z M 165 160 a 7 7 0 1 1 0.1 0 z "
        "M 205 340 c 40 0 60 -15 60 -35 v -20 h -60 v -10 h 80 c 25 0 45 -20 45 -50 "
        "c 0 -30 -20 -50 -45 -50 h -20 v 25 c 0 20 -15 35 -35 35 h -50 c -20 0 -35 15 -35 35 "
        "v 35 c 0 20 20 35 60 35 z M 235 320 a 7 7 0 1 1 0.1 0 z"
    )
    
    # 2. PyTorch Flame Logo Path
    pytorch_logo = (
        "M 200 130 c -10 25 -30 50 -50 75 c -25 30 -40 60 -40 95 c 0 50 40 90 90 90 "
        "c 50 0 90 -40 90 -90 c 0 -35 -15 -65 -40 -95 c -8 -10 -25 -30 -30 -40 z "
        "M 200 240 a 20 20 0 1 1 0.1 0 z M 225 155 a 12 12 0 1 1 0.1 0 z"
    )
    
    # 3. Hugging Face Logo Path
    huggingface_logo = (
        "M 200 130 c -60 0 -100 40 -100 100 c 0 60 40 100 100 100 c 60 0 100 -40 100 -100 "
        "c 0 -60 -40 -100 -100 -100 z M 160 190 a 15 15 0 1 1 0.1 0 z M 240 190 a 15 15 0 1 1 0.1 0 z "
        "M 150 250 c 15 30 75 30 100 0 z"
    )
    
    return python_logo, pytorch_logo, huggingface_logo

def inject_morph_animation(svg_file, is_dark=True):
    with open(svg_file, "r", encoding="utf-8") as f:
        content = f.read()
        
    python_logo, pytorch_logo, huggingface_logo = create_tech_logo_paths()
    
    color_main = "#A78BFA" if is_dark else "#7C3AED"
    color_py = "#38BDF8" if is_dark else "#0284C7"
    color_torch = "#EF4444" if is_dark else "#DC2626"
    color_hf = "#F59E0B" if is_dark else "#D97706"
    
    # Construct SMIL morphing animation groups
    # Cycle duration: 14.2s total
    # 0s - 3.0s: Portrait visible (opacity 1 -> 1 -> 0)
    # 3.0s - 4.3s: Morph to Python
    # 4.3s - 6.3s: Python Logo visible (opacity 0 -> 1 -> 1 -> 0)
    # 6.3s - 7.6s: Morph to PyTorch
    # 7.6s - 9.6s: PyTorch Logo visible (opacity 0 -> 1 -> 1 -> 0)
    # 9.6s - 10.9s: Morph to Hugging Face
    # 10.9s - 12.9s: Hugging Face Logo visible
    # 12.9s - 14.2s: Morph back to Portrait
    
    morph_group = f'''<g class="visual-morph-container">
    <!-- Layer 1: Radhika Dithered Photo Portrait -->
    <g id="layer-portrait">
      <animate attributeName="opacity" dur="14.2s" repeatCount="indefinite"
        values="1; 1; 0; 0; 0; 0; 0; 0; 1"
        keyTimes="0; 0.21; 0.30; 0.44; 0.53; 0.67; 0.76; 0.90; 1.0"/>
      <animateTransform attributeName="transform" type="scale" dur="14.2s" repeatCount="indefinite"
        values="1; 1; 0.85; 0.85; 0.85; 0.85; 0.85; 0.85; 1"
        keyTimes="0; 0.21; 0.30; 0.44; 0.53; 0.67; 0.76; 0.90; 1.0" transform-origin="200 250"/>
    </g>

    <!-- Layer 2: Python Tech Logo -->
    <g id="layer-python" opacity="0">
      <path fill="{color_py}" d="{python_logo}"/>
      <animate attributeName="opacity" dur="14.2s" repeatCount="indefinite"
        values="0; 0; 1; 1; 0; 0; 0; 0; 0"
        keyTimes="0; 0.21; 0.30; 0.44; 0.53; 0.67; 0.76; 0.90; 1.0"/>
      <animateTransform attributeName="transform" type="scale" dur="14.2s" repeatCount="indefinite"
        values="0.7; 0.7; 1; 1; 0.7; 0.7; 0.7; 0.7; 0.7"
        keyTimes="0; 0.21; 0.30; 0.44; 0.53; 0.67; 0.76; 0.90; 1.0" transform-origin="200 250"/>
    </g>

    <!-- Layer 3: PyTorch Tech Logo -->
    <g id="layer-pytorch" opacity="0">
      <path fill="{color_torch}" d="{pytorch_logo}"/>
      <animate attributeName="opacity" dur="14.2s" repeatCount="indefinite"
        values="0; 0; 0; 0; 1; 1; 0; 0; 0"
        keyTimes="0; 0.21; 0.30; 0.44; 0.53; 0.67; 0.76; 0.90; 1.0"/>
      <animateTransform attributeName="transform" type="scale" dur="14.2s" repeatCount="indefinite"
        values="0.7; 0.7; 0.7; 0.7; 1; 1; 0.7; 0.7; 0.7"
        keyTimes="0; 0.21; 0.30; 0.44; 0.53; 0.67; 0.76; 0.90; 1.0" transform-origin="200 250"/>
    </g>

    <!-- Layer 4: Hugging Face Tech Logo -->
    <g id="layer-huggingface" opacity="0">
      <path fill="{color_hf}" d="{huggingface_logo}"/>
      <animate attributeName="opacity" dur="14.2s" repeatCount="indefinite"
        values="0; 0; 0; 0; 0; 0; 1; 1; 0"
        keyTimes="0; 0.21; 0.30; 0.44; 0.53; 0.67; 0.76; 0.90; 1.0"/>
      <animateTransform attributeName="transform" type="scale" dur="14.2s" repeatCount="indefinite"
        values="0.7; 0.7; 0.7; 0.7; 0.7; 0.7; 1; 1; 0.7"
        keyTimes="0; 0.21; 0.30; 0.44; 0.53; 0.67; 0.76; 0.90; 1.0" transform-origin="200 250"/>
    </g>
  </g>'''
    
    # Wrap dither-layer inside #layer-portrait
    match = re.search(r'(<g class="dither-layer".*?</g>)', content, re.DOTALL)
    if match:
        portrait_layer = match.group(1)
        # Replace dither-layer with morph_group containing portrait inside layer-portrait
        full_morph = morph_group.replace('<g id="layer-portrait">', f'<g id="layer-portrait">\n      {portrait_layer}')
        content = re.sub(r'<g class="dither-layer".*?</g>', full_morph, content, flags=re.DOTALL)
        
        with open(svg_file, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Successfully added 14.2s SMIL Tech Logo Morph to {svg_file}")

if __name__ == "__main__":
    inject_morph_animation("dark.svg", is_dark=True)
    inject_morph_animation("light.svg", is_dark=False)
