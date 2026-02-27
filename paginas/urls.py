from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('login/', views.login, name='login'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('home/', views.home),
    path('cuidador/', views.cuidador, name='cuidador'),
    path('tutor/', views.tutor, name='tutor'),
]
