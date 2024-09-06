from django.urls import path
from .views import *

urlpatterns = [
    path('registration/',SchoolRegistration.as_view()),
    path('approve/',ApproveSchool.as_view()),
    path('delete/',DeleteSchool.as_view()),
    path('login/',LoginSchool.as_view()),
]
