import smtplib,ssl  
from time import sleep  
from email.mime.multipart import MIMEMultipart  
from email.mime.base import MIMEBase  
from email.mime.text import MIMEText  
from email.utils import formatdate  
from email import encoders
import cv2

cam = cv2.VideoCapture(-1)

ret, img = cam.read()

def send_an_email():
    cv2.imwrite('Intruder.jpg', img)

    toaddr = 'saurabha.panditraomit@gmail.com'      # To id 
    me = 'teminiproj505562@gmail.com'          # your id
    subject = "Image Test Python"              # Subject
      
    msg = MIMEMultipart()  
    msg['Subject'] = subject  
    msg['From'] = me  
    msg['To'] = toaddr  
    msg.preamble = "test "   
        #msg.attach(MIMEText(text))  
      
    part = MIMEBase('application', "octet-stream")  
    part.set_payload(open("Intruder.jpg", "rb").read())  
    encoders.encode_base64(part)  
    part.add_header('Content-Disposition', 'attachment; filename="image.jpg"')   # File name and format name
    msg.attach(part)
      
    try:  
        s = smtplib.SMTP('smtp.gmail.com', 587)  # Protocol
        s.ehlo()  
        s.starttls()  
        s.ehlo()  
        s.login(user = 'teminiproj505562@gmail.com', password = 'teproj@505562')  # User id & password
           #s.send_message(msg)  
        s.sendmail(me, toaddr, msg.as_string())  
        s.quit()  
        #except:  
        #   print ("Error: unable to send email")    
    except SMTPException as error:  
            print ("Error")                # Exception
      
send_an_email()  
