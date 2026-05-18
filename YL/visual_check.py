import cv2
import os
import math
import numpy as np


def create_contact_sheet(input_folder, output_path, max_images=40, thumb_size=(160, 120)):
    files = sorted([f for f in os.listdir(input_folder) if f.endswith(".png")])
    files = files[:max_images]

    if not files:
        print(f"No images found in {input_folder}")
        return

    thumbs = []

    for file in files:
        path = os.path.join(input_folder, file)
        img = cv2.imread(path)

        if img is None:
            continue

        img = cv2.resize(img, thumb_size)
        cv2.putText(
            img,
            file,
            (5, 15),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.4,
            (255, 255, 255),
            1
        )
        thumbs.append(img)

    cols = 5
    rows = math.ceil(len(thumbs) / cols)

    sheet_h = rows * thumb_size[1]
    sheet_w = cols * thumb_size[0]

    sheet = np.zeros((sheet_h, sheet_w, 3), dtype=np.uint8)

    for idx, img in enumerate(thumbs):
        y = (idx // cols) * thumb_size[1]
        x = (idx % cols) * thumb_size[0]
        sheet[y:y + thumb_size[1], x:x + thumb_size[0]] = img

    cv2.imwrite(output_path, sheet)
    print(f"Saved {output_path}")


create_contact_sheet("selected_frames/real", "visual_check_real.png")
create_contact_sheet("selected_frames/fake", "visual_check_fake.png")