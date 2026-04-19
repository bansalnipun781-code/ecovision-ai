import os

path = r"C:\Users\asus\OneDrive\Documents\data_final"

for folder in os.listdir(path):
    count = len(os.listdir(os.path.join(path, folder)))
    print(folder, ":", count)
    