from django.urls import path
from .views import *

urlpatterns = [
    path('subject', AddSubjectRole.as_view()),
    path('read', ReadRole.as_view()),
    path('update', UpdateRole.as_view()),
]
