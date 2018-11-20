#!/usr/bin/env python3

import threading
import cv2
import numpy as np
import base64
import queue

def extractFrames():
    # Initialize frame count 
    global extractionQueue
    global filename
    fileName = filename
    count = 0

    # open video file
    vidcap = cv2.VideoCapture(fileName)

    # read first image
    success,image = vidcap.read()
    
    print("Reading frame {} {} ".format(count, success))
    while success:
        # get a jpg encoded frame
        success, jpgImage = cv2.imencode('.jpg', image)

        #encode the frame as base 64 to make debugging easier
        jpgAsText = base64.b64encode(jpgImage)

        # add the frame to the buffer
        prod_one.acquire()
        extractionQueue.put(jpgAsText)
        cons_one.release()
       
        success,image = vidcap.read()
        print('Reading frame {} {}'.format(count, success))
        count += 1

    print("Frame extraction complete")
    prod_one.acquire()
    extractionQueue.put("Stop")
    cons_one.release()



def convert_to_grayscale():
    # initialize frame count
    global extractionQueue
    global grayscaleQueue
    count = 0
    
    

    while True:
        cons_one.acquire()
        inputFrame = extractionQueue.get()
        prod_one.release()
        if inputFrame == "Stop":
            prod_two.acquire()
            grayscaleQueue.put("Stop")
            cons_two.release()
            break
        print("Converting frame {}".format(count))
         # convert image back into raw jpeg
        jpgRawImage = base64.b64decode(inputFrame)
        
        # convert to array
        jpgImage = np.asarray(bytearray(jpgRawImage), dtype=np.uint8)
        
        # get a jpg encoded frame
        img = cv2.imdecode( jpgImage ,cv2.IMREAD_UNCHANGED)
        
        # convert the image to grayscale
        grayscaleFrame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        success, grayscaleJpg = cv2.imencode('.jpg', grayscaleFrame)
        
        # convert image back into text 
        jpgAsText = base64.b64encode(grayscaleJpg)
        
        # add grayscale frame to queue
        prod_two.acquire()
        grayscaleQueue.put(jpgAsText)
        cons_two.release()
        
        count += 1

        
    print("All frames converted to grayscale")


def displayFrames():
    # initialize frame count
    count = 0
    global grayscaleQueue
    # go through each frame in the buffer until the buffer is empty
    while True:
        # get the next frame
        cons_two.acquire()
        frameAsText = grayscaleQueue.get()
        prod_two.release()
        if frameAsText == "Stop":
            break
        
        # decode the frame 
        jpgRawImage = base64.b64decode(frameAsText)

        # convert the raw frame to a numpy array
        jpgImage = np.asarray(bytearray(jpgRawImage), dtype=np.uint8)
        
        # get a jpg encoded frame
        img = cv2.imdecode( jpgImage ,cv2.IMREAD_UNCHANGED)

        print("Displaying frame {}".format(count))        

        # display the image in a window called "video" and wait 42ms
        # before displaying the next frame
        cv2.imshow("Video", img)
        if cv2.waitKey(42) and 0xFF == ord("q"):
            break

        count += 1

    print("Finished displaying all frames")
    # cleanup the windows
    cv2.destroyAllWindows()

# filename of clip to load
global filename
filename = 'clip.mp4'
buffer_size = 10
prod_one = threading.Semaphore(buffer_size)
prod_two = threading.Semaphore(buffer_size)
cons_one = threading.Semaphore(0)
cons_two = threading.Semaphore(0)
# shared queue  
global extractionQueue
extractionQueue = queue.Queue()
global grayscaleQueue
grayscaleQueue = queue.Queue()

extract_frames_thread = threading.Thread(target=extractFrames)
convert_to_grayscale_thread = threading.Thread(target=convert_to_grayscale)
display_frames_thread = threading.Thread(target=displayFrames)

extract_frames_thread.start()
convert_to_grayscale_thread.start()
display_frames_thread.start()

'''
# extract the frames
extractFrames(filename)

convert_to_grayscale()

# display the frames
displayFrames()
'''



