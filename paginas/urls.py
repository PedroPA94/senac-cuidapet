from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('cadastro/', views.cadastro),
    path('home/', views.home),
    path('cuidador/', views.cuidador),
]
