import cv2
import numpy as np


class ThresholdProcessor:
    """Thresholding filter implementations."""
    def __init__(self):
        pass

    def apply_threshold(self, img, thresh=127, maxval=255, method='binary'):
        """
        Apply simple binary thresholding (or inverse) to an image.

        Args:
            img: Input image (BGR or single-channel)
            thresh: Threshold value (0-255)
            maxval: Value to use for the binary output
            method: 'binary' or 'binary_inv'

        Returns:
            Thresholded image as 3-channel BGR uint8
        """
        if img is None:
            return img

        # Convert to gray first
        if len(img.shape) == 3 and img.shape[2] == 3:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        else:
            gray = img.copy()

        if method == 'binary_inv':
            _, th = cv2.threshold(gray, thresh, maxval, cv2.THRESH_BINARY_INV)
        else:
            _, th = cv2.threshold(gray, thresh, maxval, cv2.THRESH_BINARY)

        # Convert back to 3-channel for display pipeline
        th_bgr = cv2.cvtColor(th, cv2.COLOR_GRAY2BGR)
        return th_bgr
