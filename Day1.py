
import cv2
import numpy as np
from pathlib import Path
import subprocess

# Load the image
image = cv2.imread("test.png")

# Check whether the image loaded successfully
if image is None:
    print("Image not found!")
    raise SystemExit

# Inspect the image
print("Shape:", image.shape)
print("Data type:", image.dtype)
print("Memory:", image.nbytes, "bytes")

# Convert BGR to RGB
rgb_image = image[:, :, ::-1].copy()

# Combine both images side by side
comparison = np.hstack((image, rgb_image))

# Display the comparison
cv2.imshow("BGR vs RGB channel order", comparison)

print("Press S to save or Q to quit.")

while True:
    key = cv2.waitKey(0) & 0xFF

    if key in (ord("s"), ord("S")):
        dialog = subprocess.run(
            [
                "osascript",
                "-e",
                'set selectedFile to choose file name with prompt "Save updated picture" '
                'default name "day1_comparison.jpg"',
                "-e",
                "POSIX path of selectedFile",
            ],
            capture_output=True,
            text=True,
        )

        if dialog.returncode != 0:
            print("Save cancelled. Press S to save or Q to quit.")
            continue

        save_path = Path(dialog.stdout.strip())
        saved = cv2.imwrite(str(save_path), comparison)
        if saved:
            print("Saved successfully:", save_path)
            break

        print("Could not save the image:", save_path)

    elif key == ord("q") or key == 27:
        print("Exited without saving.")
        break

cv2.destroyAllWindows()
