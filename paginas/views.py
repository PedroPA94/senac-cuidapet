from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, 'home.html')

def login(request):
    return render(request, 'login.html')

def cadastro(request):
    return render(request, 'cadastro.html')

def home(request):
    return render(request, 'home.html')

def cuidador(request):
    return render(request, 'cuidador.html')

def tutor(request):
    return render(request, 'tutor.html')

def agendamento(request):
    return render(request, 'agendamento.html')