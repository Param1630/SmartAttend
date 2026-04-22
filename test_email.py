# test_email.py
from email_notifier import send_email

# Replace with your own email address for testing
test_email = "your_personal_email@gmail.com"

send_email(
    to_email=test_email,
    subject="Test Email - SmartAttend",
    body="This is a test email from your SmartAttend Attendance System.\n\nIf you received this, email notifications are working correctly!"
)

print("Email test completed!")