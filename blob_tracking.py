#!/usr/bin/python3

import cv2
import numpy as np
from picamera2 import Picamera2

class BlobTracker:
    def __init__(self, lower_color, upper_color, min_area=150, max_area=2000):
        self.lower_color = lower_color
        self.upper_color = upper_color

        # Create a SimpleBlobDetector with parameters
        params = cv2.SimpleBlobDetector_Params()
        params.filterByArea = True
        params.minArea = min_area
        params.maxArea = max_area

        self.detector = cv2.SimpleBlobDetector_create(params)

        # Initialize Picamera2
        self.picam2 = Picamera2()
        self.picam2.configure(self.picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)}))
        self.picam2.start()

        cv2.startWindowThread()

    def track_blobs(self):
        while True:
            # Capture frame-by-frame
            frame = self.picam2.capture_array()

            # Convert the frame to HSV (hue, saturation, value)
            hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            # Threshold the image to get only the colors within the specified range
            mask = cv2.inRange(hsv_frame, self.lower_color, self.upper_color)

            # Detect blobs in the masked image
            keypoints = self.detector.detect(mask)

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
        self.picam2.stop()

if __name__ == "__main__":
    lower_color = np.array([30, 100, 100])
    upper_color = np.array([90, 255, 255])
    blob_tracker = BlobTracker(lower_color, upper_color)
    blob_tracker.track_blobs()