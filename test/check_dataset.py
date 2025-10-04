import os

# paths to your dataset
sets = ["dataset/train", "dataset/valid", "dataset/test"]
image_exts = [".jpg", ".png", ".jpeg"]

# class names from your dataset.yaml
names = {
    0: "Bottle",
}
num_classes = len(names)

for s in sets:
    img_dir = f"{s}/images"
    lbl_dir = f"{s}/labels"

    print(f"\nChecking {s} set...")

    # check images vs labels
    images = [f for f in os.listdir(img_dir) if os.path.splitext(f)[1].lower() in image_exts]
    labels = [f for f in os.listdir(lbl_dir) if f.endswith(".txt")]

    img_basenames = {os.path.splitext(f)[0] for f in images}
    lbl_basenames = {os.path.splitext(f)[0] for f in labels}



    # check class ids inside each label file
    for lbl_file in labels:
        with open(os.path.join(lbl_dir, lbl_file), "r") as f:
            for i, line in enumerate(f, start=1):
                parts = line.strip().split()
                if not parts:
                    continue
                cls_id = int(parts[0])
                if cls_id >= num_classes:
                    if cls_id == 1:
                        cls_id = 0

print("Check finished")
