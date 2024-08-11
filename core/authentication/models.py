import bcrypt
from mongoengine import Document, StringField, BooleanField, DateTimeField, FileField , ObjectIdField
from datetime import datetime
from django.conf import settings
from django.core.mail import send_mail
import random
from .utils import send_email

class Superadmin(Document):
    username = StringField(required=True)
    password = StringField(required=True)
    email = StringField(required=True)
    role = StringField()

    def set_password(self,req_password):
        salt = bcrypt.gensalt()
        self.password = bcrypt.hashpw(req_password.encode('utf-8'),salt).decode('utf-8')

    def check_password(self,raw_password):
        return bcrypt.checkpw(req_password.encode('utf-8'), self.password.encode('utf-8'))

class Administrator(Document):
    username = StringField(required=True, unique=True)
    password = StringField(required=True)
    is_approved = BooleanField(default=False)
    approval_date = DateTimeField(null=True)  # Date of approval
    is_rejected = BooleanField(default=False)
    rejection_date = DateTimeField(null=True)  # Date of rejection
    school_name = StringField(required=True)
    school_address = StringField()
    contact_number = StringField(required=True)
    email_address = StringField(required=True,unique=True)
    school_type = StringField(required=True)
    school_license_pdf = FileField(required=False)  # Field to store school license PDF
    approved_By = StringField(null=True)
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
        
        self.save()

        send_email(self.username , self.email_address , self.unique_ID)


    def generate_administrator_id(self):
        username_part = self.username[:3].upper()
        school_name_part = self.school_name[:3].upper()
        school_address_part = self.school_address[:3].upper()

        random_number =str(random.randint(1000,9999))

        return f"{username_part}{school_name_part}{school_address_part}{random_number}"
        

    def reject(self):
        self.is_rejected = True
        self.is_approved = False
        self.rejection_date = datetime.utcnow()
        self.save()



class Teacher(Document):
    username = StringField(required=True, unique=True)
    password = StringField(required=True)
    email_address = StringField(required=True)
    role = StringField(default='Teacher')

    def set_password(self, req_password):
        salt = bcrypt.gensalt()
        self.password = bcrypt.hashpw(req_password.encode('utf-8'), salt).decode('utf-8')

    def check_password(self, raw_password):
        """Check if the provided password matches the stored hashed password."""
        return bcrypt.checkpw(raw_password.encode('utf-8'), self.password.encode('utf-8'))