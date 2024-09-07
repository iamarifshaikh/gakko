from django.http import HttpResponse

def welcome_view(request):
    return HttpResponse("Welcome to the Django app!")
