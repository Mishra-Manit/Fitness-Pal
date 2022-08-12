from cv2 import VideoCapture
from flask import Flask
from flask import render_template
from flask import Response
from flask import request, redirect
import os

import webbrowser, _thread, time

import poseModule

import poseModule2

app = Flask(__name__)

detector = poseModule.poseDetector()
detector2 = poseModule2.poseDetector()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/exercises')
def exercises():
    return render_template('exercises.html')



@app.route('/optionsArms')
def optionsArms():
    return render_template('optionsArms.html')

@app.route('/optionsLegs')
def optionsLegs():
    return render_template('optionsLegs.html')




@app.route('/upload-video', methods=["GET"])
def display_upload_video():
    return render_template("uploadPageArms.html")

@app.route('/upload-video', methods=["GET", "POST"])
def upload_video():
    detector2.setLowRangeOfMotionCounter(0)
    detector2.setBodyLeanCounter(0)
    detector2.setKneesBentCounter(0)

    videofile = request.files['videofile']
    video_path = "useruploadedvids/useruploadedvid.mp4" 
    videofile.save(video_path)

    return poseModule2.main(detector2)


@app.route('/upload-video-legs', methods=["GET"])
def display_upload_video_legs():
    return render_template("uploadPageLegs.html")

@app.route('/upload-video-legs', methods=["GET", "POST"])
def upload_video_legs():
    detector2.setLowRangeOfMotionCounter(0)
    detector2.setBodyLeanCounter(0)
    detector2.setKneesBentCounter(0)

    videofile = request.files['videofile']
    video_path = "useruploadedvids/useruploadedvid.mp4" 
    videofile.save(video_path)

    return poseModule2.main(detector2)




@app.route('/preloaderArms')
def preloader():
    return render_template('preloaderArms.html')

@app.route('/preloaderLegs')
def preloaderLegs():
    return render_template('preloaderLegs.html')




@app.route('/demoArms')
def demo():
    detector.setLowRangeOfMotionCounter(0)
    detector.setBodyLeanCounter(0)
    detector.setKneesBentCounter(0)

    return render_template('demoArms.html')

@app.route('/demoLegs')
def demoLegs():
    detector.setLowRangeOfMotionCounter(0)
    detector.setNotGoingDeepEnoughCounter(0)
    detector.setAnkleTooBentCounter(0)

    return render_template('demoLegs.html')




@app.route('/analyticsArmsUpload')
def waitingOnResults():
    return render_template('analyticsArmsUpload.html')

@app.route('/analyticsArms')
def analytics():
    return render_template('analyticsArms.html')

@app.route('/analyticsLegs')
def analyticsLegs():
    return render_template('analyticsLegs.html')

@app.route('/analyticsLegsUpload')
def analyticsLegsUpload():
    return render_template('analyticsLegsUpload.html')





@app.route('/resultsArmsUpload')
def resultsArmsUpload():
    rangeOfMotionAmount = int(detector2.getLowRangeOfMotionCounter())
    leanAmount = int(detector2.getBodyLeanCounter())
    kneesBentAmount = int(detector2.getKneesBentCounter())

    grade = calculateGradeArms(rangeOfMotionAmount, leanAmount, kneesBentAmount)

    return render_template('resultsArmsUpload.html', grade=grade)


@app.route('/resultsArms')
def resultsArms():
    rangeOfMotionAmount = int(detector.getLowRangeOfMotionCounter())
    leanAmount = int(detector.getBodyLeanCounter())
    kneesBentAmount = int(detector.getKneesBentCounter())

    grade = calculateGradeArms(rangeOfMotionAmount, leanAmount, kneesBentAmount)

    return render_template('resultsArms.html', grade=grade)

@app.route('/resultsLegs')
def resultsLegs():
    upperBodyDownTooMuchAmount = int(detector.getUpperBodyDownTooMuchCounter())
    notDeepEnoughAmount = int(detector.getNotGoingDeepEnoughCounter())
    ankleTooBentAmount = int(detector.getAnkleTooBentCounter())

    grade = calculateGradeLegs(upperBodyDownTooMuchAmount, notDeepEnoughAmount, ankleTooBentAmount)

    return render_template('resultsLegs.html', grade=grade)

@app.route('/resultsLegsUpload')
def resultsLegsUpload():
    upperBodyDownTooMuchAmount = int(detector2.getUpperBodyDownTooMuchCounter())
    notDeepEnoughAmount = int(detector2.getNotGoingDeepEnoughCounter())
    ankleTooBentAmount = int(detector2.getAnkleTooBentCounter())

    grade = calculateGradeLegs(upperBodyDownTooMuchAmount, notDeepEnoughAmount, ankleTooBentAmount)

    return render_template('resultsLegsUpload.html', grade=grade)


def calculateGradeArms(rangeOfMotionAmount, leanAmount, kneesBentAmount):
    totalNum = 0

    gradeString = ""

    if rangeOfMotionAmount > 0:
        totalNum += 1
    if leanAmount == 0:
        totalNum += 1
    if kneesBentAmount == 0:
        totalNum += 1


    if totalNum == 0:
        gradeString = "D"
    if totalNum == 1:
        gradeString = "C"
    if totalNum == 2:
        gradeString = "B"
    if totalNum == 3:
        gradeString = "A"
    
    return gradeString

def calculateGradeLegs(upperBodyDownTooMuchAmount, notDeepEnoughAmount, ankleTooBentAmount):
    totalNum = 0

    if upperBodyDownTooMuchAmount > 0:
        totalNum += 1
    if notDeepEnoughAmount > 0:
        totalNum += 1
    if ankleTooBentAmount == 0:
        totalNum += 1


    if totalNum == 0:
        gradeString = "D"
    if totalNum == 1:
        gradeString = "C"
    if totalNum == 2:
        gradeString = "B"
    if totalNum == 3:
        gradeString = "A"

    return gradeString

    

@app.route('/video_feed')
def video_feed():
    return Response(poseModule.main(detector), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    # host
    app.run(host='127.0.0.1', debug=True, port=5000)

    
