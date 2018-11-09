#!/usr/bin/env python3

import cv2

# initialize frame count
count = 0

# open the video clip
vidcap = cv2.VideoCapture('clip.mp4')

# read one frame
success,image = vidcap.read()

print("Reading frame {} {} ".format(count, success))
while success:

  # write the current frame out as a jpeg image
  cv2.imwrite("frame_{:04d}.jpg".format(count), image)   
  success,image = vidcap.read()
  print('Reading frame {} {}'.format(count, success))
  count += 1
