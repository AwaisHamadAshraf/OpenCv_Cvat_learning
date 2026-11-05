
# ============================================================
# DAY 4: GEOMETRIC IMAGE TRANSFORMATIONS
# ============================================================
# Topics:
# 1. Translation
# 2. Rotation
# 3. Affine Transformation
# 4. Perspective Transformation
# ============================================================

import cv2
import numpy as np


# ============================================================
# STEP 1: LOAD IMAGE
# ============================================================

img = cv2.imread("test.png")

if img is None:
    print("Error: Image not found!")
    exit()

height, width = img.shape[:2]

print("Image Height:", height)
print("Image Width:", width)


# ============================================================
# STEP 2: TRANSLATION (MOVE IMAGE)
# ============================================================

# Move image 100 pixels right and 50 pixels down

translation_matrix = np.float32([
    [1, 0, 100],
    [0, 1, 50]
])

translated = cv2.warpAffine(
    img,
    translation_matrix,
    (width, height)
)

cv2.imshow("1. Translation", translated)


# ============================================================
# STEP 3: ROTATION (ROTATE IMAGE)
# ============================================================

# Find center of image

center = (width // 2, height // 2)

# Rotate 45 degrees around center

rotation_matrix = cv2.getRotationMatrix2D(
    center,
    45,
    1
)

rotated = cv2.warpAffine(
    img,
    rotation_matrix,
    (width, height)
)

cv2.imshow("2. Rotation", rotated)


# ============================================================
# STEP 4: AFFINE TRANSFORMATION
# ============================================================

# Affine transformation uses 3 point pairs.
# It can move, rotate, resize, and slant an image.

source_affine = np.float32([
    [50, 50],
    [200, 50],
    [50, 200]
])

destination_affine = np.float32([
    [100, 100],
    [250, 80],
    [80, 250]
])

# Calculate affine transformation matrix

affine_matrix = cv2.getAffineTransform(
    source_affine,
    destination_affine
)

# Apply affine transformation

affine_result = cv2.warpAffine(
    img,
    affine_matrix,
    (width, height)
)

cv2.imshow("3. Affine Transformation", affine_result)


# ============================================================
# STEP 5: PERSPECTIVE TRANSFORMATION
# ============================================================

# IMPORTANT:
# Replace these coordinates with the actual four corners
# of your document in the original image.
#
# Order:
# Top-left, Top-right, Bottom-right, Bottom-left

source_points = np.float32([
    [150, 100],
    [500, 150],
    [550, 600],
    [100, 550]
])

# Desired flat document size

document_width = 400
document_height = 500

# Destination rectangle coordinates

destination_points = np.float32([
    [0, 0],
    [document_width - 1, 0],
    [document_width - 1, document_height - 1],
    [0, document_height - 1]
])

# Calculate perspective transformation matrix

perspective_matrix = cv2.getPerspectiveTransform(
    source_points,
    destination_points
)

# Apply perspective transformation

perspective_result = cv2.warpPerspective(
    img,
    perspective_matrix,
    (document_width, document_height)
)

cv2.imshow("4. Perspective Transformation", perspective_result)


# ============================================================
# STEP 6: SAVE RESULTS
# ============================================================

cv2.imwrite("translation_result.jpg", translated)
cv2.imwrite("rotation_result.jpg", rotated)
cv2.imwrite("affine_result.jpg", affine_result)
cv2.imwrite("perspective_result.jpg", perspective_result)

print("All transformation images saved successfully!")


# ============================================================
# STEP 7: CLOSE WINDOWS
# ============================================================

cv2.waitKey(0)
cv2.destroyAllWindows()
