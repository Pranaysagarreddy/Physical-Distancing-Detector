import cv2
from flask import Flask, render_template, Response

app=Flask(__name__)

@app.route('/')
def index():
    """ video stream home page"""
    return render_template('index.html')


def gen():
    """ video streaming Geneatorr function."""

    img=cv2.imread("abcd.jpg")
    img=cv2.resize(img, (0,0), fx=1.0,fy=1.0)
    frame=cv2.imencode('.jpg',img)[1].tobytes()
    yield(b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    
    """ video streaming route.put this in the src attribute of an img tag"""
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary+frame')
