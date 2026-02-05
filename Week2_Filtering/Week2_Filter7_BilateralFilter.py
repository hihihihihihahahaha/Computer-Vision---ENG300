import cv2
import numpy as np


class BilateralProcessor:
    """Bilateral filter implementations."""
    def __init__(self):
        pass

    def apply_bilateral(self, img, d=9, sigmaColor=75, sigmaSpace=75):
        """
        Apply bilateral filter which preserves edges while smoothing.

        Args:
            img: Input image (BGR or single-channel)
            d: Diameter of each pixel neighborhood.
            sigmaColor: Filter sigma in the color space.
            sigmaSpace: Filter sigma in the coordinate space.

        Returns:
            Filtered image as 3-channel BGR uint8
        """
        if img is None:
            return img

        # Ensure 3-channel BGR
        if len(img.shape) == 2 or img.shape[2] == 1:
            img_bgr = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        else:
            img_bgr = img.copy()

        # OpenCV bilateralFilter expects single-channel or 3-channel BGR
        # Apply bilateral filter per OpenCV API
        filtered = cv2.bilateralFilter(img_bgr, d=d, sigmaColor=sigmaColor, sigmaSpace=sigmaSpace)
        return filtered
