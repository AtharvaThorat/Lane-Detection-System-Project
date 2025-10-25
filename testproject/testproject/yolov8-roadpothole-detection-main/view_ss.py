import cv2
import base64
import psycopg2
import numpy as np
from tkinter import simpledialog

def view_screenshots():
    try:
        # Connect to PostgreSQL database
        conn = psycopg2.connect(
            host="localhost",
            user="postgres",
            password="root",
            database="pothole"
        )

        # Create a cursor object to interact with the database
        cursor = conn.cursor()

        # Execute SQL query to retrieve image data and screenshot paths
        cursor.execute("SELECT id, image_data FROM images")
        records = cursor.fetchall()

        # Prompt the user to enter the number of images to display
        num_images = simpledialog.askinteger("Enter number of images", "Enter the number of images to display:")

        if num_images is not None:
            # Limit the number of records to the user input
            records = records[:num_images]

            # Iterate through the records and display images
            for record in records:
                id, image_data = record

                # Decode base64 and convert image data to OpenCV image
                img_data = base64.b64decode(image_data)
                nparr = np.frombuffer(img_data, np.uint8)
                img_cv2 = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

                # Display the image in a window
                cv2.imshow(f"Screenshot {id}", img_cv2)
                cv2.waitKey(0)  # Wait for any key press to proceed to the next image

        # Close the database connection
        conn.close()

    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Call the function to view screenshots
view_screenshots()
