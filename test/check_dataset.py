import os

image_dir = "dataset/train/images"
label_dir = "dataset/train/labels"

for file in os.listdir(label_dir):
    if not file.endswith(".txt"):
        continue

    label_path = os.path.join(label_dir, file)
    image_path = os.path.join(image_dir, file.replace(".txt", ".jpg"))

    if os.path.getsize(label_path) == 0 or open(label_path).read().strip() == "":
        print(f"🗑 Removing empty label and image: {file}")
        os.remove(label_path)
        if os.path.exists(image_path):
            os.remove(image_path)

print("✅ Done! All empty labels and images removed.")
