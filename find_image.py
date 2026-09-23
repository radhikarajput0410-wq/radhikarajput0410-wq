import os
import glob
import time
from PIL import Image, ImageEnhance, ImageOps, ImageFilter

def find_latest_image():
    search_paths = [
        r"C:\Users\Radhika\.gemini\antigravity-ide\**\*.jpg",
        r"C:\Users\Radhika\.gemini\antigravity-ide\**\*.png",
        r"C:\Users\Radhika\.gemini\antigravity-ide\**\*.jpeg",
        r"C:\Users\Radhika\.gemini\antigravity-ide\**\*.webp",
        r"C:\Users\Radhika\AppData\Local\Temp\**\*.jpg",
        r"C:\Users\Radhika\AppData\Local\Temp\**\*.png",
        r"C:\Users\Radhika\Desktop\**\*.jpg",
        r"C:\Users\Radhika\Desktop\**\*.png",
    ]
    
    candidates = []
    now = time.time()
    for p in search_paths:
        for f in glob.glob(p, recursive=True):
            try:
                mtime = os.path.getmtime(f)
                if now - mtime < 7200: # Modified in last 2 hours
                    candidates.append((mtime, f))
            except Exception:
                pass
                
    candidates.sort(key=lambda x: x[0], reverse=True)
    print("Found candidate images:", candidates[:5])
    if candidates:
        return candidates[0][1]
    return None

if __name__ == "__main__":
    img_path = find_latest_image()
    print("Selected Image:", img_path)
