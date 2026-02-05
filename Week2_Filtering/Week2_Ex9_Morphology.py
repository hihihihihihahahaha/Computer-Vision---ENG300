import cv2
import numpy as np


class MorphologyProcessor:
    """Erosion and dilation operations."""
    def __init__(self):
        pass

    def _ensure_bgr(self, img):
        if img is None:
            return img
        if len(img.shape) == 2 or img.shape[2] == 1:
            return cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        return img

    def apply_erode(self, img, kernel_size=3, iterations=1):
        if img is None:
            return img
        img_bgr = self._ensure_bgr(img)
        k = max(1, int(kernel_size))
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (k, k))
        out = cv2.erode(img_bgr, kernel, iterations=iterations)
        return out

    def apply_dilate(self, img, kernel_size=3, iterations=1):
        if img is None:
            return img
        img_bgr = self._ensure_bgr(img)
        k = max(1, int(kernel_size))
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (k, k))
        out = cv2.dilate(img_bgr, kernel, iterations=iterations)
        return out
