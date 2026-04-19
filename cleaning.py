import os
from PIL import Image
import imagehash
import cv2

# ==============================
# CONFIG
# ==============================
DATASET_PATH = r"C:\Users\asus\OneDrive\Documents\data"
MIN_SIZE = (100, 100)
RESIZE_TO = (224, 224)
BLUR_THRESHOLD = 100

# ==============================
# FUNCTIONS
# ==============================

def is_blurry(image_path, threshold=100):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        return False
    variance = cv2.Laplacian(img, cv2.CV_64F).var()
    return variance < threshold


def clean_dataset(dataset_path):
    hashes = {}
    
    corrupt_count = 0
    duplicate_count = 0
    small_count = 0
    blurry_count = 0
    processed = 0

    for root, dirs, files in os.walk(dataset_path):
        for file in files:
            path = os.path.join(root, file)
            processed += 1

            # ---- 1. Remove corrupt images ----
            try:
                with Image.open(path) as img:
                    img.verify()
            except:
                os.remove(path)
                corrupt_count += 1
                print(f"[CORRUPT REMOVED] {path}")
                continue

            # Reload image after verify
            try:
                img = Image.open(path).convert("RGB")
            except:
                continue

            # ---- 2. Remove duplicates ----
            try:
                img_hash = imagehash.phash(img)
                if img_hash in hashes:
                    os.remove(path)
                    duplicate_count += 1
                    print(f"[DUPLICATE REMOVED] {path}")
                    continue
                else:
                    hashes[img_hash] = path
            except:
                pass

            # ---- 3. Remove small images ----
            if img.size[0] < MIN_SIZE[0] or img.size[1] < MIN_SIZE[1]:
                os.remove(path)
                small_count += 1
                print(f"[SMALL IMAGE REMOVED] {path}")
                continue

            # ---- 4. Remove blurry images ----
            try:
                if is_blurry(path, BLUR_THRESHOLD):
                    os.remove(path)
                    blurry_count += 1
                    print(f"[BLURRY IMAGE REMOVED] {path}")
                    continue
            except:
                pass

            # ---- 5. Resize & standardize ----
            try:
                img = img.resize(RESIZE_TO)
                img.save(path, "JPEG")
            except:
                pass

    # ==============================
    # SUMMARY
    # ==============================
    print("\n===== CLEANING SUMMARY =====")
    print(f"Total processed: {processed}")
    print(f"Corrupt removed: {corrupt_count}")
    print(f"Duplicates removed: {duplicate_count}")
    print(f"Small images removed: {small_count}")
    print(f"Blurry images removed: {blurry_count}")
    print("Dataset cleaning complete ✅")


# ==============================
# RUN
# ==============================
clean_dataset(DATASET_PATH)


