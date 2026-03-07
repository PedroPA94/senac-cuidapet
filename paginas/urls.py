from django.urls import path
from . import views

urlpatterns = [
    # Páginas gerais
    path("", views.index, name="index"),
    path('login/', views.login_view, name='login'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('home/', views.home, name='home'),
    
    # Cadastro Tutor
    path('tutor/register/', views.TutorCreateView.as_view(), name='tutor_create'),

    # Cadastro e Perfil Cuidador
    path('cuidador/register/', views.CuidadorCreateView.as_view(), name='cuidador_create'),
        
    # Agendamentos
    path('agendamentos/novo/<int:cuidador_id>/', views.AgendamentoCreateView.as_view(), name='agendamento_create'),
    path('agendamento/', views.agendamento, name='agendamento'),  # backward compatibility
    
    # Avaliações
    path('avaliacoes/<int:agendamento_id>/', views.AvaliacaoCreateView.as_view(), name='avaliacao_create'),
]
