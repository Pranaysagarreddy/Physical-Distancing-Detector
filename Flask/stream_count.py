import time
import cv2
from flask import Flask, render_template, Response

app=Flask(__name__)

@app.route('/')
def index():
    """ video stream home page"""
    return render_template('index.html')


def gen():
    """ video streaming Geneatorr function."""
    cap=cv2.VideoCapture('test.mp4')
    while(cap.isOpened()):
        #capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            frame = cv2.VideoCapture("test.mp4")
            continue
        if ret:
            image = cv2.resize(frame, (0,0), None, 1, 1)
            gray =cv2.cvtcolor(image,cv2.COLOR_BGR2GRAY)
            fgmask = sub.apply(gray)
            kernel=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
            closing=cv2.morphologyEx(fgmask, cv2.MORPH_CLOSE,kernel)
            opening=cv2.morphologyEx(closing,cv2.MORPH_OPEN,kernel)
            dilation=cv2.dilate(opening, kernel)
            retvalbin, bins=cv2.threshold(dilation,220,255,cv2.THRESH_BINARY)
            contours, hierarchy =cv2.findContours(dilation,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            minarea=400
            maxarea=50000
            for i in range(len(contours)):
                if hierarchy[0, i, 3]== -1:
                    area=cv2.contourArea(contours[i])
                    if minarea < area < maxarea:
                        cnt =contours[i]
                        M=cv2.moments(cnt)
                        cx=int(M['m10']/M['m00'])
                        cy=int(M['m01']/M['m00'])

                        x,y,w,h=cv2.boundingRect(cnt)

                        cv2.rectangle(image, (x,y),(x + w, y + h),(0,255,0),2)

                        cv2.puttext(image,str(cx)+ "," + str(cy),(cx + 10,cy + 10),cv2.FONT_HERSHEY_SIMPLEX,.3, (0,0,255),1)
                        cv2.drawMarker(image, (cx,cy), (0,255,255),cv2.MARKER_CROSS,markerSize=8,thickness=3,line_type=cv2.LINE_8)
            frame=cv2.imencode('.jpg',image)[1].tobytes()
            yield(b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            time.sleep(0.1)
            key=cv2.waitKey(20)
            if key==27:
                break


@app.route('/video_feed')
def video_feed():
    """ video streaming route.put this in the src attribute of an img tag"""
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace;boundary=frame')

