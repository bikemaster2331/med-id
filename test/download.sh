#!/bin/bash
# === Download Negative Images for YOLO Training  ===

REPO_API="https://api.github.com/repos/JoakimSoderberg/haarcascade-negatives/contents/images"

download_negatives() {
  local TARGET_DIR=$1
  local COUNT=$2
  echo "📥 Downloading $COUNT negatives into $TARGET_DIR ..."
  mkdir -p "$TARGET_DIR"
  cd "$TARGET_DIR" || exit 1

  # Fetch image URLs and download them visibly
  curl -s "$REPO_API" \
  | grep '"download_url"' \
  | cut -d '"' -f 4 \
  | shuf -n "$COUNT" \
  | while read -r url; do
      filename=$(basename "$url")
      if [ ! -f "$filename" ]; then
        echo "⬇️  Downloading $filename ..."
        wget -q --show-progress "$url"
      else
        echo "⚠️  Skipping $filename (already exists)"
      fi
    done

  cd - >/dev/null || exit
  echo "✅ Done: $COUNT negatives added to $TARGET_DIR"
  echo ""
}

# === Adjust paths as needed ===
download_negatives "dataset/train/images" 100
download_negatives "dataset/valid/images" 12
download_negatives "dataset/test/images" 8

echo "🎉 All negatives downloaded successfully!"
