import cv2
import mediapipe as mp
import os

mp_face_mesh = mp.solutions.face_mesh

def extract_roi(frame, face_landmarks, w, h):
    # göz ve ağız landmark indexleri (mediapipe)
    left_eye = [33, 133]
    right_eye = [362, 263]
    mouth = [13, 14]

    points = []

    for idx in left_eye + right_eye + mouth:
        lm = face_landmarks.landmark[idx]
        points.append((int(lm.x * w), int(lm.y * h)))

    xs = [p[0] for p in points]
    ys = [p[1] for p in points]

    x_min, x_max = min(xs), max(xs)
    y_min, y_max = min(ys), max(ys)

    return frame[y_min:y_max, x_min:x_max]


def process_frames(input_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    with mp_face_mesh.FaceMesh(static_image_mode=True) as face_mesh:
        for file in os.listdir(input_folder):
            path = os.path.join(input_folder, file)
            img = cv2.imread(path)

            if img is None:
                continue

            h, w, _ = img.shape
            rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            results = face_mesh.process(rgb)

            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:
                    roi = extract_roi(img, face_landmarks, w, h)
                    cv2.imwrite(os.path.join(output_folder, file), roi)


# kullan
process_frames("frames/real", "roi/real")
process_frames("frames/fake", "roi/fake")