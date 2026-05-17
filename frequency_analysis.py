import cv2
import numpy as np
import os


def apply_fft(image_path, output_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    if img is None:
        return

    # FFT
    f = np.fft.fft2(img)
    fshift = np.fft.fftshift(f)

    magnitude_spectrum = 20 * np.log(np.abs(fshift) + 1)

    # normalize
    spectrum = cv2.normalize(
        magnitude_spectrum,
        None,
        0,
        255,
        cv2.NORM_MINMAX
    )

    cv2.imwrite(output_path, spectrum)


def process_folder(input_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    for file in os.listdir(input_folder):
        input_path = os.path.join(input_folder, file)
        output_path = os.path.join(output_folder, file)

        apply_fft(input_path, output_path)

    print(f"Processed: {input_folder}")


process_folder(
    "selected_frames/real",
    "fft/real"
)

process_folder(
    "selected_frames/fake",
    "fft/fake"
)