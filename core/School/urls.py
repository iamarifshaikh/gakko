from django.urls import path
from .views import *

urlpatterns = [
    path('registration/',SchoolRegistration.as_view()),
    path('approve/',ApproveSchool.as_view()),
    path('delete/<str:id>/',DeleteSchool.as_view()),
    path('update/<str:id>/',Updateschool.as_view()),
    path('verifiedSchool/',ReadVerifiedSchool.as_view()),
    path('unverifiedSchool/',ReadUnverifiedSchool.as_view())
]