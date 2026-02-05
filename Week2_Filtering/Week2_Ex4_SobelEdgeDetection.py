import cv2
import numpy as np


class SobelProcessor:
    def __init__(self):
        pass

    def apply_sobel_x(self, img, ksize=3, scale=1, delta=0):
        """
        Apply Sobel edge detection in the X direction and return a 3-channel BGR image

        Args:
            img: Input image (BGR or grayscale)
            ksize: Aperture size for the Sobel operator (1,3,5,7)
            scale: Optional scale factor for the computed derivative values
            delta: Optional delta added to the results

        Returns:
            np.ndarray: 3-channel BGR image with Sobel X edges for display
        """
        try:
            if img is None:
                return None

            # Convert to grayscale if needed
            if len(img.shape) == 3:
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            else:
                gray = img

            # Compute Sobel in X direction
            sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=ksize, scale=scale, delta=delta)
            abs_sobelx = np.absolute(sobelx)
            sobel_8u = cv2.convertScaleAbs(abs_sobelx)

            # Normalize for better visibility
            if sobel_8u.max() > 0:
                sobel_norm = cv2.normalize(sobel_8u, None, 0, 255, cv2.NORM_MINMAX)
            else:
                sobel_norm = sobel_8u

            # Convert single-channel to 3-channel BGR for display compatibility
            sobel_bgr = cv2.cvtColor(sobel_norm, cv2.COLOR_GRAY2BGR)
            return sobel_bgr
        except Exception as e:
            print("Error applying Sobel X:", e)
            return None

    def apply_sobel_y(self, img, ksize=3, scale=1, delta=0):
        """Apply Sobel in Y direction (similar to apply_sobel_x)"""
        try:
            if img is None:
                return None
            if len(img.shape) == 3:
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            else:
                gray = img
            sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=ksize, scale=scale, delta=delta)
            abs_sobely = np.absolute(sobely)
            sobel_8u = cv2.convertScaleAbs(abs_sobely)
            if sobel_8u.max() > 0:
                sobel_norm = cv2.normalize(sobel_8u, None, 0, 255, cv2.NORM_MINMAX)
            else:
                sobel_norm = sobel_8u
            sobel_bgr = cv2.cvtColor(sobel_norm, cv2.COLOR_GRAY2BGR)
            return sobel_bgr
        except Exception as e:
            print("Error applying Sobel Y:", e)
            return None

    def apply_magnitude(self, img, ksize=3):
        """
        Compute gradient magnitude from Sobel X and Y and return 3-channel BGR
        """
        try:
            if img is None:
                return None
            if len(img.shape) == 3:
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            else:
                gray = img
            sx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=ksize)
            sy = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=ksize)
            mag = np.sqrt(sx**2 + sy**2)
            mag_8u = cv2.convertScaleAbs(mag)
            if mag_8u.max() > 0:
                mag_norm = cv2.normalize(mag_8u, None, 0, 255, cv2.NORM_MINMAX)
            else:
                mag_norm = mag_8u
            mag_bgr = cv2.cvtColor(mag_norm, cv2.COLOR_GRAY2BGR)
            return mag_bgr
        except Exception as e:
            print("Error computing magnitude:", e)
            return None


if __name__ == "__main__":
    proc = SobelProcessor()
    print("SobelProcessor ready")
