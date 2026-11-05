
import cv2
import numpy as np

# ==================================================
# 1. LOAD THE ORIGINAL IMAGE
# ==================================================

image = cv2.imread("test.png")

if image is None:
    print("Error: Could not load photo.jpg")
    print("Make sure the photo is in the same folder as this file.")
    raise SystemExit

height, width = image.shape[:2]

print("Original image shape:", image.shape)
print("Image height:", height)
print("Image width:", width)
print("Image data type:", image.dtype)
print("Image memory:", image.nbytes, "bytes")


# ==================================================
# 2. CROP / CUT OUT A REGION OF INTEREST (ROI)
# ==================================================

# Select the middle half of the image.
# You can change these coordinates to select a specific object.

x1 = width // 4
y1 = height // 4
x2 = (3 * width) // 4
y2 = (3 * height) // 4

# .copy() gives us an independent cropped image.
roi = image[y1:y2, x1:x2].copy()

if roi.size == 0:
    print("Error: The selected crop is empty.")
    raise SystemExit

print("Cropped ROI shape:", roi.shape)


# ==================================================
# 3. RESIZE THE CROP TO 200 x 200
# ==================================================

resized = cv2.resize(roi, (200, 200))

print("Resized image shape:", resized.shape)


# ==================================================
# 4. ENHANCE BRIGHTNESS AND CONTRAST
# ==================================================

# alpha controls contrast.
# beta controls brightness.
#
# alpha = 1.0 means normal contrast.
# alpha > 1.0 increases contrast.
# beta > 0 makes the image brighter.

enhanced = cv2.convertScaleAbs(
    resized,
    alpha=1.3,
    beta=25
)

# Optional sharpening using a simple sharpening kernel.
sharpen_kernel = np.array([
    [ 0, -1,  0],
    [-1,  5, -1],
    [ 0, -1,  0]
], dtype=np.float32)

sharpened = cv2.filter2D(
    enhanced,
    -1,
    sharpen_kernel
)


# ==================================================
# 5. FLIP THE CROPPED IMAGE IN THREE WAYS
# ==================================================

# Left <-> right
horizontal_flip = cv2.flip(resized, 1)

# Top <-> bottom
vertical_flip = cv2.flip(resized, 0)

# Both directions
both_flip = cv2.flip(resized, -1)


# ==================================================
# 6. MERGE IMAGES SIDE BY SIDE
# ==================================================

# Make comparison images the same size.
# This makes them easier to join with NumPy.

original_preview = cv2.resize(image, (300, 200))

enhanced_preview = cv2.resize(enhanced, (300, 200))
sharpened_preview = cv2.resize(sharpened, (300, 200))
horizontal_preview = cv2.resize(horizontal_flip, (300, 200))
vertical_preview = cv2.resize(vertical_flip, (300, 200))
both_preview = cv2.resize(both_flip, (300, 200))

# Join images horizontally.
row1 = np.hstack((
    original_preview,
    enhanced_preview
))

row2 = np.hstack((
    sharpened_preview,
    horizontal_preview
))

row3 = np.hstack((
    vertical_preview,
    both_preview
))

# Join the rows vertically.
comparison = np.vstack((
    row1,
    row2,
    row3
))

print("Comparison image shape:", comparison.shape)


# ==================================================
# 7. PASTE THE FLIPPED CROP INTO THE ORIGINAL IMAGE
# ==================================================

# Preserve the original by working on a copy.
result = image.copy()

# Place the 200 x 200 crop at the bottom-right.
# These coordinates ensure the crop fits inside the image.

target_x = width - 200
target_y = height - 200

if target_x >= 0 and target_y >= 0:

    result[
        target_y:target_y + 200,
        target_x:target_x + 200
    ] = horizontal_flip

    print("Flipped crop pasted into the original image.")

else:
    print(
        "The original image is smaller than 200 x 200. "
        "The crop was not pasted."
    )


# ==================================================
# 8. DISPLAY THE RESULTS
# ==================================================

cv2.imshow("1 - Original Image", image)
cv2.imshow("2 - Cropped ROI", roi)
cv2.imshow("3 - Resized ROI", resized)
cv2.imshow("4 - Brightness and Contrast Enhanced", enhanced)
cv2.imshow("5 - Sharpened Image", sharpened)

cv2.imshow("6 - Horizontal Flip", horizontal_flip)
cv2.imshow("7 - Vertical Flip", vertical_flip)
cv2.imshow("8 - Flip Both Directions", both_flip)

cv2.imshow("9 - Merged Comparison", comparison)
cv2.imshow("10 - Final Image with Pasted Crop", result)


# ==================================================
# 9. SAVE YOUR WORK
# ==================================================

print("\nPress S to save all results.")
print("Press Q or ESC to exit without saving.")

while True:

    key = cv2.waitKey(0) & 0xFF

    if key == ord("s"):

        files_to_save = {
            "day2_cropped.jpg": roi,
            "day2_resized.jpg": resized,
            "day2_enhanced.jpg": enhanced,
            "day2_sharpened.jpg": sharpened,
            "day2_horizontal_flip.jpg": horizontal_flip,
            "day2_vertical_flip.jpg": vertical_flip,
            "day2_both_flip.jpg": both_flip,
            "day2_comparison.jpg": comparison,
            "day2_final_result.jpg": result
        }

        for filename, output_image in files_to_save.items():
            success = cv2.imwrite(filename, output_image)
            print(filename, "->", "Saved" if success else "Failed")

        break

    elif key == ord("q") or key == 27:
        print("Exited without saving.")
        break


# ==================================================
# 10. CLOSE ALL WINDOWS
# ==================================================

cv2.destroyAllWindows()
