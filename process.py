import time
import cv2
import numpy as np
from Week2_Filtering.Week2_Ex1_Grayscale import GrayscaleProcessor
from Week2_Filtering.Week2_Ex2_Gausian import GaussianProcessor
from Week2_Filtering.Week2_Ex3_MedianBlur import MedianProcessor
from Week2_Filtering.Week2_Ex4_SobelEdgeDetection import SobelProcessor
from Week2_Filtering.Week2_Ex5_LaplacianEdgeDetection import LaplacianProcessor
from Week2_Filtering.Week2_Ex6_Sharpen import SharpenProcessor
from Week2_Filtering.Week2_Filter7_BilateralFilter import BilateralProcessor
from Week2_Filtering.Week2_Ex8_Thresholding import ThresholdProcessor
from Week2_Filtering.Week2_Ex9_Morphology import MorphologyProcessor


class ImageProcessor:
    """
    Class for processing images from camera feed
    """
    frame = None  # BGR numpy array

    def __init__(self, frame=None):
        """Initialize image processor"""
        self.frame = frame
        self.grayscale_processor = GrayscaleProcessor()
        self.gaussian_processor = GaussianProcessor()
        self.median_processor = MedianProcessor()
        self.sobel_processor = SobelProcessor()
        self.laplacian_processor = LaplacianProcessor()
        self.sharpen_processor = SharpenProcessor()
        self.bilateral_processor = BilateralProcessor()
        self.threshold_processor = ThresholdProcessor()
        self.morphology_processor = MorphologyProcessor()

    def process_frame(self, bgr_img, filter_name='sobel', filter_strength=1.0, filter_param=None):
        """
        Process a single frame

        Args:
            bgr_img: Input image in BGR format (numpy array)

        Returns:
            tuple: (Processed image, process time in ms)
        """
        if bgr_img is None:
            raise ValueError("Input frame is None")

        start_time = time.perf_counter()

        h, w = bgr_img.shape[:2]
        side = int(min(h, w) * 0.5)
        cx, cy = w // 2, h // 2
        x0 = max(0, cx - side // 2)
        y0 = max(0, cy - side // 2)
        crop = bgr_img[y0:y0+side, x0:x0+side].copy()

        # Convert to grayscale (3-channel for display compatibility)
        processed = self.grayscale_processor.convert_to_grayscale(crop)

        # Choose filter
        f = (filter_name or '').strip().lower()
        if f == 'gaussian':
            processed = self.gaussian_processor.apply_gaussian_filter(processed, kernel_size=(25, 25), sigma=3.0)
        elif f == 'median':
            # median kernel must be odd integer
            processed = self.median_processor.apply_median_blur(processed, kernel_size=25)
        elif f == 'sobel':
            processed = self.sobel_processor.apply_sobel_x(processed, ksize=3)
        elif f == 'sharpen':
            processed = self.sharpen_processor.apply_sharpen(processed, strength=float(filter_strength))
        elif f == 'bilateral':
            processed = self.bilateral_processor.apply_bilateral(processed, d=9, sigmaColor=75, sigmaSpace=75)
        elif f == 'threshold':
            # default binary threshold at 127
            processed = self.threshold_processor.apply_threshold(processed, thresh=127, maxval=255, method='binary')
        elif f == 'erode' or f == 'dilate':
            # use filter_param as kernel size when provided
            k = 3
            try:
                if filter_param is not None:
                    k = max(1, int(filter_param))
            except Exception:
                k = 3
            if f == 'erode':
                processed = self.morphology_processor.apply_erode(processed, kernel_size=k, iterations=1)
            else:
                processed = self.morphology_processor.apply_dilate(processed, kernel_size=k, iterations=1)
        elif f == 'laplacian':
            processed = self.laplacian_processor.apply_laplacian(processed, ksize=3)
        else:
            # default: grayscale (already applied)
            pass

        # Resize to 256x256
        processed = cv2.resize(processed, (256, 256))

        process_time_ms = (time.perf_counter() - start_time) * 1000

        return processed, process_time_ms

    def preprocess(self, bgr_img):
        """
        Preprocess image (e.g., resize, normalize)

        Args:
            bgr_img: Input image in BGR format

        Returns:
            Preprocessed image
        """
        # TODO: Implement preprocessing
        pass

    def postprocess(self, result):
        """
        Postprocess results

        Args:
            result: Processed result

        Returns:
            Postprocessed result
        """
        # TODO: Implement postprocessing
        pass
