
import mediapipe as mp
import cv2
import math

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Eye landmark indices for blink detection
LEFT_EYE = [362, 385, 387, 263, 373, 380]
RIGHT_EYE = [33, 160, 158, 133, 153, 144]

def euclidean_dist(pt1, pt2):
    return math.sqrt((pt1[0] - pt2[0])**2 + (pt1[1] - pt2[1])**2)

def get_eye_aspect_ratio(landmarks, eye_indices, image_w, image_h):
    points = [(int(landmarks[idx].x * image_w), int(landmarks[idx].y * image_h)) for idx in eye_indices]
    vertical = euclidean_dist(points[1], points[5])
    horizontal = euclidean_dist(points[0], points[3])
    return vertical / horizontal if horizontal else 0

def detect_blink(frame):
    h, w, _ = frame.shape
    results = face_mesh.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            left_ear = get_eye_aspect_ratio(face_landmarks.landmark, LEFT_EYE, w, h)
            right_ear = get_eye_aspect_ratio(face_landmarks.landmark, RIGHT_EYE, w, h)
            avg_ear = (left_ear + right_ear) / 2.0
            if avg_ear < 0.2:  # EAR threshold for blink
                return True
    return False
