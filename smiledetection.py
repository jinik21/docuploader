import cv2 as cv
import numpy as np

#using pre-made haarcascades
faceCascade=cv.CascadeClassifier('haarcascade_frontalface_default.xml')
smileCascade=cv.CascadeClassifier('haarcascade_smile.xml')

#opening the webcam of the PC
cap=cv.VideoCapture(0)
#extracting data from the webcam, then converting image to grayscale
while True:
    ret,img=cap.read()
    gray=cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    faces=faceCascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=1,minSize=(30,30))
    #making a rectangle around the face to detect it
    for (x,y,w,h) in faces:
        cv.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
                
        smile = smileCascade.detectMultiScale(
            roi_gray,
            scaleFactor= 1.5,
            minNeighbors=5,
            minSize=(25, 25),
            )
        #if smile is detected, then display message
        for i in smile:
            if len(smile)>1:
                cv.putText(img,"U are smiling",(x,y-30),cv.FONT_HERSHEY_SIMPLEX,2,(0,255,0),3,cv.LINE_AA)
               
    cv.imshow('video', img)
    k = cv.waitKey(30) & 0xff
    # press 'ESC' to quit
    if k == 27: 
        break

cap.release()
cv.destroyAllWindows()