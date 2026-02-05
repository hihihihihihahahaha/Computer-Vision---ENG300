import cv2
import numpy as np


class SharpenProcessor:
    """Sharpening filter implementations."""
    def __init__(self):
        pass

    def apply_sharpen(self, img, strength=1.0):
        """
        Apply sharpening using unsharp masking (Gaussian blur + weighted add).

        Args:
            img: Input image (BGR or single-channel)
            strength: float, sharpening strength (0.0 = no change, ~1.0 typical)

        Returns:
            Sharpened image as 3-channel BGR uint8
        """
        if img is None:
            return img

        if len(img.shape) == 2 or img.shape[2] == 1:
            img_bgr = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        else:
            img_bgr = img.copy()

        # Use a small Gaussian to create the mask
        blurred = cv2.GaussianBlur(img_bgr, (0, 0), sigmaX=3)

        # sharpened = img * (1+strength) + blurred * (-strength)
        sharpened = cv2.addWeighted(img_bgr, 1.0 + strength, blurred, -strength, 0)

        sharpened = np.clip(sharpened, 0, 255).astype(np.uint8)
        return sharpened
