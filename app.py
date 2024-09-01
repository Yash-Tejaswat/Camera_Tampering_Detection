from flask import Flask, render_template, Response
import cv2
import threading
from camera_tampering import detect_tampering  # Import the function

app = Flask(__name__)
camera = None
is_running = False

def generate_frames():
    global camera
    while is_running:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/start_detection')
def start_detection():
    global camera, is_running
    if not is_running:
        camera = cv2.VideoCapture(0)
        is_running = True
        threading.Thread(target=detect_tampering, args=(camera,)).start()
    return "Detection Started"

@app.route('/stop_detection')
def stop_detection():
    global camera, is_running
    if is_running:
        is_running = False
        camera.release()
        camera = None
    return "Detection Stopped"

if __name__ == "__main__":
    app.run(debug=True)