#!/usr/bin/python3

import cv2
import numpy as np
from picamera2 import Picamera2

# Define the color range for blob detection (in HSV format)
lower_color = np.array([30, 100, 100])  
upper_color = np.array([90, 255, 255])

# Create a SimpleBlobDetector with default parameters
params = cv2.SimpleBlobDetector_Params()
params.filterByArea = True
params.minArea = 150  # Minimum blob area
params.maxArea = 2000  # Maximum blob area

# Create a detector with the parameters
detector = cv2.SimpleBlobDetector_create(params)

# Initialize Picamera2
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)}))
picam2.start()

cv2.startWindowThread()

while True:
    # Capture frame-by-frame
    frame = picam2.capture_array()

    # Convert the frame to HSV (hue, saturation, value)
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Threshold the image to get only the colors within the specified range
    mask = cv2.inRange(hsv_frame, lower_color, upper_color)

    # Detect blobs in the masked image
    keypoints = detector.detect(mask)

    # Draw detected blobs as red circles
    frame_with_keypoints = cv2.drawKeypoints(frame, keypoints, np.array([]), (0, 0, 255),
                                             cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    # Display the frame with keypoints
    cv2.imshow('Blob Detection', frame_with_keypoints)

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources and close windows
cv2.destroyAllWindows()
picam2.stop()