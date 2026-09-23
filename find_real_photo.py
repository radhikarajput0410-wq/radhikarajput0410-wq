import os
import time
from PIL import Image

def find_user_photo():
    search_dirs = [
        r"C:\Users\Radhika\AppData\Local\Temp",
        r"C:\Users\Radhika\Downloads",
        r"C:\Users\Radhika\Desktop",
        r"C:\Users\Radhika\.gemini",
        r"C:\Users\Radhika\Pictures",
    ]
    
    found = []
    now = time.time()
    
    for d in search_dirs:
        for root, dirs, files in os.walk(d):
            # Skip node_modules or .git
            if "node_modules" in root or ".git" in root or "AppData\\Local\\Microsoft" in root:
                continue
            for file in files:
                if file.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                    fp = os.path.join(root, file)
                    try:
                        mtime = os.path.getmtime(fp)
                        if now - mtime < 14400: # Last 4 hours
                            with Image.open(fp) as im:
                                w, h = im.size
                                if w > 300 and h > 300:
                                    found.append((mtime, w, h, fp))
                    except Exception:
                        pass
                        
    found.sort(key=lambda x: x[0], reverse=True)
    print(f"Found {len(found)} candidate photos:")
    for mtime, w, h, fp in found[:10]:
        print(f"Size: {w}x{h}, File: {fp}")

if __name__ == "__main__":
    find_user_photo()
