from ultralytics import YOLO
import cv2
import numpy as np

# Load a model
model = YOLO("best1.pt")
class_names = model.names  # Assuming model.names returns a list of class names
cap = cv2.VideoCapture('zebra5.mp4')
count = 0

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output_video.avi', fourcc, 30.0, (1020, 500))



while True:
    ret, img = cap.read()
    if not ret:
        break
    count += 1
    if count % 3 != 0:
        continue

    img = cv2.resize(img, (1020, 500))
    h, w, _ = img.shape
    results = model.predict(img)

    # Flag to check if zebra crossing is detected
    zebra_detected = False

    # Flags to check if green or yellow signal is detected
    green_detected = False
    yellow_detected = False

    for r in results:
        boxes = r.boxes  # Boxes object for bbox outputs
        masks = r.masks  # Masks object for segment masks outputs

        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            cls = int(box.cls[0])

            if class_names[cls] == "red-light":  # Check if object is a zebra
                zebra_detected = True
                cv2.putText(img, "Red Light: Please stop the car and wait for green light", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)



            elif class_names[cls] == "green-light":  # Check if object is a green signal
                green_detected = True
                cv2.putText(img, "Green light:You can now proceed ahead safely", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)


            elif class_names[cls] == "yellow-light":  # Check if object is a yellow signal
                yellow_detected = True
                cv2.putText(img, "slow down the car!Zebra Crossing ahead", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            elif class_names[cls] == "zebra":  # Check if object is a yellow signal
                zebra_detected = True
                cv2.putText(img, "slow down the car!Zebra Crossing ahead", (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)





    out.write(img)
    cv2.imshow('img', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()