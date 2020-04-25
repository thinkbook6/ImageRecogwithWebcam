import io
import os
from datetime import datetime

import numpy

import cv2
from google.cloud import vision_v1p3beta1 as vision

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'G:/Docs/Python/ImageRecok/key/FruitRecogProject-key.json'

SOURCE_PATH = "G:/Docs/Python/ImageRecok/"

FOOD_CATEGORY = 'Fruit'

def load_name(FOOD_CATEGORY):
    names = [line.rstrip('\n').lower() for line in open('food_dictionary/' + FOOD_CATEGORY + '.txt')]
    return names


def recognize_image(img_path, list_foods):
    
    # Read image with opencv
    img = cv2.imread(img_path)

    # Get image size
    height, width = img.shape[:2]

    #scale Image

    img = cv2.resize(img, (800, int((height * 800) / width)))

    #Save image to temp file

    cv2.imwrite(SOURCE_PATH + 'output.jpg', img)

    img_path = SOURCE_PATH + 'output.jpg'

    #create google vision client

    client = vision.ImageAnnotatorClient()

    #Read image file

    with io.open(img_path, 'rb') as image_file:
    	content = image_file.read()

    image = vision.types.Image(content=content)

    #recognize Content

    response = client.label_detection(image=image)

    labels = response.label_annotations

    for label in labels:
        # if len(text.description) == 10:
        desc = label.description.lower()
        score = round(label.score, 2)
        print("label: ", desc, "  score: ", score)

        if (desc in list_foods):
            # If Image is recognized, then print the identified label on the image and save it. 

            cv2.putText(img, desc.upper(), (300, 150), cv2.FONT_HERSHEY_PLAIN, 1, (50, 50, 200), 2)
            cv2.imshow('Identified Image', img)
            cv2.waitKey(0)

            #Stop after recognizing the first fruit

            break




key = cv2. waitKey(1)
webcam = cv2.VideoCapture(0)

while True:
    try:
        check, frame = webcam.read()

        cv2.imshow("Webcam Capturing", frame)
        key = cv2.waitKey(1)

        if key == ord('c'): 
            
            cv2.imwrite(filename='pic/saved_img.jpg', img=frame)
            webcam.release()
            
            img_new = cv2.imread('pic/saved_img.jpg', cv2.IMREAD_COLOR)
            img_new = cv2.imshow("Captured Image", img_new)
            
            cv2.waitKey(1800)
            cv2.destroyAllWindows()

            print("Image saved!")
            
            # Call Food Recognition method

            list_foods = load_name(FOOD_CATEGORY)
            path = SOURCE_PATH + 'pic/saved_img.jpg'
            recognize_image(path, list_foods)
            
            break

        elif key == ord('q'):
            print("Turning off camera.")
            webcam.release()
            print("Camera off.")
            cv2.destroyAllWindows()
            break
        
    except(KeyboardInterrupt):
        print("Turning off camera.")
        webcam.release()
        print("Camera off.")
        cv2.destroyAllWindows()
        break