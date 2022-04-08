from picamera import PiCamera
import datetime

PICTURE_NAME = 'pic.jpg'

def take_picture():
    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.capture('/home/pi/SISC/' + PICTURE_NAME)
    camera.close()
    del camera
    
take_picture()

now = datetime.datetime.now()
print ("Current date and time : ")
print (now.strftime("%Y-%m-%d %H:%M:%S"))
message = "Date: {}".format(now.strftime("%d-%m-%Y %H:%M:%S"))
with open('/home/pi/SISC/pic.txt', "w") as myfile:
    myfile.write(message)
    print(message) # Console information