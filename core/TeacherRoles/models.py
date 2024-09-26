from mongoengine import  StringField, fields
from Teacher.models import Teacher
from Base.models import TimestampedDocument
from School.models import School
from mongoengine import CASCADE

class Roles:
    classTeacher = 'class'
    subjectTeacher = 'subject'

    CHOICES = [
        (classTeacher, "class"),
        (subjectTeacher, "subject")
    ]

class TeacherRoles(TimestampedDocument):
    role_id = StringField(null=True,required=False)
    teacher_id = fields.ReferenceField(Teacher, reverse_delete_rule=CASCADE)
    role_type = StringField(choices=Roles.CHOICES)
    school_id = fields.ReferenceField(School, reverse_delete_rule=CASCADE)
    subject_name = StringField(null=True,required=False)
    class_id = StringField(null=True,required=False) # Later chnage it to class Reference

    

   