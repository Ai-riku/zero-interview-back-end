from flask import Flask, render_template, Response
import cv2
import time

app=Flask(__name__)

def video_capture():
    camera=cv2.VideoCapture(0)
    frame_width = int(camera.get(3)) 
    frame_height = int(camera.get(4)) 
    size = (frame_width, frame_height)
    fps = camera.get(cv2.CAP_PROP_FPS) 
    out = cv2.VideoWriter('output.avi',  
                         cv2.VideoWriter_fourcc(*'MJPG'), 
                         fps, size) 
    start = time.time()
    end = start
    while end - start < 5:
        ## read the camera frame
        success, frame = camera.read()
        if not success:
            break
        out.write(frame)
        ret, buffer = cv2.imencode('.jpg',frame)
        frame = buffer.tobytes()
        yield(b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        end = time.time()
    camera.release()
    out.release()
    print("Video saved!")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    return Response(video_capture(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__=="__main__":
    app.run(debug=True)