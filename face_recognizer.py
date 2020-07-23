import smtplib,ssl
import RPi.GPIO as GPIO
import time
from email.mime.multipart import MIMEMultipart  
from email.mime.base import MIMEBase  
from email.mime.text import MIMEText  
from email.utils import formatdate  
from email import encoders
import cv2
import numpy as np
import os 

def send_email():
    to = 'saurabha.panditrao@gmail.com'
    me = 'teminiproj505562@gmail.com'
    subject = "Intruder Alert"

    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = me
    msg['To'] = to
    msg.preamble = "test"

    part = MIMEBase('application', "octet-stream")
    part.set_payload(open("Intruder.jpg", "rb").read())  
    encoders.encode_base64(part)  
    part.add_header('Content-Disposition', 'attachment; filename="image.jpg"')
    msg.attach(part)
      
    try:  
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.ehlo()  
        s.starttls()  
        s.ehlo()  
        s.login(user = 'teminiproj505562@gmail.com', password = 'teproj@505562')
        s.sendmail(me, toaddr, msg.as_string())  
        s.quit()     
    except SMTPException as error:
        print ("Error")  


def motor():
    servopin = 17
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(servopin, GPIO.OUT)
    GPIO.setwarnings(False)
    p = GPIO.PWM(servopin, 50)
    p.start(8.5)

    try:
        p.ChangeDutyCycle(8.5)
        time.sleep(1)
        p.ChangeDutyCycle(3)
        time.sleep(5)
        p.ChangeDutyCycle(8.5)
        time.sleep(1)
    except KeyboardInterrupt:
        p.stop()
        GPIO.cleanup()


recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath);

font = cv2.FONT_HERSHEY_SIMPLEX

id = 0

names = ['None', 'Apurva', 'Saurabha'] 

cam = cv2.VideoCapture(-1)
cam.set(3, 640) # set video widht
cam.set(4, 480) # set video height

minW = 0.1*cam.get(3)
minH = 0.1*cam.get(4)

while True:

    ret, img =cam.read()
    if ret:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale( 
            gray,
            scaleFactor = 1.2,
            minNeighbors = 5,
            minSize = (int(minW), int(minH)),
           )

        for(x,y,w,h) in faces:

            cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)

            id, confidence = recognizer.predict(img[y:y+h,x:x+w])

            # Check if confidence is less them 100 ==> "0" is perfect match 
            if (confidence < 30):
                id = names[id]
                confidence = "  {0}%".format(round(100 - confidence))
                motor()
            else:
                id = "unknown"
                confidence = "  {0}%".format(round(100 - confidence))
                cv2.imwrite('Intruder.jpg', img)
                send_email()
            
            cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
            cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)  
        
        cv2.imshow('camera',img) 

    k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
    if k == 27:
        break

print("\n [INFO] Exiting Program and cleanup stuff")
cam.release()
cv2.destroyAllWindows()
