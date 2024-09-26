from django.urls import path
from .views import *

urlpatterns = [
    path('SelectClass/',DefineClasses.as_view()),
    path('update-standards-format/',UpdateStandardsView.as_view())
] 