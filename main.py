import numpy as np
import cv2
import pickle
import imutils

# CONF CASCADE
FACE_CASCADE = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_alt2.xml')

EYES_CASCADE = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_eye.xml')

FULLBODY_CASCADE = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_fullbody.xml')

# CONF RECOGNITION
RECOGNIZER = cv2.face.LBPHFaceRecognizer_create()
RECOGNIZER.read("src/trainner.yml")

hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

labels = {"person_name": 1}

with open("src/lables.pickle", 'rb') as f:
    og_labels = pickle.load(f)
    labels = {v: k for k, v in og_labels.items()}

# CAMERA PARAMS
camera = cv2.VideoCapture(0)

# Camera resolution
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
# camera FPS
camera.set(cv2.CAP_PROP_FPS, 60)


# FONCTIONS

def FaceDetection():
    faces = FACE_CASCADE.detectMultiScale(
        gray, scaleFactor=1.3, minNeighbors=1)

    for(x, y, z, h) in faces:
        color_face = (0, 200, 0)  # BGR 0-255
        stroke = 2
        end_coord_x = x + z
        end_coord_y = y + h
        cv2.rectangle(frame, (x, y), (end_coord_x, end_coord_y),
                      color_face, stroke)
    FacialRecognition(faces)


def FacialRecognition(faces):
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
        else:
            print(' Unkown person detected')
            # here need to implement the mail to tell that a unkown person has been detected but need to send it once.


def EyesDetection():
    eye = EYES_CASCADE.detectMultiScale(
        gray, scaleFactor=3.4, minNeighbors=2)

    for(x, y, z, h) in eye:
        color_face = (255, 0, 0)  # BGR 0-255
        stroke = 2
        end_coord_x = x + z
        end_coord_y = y + h
        cv2.rectangle(frame, (x, y), (end_coord_x, end_coord_y),
                      color_face, stroke)


def FullBodyDetection():
    fullBody = FULLBODY_CASCADE.detectMultiScale(
        gray, scaleFactor=1.3, minNeighbors=1)

    for(x, y, z, h) in fullBody:
        color_body = (0, 0, 255)
        stroke = 2
        end_coord_x = x + z
        end_coord_y = y + h
        cv2.rectangle(frame, (x, y), (end_coord_x, end_coord_y),
                      color_body, stroke)


while(True):
    # capture frame par frame
    ret, frame = camera.read()

    # converstion to gray shape
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    FaceDetection()

    # Display frame
    cv2.imshow('Reconaissance faciale', frame)
    cv2.namedWindow('Reconaissance faciale', cv2.WINDOW_OPENGL)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

# When done, we stop capturing and release camera
camera.release()
cv2.destroyAllWindows()
