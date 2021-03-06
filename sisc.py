import numpy as np
import cv2
from gpiozero import Button
from time import sleep
from picamera import PiCamera
from fbchat import Client
from fbchat.models import *

PICTURE_NAME = 'camera_snapshot.jpg'
SENSOR_PIN = 24
sensor = Button(SENSOR_PIN)
fb_client = None

FIGURES = ['cat', 'dog', 'person']

FB_SEND = True
FB_USER = 'sisc.elsys@gmail.com'
FB_PASS = '******'
RECIPIENTS = ['yordan.markov.90']

def take_picture():
    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.capture('/home/pi/SISC/' + PICTURE_NAME)
    camera.close()
    del camera
    
def extract_boxes_confidences_classids(outputs, confidence, width, height):
    boxes = []
    confidences = []
    classIDs = []

    for output in outputs:
        for detection in output:            
            scores = detection[5:]
            classID = np.argmax(scores)
            conf = scores[classID]
            if conf > confidence:
                box = detection[0:4] * np.array([width, height, width, height])
                centerX, centerY, w, h = box.astype('int')
                x = int(centerX - (w / 2))
                y = int(centerY - (h / 2))
                boxes.append([x, y, int(w), int(h)])
                confidences.append(float(conf))
                classIDs.append(classID)

    return boxes, confidences, classIDs

def draw_bounding_boxes(image, boxes, confidences, classIDs, idxs, colors, labels):
    if len(idxs) > 0:
        for i in idxs.flatten():
            x, y = boxes[i][0], boxes[i][1]
            w, h = boxes[i][2], boxes[i][3]

            color = [int(c) for c in colors[classIDs[i]]]
            cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
            text = "{}: {:.4f}".format(labels[classIDs[i]], confidences[i])
            cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    return image
 
def make_prediction(net, layer_names, labels, image, confidence, threshold):
    height, width = image.shape[:2]
    

    blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    outputs = net.forward(layer_names)

    boxes, confidences, classIDs = extract_boxes_confidences_classids(outputs, confidence, width, height)

    idxs = cv2.dnn.NMSBoxes(boxes, confidences, confidence, threshold)

    return boxes, confidences, classIDs, idxs

def analyze_picture():
    labels = open('/home/pi/SISC/model/coco.names').read().strip().split('\n')
    colors = np.random.randint(0, 255, size=(len(labels), 3), dtype='uint8')
    net = cv2.dnn.readNetFromDarknet('/home/pi/SISC/model/yolov3.cfg', '/home/pi/SISC/model/yolov3.weights')
    layer_names = net.getLayerNames()
    layer_names = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    image = cv2.imread('/home/pi/SISC/' + PICTURE_NAME)

    confidence=0.5  
    threshold=0.3   

    boxes, confidences, classIDs, idxs = make_prediction(net, layer_names, labels, image, confidence, threshold)
    found_figures = []
    for id in classIDs:
        found_figures.append(labels[id])
    image = draw_bounding_boxes(image, boxes, confidences, classIDs, idxs, colors, labels)
    cv2.imwrite(f'/home/pi/SISC/analyzed_{PICTURE_NAME}', image)
    cv2.destroyAllWindows()

    return found_figures

print("SISC started...")
while True:
    if not sensor.is_pressed:
        sleep(1)
        continue
    print ("Movement detected! Picture taken! Processing...")
    take_picture()
    found_figures = analyze_picture()
    matching_figures = []
    for figure in found_figures:
        if figure in FIGURES:
            matching_figures.append(figure)
    if len(matching_figures) >= 1: #0
        message = "Detected {}!".format(', '.join(matching_figures))
        print(message)
    else:
        continue
    image = "/home/pi/SISC/analyzed_{}".format(PICTURE_NAME)
    if FB_SEND:
        message = "Movement detected! Detected {}!".format(', '.join(matching_figures))
        if not fb_client:
            fb_client = Client(FB_USER, FB_PASS)
        for to_user in RECIPIENTS:
            user = fb_client.searchForUsers(to_user)
            if not user:
                continue
            if not image:
                fb_client.send(Message(text=message), thread_id=user[0].uid, thread_type=ThreadType.USER)
            else:
                fb_client.sendLocalFiles(image, message=Message(text=message), thread_id=user[0].uid, thread_type=ThreadType.USER)
    sleep(10)

