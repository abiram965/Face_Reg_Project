import face_recognition
import cv2
import numpy as np

imgelon_bgr = face_recognition.load_image_file('rdjtest.jpg')
imgelon_rgb = cv2.cvtColor(imgelon_bgr,cv2.COLOR_BGR2RGB)
cv2.imshow('bgr', imgelon_bgr)
cv2.imshow('rgb', imgelon_rgb)
cv2.waitKey(0)

imgelon =face_recognition.load_image_file('rdjtest.jpg')
imgelon = cv2.cvtColor(imgelon,cv2.COLOR_BGR2RGB)
#----------Finding face Location for drawing bounding boxes-------
face = face_recognition.face_locations(imgelon_rgb)[0]
copy = imgelon.copy()
#-------------------Drawing the Rectangle-------------------------
cv2.rectangle(copy, (face[3], face[0]),(face[1], face[2]), (255,0,255), 2)
cv2.imshow('copy', copy)
cv2.imshow('rdjtest',imgelon)
cv2.waitKey(0)

train_elon_encodings = face_recognition.face_encodings(imgelon)[0]

# lets test an image
test = face_recognition.load_image_file('rdj.jpg')
test = cv2.cvtColor(test, cv2.COLOR_BGR2RGB)
test_encode = face_recognition.face_encodings(test)[0]
print(face_recognition.compare_faces([train_elon_encodings],test_encode))
