import cv2
import mediapipe as mp
import time
import math


class poseDetector():

    def __init__(self, mode=False, upBody=False, smooth=True, detectionCon=0.5, trackCon=0.5):

        self.mode = mode
        self.upBody = upBody
        self.smooth = smooth
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(static_image_mode=self.mode, model_complexity=self.upBody,
                                     smooth_landmarks=self.smooth,
                                     min_detection_confidence=self.detectionCon,
                                     min_tracking_confidence=self.trackCon)

        # Arms Curl Mistakes
        self.lowRangeOfMotionCounter = 0
        self.bodyLeanCounter = 0
        self.kneesBentCounter = 0

        #Leg Exercise Mistakes
        self.upperBodyDownTooMuchCounter = 0
        self.notGoingDeepEnoughCounter = 0
        self.ankleTooBentCounter = 0

    def findPose(self, img, draw=True):

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)

        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)

        return img

    def findPosition(self, img, draw=True):
        lmList = []

        if self.results.pose_landmarks:

            for id, landmark in enumerate(self.results.pose_landmarks.landmark):

                h, w, c = img.shape

                cx, cy = int(landmark.x * w), int(landmark.y * h)
                lmList.append([id, cx, cy])

                if draw:
                    cv2.circle(img, (cx, cy), 3, (255, 0, 0), cv2.FILLED)
                    cv2.putText(img, str(id), (cx, cy),
                                cv2.FONT_HERSHEY_PLAIN, 1, (155, 50, 23), 1)
        return lmList

    def getLowRangeOfMotionCounter(self):
        return self.lowRangeOfMotionCounter

    def setLowRangeOfMotionCounter(self, val):
        self.lowRangeOfMotionCounter = val

    def getBodyLeanCounter(self):
        return self.bodyLeanCounter

    def setBodyLeanCounter(self, val):
        self.bodyLeanCounter = val

    def getKneesBentCounter(self):
        return self.kneesBentCounter

    def setKneesBentCounter(self, val):
        self.kneesBentCounter = val

    def getUpperBodyDownTooMuchCounter(self):
        return self.upperBodyDownTooMuchCounter

    def setUpperBodyDownTooMuchCounter(self, val):
        self.upperBodyDownTooMuchCounter = val

    def getNotGoingDeepEnoughCounter(self):
        return self.notGoingDeepEnoughCounter

    def setNotGoingDeepEnoughCounter(self, val):
        self.notGoingDeepEnoughCounter = val

    def getAnkleTooBentCounter(self):
        return self.ankleTooBentCounter

    def setAnkleTooBentCounter(self, val):
        self.ankleTooBentCounter = val



    def detectLowRangeOfMotion(self, lmlist):
        # right_shoulder = 11
        # right_elbow = 13
        # right_wrist = 15
        '''
            1. if angle < 80
            2. counter ++
            3. return counter

            greater than 0 means good form
        '''
        try:

            right_shoulder = 12
            right_elbow = 14
            right_wrist = 16
        except IndexError:
            return

        listOfAngles = []

        listOfAngles.append(self.findAngle(right_shoulder, right_elbow, right_wrist, lmlist))

        for angle in listOfAngles:
            if (angle != None) and (angle < 85):
                self.lowRangeOfMotionCounter += 1

    def detectLeaningBody(self, lmlist):
        # right_shoulder = 12
        # waist = 24
        # right_ankle = 28
        '''
            1. if angle < 170
            2. counter ++
            3. return counter

            0 means good form
        '''
        try:

            right_shoulder = 12
            waist = 24
            right_ankle = 28

        except IndexError:
            return

        listOfAngles1 = []

        listOfAngles1.append(self.findAngle(right_shoulder, waist, right_ankle, lmlist))

        for angle in listOfAngles1:
            if (angle != None) and (angle < 170):
                self.bodyLeanCounter += 1

    def detectBentKnees(self, lmlist):
        # right waist = 24
        # right knee = 26
        # right ankle = 28
        '''
            1. if angle > 170
            2. counter ++
            3. return counter

            0 means good form
        '''
        try:

            right_waist = 24
            right_knee = 26
            right_ankle = 28

        except IndexError:
            return

        listOfAngles1 = []

        listOfAngles1.append(self.findAngle(right_waist, right_knee, right_ankle, lmlist))

        for angle in listOfAngles1:
            if (angle != None) and (angle > 210):
                self.kneesBentCounter += 1


    def detectUpperBodyDownTooMuch(self, lmlist):
        # right shoulder = 12
        # right waist = 24
        # right knee = 26
        '''
            1. if angle < 50
            2. counter ++
            3. return counter

            greater than 0 means good form
        '''
        try:
            right_shoulder = 12
            right_waist = 24
            right_knee = 26

        except IndexError:
            return

        listOfAngles1 = []

        listOfAngles1.append(self.findAngle(right_shoulder, right_waist, right_knee, lmlist))

        for angle in listOfAngles1:
            if (angle != None) and (angle < 50):
                self.upperBodyDownTooMuchCounter += 1



    def detectNotGoingDeepEnough(self, lmlist):
        # right waist = 24
        # right knee = 26
        # right ankle = 28
        
        '''
            1. if angle > 200
            2. counter ++
            3. return counter

            greater than 0 means good form
        '''
        try:
            right_waist = 24
            right_knee = 26
            right_ankle = 28

        except IndexError:
            return

        listOfAngles1 = []

        listOfAngles1.append(self.findAngle(right_waist, right_knee, right_ankle, lmlist))

        for angle in listOfAngles1:
            if (angle != None) and (angle > 200):
                self.notGoingDeepEnoughCounter += 1

    def detectAnkleTooBent(self, lmlist):
        # right knee = 26
        # right ankle = 28
        # right toe = 32

        '''
            1. if angle < 70
            2. counter ++
            3. return counter

            0 means good form
        '''
        try:
            right_knee = 26
            right_ankle = 28
            right_toe = 32

        except IndexError:
            return

        listOfAngles1 = []

        listOfAngles1.append(self.findAngle(right_knee, right_ankle, right_toe, lmlist))

        for angle in listOfAngles1:
            if (angle != None) and (angle < 70):
                self.ankleTooBentCounter += 1





    def findAngle(self, p1, p2, p3, lmlist):
        # Get Landmarks
        try:
            x1, y1 = lmlist[p1][1:]
            x2, y2 = lmlist[p2][1:]
            x3, y3 = lmlist[p3][1:]

        except IndexError:
            return

        # Calculate the Angle
        angle = int(math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2)))

        if angle < 0:
            angle += 360

        return int(angle)

def main(detector):

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    while True:

        _, img = cap.read()
        
        img = detector.findPose(img)

        lmlist = detector.findPosition(img, draw=False)

        detector.detectLowRangeOfMotion(lmlist)
        detector.detectLeaningBody(lmlist)
        detector.detectBentKnees(lmlist)

        detector.detectUpperBodyDownTooMuch(lmlist)
        detector.detectNotGoingDeepEnough(lmlist)
        detector.detectAnkleTooBent(lmlist)

        cv2.waitKey(10)
        if _:
            img = cv2.imencode('.jpg', img)[1].tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n')
        else:
            break
    
    cap.release()
    cv2.destroyAllWindows()
