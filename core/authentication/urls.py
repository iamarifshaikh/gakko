from django.urls import path
from .views import *

urlpatterns = [
    path("Administrator/Register/",RegisterAdministrator.as_view()),
    path('Administrator/Approve/',ApproveAdministrator.as_view()),
    path('UnApprovedAdministrator/',getALLUnApprovedAdministrator.as_view()),
    path("Login/",LoginView.as_view()),
]