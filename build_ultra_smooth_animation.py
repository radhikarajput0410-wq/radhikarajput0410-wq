import re

def update_smooth_smil_animation(filename, is_dark=True):
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()
        
    color = "#A78BFA" if is_dark else "#7C3AED"
    
    # 16-second total cycle timeline
    # KeyTimes: 0, 0.05, 0.20, 0.25, 0.30, 0.45, 0.50, 0.55, 0.70, 0.75, 0.80, 0.95, 1.0
    key_times = "0; 0.04; 0.20; 0.25; 0.29; 0.45; 0.50; 0.54; 0.70; 0.75; 0.79; 0.95; 1.0"
    
    # Smooth easing splines for all transitions
    splines = (
      "0.4 0 0.2 1; 0.4 0 0.2 1; 0.4 0 0.2 1; 0.4 0 0.2 1; "
      "0.4 0 0.2 1; 0.4 0 0.2 1; 0.4 0 0.2 1; 0.4 0 0.2 1; "
      "0.4 0 0.2 1; 0.4 0 0.2 1; 0.4 0 0.2 1; 0.4 0 0.2 1"
    )
    
    # Smooth Opacity Curves (Cross-Fading with gradual ease-in and ease-out)
    op_portrait = "1; 1; 1; 0.5; 0; 0; 0; 0; 0; 0; 0; 0.5; 1"
    scale_portrait = "1; 1.02; 1; 0.92; 0.85; 0.85; 0.85; 0.85; 0.85; 0.85; 0.85; 0.92; 1"
    
    op_py = "0; 0; 0; 0.5; 1; 1; 0.5; 0; 0; 0; 0; 0; 0"
    scale_py = "0.85; 0.85; 0.85; 0.92; 1; 1.02; 0.92; 0.85; 0.85; 0.85; 0.85; 0.85; 0.85"
    
    op_torch = "0; 0; 0; 0; 0; 0; 0.5; 1; 1; 0.5; 0; 0; 0"
    scale_torch = "0.85; 0.85; 0.85; 0.85; 0.85; 0.85; 0.92; 1; 1.02; 0.92; 0.85; 0.85; 0.85"
    
    op_hf = "0; 0; 0; 0; 0; 0; 0; 0; 0; 0.5; 1; 1; 0"
    scale_hf = "0.85; 0.85; 0.85; 0.85; 0.85; 0.85; 0.85; 0.85; 0.85; 0.92; 1; 1.02; 0.85"

    # Find portrait layer
    portrait_match = re.search(r'(<g class="dither-layer".*?</g>)', content, re.DOTALL)
    if not portrait_match:
        print(f"Could not find dither-layer in {filename}")
        return
    dither_layer = portrait_match.group(1)
    
    # Extract path d for Python, PyTorch, Hugging Face
    py_match = re.search(r'<g id="layer-python".*?<path.*?d="(.*?)".*?</g>', content, re.DOTALL)
    torch_match = re.search(r'<g id="layer-pytorch".*?<path.*?d="(.*?)".*?</g>', content, re.DOTALL)
    hf_match = re.search(r'<g id="layer-huggingface".*?<path.*?d="(.*?)".*?</g>', content, re.DOTALL)
    
    py_d = py_match.group(1) if py_match else ""
    torch_d = torch_match.group(1) if torch_match else ""
    hf_d = hf_match.group(1) if hf_match else ""

    # Reconstruct container with calcMode="spline" and keySplines for silky smooth ease-in-out
    smooth_container = f'''<g class="visual-morph-container">
    <!-- Layer 1: Radhika Photo Portrait (Smooth Dissolve) -->
    <g id="layer-portrait">
      {dither_layer}
      <animate attributeName="opacity" dur="16s" repeatCount="indefinite"
        calcMode="spline" keyTimes="{key_times}" keySplines="{splines}" values="{op_portrait}"/>
      <animateTransform attributeName="transform" type="scale" dur="16s" repeatCount="indefinite"
        calcMode="spline" keyTimes="{key_times}" keySplines="{splines}" values="{scale_portrait}" transform-origin="200 270"/>
    </g>

    <!-- Layer 2: Python Logo (Smooth Cross-Fade & Scale) -->
    <g id="layer-python" opacity="0">
      <path shape-rendering="crispEdges" fill="{color}" d="{py_d}"/>
      <animate attributeName="opacity" dur="16s" repeatCount="indefinite"
        calcMode="spline" keyTimes="{key_times}" keySplines="{splines}" values="{op_py}"/>
      <animateTransform attributeName="transform" type="scale" dur="16s" repeatCount="indefinite"
        calcMode="spline" keyTimes="{key_times}" keySplines="{splines}" values="{scale_py}" transform-origin="200 270"/>
    </g>

    <!-- Layer 3: PyTorch Logo (Smooth Cross-Fade & Scale) -->
    <g id="layer-pytorch" opacity="0">
      <path shape-rendering="crispEdges" fill="{color}" d="{torch_d}"/>
      <animate attributeName="opacity" dur="16s" repeatCount="indefinite"
        calcMode="spline" keyTimes="{key_times}" keySplines="{splines}" values="{op_torch}"/>
      <animateTransform attributeName="transform" type="scale" dur="16s" repeatCount="indefinite"
        calcMode="spline" keyTimes="{key_times}" keySplines="{splines}" values="{scale_torch}" transform-origin="200 270"/>
    </g>

    <!-- Layer 4: Hugging Face Logo (Smooth Cross-Fade & Scale) -->
    <g id="layer-huggingface" opacity="0">
      <path shape-rendering="crispEdges" fill="{color}" d="{hf_d}"/>
      <animate attributeName="opacity" dur="16s" repeatCount="indefinite"
        calcMode="spline" keyTimes="{key_times}" keySplines="{splines}" values="{op_hf}"/>
      <animateTransform attributeName="transform" type="scale" dur="16s" repeatCount="indefinite"
        calcMode="spline" keyTimes="{key_times}" keySplines="{splines}" values="{scale_hf}" transform-origin="200 270"/>
    </g>
  </g>'''

    # Replace visual-morph-container
    new_content = re.sub(r'<g class="visual-morph-container".*?</g>\s*</g>', smooth_container + "\n  </g>", content, flags=re.DOTALL)
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(new_content)
        
    print(f"Updated {filename} with silky smooth spline cross-fade animations!")

if __name__ == "__main__":
    update_smooth_smil_animation("dark.svg", is_dark=True)
    update_smooth_smil_animation("light.svg", is_dark=False)
