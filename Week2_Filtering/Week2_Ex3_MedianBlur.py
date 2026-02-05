import cv2
import numpy as np


class MedianProcessor:
    def __init__(self):
        pass

    def apply_median_blur(self, img, kernel_size=5):
        """
        Apply median blur to reduce salt-and-pepper noise

        Args:
            img: Input image (BGR or grayscale)
            kernel_size: Size of the median filter (must be odd integer)

        Returns:
            np.ndarray: Filtered image
        """
        try:
            if img is None:
                return None

            # Ensure kernel_size is odd and >=1
            k = int(kernel_size)
            if k <= 1:
                return img
            if k % 2 == 0:
                k += 1

            filtered = cv2.medianBlur(img, k)
            return filtered
        except Exception as e:
            print("Error applying median blur:", e)
            return None

    def apply_adaptive_median(self, img, max_kernel=7):
        """
        A simple adaptive median filter fallback using increasing kernel sizes.
        Not optimized but useful for strong impulse noise.

        Args:
            img: Input image (grayscale expected)
            max_kernel: Maximum kernel size (odd)

        Returns:
            np.ndarray: Filtered image
        """
        try:
            if img is None:
                return None

            # Work on grayscale
            if len(img.shape) == 3:
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            else:
                gray = img

            result = gray.copy()
            max_k = int(max_kernel)
            if max_k % 2 == 0:
                max_k += 1

            rows, cols = gray.shape
            pad = max_k // 2
            padded = cv2.copyMakeBorder(gray, pad, pad, pad, pad, cv2.BORDER_REFLECT)

            for i in range(rows):
                for j in range(cols):
                    k = 3
                    while True:
                        window = padded[i+pad-(k//2):i+pad+(k//2)+1, j+pad-(k//2):j+pad+(k//2)+1]
                        z_min = window.min()
                        z_max = window.max()
                        z_med = np.median(window)
                        z_xy = padded[i+pad, j+pad]

                        A1 = z_med - z_min
                        A2 = z_med - z_max
                        if A1 > 0 and A2 < 0:
                            B1 = z_xy - z_min
                            B2 = z_xy - z_max
                            if B1 > 0 and B2 < 0:
                                result[i, j] = z_xy
                            else:
                                result[i, j] = z_med
                            break
                        else:
                            k += 2
                            if k > max_k:
                                result[i, j] = z_med
                                break
            return result
        except Exception as e:
            print("Error in adaptive median:", e)
            return None


if __name__ == "__main__":
    proc = MedianProcessor()
    print("MedianProcessor ready")
