import os

path = r"C:\Users\asus\OneDrive\Documents\split_data"

for split in ["train","val","test"]:
    print("\n", split.upper())
    split_path = os.path.join(path, split)
    
    for category in os.listdir(split_path):
        count = len(os.listdir(os.path.join(split_path, category)))
        print(category, ":", count)