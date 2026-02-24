from django.shortcuts import render

# polls/views.py
from django.http import HttpResponse

def index(request):
    # message simple pour tester
    return HttpResponse("Hello, world. You're at the polls index.")
