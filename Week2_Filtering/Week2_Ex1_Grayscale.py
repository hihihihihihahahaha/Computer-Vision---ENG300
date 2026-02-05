import cv2
import numpy as np


class GrayscaleProcessor:
    def __init__(self):
        pass
    
    # =============================================================================
    # STEP 1: BASIC IMAGE CAPTURE (Weeks 1-2)
    # Topic: Introduction to Computer Vision, Images as Functions & Filtering
    # =============================================================================
    
    def convert_to_grayscale(self, bgr_img):
        """
        Convert BGR image to grayscale
        
        Args:
            bgr_img: Input image in BGR format
            
        Returns:
            np.ndarray: Grayscale image (3-channel for display compatibility)
        """
        if bgr_img is None:
            return None

        try:
            # Convert BGR to Grayscale (single channel)
            gray_img = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2GRAY)
            
            # Convert single-channel gray back to 3-channel BGR for proper display
            gray_bgr = cv2.cvtColor(gray_img, cv2.COLOR_GRAY2BGR)
            
            return gray_bgr
        except Exception as e:
            print("Error converting to grayscale:", e)
            return None

    def apply_gaussian_blur(self, img, kernel_size=(5, 5), sigma=1.0):
        """
        Apply Gaussian blur filter to image
        
        Args:
            img: Input image (BGR or grayscale)
            kernel_size: Size of the blur kernel (must be odd)
            sigma: Standard deviation for Gaussian kernel
            
        Returns:
            np.ndarray: Blurred image
        """
        try:
            if img is None:
                return None
            
            # Ensure kernel size is odd
            if kernel_size[0] % 2 == 0:
                kernel_size = (kernel_size[0] + 1, kernel_size[1] + 1)
            
            blurred = cv2.GaussianBlur(img, kernel_size, sigma)
            return blurred
        except Exception as e:
            print("Error applying Gaussian blur:", e)
            return None

    def apply_median_blur(self, img, kernel_size=5):
        """
        Apply median blur filter to image
        
        Args:
            img: Input image
            kernel_size: Size of the median filter (must be odd)
            
        Returns:
            np.ndarray: Filtered image
        """
        try:
            if img is None:
                return None
            
            # Ensure kernel size is odd
            if kernel_size % 2 == 0:
                kernel_size += 1
            
            filtered = cv2.medianBlur(img, kernel_size)
            return filtered
        except Exception as e:
            print("Error applying median blur:", e)
            return None

    def apply_bilateral_filter(self, img, diameter=9, sigma_color=75, sigma_space=75):
        """
        Apply bilateral filter (edge-preserving blur)
        
        Args:
            img: Input image
            diameter: Diameter of each pixel neighborhood
            sigma_color: Filter sigma in the color space
            sigma_space: Filter sigma in the coordinate space
            
        Returns:
            np.ndarray: Filtered image
        """
        try:
            if img is None:
                return None
            
            filtered = cv2.bilateralFilter(img, diameter, sigma_color, sigma_space)
            return filtered
        except Exception as e:
            print("Error applying bilateral filter:", e)
            return None

    def apply_morphological_operation(self, img, operation='open', kernel_size=(5, 5), iterations=1):
        """
        Apply morphological operations (open, close, dilate, erode)
        
        Args:
            img: Input image (typically grayscale or binary)
            operation: Type of operation ('open', 'close', 'dilate', 'erode')
            kernel_size: Size of the morphological kernel
            iterations: Number of times the operation is applied
            
        Returns:
            np.ndarray: Processed image
        """
        try:
            if img is None:
                return None
            
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, kernel_size)
            
            if operation == 'open':
                result = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel, iterations=iterations)
            elif operation == 'close':
                result = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel, iterations=iterations)
            elif operation == 'dilate':
                result = cv2.dilate(img, kernel, iterations=iterations)
            elif operation == 'erode':
                result = cv2.erode(img, kernel, iterations=iterations)
            else:
                return None
            
            return result
        except Exception as e:
            print("Error applying morphological operation:", e)
            return None

    def apply_edge_detection(self, img, method='canny', threshold1=100, threshold2=200):
        """
        Apply edge detection (Canny or Sobel)
        
        Args:
            img: Input image (grayscale)
            method: 'canny' or 'sobel'
            threshold1: Lower threshold for Canny
            threshold2: Upper threshold for Canny
            
        Returns:
            np.ndarray: Edge-detected image
        """
        try:
            if img is None:
                return None
            
            # Convert to grayscale if needed
            if len(img.shape) == 3:
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            else:
                gray = img
            
            if method == 'canny':
                edges = cv2.Canny(gray, threshold1, threshold2)
            elif method == 'sobel':
                sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
                sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
                edges = np.sqrt(sobelx**2 + sobely**2).astype(np.uint8)
            else:
                return None
            
            return edges
        except Exception as e:
            print("Error applying edge detection:", e)
            return None

    def apply_histogram_equalization(self, img):
        """
        Apply histogram equalization to enhance image contrast
        
        Args:
            img: Input image (grayscale or BGR)
            
        Returns:
            np.ndarray: Equalized image
        """
        try:
            if img is None:
                return None
            
            if len(img.shape) == 3:
                # For color image, convert to HSV and equalize V channel
                hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
                hsv[:, :, 2] = cv2.equalizeHist(hsv[:, :, 2])
                result = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
            else:
                # For grayscale
                result = cv2.equalizeHist(img)
            
            return result
        except Exception as e:
            print("Error applying histogram equalization:", e)
            return None

    def apply_thresholding(self, img, threshold_value=127, method='binary'):
        """
        Apply image thresholding
        
        Args:
            img: Input grayscale image
            threshold_value: Threshold value (0-255)
            method: 'binary', 'binary_inv', or 'adaptive'
            
        Returns:
            np.ndarray: Thresholded image
        """
        try:
            if img is None:
                return None
            
            # Convert to grayscale if needed
            if len(img.shape) == 3:
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            else:
                gray = img
            
            if method == 'binary':
                _, result = cv2.threshold(gray, threshold_value, 255, cv2.THRESH_BINARY)
            elif method == 'binary_inv':
                _, result = cv2.threshold(gray, threshold_value, 255, cv2.THRESH_BINARY_INV)
            elif method == 'adaptive':
                result = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                              cv2.THRESH_BINARY, 11, 2)
            else:
                return None
            
            return result
        except Exception as e:
            print("Error applying thresholding:", e)
            return None

    def apply_laplacian_filter(self, img):
        """
        Apply Laplacian filter for edge detection
        
        Args:
            img: Input image
            
        Returns:
            np.ndarray: Laplacian-filtered image
        """
        try:
            if img is None:
                return None
            
            # Convert to grayscale if needed
            if len(img.shape) == 3:
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            else:
                gray = img
            
            laplacian = cv2.Laplacian(gray, cv2.CV_64F)
            return np.uint8(np.absolute(laplacian))
        except Exception as e:
            print("Error applying Laplacian filter:", e)
            return None

    def apply_contrast_brightness(self, img, alpha=1.0, beta=0):
        """
        Adjust image contrast and brightness
        
        Args:
            img: Input image
            alpha: Contrast control (1.0-3.0)
            beta: Brightness control (0-100)
            
        Returns:
            np.ndarray: Adjusted image
        """
        try:
            if img is None:
                return None
            
            adjusted = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)
            return adjusted
        except Exception as e:
            print("Error adjusting contrast/brightness:", e)
            return None


if __name__ == "__main__":
    # Test the class
    processor = GrayscaleProcessor()
    print("GrayscaleProcessor initialized successfully")
