# # from mongoengine import fields
# # from django.db import models
# # from School.models import School
# # from mongoengine import CASCADE

# # # Create your models here.
# # class ClassStandard(models.TextChoices):
# #     NURSERY = 'Nursery', 'Nursery'
# #     JR_KG = 'Jr_KG', 'Junior KG'
# #     SR_KG = 'Sr_KG', 'Senior KG'
# #     FIRST = 'First', 'First'
# #     SECOND = 'Second', 'Second'
# #     THIRD = 'Third', 'Third'
# #     FOURTH = 'Fourth', 'Fourth'
# #     FIFTH = 'Fifth', 'Fifth'
# #     SIXTH = 'Sixth', 'Sixth'
# #     SEVENTH = 'Seventh', 'Eigth'
# #     EIGHTH = 'Eighth', 'Eighth'
# #     NINTH = 'Ninth', 'Ninth'
# #     TENTH = 'Tenth', 'Tenth'

# # class ClassDivision(models.TextChoices):
# #     A = 'A', 'A'
# #     B = 'B', 'B'
# #     C = 'C', 'C'
# #     D = 'D', 'D'
# #     E = 'E', 'E'

# # class Class(models.Model):
# #     class_id = models.AutoField(primary_key=True)
# #     class_std = models.CharField(max_length=10, choices=ClassStandard.choices)
# #     class_division = models.CharField(max_length=1, choices=ClassDivision.choices)
# #     # To do by @Alfiya
# #     # class_teacher_id = fields.ReferenceField(Teacher,reverse_delete_rule=CASCADE) 
# #     school_id = fields.ReferenceField(School, reverse_delete_rule=CASCADE)

# #     updated_at = models.DateTimeField(auto_now=True)

# #     class Meta:
# #         unique_together = ('class_std', 'class_division')

# #     def __str__(self):
# #         return f"{self.class_std} - {self.class_division} ({self.school_id.school_name})" 


# from mongoengine import Document, fields, CASCADE
# from School.models import School

# class ClassStandard:
#     NURSERY = 'Nursery'
#     JR_KG = 'Jr_KG'
#     SR_KG = 'Sr_KG'
#     FIRST = 'First'
#     SECOND = 'Second'
#     THIRD = 'Third'
#     FOURTH = 'Fourth'
#     FIFTH = 'Fifth'
#     SIXTH = 'Sixth'
#     SEVENTH = 'Seventh'
#     EIGHTH = 'Eighth'
#     NINTH = 'Ninth'
#     TENTH = 'Tenth'

# class ClassDivision:
#     A = 'A'
#     B = 'B'
#     C = 'C'
#     D = 'D'
#     E = 'E'

# class Class(Document):
#     class_id = fields.IntField(primary_key=True)
#     class_std = fields.StringField(choices=[
#         (ClassStandard.NURSERY, 'Nursery'),
#         (ClassStandard.JR_KG, 'Junior KG'),
#         (ClassStandard.SR_KG, 'Senior KG'),
#         (ClassStandard.FIRST, 'First'),
#         (ClassStandard.SECOND, 'Second'),
#         (ClassStandard.THIRD, 'Third'),
#         (ClassStandard.FOURTH, 'Fourth'),
#         (ClassStandard.FIFTH, 'Fifth'),
#         (ClassStandard.SIXTH, 'Sixth'),
#         (ClassStandard.SEVENTH, 'Seventh'),
#         (ClassStandard.EIGHTH, 'Eighth'),
#         (ClassStandard.NINTH, 'Ninth'),
#         (ClassStandard.TENTH, 'Tenth')
#     ])
#     class_division = fields.StringField(choices=[
#         (ClassDivision.A, 'A'),
#         (ClassDivision.B, 'B'),
#         (ClassDivision.C, 'C'),
#         (ClassDivision.D, 'D'),
#         (ClassDivision.E, 'E')
#     ])
#     school_id = fields.ReferenceField(School, reverse_delete_rule=CASCADE)
#     # updated_at = fields.DateTimeField(auto_now=True)  # MongoEngine doesn't have auto_now=True; you'll need to manually handle updates

#     meta = {
#         'indexes': [
#             {
#                 'fields': ('class_std', 'class_division'),
#                 'unique': True
#             }
#         ]
#     }

#     def __str__(self):
#         return f"{self.class_std} - {self.class_division} ({self.school_id.school_name})" if self.school_id else f"{self.class_std} - {self.class_division}"

from mongoengine import Document, fields, CASCADE
from School.models import School
from datetime import datetime

class ClassStandard:
    NURSERY = 'Nursery'
    JR_KG = 'Jr_KG'
    SR_KG = 'Sr_KG'
    FIRST = 'First'
    SECOND = 'Second'
    THIRD = 'Third'
    FOURTH = 'Fourth'
    FIFTH = 'Fifth'
    SIXTH = 'Sixth'
    SEVENTH = 'Seventh'
    EIGHTH = 'Eighth'
    NINTH = 'Ninth'
    TENTH = 'Tenth'

class ClassDivision:
    A = 'A'
    B = 'B'
    C = 'C'
    D = 'D'
    E = 'E'

class Class(Document):
    # class_id = fields.IntField(primary_key=True)
    class_std = fields.StringField(choices=[
        (ClassStandard.NURSERY, 'Nursery'),
        (ClassStandard.JR_KG, 'Junior KG'),
        (ClassStandard.SR_KG, 'Senior KG'),
        (ClassStandard.FIRST, 'First'),
        (ClassStandard.SECOND, 'Second'),
        (ClassStandard.THIRD, 'Third'),
        (ClassStandard.FOURTH, 'Fourth'),
        (ClassStandard.FIFTH, 'Fifth'),
        (ClassStandard.SIXTH, 'Sixth'),
        (ClassStandard.SEVENTH, 'Seventh'),
        (ClassStandard.EIGHTH, 'Eighth'),
        (ClassStandard.NINTH, 'Ninth'),
        (ClassStandard.TENTH, 'Tenth')
    ])
    class_division = fields.StringField(choices=[
        (ClassDivision.A, 'A'),
        (ClassDivision.B, 'B'),
        (ClassDivision.C, 'C'),
        (ClassDivision.D, 'D'),
        (ClassDivision.E, 'E')
    ])
    school_id = fields.ReferenceField(School, reverse_delete_rule=CASCADE)
    updated_at = fields.DateTimeField(default=datetime.utcnow)  # Handle this manually

    meta = {
        'indexes': [
            {
                'fields': ('class_std', 'class_division'),
                'unique': True
            }
        ]
    }

    def save(self, *args, **kwargs):
        self.updated_at = datetime.utcnow()  # Update timestamp on save
        return super(Class, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.class_std} - {self.class_division} ({self.school_id.school_name})" if self.school_id else f"{self.class_std} - {self.class_division}"
