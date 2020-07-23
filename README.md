# FacialRecognitionSecurity
A facial recognition based security system for a simple household door.

---

The aim of this project is to develop a security system for a simple household door. The system implements a facial recognition algorithm based on Haar Cascade to detect and recognize a known face.  
Haar Cascade is a classifier used to detect the object it has been trained for by superimposing the positive image over a set of negative images. It is used to detect simple facial features such as eyes, nose, mouth, etc. which are known as Haar Features.  
The algorithm for detection and recognition has been implemented on Raspberry Pi B+.  

---

Since RaspberryPi is a very computationally limited device, we had to opt for simpler technologies such as LBPH and Haar Cascades for the facial recognition available in the OpenCV Library. The motors interfaced with the Pi are Servo Motors SG90.  
The operating voltage of the motor is 5V with a torque of 2.5kg/cm. It has a rotation range of 0 – 180 degree. The control of the motor is using PWM through the Pi.  
E-Mail utilities have been added to provide an email based update for intrusion.
