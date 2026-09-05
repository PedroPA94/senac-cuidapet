from django.urls import path
from . import views

urlpatterns = [
    # Páginas gerais
    path("", views.home, name="home"),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('home/', views.home, name='home'),
    
    # Cadastro Tutor
    path('tutor/register/', views.TutorCreateView.as_view(), name='tutor_create'),

    # Cadastro Cuidador
    path('cuidador/register/', views.CuidadorCreateView.as_view(), name='cuidador_create'),
        
    # Agendamentos
    path('agendamentos/', views.AgendamentoListView.as_view(), name='agendamento_list'),
    path('agendamentos/novo/<int:cuidador_id>/', views.AgendamentoCreateView.as_view(), name='agendamento_create'),
    path('cuidador/solicitacoes/', views.CuidadorSolicitacoesView.as_view(), name='cuidador_solicitacoes'),
    path('cuidador/solicitacoes/<int:pk>/', views.CuidadorSolicitacaoDetailView.as_view(), name='cuidador_solicitacao_detail'),
    path('cuidador/solicitacoes/<int:pk>/<str:acao>/', views.CuidadorSolicitacaoStatusView.as_view(), name='cuidador_solicitacao_status'),
    
    # Avaliações
    path('avaliacoes/<int:agendamento_id>/', views.AvaliacaoCreateView.as_view(), name='avaliacao_create'),
]
