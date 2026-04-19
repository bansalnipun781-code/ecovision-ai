import os
import shutil
import random

SOURCE = r"C:\Users\asus\OneDrive\Documents\data_final"
DEST = r"C:\Users\asus\OneDrive\Documents\split_data"

SPLIT_RATIO = (0.7, 0.15, 0.15)

for category in os.listdir(SOURCE):
    category_path = os.path.join(SOURCE, category)

    if not os.path.isdir(category_path):
        continue

    images = os.listdir(category_path)
    random.shuffle(images)

    total = len(images)
    train_end = int(total * SPLIT_RATIO[0])
    val_end = train_end + int(total * SPLIT_RATIO[1])

    splits = {
        "train": images[:train_end],
        "val": images[train_end:val_end],
        "test": images[val_end:]
    }

    for split_name, split_files in splits.items():
        split_folder = os.path.join(DEST, split_name, category)
        os.makedirs(split_folder, exist_ok=True)

        for file in split_files:
            shutil.copy(
                os.path.join(category_path, file),
                os.path.join(split_folder, file)
            )

print("Dataset split complete")