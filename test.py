import pyseq
import json
import os
import pandas as pd
import subprocess

date_path = "/home/rapa/show/my_project/product/scan/20241226_2/"
thumbnails_dir = "/home/rapa/show/my_project/product/scan/20241226_2/thumbnails"


def exr_to_jpg(exr_path, jpg_path):
    cmd = ["ffmpeg", "-y", "-i", exr_path, "-q:v", "2", jpg_path]
    subprocess.run(cmd, check=True)
    print(f"[EXR to JPG] {exr_path} → {jpg_path}")

def mov_to_jpg(mov_path, jpg_path):
    cmd = ["ffmpeg", "-y", "-i", mov_path, "-frames:v", "1", "-q:v", "2", jpg_path]
    subprocess.run(cmd, check=True)
    print(f"[MOV to JPG] {mov_path} → {jpg_path}")

meta_list = []
for root, dirs, seqs in pyseq.walk(date_path):
    dirs[:] = [d for d in dirs if d != "thumbnails"]
    scan_data_path = ""
    for seq in seqs:
        _, ext = os.path.splitext(seq.name)
        if ext == ".exr":
            scan_data_path = seq[0].path
            thumb_name = seq.head().strip(".") + ".jpg"
            thumb_path = os.path.join(thumbnails_dir, thumb_name)
            # print(scan_data_path)
            # print(thumb_path)
            exr_to_jpg(scan_data_path, thumb_path)

        elif ext == ".mov":
            mov_path = os.path.join(root, seq.name)
            scan_data_path = mov_path # for export meta data
            thumb_name = os.path.splitext(seq.name)[0] + ".jpg"
            thumb_path = os.path.join(thumbnails_dir, thumb_name)
            # print(mov_path)
            # print(thumb_path)
            mov_to_jpg(mov_path, thumb_path)
        else:
            print(f"[Skip] {seq} is not EXR OR JPG")
            continue

        # 메타데이터 추출
        result = subprocess.run(
            ["exiftool", "-json", scan_data_path],
            capture_output=True, 
            text=True
        )

        # meta data json 파싱
        meta = json.loads(result.stdout)[0]
        meta["thumbnail_path"] = thumb_path
        meta["thumbnail"] = thumb_path
        meta_list.append(meta)


df = pd.DataFrame(meta_list)

new_cols = ["type" ,"version", "shot_name", "seq_name", "roll"]
for col in new_cols:
    if col not in df.columns:
        df.insert(0, col, "")

if "thumbnail_path" in df.columns:
    df.insert(0, "thumbnail_path", df.pop("thumbnail_path"))
if "thumbnail" in df.columns:
    df.insert(0, "thumbnail", df.pop("thumbnail"))

csv_path = os.path.join(date_path, "meta_output.csv")

df.to_csv(csv_path, index=False)

print(f"[COMPLETE] Metadata exported to:\n{csv_path}")