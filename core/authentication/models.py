import bcrypt
from mongoengine import Document, StringField, BooleanField, DateTimeField, FileField , ObjectIdField
from datetime import datetime
from django.conf import settings
from django.core.mail import send_mail
import random
import string
from .utils import send_email , send_Teacher_email

class Superadmin(Document):
    username = StringField(required=True)
    password = StringField(required=True)
    email = StringField(required=True)
    role = StringField(default="Admin")

    def set_password(self,req_password):
        salt = bcrypt.gensalt()
        self.password = bcrypt.hashpw(req_password.encode('utf-8'),salt).decode('utf-8')

    def check_password(self,raw_password):
        return bcrypt.checkpw(req_password.encode('utf-8'), self.password.encode('utf-8'))

class Administrator(Document):
    password = StringField(null=True)
    is_approved = BooleanField(default=False)
    approval_date = DateTimeField(null=True)  # Date of approval
    is_rejected = BooleanField(default=False)
    rejection_date = DateTimeField(null=True)  # Date of rejection
    school_name = StringField(required=True)
    school_address = StringField(required=True)
    contact_number = StringField(required=True)
    email_address = StringField(required=True,unique=True)
    school_type = StringField(required=True)
    school_license_pdf = FileField(required=False,upload_to = "Administrator")  # Field to store school license PDF
    role = StringField(default='Administrator')
    unique_ID = StringField(null=True,unique=True)



    def set_password(self, req_password):
        salt = bcrypt.gensalt()
        self.password = bcrypt.hashpw(req_password.encode('utf-8'), salt).decode('utf-8')

    def check_password(self, raw_password):
        """Check if the provided password matches the stored hashed password."""
        return bcrypt.checkpw(raw_password.encode('utf-8'), self.password.encode('utf-8'))

    def approve(self):
        self.is_approved = True
        self.is_rejected = False
        self.approval_date = datetime.utcnow()
        self.unique_ID = self.generate_administrator_id()

        password = self.generate_random_password()

        self.set_password(password)
        
        self.save()

        send_email(self.school_name,self.email_address , self.unique_ID , password)

    def generate_random_password(self,length=8):
        characters = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(characters) for i in range(length))

    def generate_administrator_id(self):
        # username_part = self.username[:3].upper()
        school_name_part = self.school_name[:4].upper()
        school_address_part = self.school_address[:4].upper()

        random_number =str(random.randint(1000,9999))

        return f"{school_name_part}{school_address_part}{random_number}"
        

    def reject(self):
        self.is_rejected = True
        self.is_approved = False
        self.rejection_date = datetime.utcnow()
        self.save()


class Teacher(Document):
    Name = StringField(required=True, null=True)
    password = StringField(null=True)
    email_address = StringField(required=True, unique=True)
    unique_ID = StringField(unique=True)
    role = StringField(default='Teacher')
    classNo = StringField(required=True)

    def register(self):
        # Generate and set the random password
        password = self.generate_random_password()
        self.set_password(password)
        
        # Generate and set the unique ID
        self.unique_ID = self.generate_Teacher_id()

        # Save the Teacher instance
        self.save()

        # Send the registration email
        send_Teacher_email(self.Name, self.email_address, self.unique_ID, password)

    def generate_random_password(self, length=8):
        characters = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(characters) for i in range(length))

    def generate_Teacher_id(self):
        Name_part = self.Name[:3].upper()
        classNo_part = self.classNo.upper()  # Using self.classNo
        random_number = str(random.randint(1000, 9999))
        return f"{Name_part}{classNo_part}{random_number}"

    def set_password(self, req_password):
        salt = bcrypt.gensalt()
        self.password = bcrypt.hashpw(req_password.encode('utf-8'), salt).decode('utf-8')

    def check_password(self, raw_password):
        return bcrypt.checkpw(raw_password.encode('utf-8'), self.password.encode('utf-8'))