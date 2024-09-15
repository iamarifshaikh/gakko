# from .models import *
import time
from django.core.mail import send_mail
from django.conf import settings

def send_email(username , recipient_list , unique_ID,password):
    print("In email send function")

    subject = "Congratulations! Your Registration is Successful"

    message = (
        f"Dear {username},  \n\n"
        f"Congratulations! Your registration as an Administrator has been successfully approved. "
        f"You can now access the various functionalities of our application.\n\n"
        f"Here is your unique Administrator ID: {unique_ID} and password: {password}\n\n"
        f"Please keep this ID safe as it will be required for logging into the system.\n\n"
        f"Thank you for joining us, and we look forward to your valuable contribution to our community.\n\n"
        f"Best Regards,\n"
        f"The Gakko Team"
    )
    from_email=settings.EMAIL_HOST_USER
    recipient_list = [recipient_list]
    send_mail(subject,message,from_email,recipient_list)