

from pathlib import Path

import cv2


def main() -> None:
    image_path = Path(__file__).parent / "test.png"
    output_path = Path(__file__).parent / "day6_contours.jpg"

    image = cv2.imread(str(image_path))
    if image is None:
        raise FileNotFoundError(f"Could not load image: {image_path}")

    # Convert to grayscale and reduce small image noise before edge detection.
    grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(grayscale, (5, 5), 0)

    # Canny highlights strong changes in brightness, which usually correspond
    # to the boundaries of objects.
    edges = cv2.Canny(blurred, 50, 150)

    contours, _ = cv2.findContours(
        edges,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE,
    )

    result = image.copy()
    cv2.drawContours(result, contours, -1, (0, 255, 0), 2)

    if not cv2.imwrite(str(output_path), result):
        raise OSError(f"Could not save result: {output_path}")

    print(f"Detected contours: {len(contours)}")
    print(f"Saved result to: {output_path}")

    cv2.imshow("Original Image", image)
    cv2.imshow("Canny Edges", edges)
    cv2.imshow("Detected Contours", result)

    print("Press any key in an image window to exit.")
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()