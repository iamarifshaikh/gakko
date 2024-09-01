from django.urls import path
from .views import *

urlpatterns = [
    path('teacher-role/subject/', AddSubjectRole.as_view()),
    path('teacher-role/read', ReadRole.as_view()),
    path('teacher-role/update', UpdateRole.as_view()),
]
