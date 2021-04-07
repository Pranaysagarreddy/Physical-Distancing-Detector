import time
import cv2
from flask import Flask,render_template,Response

app=Flask(__name__)

@app.route('/')
def index():
    """ video stream home page"""
    return render_template('index.html')
def gen():
    """ video streaming Gender function."""
    cap=cv2.VideoCapture('output.gif')
    #read until video is captured
    while(cap.isOpened()):
        #capture frame-by-frame
        ret,img=cap.read()
        if ret==True:
            img=cv2.resize(img, (0,0), fx=1.5,fy=1.5)
            frame=cv2.imencode('.jpg',img)[1].tobytes()
            yield(b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            time.sleep(0.1)
        else:
            break

@app.route('/video_feed')
def video_feed():
    """ video streaming route.put this in the src attribute of an img tag"""
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace;boundary=frame')

