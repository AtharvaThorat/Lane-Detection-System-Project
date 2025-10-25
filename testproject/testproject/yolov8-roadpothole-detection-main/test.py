import cv2
import numpy as np
from ultralytics import YOLO
import base64
import psycopg2


# Function to run pothole detection
def run_pothole_detection(video_path):
    try:
        # Load YOLO model
        model = YOLO("best.pt")
        class_names = model.names

        # Open the video file
        cap = cv2.VideoCapture(video_path)

        # Connect to PostgreSQL database
        conn = psycopg2.connect(
            host="localhost",
            user="postgres",
            password="root",
            database="pothole"
        )

        # Create a cursor object to interact with the database
        cursor = conn.cursor()

        # Create the 'images' table if not exists
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS images (
                id SERIAL PRIMARY KEY,
                image_data BYTEA,
                screenshot_path TEXT
            )
        ''')

        count = 0
        frame_skip = 10  # Process every 100th frame 
        screenshot_count = 0
        pothole_detected = False  

        while True:
            # Jump to the next frame to be processed
            cap.set(cv2.CAP_PROP_POS_FRAMES, count)
            ret, img = cap.read()
            if not ret:
                break

            img = cv2.resize(img, (1020, 500))
            h, w, _ = img.shape
            results = model.predict(img)

            for r in results:
                boxes = r.boxes  # Boxes object for bbox outputs
                masks = r.masks  # Masks object for segment masks outputs

                if masks is not None:
                    masks = masks.data.cpu()
                    for seg, box in zip(masks.data.cpu().numpy(), boxes):
                        seg = cv2.resize(seg, (w, h))
                        contours, _ = cv2.findContours((seg).astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                        for contour in contours:
                            d = int(box.cls)
                            c = class_names[d]
                            x, y, x1, y1 = cv2.boundingRect(contour)
                            cv2.polylines(img, [contour], True, color=(0, 0, 255), thickness=2)

                            # Check if the detected object is a pothole
                            if c == 'road_potholes' and count % 1 == 0:  # Change this to the class name of potholes in your dataset
                                pothole_detected = True
                                cv2.putText(img, "Pothole Detected...Please Slow Down Vehicle", (50, 50),cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
                                # Show the frame with detected pothole
                                cv2.imshow('Pothole Detected', img)
                                cv2.waitKey(1)  # Wait for a short time to display the frame

            # Save every 50th frame in the database if a pothole is detected
            if count % 50 == 0 and pothole_detected:
                                # Convert image to base64 for storage in the database
                _, img_buffer = cv2.imencode('.png', img)
                img_base64 = base64.b64encode(img_buffer).decode('utf-8')

                # Store image data and screenshot path in the database
                screenshot_path = f"screenshot_{screenshot_count}.png"
                cursor.execute('''INSERT INTO images (image_data, screenshot_path) VALUES (%s, %s)''',
                               (img_base64, screenshot_path))
                conn.commit()
                print(f"Image stored in database with screenshot path: {screenshot_path}")
                screenshot_count += 1

            # Increment frame count
            count += frame_skip

        # Display message if no potholes are detected
        if not pothole_detected:
            print("No potholes detected in the input video.")

        # Close the database connection
        conn.close()

        # Release the video capture object
        cap.release()

        # Destroy all OpenCV windows
        cv2.destroyAllWindows()

    except Exception as e:
        print(f"An error occurred during pothole detection: {str(e)}")

# Function to run combined detection
def run_combined_detection():
    pothole_video_path = r"C:\Users\ATHARVA\Desktop\testproject\testproject\testproject\yolov8-roadpothole-detection-main\ALL_VIDEOS\p.mp4"

    # Run pothole detection
    run_pothole_detection(pothole_video_path)

if __name__ == "__main__":
    run_combined_detection()
