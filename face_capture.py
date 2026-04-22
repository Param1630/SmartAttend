
import cv2
import os
import datetime
from blink_detection import detect_blink

def capture_face(filename_prefix="captured_face"):
    cap = cv2.VideoCapture(0)
    img_path = None
    blinked = False

    print("Press 'c' to capture after blinking. Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        if detect_blink(frame):
            blinked = True
            print("Blink detected! Now press 'c' to capture.")

        cv2.imshow("Capture Face (Blink First)", frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord('c') and blinked:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            img_path = f"{filename_prefix}_{timestamp}.jpg"
            cv2.imwrite(img_path, frame)
            print(f"Face captured and saved as {img_path}")
            break

        if key == ord('q'):
            print("Capture cancelled.")
            break

    cap.release()
    cv2.destroyAllWindows()
    return img_path
