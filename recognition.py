import cv2
import numpy as np
from insightface.app import FaceAnalysis
import os

# Initialize once
app = FaceAnalysis(name='buffalo_l')  # ArcFace model with retinaface detector
app.prepare(ctx_id=0, det_size=(640, 640))

def recognize_face(captured_img_path, rollno, threshold=0.4):
    """
    Recognize face by comparing with stored image for given roll number.
    Returns True if match found, False otherwise.
    Prints similarity score for debugging.
    """
    try:
        # Path to stored face image
        ref_path = f"known_faces/{rollno}.jpg"
        
        # Check if reference image exists
        if not os.path.exists(ref_path):
            print(f"Error: Reference image not found for roll no {rollno}")
            return False
        
        # Load images
        ref_img = cv2.imread(ref_path)
        test_img = cv2.imread(captured_img_path)

        if ref_img is None:
            print(f"Error: Could not load reference image from {ref_path}")
            return False
            
        if test_img is None:
            print(f"Error: Could not load captured image from {captured_img_path}")
            return False

        # Get face embeddings
        ref_faces = app.get(ref_img)
        test_faces = app.get(test_img)

        if not ref_faces:
            print("No face detected in reference image. Please re-register student.")
            return False
            
        if not test_faces:
            print("No face detected in captured image. Please try again with better lighting.")
            return False

        # Get embeddings (first face only)
        ref_emb = ref_faces[0].embedding
        test_emb = test_faces[0].embedding

        # Cosine similarity
        similarity = np.dot(ref_emb, test_emb) / (np.linalg.norm(ref_emb) * np.linalg.norm(test_emb))
        print(f"Similarity score for roll no {rollno}: {similarity:.4f} (Threshold: {threshold})")

        # Return True if similarity meets threshold
        return similarity > threshold
        
    except Exception as e:
        print(f"InsightFace recognition error: {e}")
        return False

# NEW FUNCTION FOR WEEK 7: Validate face before registration
def validate_face_quality(image_path):
    """
    Check if a face is clearly visible in the image.
    Returns True if face detected, False otherwise.
    """
    try:
        img = cv2.imread(image_path)
        if img is None:
            return False
        
        faces = app.get(img)
        if not faces:
            return False
        
        # Check if face is large enough (optional)
        bbox = faces[0].bbox
        face_width = bbox[2] - bbox[0]
        face_height = bbox[3] - bbox[1]
        
        if face_width < 100 or face_height < 100:
            print(f"Face too small: {face_width}x{face_height}")
            return False
            
        return True
    except Exception as e:
        print(f"Face validation error: {e}")
        return False