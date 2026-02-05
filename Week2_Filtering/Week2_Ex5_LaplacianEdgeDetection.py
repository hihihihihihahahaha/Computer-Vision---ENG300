import cv2
import numpy as np


class LaplacianProcessor:
    def __init__(self):
        pass

    def apply_laplacian(self, img, ksize=3):
        """
        Apply Laplacian edge detection and return a 3-channel BGR image suitable for display.

        Args:
            img: Input image (BGR or grayscale)
            ksize: Aperture size for the Laplacian operator (1,3,5,7)

        Returns:
            np.ndarray: 3-channel BGR image showing Laplacian edges
        """
        try:
            if img is None:
                return None

            # Convert to grayscale if needed
            if len(img.shape) == 3:
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            else:
                gray = img

            # Compute Laplacian (64F for precision)
            lap = cv2.Laplacian(gray, cv2.CV_64F, ksize=ksize)
            abs_lap = np.absolute(lap)
            lap_8u = cv2.convertScaleAbs(abs_lap)

            # Normalize to full 0-255 for visibility
            if lap_8u.max() > 0:
                lap_norm = cv2.normalize(lap_8u, None, 0, 255, cv2.NORM_MINMAX)
            else:
                lap_norm = lap_8u

            # Convert single-channel to 3-channel BGR
            lap_bgr = cv2.cvtColor(lap_norm, cv2.COLOR_GRAY2BGR)
            return lap_bgr
        except Exception as e:
            print("Error applying Laplacian:", e)
            return None


if __name__ == '__main__':
    proc = LaplacianProcessor()
    print('LaplacianProcessor ready')
