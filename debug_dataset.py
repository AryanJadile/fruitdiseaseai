import os
from PIL import Image
import warnings

# Suppress warnings
warnings.filterwarnings("error")

DATA_DIR = 'Cassava'
ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.bmp', '.gif'}

print(f"Scanning {DATA_DIR} to verify image integrity...")
count = 0
for root, dirs, files in os.walk(DATA_DIR):
    for file in files:
        full_path = os.path.join(root, file)
        ext = os.path.splitext(file)[1].lower()
        
        should_delete = False
        
        if ext not in ALLOWED_EXTENSIONS:
            print(f"Invalid extension: {full_path}")
            should_delete = True
        else:
            try:
                with Image.open(full_path) as img:
                    img.verify() # Verify it's an image
            except Exception as e:
                print(f"Corrupt image: {full_path} - Error: {e}")
                should_delete = True

        if should_delete:
            try:
                os.remove(full_path)
                print(f"Deleted: {full_path}")
                count += 1
            except Exception as e:
                print(f"Failed to delete {full_path}: {e}")

print(f"Deleted {count} problematic files.")
