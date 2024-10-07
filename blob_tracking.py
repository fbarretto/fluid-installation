import cv2
import numpy as np

# Initialize the camera
# List available cameras
index = 0
arr = []
while True:
    cap = cv2.VideoCapture(index)
    if not cap.read()[0]:
        break
    else:
        arr.append(index)
    cap.release()
    index += 1

print("Available cameras:", arr)

# Initialize the camera (using the first available camera)
if arr:
    cap = cv2.VideoCapture(arr[0])
else:
    raise Exception("No cameras found")

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

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

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

# Release the camera and close windows
cap.release()
cv2.destroyAllWindows()
