import cv2
import os
import numpy as np
class CaptureSaveImgProcessor:
    def __init__(self):
        pass
    
    # =============================================================================
    # STEP 1: BASIC IMAGE CAPTURE (Weeks 1-2)
    # Topic: Introduction to Computer Vision, Images as Functions & Filtering
    # =============================================================================
    def capture_and_save_image(self, bgr_img, filename):
        """
        Capture and save static image from camera
        
        Args:
            bgr_img: Input image in BGR format (numpy array)
            filename: Path to save the image
            
        Returns:
            bool: True if successful, False otherwise
        """
        # TODO: Implement image capture and saving
        # Sinh viên cần:
        # 1. Kiểm tra bgr_img có hợp lệ không
        # 2. Lưu ảnh vào thư mục CapturedImage/
        # 3. Trả về True nếu thành công, False nếu thất bại
        pass
    
        try:
            # 1. Kiểm tra ảnh đầu vào có hợp lệ không
            if bgr_img is None or not isinstance(bgr_img, np.ndarray):
                return False

            # 2. Tạo thư mục CapturedImage nếu chưa tồn tại
            save_dir = "CapturedImage"
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)

            # Ghép đường dẫn lưu ảnh
            save_path = os.path.join(save_dir, filename)

            # 3. Lưu ảnh
            success = cv2.imwrite(save_path, bgr_img)

            return success

        except Exception as e:
            print("Error saving image:", e)
            return False

    def load_image(self, image_path):
        """
        Load an image from file
        
        Args:
            image_path: Path to the image file
            
        Returns:
            np.ndarray: Image in BGR format, or None if failed
        """
        try:
            if not os.path.exists(image_path):
                print(f"Image file not found: {image_path}")
                return None
            
            bgr_img = cv2.imread(image_path)
            if bgr_img is None:
                print(f"Failed to load image: {image_path}")
                return None
            
            return bgr_img
        
        except Exception as e:
            print("Error loading image:", e)
            return None

    def display_image(self, bgr_img, window_name="Image"):
        """
        Display an image in a window
        
        Args:
            bgr_img: Input image in BGR format
            window_name: Name of the display window
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if bgr_img is None or not isinstance(bgr_img, np.ndarray):
                print("Invalid image for display")
                return False
            
            cv2.imshow(window_name, bgr_img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            
            return True
        
        except Exception as e:
            print("Error displaying image:", e)
            return False

    def capture_video(self, duration=10, output_file="captured_video.avi"):
        """
        Capture video from webcam
        
        Args:
            duration: Duration to capture in seconds
            output_file: Output video filename
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            cap = cv2.VideoCapture(0)
            
            if not cap.isOpened():
                print("Failed to open camera")
                return False
            
            # Get camera properties
            frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            
            # Create video writer
            save_dir = "CapturedVideo"
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)
            
            video_path = os.path.join(save_dir, output_file)
            fourcc = cv2.VideoWriter_fourcc(*'MJPG')
            out = cv2.VideoWriter(video_path, fourcc, fps, (frame_width, frame_height))
            
            # Capture frames
            start_time = cv2.getTickCount()
            frame_count = 0
            
            while True:
                ret, frame = cap.read()
                
                if not ret:
                    break
                
                out.write(frame)
                cv2.imshow('Recording...', frame)
                frame_count += 1
                
                # Check if duration is exceeded
                elapsed_time = (cv2.getTickCount() - start_time) / cv2.getTickFrequency()
                if elapsed_time >= duration:
                    break
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            
            cap.release()
            out.release()
            cv2.destroyAllWindows()
            
            print(f"Video saved: {video_path}")
            return True
        
        except Exception as e:
            print("Error capturing video:", e)
            return False

    def get_image_info(self, bgr_img):
        """
        Get information about an image
        
        Args:
            bgr_img: Input image in BGR format
            
        Returns:
            dict: Dictionary containing image information
        """
        try:
            if bgr_img is None or not isinstance(bgr_img, np.ndarray):
                return None
            
            height, width = bgr_img.shape[:2]
            channels = bgr_img.shape[2] if len(bgr_img.shape) == 3 else 1
            dtype = bgr_img.dtype
            
            info = {
                'width': width,
                'height': height,
                'channels': channels,
                'data_type': str(dtype),
                'size_bytes': bgr_img.nbytes
            }
            
            return info
        
        except Exception as e:
            print("Error getting image info:", e)
            return None


if __name__ == "__main__":
    # Test the class
    processor = CaptureSaveImgProcessor()
    print("CaptureSaveImgProcessor initialized successfully")
