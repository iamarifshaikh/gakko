from django.db import models
from mongoengine import Document , StringField , BooleanField , DateTimeField , FileField , IntField 
import bcrypt
import random
import string
from datetime import datetime
from authentication.utils import send_email
from django.core.mail import settings

class School(Document):
    school_id = StringField(null=True,required=False)
    school_name = StringField(required=True,null=False)
    school_license = FileField(required=False)
    school_email = StringField(null=False,required=True)
    school_number = IntField(null=False,required=True)
    created_at = DateTimeField(default=datetime.utcnow())
    approved_at = DateTimeField()
    principal_name = StringField(required=True)
    password = StringField(null=True)
    verified = BooleanField(default=False)

    def approve(self):
        self.verified = True
        self.approved_at = datetime.utcnow()
        password = self.generate_random_password()
        self.set_password(password)
        self.school_id = str(self.id)[-4:]

        self.save()

        send_email(self.school_name,self.school_email,self.school_id,password)

    def set_password(self, req_password):
        salt = bcrypt.gensalt()
        self.password = bcrypt.hashpw(req_password.encode('utf-8'), salt).decode('utf-8')

    def check_password(self, raw_password):
        """Check if the provided password matches the stored hashed password."""
        return bcrypt.checkpw(raw_password.encode('utf-8'), self.password.encode('utf-8'))

    def generate_random_password(self,length=8):
        characters = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(characters) for i in range(length))