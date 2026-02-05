from flask import Flask, render_template, Response, request, jsonify
import cv2
import threading
import time
import base64
import numpy as np
from process import ImageProcessor
from camera import VideoCamera
app = Flask(__name__)


# initialize two camera handlers (two columns)
cameras = {
    1: VideoCamera(),
    2: VideoCamera()
}

# --- Routes ---
@app.route('/')
def index():
    return render_template('index.html')

def mjpeg_generator(cam_id):
    cam = cameras.get(cam_id)
    if cam is None:
        return
    boundary = b'--frame'
    while True:
        frame_bytes = cam.get_frame_jpeg()
        if frame_bytes:
            yield b'%s\r\nContent-Type: image/jpeg\r\nContent-Length: %d\r\n\r\n%s\r\n' % (boundary, len(frame_bytes), frame_bytes)
        else:
            # serve a small blank JPEG fallback so client doesn't break
            blank = create_blank_jpeg()
            yield b'%s\r\nContent-Type: image/jpeg\r\nContent-Length: %d\r\n\r\n%s\r\n' % (boundary, len(blank), blank)
        time.sleep(0.04)

def create_blank_jpeg():
    # create gray placeholder
    img = 128 * np.ones((240, 320, 3), dtype=np.uint8)
    ret, jpeg = cv2.imencode('.jpg', img)
    return jpeg.tobytes() if ret else b''

@app.route('/video_feed/<int:cam_id>')
def video_feed(cam_id):
    # returns multipart mjpeg stream
    return Response(mjpeg_generator(cam_id),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/set_source', methods=['POST'])
def set_source():
    # payload: { cam_id: int, source: str }
    data = request.get_json()
    cam_id = int(data.get('cam_id'))
    source = data.get('source', '').strip()
    if cam_id not in cameras:
        return jsonify({'ok': False, 'error': 'invalid cam_id'}), 400
    if source == '':
        # stop camera if empty
        cameras[cam_id].stop()
        return jsonify({'ok': True, 'msg': 'stopped'})
    try:
        cameras[cam_id].start(source)
        return jsonify({'ok': True})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500

@app.route('/capture', methods=['POST'])
def capture():
    # payload: { cam_id: int }
    data = request.get_json()
    cam_id = int(data.get('cam_id'))
    filter_name = data.get('filter', '').strip().lower()
    filter_strength = float(data.get('filter_strength', 1.0))
    # generic numeric parameter for filters (e.g., kernel size for morphology)
    filter_param = data.get('filter_param', None)
    try:
        filter_param = int(filter_param) if filter_param is not None else None
    except Exception:
        filter_param = None
    if cam_id not in cameras:
        return jsonify({'ok': False, 'error': 'invalid cam_id'}), 400
    cam = cameras[cam_id]
    frame = cam.get_frame_bgr()
    if frame is None:
        return jsonify({'ok': False, 'error': 'no frame yet'}), 400

    # Convert BGR -> JPEG base64 for immediate display
    ret, jpg = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
    if not ret:
        return jsonify({'ok': False, 'error': 'encode_failed'}), 500
    raw = jpg.tobytes()
    b64 = base64.b64encode(raw).decode('utf-8')
    data_uri = 'data:image/jpeg;base64,' + b64

    # Process with selected filter
    processed, process_time_ms = process_image_placeholder(frame, filter_name, filter_strength, filter_param)

    ret2, jpg2 = cv2.imencode('.jpg', processed, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
    raw2 = jpg2.tobytes()
    b642 = base64.b64encode(raw2).decode('utf-8')
    processed_uri = 'data:image/jpeg;base64,' + b642

    return jsonify({'ok': True, 'image': data_uri, 'processed': processed_uri, 'process_time_ms': round(process_time_ms, 2)})

def process_image_placeholder(bgr_img, filter_name='', filter_strength=1.0, filter_param=None):
    """
    Placeholder image processing:
    - crop a center square at 50% of min(height,width)
    Replace this with your real processing.
    """
    print("Processing image placeholder...")
    # Use ImageProcessor pipeline and pass filter_name
    processed_frame, process_time_ms = ImageProcessor(bgr_img).process_frame(bgr_img, filter_name=filter_name, filter_strength=filter_strength, filter_param=filter_param)
    return processed_frame, process_time_ms

if __name__ == '__main__':
    # debug mode off in production
    app.run(host='0.0.0.0', port=5000, threaded=True)
