from mongoengine import fields, Document
from django.db import models
from School.models import School
from Teacher.models import Teacher
from mongoengine import CASCADE

# Create your models here.
class ClassStandard(models.TextChoices):
    NURSERY = 'Nursery', 'Nursery'
    JR_KG = 'Jr_KG', 'Junior KG'
    SR_KG = 'Sr_KG', 'Senior KG'
    FIRST = 'First', 'First'
    SECOND = 'Second', 'Second'
    THIRD = 'Third', 'Third'
    FOURTH = 'Fourth', 'Fourth'
    FIFTH = 'Fifth', 'Fifth'
    SIXTH = 'Sixth', 'Sixth'
    SEVENTH = 'Seventh', 'Eigth'
    EIGHTH = 'Eighth', 'Eighth'
    NINTH = 'Ninth', 'Ninth'
    TENTH = 'Tenth', 'Tenth'

class ClassDivision(models.TextChoices):
    A = 'A', 'A'
    B = 'B', 'B'
    C = 'C', 'C'
    D = 'D', 'D'
    E = 'E', 'E'

class Class(Document):
    class_id = models.AutoField(primary_key=True)
    class_std = models.CharField(max_length=10, choices=ClassStandard.choices)
    class_division = models.CharField(max_length=1, choices=ClassDivision.choices)
    class_teacher_id = fields.ReferenceField(Teacher,reverse_delete_rule=CASCADE) 
    school_id = fields.ReferenceField(School, reverse_delete_rule=CASCADE)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('class_std', 'class_division', 'school')

    def __str__(self):
        return f"{self.class_std} - {self.class_division} ({self.school_id.school_name})"
