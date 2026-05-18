import cv2
import mediapipe as mp
import os

mp_face_mesh = mp.solutions.face_mesh

LEFT_EYE = [33, 133]
RIGHT_EYE = [362, 263]
MOUTH = [13, 14]

COMBINED_INDICES = LEFT_EYE + RIGHT_EYE + MOUTH
EYES_INDICES = LEFT_EYE + RIGHT_EYE
MOUTH_INDICES = MOUTH


def crop_by_indices(frame, face_landmarks, indices, w, h, padding=20):
    points = []

    for idx in indices:
        lm = face_landmarks.landmark[idx]
        points.append((int(lm.x * w), int(lm.y * h)))

    xs = [p[0] for p in points]
    ys = [p[1] for p in points]

    x_min = max(min(xs) - padding, 0)
    x_max = min(max(xs) + padding, w)
    y_min = max(min(ys) - padding, 0)
    y_max = min(max(ys) + padding, h)

    return frame[y_min:y_max, x_min:x_max]


def process_frames(input_folder, output_base_folder, label):
    folders = {
        "combined": os.path.join(output_base_folder, "combined", label),
        "eyes": os.path.join(output_base_folder, "eyes", label),
        "mouth": os.path.join(output_base_folder, "mouth", label),
    }

    for folder in folders.values():
        os.makedirs(folder, exist_ok=True)

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
                face_landmarks = results.multi_face_landmarks[0]

                combined_roi = crop_by_indices(img, face_landmarks, COMBINED_INDICES, w, h)
                eyes_roi = crop_by_indices(img, face_landmarks, EYES_INDICES, w, h)
                mouth_roi = crop_by_indices(img, face_landmarks, MOUTH_INDICES, w, h)

                cv2.imwrite(os.path.join(folders["combined"], file), combined_roi)
                cv2.imwrite(os.path.join(folders["eyes"], file), eyes_roi)
                cv2.imwrite(os.path.join(folders["mouth"], file), mouth_roi)


process_frames("frames/real", "roi", "real")
process_frames("frames/fake", "roi", "fake")