from django.http import HttpResponse
from django.shortcuts import render
# from .models import

# Create your views here.

def index(request):
    return render(request, 'index.html')

def record(request):
    return render(request, 'record.html')

def result(request):
    return render(request, 'result.html')