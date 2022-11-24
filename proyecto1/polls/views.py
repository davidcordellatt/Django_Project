from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("11:11 am")
