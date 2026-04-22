import tkinter as tk
from tkinter import ttk, messagebox
from database import connect_db
# from export_utils import export_attendance_to_excel, export_attendance_to_pdf  # Will add in Week 12
import datetime

class AdminDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Admin Dashboard - Attendance Records")
        self.root.geometry("900x500")

        # Updated columns to include Roll No
        self.tree = ttk.Treeview(root, columns=("ID", "Roll No", "Name", "Date", "Time", "Status"), show="headings")
        
        # Set column headings and widths
        self.tree.heading("ID", text="ID")
        self.tree.heading("Roll No", text="Roll No")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Date", text="Date")
        self.tree.heading("Time", text="Time")
        self.tree.heading("Status", text="Status")
        
        # Set column widths
        self.tree.column("ID", width=50)
        self.tree.column("Roll No", width=100)
        self.tree.column("Name", width=150)
        self.tree.column("Date", width=100)
        self.tree.column("Time", width=80)
        self.tree.column("Status", width=80)
        
        self.tree.pack(fill="both", expand=True)

        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Refresh", command=self.load_attendance).pack(side="left", padx=5)
        # Export buttons commented for Week 11 - will enable in Week 12
        # tk.Button(btn_frame, text="Export to Excel", command=self.export_excel).pack(side="left", padx=5)
        # tk.Button(btn_frame, text="Export to PDF", command=self.export_pdf).pack(side="left", padx=5)

        self.load_attendance()

    def load_attendance(self):
        # Clear existing rows
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        db = connect_db()
        cursor = db.cursor()
        # Updated query to include rollno
        cursor.execute("""
            SELECT a.attendance_id, s.rollno, s.name, a.date, a.time, a.status
            FROM attendance a
            JOIN students s ON a.student_id = s.student_id
            ORDER BY a.date DESC, a.time DESC
        """)
        for row in cursor.fetchall():
            self.tree.insert("", "end", values=row)
        db.close()

    # Export functions commented for Week 11
    # def export_excel(self):
    #     export_attendance_to_excel()
    #     messagebox.showinfo("Success", "Attendance exported to Excel.")
    #
    # def export_pdf(self):
    #     export_attendance_to_pdf()
    #     messagebox.showinfo("Success", "Attendance exported to PDF.")

if __name__ == "__main__":
    root = tk.Tk()
    app = AdminDashboard(root)
    root.mainloop()