import os
import cv2
from PIL import Image
import numpy as np
import pickle

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "images")
FACE_CASCADE = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_alt2.xml')

RECOGNIZER = cv2.face.LBPHFaceRecognizer_create()

current_id = 0
label_ids = {}
y_label = []
x_train = []

# recupérer les images dans leurs dossiers
for root, dirs, files in os.walk(IMAGE_DIR):
    for file in files:
        if file.endswith("png") or file.endswith('jpg') or file.endswith('jpeg'):
            path = os.path.join(root, file)
            label = os.path.basename(root).replace(' ', '-').lower()
            #print(label, path)
            if not label in label_ids:
                label_ids[label] = current_id
                current_id += 1

            id_ = label_ids[label]
            # print(label_ids)

            pil_image = Image.open(path).convert("L")  # convertir en gris
            size = (560, 560)
            final_image = pil_image.resize(size, Image.ANTIALIAS)
            image_array = np.array(final_image, "uint8")
            # print(image_array)
            faces = FACE_CASCADE.detectMultiScale(
                image_array, scaleFactor=1.1, minNeighbors=1, minSize=(1, 1))
            for(x, y, z, h) in faces:
                roi = image_array[y:y+h, x:x+z]
                x_train.append(roi)
                y_label.append(id_)

with open("lables.pickle", 'wb') as f:
    pickle.dump(label_ids, f)

RECOGNIZER.train(x_train, np.array(y_label))
RECOGNIZER.save("trainner.yml")
