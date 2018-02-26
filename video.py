
# coding: utf-8

import numpy as np
import cv2


def start_new_scanning():
    name = input()
    scanning()
    combineFaces(faces, w=100, h=100, numPerRow=5)
    eigenVector = cv2.PCACompute(data, mean=None, maxComponents=10)
    #сохранить данные в csv_файл
    
def destroy_all():
    cap.release()
    cv2.destroyAllWindows()


#функция, выделяющая лицо человека
def scanning():
    import cv2
    import sys

    cascPath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascPath)

    cap = cv2.VideoCapture(0)
  
    while cap.isOpened():
        
        ret, frame = cap.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        # flags=cv2.cv.CV_HAAR_SCALE_IMAGE
        flags=0
                        )

    # Нарисуем прямоугольник вокруг faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
        #нужно собрать data matrix
        #mean, eigenVectors = cv2.PCACompute(data, mean=None, maxComponents=10)
        
        
        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()



#собирает кадры матрицу данных
def combineFaces(faces, w=100, h=100, numPerRow=5):
    small_img = []
    row_img = []
    count = 0
    for img in faces:
        small_img.append(cv2.resize(img, (w, h)))
        count += 1
        if count % numPerRow == 0:
            count = 0
            row_img.append(np.concatenate(small_img, axis=1))
            small_img = []
    if len(small_img) > 0:
        for x in range (0, numPerRow-len(small_img)):
            small_img.append(np.zeros((h,w), np.uint8))
        row_img.append(np.concatenate(small_img, axis=1))
    
    data = np.concatenate(row_img, axis=0)
    return data

