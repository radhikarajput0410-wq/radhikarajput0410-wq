import os
import glob
from PIL import Image

def inspect_temp_images():
    pattern = r"C:\Users\Radhika\AppData\Local\Temp\scoped_dir6160_1771263499\*.png"
    files = glob.glob(pattern)
    print(f"Found {len(files)} files in temp dir:")
    for f in files:
        try:
            im = Image.open(f)
            print(f"File: {f}, Size: {im.size}, Mode: {im.mode}")
        except Exception as e:
            print(f"File: {f}, Error: {e}")

if __name__ == "__main__":
    inspect_temp_images()
