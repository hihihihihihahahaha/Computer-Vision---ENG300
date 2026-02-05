import cv2
import numpy as np


class GaussianProcessor:
    def __init__(self):
        pass
    
    # =============================================================================
    # STEP 1: BASIC IMAGE CAPTURE (Weeks 1-2)
    # Topic: Introduction to Computer Vision, Images as Functions & Filtering
    # =============================================================================
    
    def apply_gaussian_filter(self, img, kernel_size=(5, 5), sigma=1.0):
        """
        Apply Gaussian filtering to reduce noise
        
        Args:
            img: Input image
            kernel_size: Size of Gaussian kernel (must be odd)
            sigma: Standard deviation
            
        Returns:
            Filtered image
        """
        if img is None:
            return None

        try:
            # Ensure kernel size is odd
            if kernel_size[0] % 2 == 0:
                kernel_size = (kernel_size[0] + 1, kernel_size[1] + 1)
            
            filtered_img = cv2.GaussianBlur(img, kernel_size, sigma)
            return filtered_img
        except Exception as e:
            print("Error applying Gaussian filter:", e)
            return None

    def apply_multi_scale_gaussian(self, img, scales=3):
        """
        Apply Gaussian blur at multiple scales
        
        Args:
            img: Input image
            scales: Number of different blur scales
            
        Returns:
            List of blurred images at different scales
        """
        try:
            if img is None:
                return None
            
            results = [img]
            for i in range(1, scales):
                kernel_size = (3 + i * 2, 3 + i * 2)
                blurred = cv2.GaussianBlur(img, kernel_size, sigma=1.0)
                results.append(blurred)
            
            return results
        except Exception as e:
            print("Error applying multi-scale Gaussian:", e)
            return None

    def apply_gaussian_pyramid(self, img, levels=4):
        """
        Create a Gaussian pyramid (multi-scale representation)
        
        Args:
            img: Input image
            levels: Number of pyramid levels
            
        Returns:
            List of images at different scales
        """
        try:
            if img is None:
                return None
            
            pyramid = [img]
            current = img
            
            for i in range(1, levels):
                current = cv2.pyrDown(current)
                pyramid.append(current)
            
            return pyramid
        except Exception as e:
            print("Error creating Gaussian pyramid:", e)
            return None

    def apply_laplacian_pyramid(self, img, levels=4):
        """
        Create a Laplacian pyramid (edge-based pyramid)
        
        Args:
            img: Input image
            levels: Number of pyramid levels
            
        Returns:
            List of Laplacian images at different scales
        """
        try:
            if img is None:
                return None
            
            # First create Gaussian pyramid
            gaussian_pyramid = self.apply_gaussian_pyramid(img, levels)
            
            laplacian_pyramid = []
            for i in range(len(gaussian_pyramid) - 1):
                # Expand lower level and subtract from current level
                expanded = cv2.pyrUp(gaussian_pyramid[i + 1])
                
                # Handle size mismatch
                if expanded.shape != gaussian_pyramid[i].shape:
                    expanded = expanded[:gaussian_pyramid[i].shape[0], :gaussian_pyramid[i].shape[1]]
                
                laplacian = cv2.subtract(gaussian_pyramid[i], expanded)
                laplacian_pyramid.append(laplacian)
            
            # Add the last level of Gaussian pyramid
            laplacian_pyramid.append(gaussian_pyramid[-1])
            
            return laplacian_pyramid
        except Exception as e:
            print("Error creating Laplacian pyramid:", e)
            return None

    def apply_bilateral_gaussian(self, img, diameter=9, sigma_color=75, sigma_space=75):
        """
        Apply bilateral Gaussian filter (edge-preserving smoothing)
        
        Args:
            img: Input image
            diameter: Diameter of pixel neighborhood
            sigma_color: Color space standard deviation
            sigma_space: Coordinate space standard deviation
            
        Returns:
            Filtered image
        """
        try:
            if img is None:
                return None
            
            filtered = cv2.bilateralFilter(img, diameter, sigma_color, sigma_space)
            return filtered
        except Exception as e:
            print("Error applying bilateral Gaussian filter:", e)
            return None

    def apply_morphological_gaussian(self, img, kernel_size=(5, 5)):
        """
        Apply morphological operations combined with Gaussian smoothing
        
        Args:
            img: Input image
            kernel_size: Size of morphological kernel
            
        Returns:
            Processed image
        """
        try:
            if img is None:
                return None
            
            # Create morphological kernel
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, kernel_size)
            
            # Apply morphological opening (erosion followed by dilation)
            opened = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
            
            # Apply Gaussian blur to smooth
            result = cv2.GaussianBlur(opened, (5, 5), 1.0)
            
            return result
        except Exception as e:
            print("Error applying morphological Gaussian:", e)
            return None

    def apply_selective_gaussian_blur(self, img, sigma_s=10, sigma_r=0.4):
        """
        Apply selective Gaussian blur (domain transform)
        
        Args:
            img: Input image (BGR)
            sigma_s: Spatial standard deviation
            sigma_r: Range standard deviation
            
        Returns:
            Filtered image
        """
        try:
            if img is None:
                return None
            
            # Use domain transform filter for selective blur
            result = cv2.ximgproc.dtFilter(img, img, sigma_s, sigma_r)
            return result
        except Exception as e:
            print("Error applying selective Gaussian blur:", e)
            # Fallback to regular bilateral filter
            return cv2.bilateralFilter(img, 9, 75, 75)

    def apply_difference_of_gaussians(self, img, kernel1=(3, 3), kernel2=(5, 5)):
        """
        Apply Difference of Gaussians (DoG) filter for edge detection
        
        Args:
            img: Input image
            kernel1: First Gaussian kernel size
            kernel2: Second Gaussian kernel size
            
        Returns:
            DoG filtered image
        """
        try:
            if img is None:
                return None
            
            # Convert to grayscale if color
            if len(img.shape) == 3:
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            else:
                gray = img
            
            # Apply two Gaussians with different sizes
            gaussian1 = cv2.GaussianBlur(gray, kernel1, 1.0)
            gaussian2 = cv2.GaussianBlur(gray, kernel2, 1.0)
            
            # Compute difference
            dog = cv2.subtract(gaussian1, gaussian2)
            
            return dog
        except Exception as e:
            print("Error applying Difference of Gaussians:", e)
            return None

    def apply_stack_blur(self, img, radius=5):
        """
        Apply stack blur (fast approximation of Gaussian blur)
        
        Args:
            img: Input image
            radius: Blur radius (higher = more blur)
            
        Returns:
            Blurred image
        """
        try:
            if img is None:
                return None
            
            # Stack blur approximation using box filters
            kernel_size = 2 * radius + 1
            
            # Apply multiple box blurs
            result = img.copy()
            for _ in range(3):
                result = cv2.boxFilter(result, -1, (kernel_size, kernel_size))
            
            return result
        except Exception as e:
            print("Error applying stack blur:", e)
            return None

    def estimate_blur(self, img):
        """
        Estimate the amount of blur in an image (Laplacian variance)
        
        Args:
            img: Input image
            
        Returns:
            float: Blur estimate (higher = less blurry)
        """
        try:
            if img is None:
                return None
            
            # Convert to grayscale if needed
            if len(img.shape) == 3:
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            else:
                gray = img
            
            # Compute Laplacian and its variance
            laplacian = cv2.Laplacian(gray, cv2.CV_64F)
            variance = laplacian.var()
            
            return variance
        except Exception as e:
            print("Error estimating blur:", e)
            return None


if __name__ == "__main__":
    # Test the class
    processor = GaussianProcessor()
    print("GaussianProcessor initialized successfully")
    