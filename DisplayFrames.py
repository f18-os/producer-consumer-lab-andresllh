#!/usr/bin/env python3

import cv2

# initialize frame count
count = 0

# Generate the filename for the first frame 
frameFileName = "grayscale_{:04d}.jpg".format(count)

# load the frame
frame = cv2.imread(frameFileName)

while frame is not None:
    print("Displaying frame {}".format(count))

    # Display the frame in a window called "Video"
    cv2.imshow("Video", frame)

    # Wait for 42 ms and check if the user wants to quit
    if cv2.waitKey(42) and 0xFF == ord("q"):
        break

    # get the next frame filename
    count += 1
    frameFileName = "grayscale_{:04d}.jpg".format(count)

    # Read the next frame file
    frame = cv2.imread(frameFileName)

# make sure we cleanup the windows, otherwise we might end up with a mess
cv2.destroyAllWindows()
