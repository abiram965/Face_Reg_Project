#Import Necessary Libraries
import csv
from random import choice
import cv2
import face_recognition
import os
import numpy as np
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


print("***** Face Recognition Attendance System By FRIENDS ON CODE*****")

def menuDisplay():
    print('============================')
    print('======= WELCOME MENU =======')
    print('============================')
    print("[1] Recognition Faces")
    print("[2] View_Attendance")
    print("[3] Send Mail to ADMIN")
    print("[4] Exit")
    CHOICE = int(input("Enter choice: "))
    menuSelection(CHOICE)
    

def menuSelection(CHOICE):
    if CHOICE == 1:
        Live_cam()
    elif CHOICE == 2:
        View_Attendance()
    elif CHOICE == 3:
        sent_mail()
    elif CHOICE == 4:
        print('=============================')
        print("======= Program Ended =======")
        print('=============================')
        exit

#To read the CSV file

def View_Attendance():
    my_file = open("C:/Users/ABIRAM R/OneDrive/Desktop/Programs/foc_project/AttendanceFOC.csv","r")
    to_read = my_file.read()
    print(to_read)
    my_file.close()
    CHOICE = int (input("Enter 0 to Continue (OR) 4 to Exit : "))
    if CHOICE == 0:
        menuDisplay()
    else:
         print('=============================')
         print("======= Program Ended =======")
         print('=============================')
         exit
    

#send mail

def sent_mail():
    fromaddr = "abiram965@gmail.com"
    password = "9788082490"
    toaddr = "vishalvvh1@gmail.com"


    # instance of MIMEMultipart
    msg = MIMEMultipart()

    # storing the senders email address
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "MAIL SENT BY Face_Recognition SYSTEM"

    # string to store the body of the mail
    body = "SNSCT-AIML-Attendance"

    # attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))

    # open the file to be sent
    filename = "C:/Users/ABIRAM R/OneDrive/Desktop/Programs/foc_project/AttendanceFOC.csv"
    attachment = open(filename, "rb")

    # instance of MIMEBase and named as p
    p = MIMEBase('application', 'octet-stream')

    # To change the payload into encoded form
    p.set_payload((attachment).read())


    # encode into base64
    encoders.encode_base64(p)

    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    # attach the instance 'p' to instance 'msg'
    msg.attach(p)

    # creates SMTP session
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr,password)

    # Converts the Multipart msg into a string
    text = msg.as_string()

    server.send_message(msg)

    server.quit()
    print("Mail sent successfully")
    CHOICE = int (input("Enter 0 to Continue (OR) 4 to Exit : "))
    if CHOICE == 0:
        menuDisplay()
    else:
         print('=============================')
         print("======= Program Ended =======")
         print('=============================')
         exit

#Define a folder path where your training image dataset will be stored

path = 'C:/Users/ABIRAM R/OneDrive/Desktop/Programs/foc_project/imagesattendance'

images = []
classNames = [] 
mylist = os.listdir(path)
for cl in mylist:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])

#•	create a function to encode all the train images and store them in a variable encoded_face_train. 

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encoded_face = face_recognition.face_encodings(img)[0]
        encodeList.append(encoded_face)
    return encodeList
encoded_face_train = findEncodings(images)

#•	Creating a function that will create a Attendance.csv file to store the attendance with time.

def markAttendance(name):
    with open('C:/Users/ABIRAM R/OneDrive/Desktop/Programs/foc_project/AttendanceFOC.csv','r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            time = now.strftime('%I:%M:%S:%p')
            date = now.strftime('%d-%B-%Y')
            f.writelines(f'\n{name}, {time}, {date}')

#Read Webcam for Real-Time Recognition.
# take pictures from webcam 
def Live_cam():
    while True:
        cap = cv2.VideoCapture(0)
        success, img = cap.read()
        imgS = cv2.resize(img, (0,0), None, 0.25,0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
        faces_in_frame = face_recognition.face_locations(imgS)
        encoded_faces = face_recognition.face_encodings(imgS, faces_in_frame)
        for encode_face, faceloc in zip(encoded_faces,faces_in_frame):
            
            matches = face_recognition.compare_faces(encoded_face_train, encode_face)
            faceDist = face_recognition.face_distance(encoded_face_train, encode_face)
            matchIndex = np.argmin(faceDist)
            print(matchIndex)
            if matches[matchIndex]:
                
                name = classNames[matchIndex].upper().lower()
                y1,x2,y2,x1 = faceloc
                # since we scaled down by 4 times
                y1, x2,y2,x1 = y1*4,x2*4,y2*4,x1*4
                cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
                cv2.rectangle(img, (x1,y2-35),(x2,y2), (0,255,0), cv2.FILLED)
                cv2.putText(img,name, (x1+6,y2-5), cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
                markAttendance(name)
        cv2.imshow('webcam', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    CHOICE = int (input("Enter 0 to Continue (OR) 4 to Exit : "))
    if CHOICE == 0:
        menuDisplay()
    else:
         print('=============================')
         print("======= Program Ended =======")
         print('=============================')
         exit
            
menuDisplay()
