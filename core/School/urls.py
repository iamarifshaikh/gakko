from django.urls import path
from .views import *

urlpatterns = [
    path('Registration/',SchoolRegistration.as_view()),
    path('Approve/',ApproveSchool.as_view()),
    path('Delete/',DeleteSchool.as_view()),
    path('login/',LoginSchool.as_view()),
]