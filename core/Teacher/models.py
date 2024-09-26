from mongoengine import StringField  , fields, IntField
from Base.models import TimestampedDocument
from mongoengine import CASCADE
from School.models import School

class Teacher(TimestampedDocument):
    teacher_id = StringField(null=True,required=False)
    teacher_name = StringField(required=True,null=False)
    teacher_email = StringField(null=False,required=True)
    teacher_number = IntField(null=False,required=True)
    school_id = fields.ReferenceField(School, reverse_delete_rule=CASCADE)