
import os
import pickle
import sys
import time
import datetime
from threading import Thread

import cv2
import imutils
import numpy as np

from src.sendMail import *
from src.log import *


class Detection(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.state = True

        '''
        CASCADE CONFIGURATION
        You can add here any cascade configuration you want to use. I only use FACE and EYES for now
        '''
        self.FACE_CASCADE = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        self.EYES_CASCADE = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_eye.xml')

        # Device used for video input
        self.camera = cv2.VideoCapture(0)

        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.flag = 0
        self.date = datetime.datetime.now()

    def run(self):

        # CONF RECOGNITION
        RECOGNIZER = cv2.face.LBPHFaceRecognizer_create()
        RECOGNIZER.read(self.BASE_DIR + "/src/trainner.yml")

        hog = cv2.HOGDescriptor()
        hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

        labels = {"person_name": 1}

        with open(self.BASE_DIR + "/src/lables.pickle", 'rb') as f:
            og_labels = pickle.load(f)
            labels = {v: k for k, v in og_labels.items()}

        # Camera resolution
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        # camera FPS
        self.camera.set(cv2.CAP_PROP_FPS, 30)

        # FONCTIONS

        def FaceDetection(frame, gray):
            faces = self.FACE_CASCADE.detectMultiScale(
                gray, scaleFactor=1.05, minNeighbors=3)

            for(x, y, z, h) in faces:
                color_face = (0, 200, 0)  # BGR 0-255
                stroke = 2
                end_coord_x = x + z
                end_coord_y = y + h
                cv2.rectangle(frame, (x, y), (end_coord_x, end_coord_y),
                              color_face, stroke)
                FacialRecognition(faces, gray, frame)

        def FacialRecognition(faces, gray, frame):
            for(x, y, z, h) in faces:
                roi_gray = gray[y:y+h, x:x+z]

                # reconaissance
                id_, conf = RECOGNIZER.predict(roi_gray)
                if conf < 98:
                    print(labels[id_])
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    name = labels[id_]
                    color = (255, 0, 0)
                    stroke = 1
                    cv2.putText(frame, name, (x, y), font, 1,
                                color, stroke, cv2.LINE_AA)
                    self.flag = 0
                else:
                    # Do something when a person has been detected but not reconized
                    print(' Unkown person detected')
                    self.flag += 1
                    if self.flag == 5:
                        print('Flag at 5')
                        sendMail('Unkown person detected in your house !',
                                 'Unkown person detected')
                        self.flag = 0

        while(self.state == True):
                # capture frame par frame
            ret, frame = self.camera.read()

            # Conversion to Grey shape
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            FaceDetection(frame, gray)

            # Display frame
            cv2.imshow('Reconaissance faciale', frame)
            cv2.namedWindow('Reconaissance faciale', cv2.WINDOW_OPENGL)
            if cv2.waitKey(20) & 0xFF == ord('q'):
                break

            # When done, we stop capturing and release camera
        self.camera.release()
        cv2.destroyAllWindows()

    def stop(self):
        self.state = False


# Starting detection thread
detection = Detection()
detection.start()
