from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("tatu")

def cadastro(request):
    return render(request, 'cadastro.html')

def home(request):
    return render(request, 'home.html')

def cuidador(request):
    return render(request, 'cuidador.html')

