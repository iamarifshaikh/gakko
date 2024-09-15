from django.urls import path
from . import views

urlpatterns = [
    path('add', views.AddTeacher.as_view()),
    path('readone', views.ReadOneTeacher.as_view()),
    path('readall', views.ReadAllTeacher.as_view()),
    path('update', views.UpdateTeacher.as_view()),
    path('delete', views.DeleteTeacher.as_view())
]
