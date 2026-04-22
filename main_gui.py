# Started in Week 2:
import tkinter as tk
from tkinter import messagebox, simpledialog
from database import verify_user_credentials, add_student, get_student_info, insert_attendance_record, is_attendance_marked_today
from face_capture import capture_face
from recognition import recognize_face, validate_face_quality 
from email_notifier import send_email
from admin_dashboard import AdminDashboard
import os
import shutil
import cv2
import datetime

class FaceBlinkAttendanceApp:
    def __init__(self, root):
        self.root = root    
        self.root.title("Face Blink Attendance System")
        self.root.geometry("400x350")

        # Username
        tk.Label(root, text="Username").pack(pady=5)
        self.username_entry = tk.Entry(root)
        self.username_entry.pack()

        # Password
        tk.Label(root, text="Password").pack(pady=5)
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.pack()

        # Buttons
        tk.Button(root, text="Login", command=self.login).pack(pady=5)
        tk.Button(root, text="Student Register", command=self.open_registration).pack(pady=5)
        tk.Button(root, text="View Attendance Records", command=self.open_admin_dashboard).pack(pady=5) 

        # Create known_faces directory if it doesn't exist
        self.face_dir = "known_faces"
        os.makedirs(self.face_dir, exist_ok=True)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter username and password")
            return
        
        if verify_user_credentials(username, password):
            messagebox.showinfo("Success", f"Welcome {username}!")
            self.attendance_loop()  # Take attendance
        else:
            messagebox.showerror("Error", "Invalid username or password")

    # Open Admin Dashboard directly (no login required for viewing records)
    def open_admin_dashboard(self):
        admin_window = tk.Toplevel(self.root)
        AdminDashboard(admin_window)

    # Student registration
    def open_registration(self):
        reg_window = tk.Toplevel(self.root)
        reg_window.title("Student Registration")
        reg_window.geometry("400x500")
        reg_window.transient(self.root)
        reg_window.grab_set()
        
        labels = ["Roll No", "Name", "Email", "Phone", "Department"]
        entries = []
        
        for label in labels:
            tk.Label(reg_window, text=label).pack()
            entry = tk.Entry(reg_window)
            entry.pack()
            entries.append(entry)

        def register_student():
            roll, name, email, phone, dept = [e.get() for e in entries]
            
            if not all([roll, name, email, phone, dept]):
                messagebox.showerror("Error", "Please fill all fields")
                return
            
            messagebox.showinfo("Info", "Camera will open.\nFirst blink, then press 'c' to capture.")
            img_path = capture_face(filename_prefix=roll)
            
            if img_path:
                if not validate_face_quality(img_path):
                    messagebox.showerror("Error", "No clear face detected. Please register again with better lighting and position.")
                    return
                
                dest_path = os.path.join(self.face_dir, f"{roll}.jpg")
                shutil.copy(img_path, dest_path)
                add_student(name, email, phone, dept, roll)
                messagebox.showinfo("Success", f"Student {name} registered successfully!")
                reg_window.destroy()
            else:
                messagebox.showerror("Error", "Registration cancelled - no photo captured")

        tk.Button(reg_window, text="Register Student", command=register_student).pack(pady=10)

    # Attendance marking loop
    def attendance_loop(self):
        while True:
            rollno = simpledialog.askstring("Student Roll No", 
                                            "Enter Roll Number (Cancel to stop):", 
                                            parent=self.root)
            if not rollno:
                break

            student_info = get_student_info(rollno)
            if not student_info:
                messagebox.showerror("Error", f"Student with roll number {rollno} is not registered. Please register first.")
                continue

            if is_attendance_marked_today(rollno):
                messagebox.showinfo("Info", f"Attendance already marked for roll no {rollno} today.")
                continue

            img_path = capture_face(filename_prefix=rollno)
            if not img_path:
                messagebox.showerror("Error", "Face capture cancelled or failed.")
                continue

            matched = recognize_face(img_path, rollno)

            if matched:
                messagebox.showinfo("Match Confirmed", 
                                   f"Face verified for roll no {rollno}. Attendance marked.")
                insert_attendance_record(rollno, status='Present')
                
                student_email = student_info[3]
                if student_email:
                    try:
                        send_email(
                            to_email=student_email,
                            subject="Attendance Marked - SmartAttend",
                            body=f"Dear Student,\n\nYour attendance has been successfully marked for Roll No: {rollno}.\n\nDate: {datetime.datetime.now().strftime('%Y-%m-%d')}\nTime: {datetime.datetime.now().strftime('%H:%M:%S')}\n\nThank you.\n\n- SmartAttend System"
                        )
                        print(f"Email sent to {student_email}")
                    except Exception as e:
                        print(f"Failed to send email: {e}")
                else:
                    print("No email address found for this student")
            else:
                messagebox.showerror("Mismatch", f"Face and roll number {rollno} do not match. Attendance not marked.")

if __name__ == "__main__":
    root = tk.Tk()
    app = FaceBlinkAttendanceApp(root)
    root.mainloop()