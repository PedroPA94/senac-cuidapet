from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, FormView, View, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.contrib import messages
from django.db import IntegrityError
from decimal import Decimal

from .models import Cuidador, Agendamento
from .forms import (
    TutorForm, 
    PetFormTutor,
    CuidadorRegistroForm, 
    CuidadorForm,  
    AgendamentoForm, 
    AvaliacaoForm
)


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f"Bem-vindo, {user.first_name}!")
            return redirect('home')
        else:
            messages.error(request, "Email ou senha inválidos. Tente novamente.")
    
    return render(request, 'login.html')


def cadastro(request):
    return render(request, 'cadastro.html')


def home(request):
    uf_filtro = request.GET.get('uf', '')
    cidade_filtro = request.GET.get('cidade', '')

    cuidadores = Cuidador.objects.all()
    
    if uf_filtro:
        cuidadores = cuidadores.filter(uf=uf_filtro)
    if cidade_filtro:
        cuidadores = cuidadores.filter(cidade__icontains=cidade_filtro)
    
    cuidadores = cuidadores.select_related('usuario').order_by('usuario__first_name')
    
    context = {
        'cuidadores': cuidadores,
        'uf_filtro': uf_filtro,
        'cidade_filtro': cidade_filtro,
        'ufs': Cuidador.UF.choices
    }
    
    return render(request, 'home.html', context)


class TutorCreateView(View):
    template_name = 'tutor_form.html'
    
    def get(self, request):
        tutor_form = TutorForm()
        pet_form = PetFormTutor()
        return render(request, self.template_name, {
            'tutor_form': tutor_form,
            'pet_form': pet_form
        })
    
    def post(self, request):
        tutor_form = TutorForm(request.POST)
        pet_form = PetFormTutor(request.POST, required=False)
        
        if not tutor_form.is_valid():
            # Formulário inválido, retornar com erros
            return render(request, self.template_name, {
                'tutor_form': tutor_form,
                'pet_form': pet_form
            })
        
        if request.POST.get('nome') and not pet_form.is_valid():
            return render(request, self.template_name, {
                'tutor_form': tutor_form,
                'pet_form': pet_form
            })
        
        try:
            user = tutor_form.save()
            
            if request.POST.get('nome'):
                pet = pet_form.save(commit=False)
                pet.usuario = user
                pet.save()
                messages.success(request, "Tutor e pet cadastrados com sucesso! Faça login para continuar.")
            else:
                messages.success(request, "Tutor cadastrado com sucesso! Faça login para continuar.")
            
            return redirect('login')
        except IntegrityError as e:
            tutor_form.add_error('email', "Erro ao salvar. Este email pode já estar registrado.")
            return render(request, self.template_name, {
                'tutor_form': tutor_form,
                'pet_form': pet_form
            })


class CuidadorCreateView(View):
    template_name = 'cuidador_form.html'
    
    def get(self, request):
        usuario_form = CuidadorRegistroForm()
        cuidador_form = CuidadorForm()
        return render(request, self.template_name, {
            'usuario_form': usuario_form,
            'cuidador_form': cuidador_form
        })
    
    def post(self, request):
        usuario_form = CuidadorRegistroForm(request.POST)
        cuidador_form = CuidadorForm(request.POST, request.FILES)
        
        usuario_valid = usuario_form.is_valid()
        cuidador_valid = cuidador_form.is_valid()
        
        if usuario_valid and cuidador_valid:
            try:
                user = usuario_form.save()
                
                cuidador = cuidador_form.save(commit=False)
                cuidador.usuario = user
                cuidador.save()
                cuidador_form.save_m2m()
                
                messages.success(request, "Cuidador cadastrado com sucesso! Faça login para continuar.")
                return redirect('login')
            except IntegrityError as e:
                usuario_form.add_error('email', "Erro ao salvar. Este email pode já estar registrado.")
                return render(request, self.template_name, {
                    'usuario_form': usuario_form,
                    'cuidador_form': cuidador_form
                })
            except Exception as e:
                messages.error(request, f"Erro ao salvar: {str(e)}")
        
        return render(request, self.template_name, {
            'usuario_form': usuario_form,
            'cuidador_form': cuidador_form
        })


class AgendamentoCreateView(LoginRequiredMixin, FormView):
    form_class = AgendamentoForm
    template_name = 'agendamento_form.html'
    success_url = reverse_lazy('agendamento_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        pet = form.cleaned_data['pet']
        cuidador_id = self.kwargs.get('cuidador_id')
        cuidador = get_object_or_404(Cuidador, id=cuidador_id)
        
        data_inicio = form.cleaned_data['data_inicio']
        data_fim = form.cleaned_data['data_fim']
        forma_pagamento = form.cleaned_data['forma_pagamento']

        # Calcular valor total (dias × valor_diaria)
        dias = (data_fim - data_inicio).days + 1
        if dias <= 0:
            dias = 1
        valor_total = Decimal(dias) * cuidador.valor_diaria

        agendamento = Agendamento.objects.create(
            usuario=self.request.user,
            cuidador=cuidador,
            pet=pet,
            forma_pagamento=forma_pagamento,
            data_inicio=data_inicio,
            data_fim=data_fim,
            valor_total=valor_total
        )

        messages.success(self.request, "Agendamento criado com sucesso!")
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cuidador_id = self.kwargs.get('cuidador_id')
        context['cuidador'] = get_object_or_404(Cuidador, id=cuidador_id)
        return context


class AgendamentoListView(LoginRequiredMixin, ListView):
    model = Agendamento
    template_name = 'agendamento_list.html'
    context_object_name = 'agendamentos'

    def get_queryset(self):
        return Agendamento.objects.filter(usuario=self.request.user).select_related('cuidador', 'pet').order_by('-data_criacao')


class AvaliacaoCreateView(LoginRequiredMixin, CreateView):
    form_class = AvaliacaoForm
    template_name = 'avaliacao_form.html'
    success_url = reverse_lazy('agendamento_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        agendamento_id = self.kwargs.get('agendamento_id')
        context['agendamento'] = get_object_or_404(Agendamento, id=agendamento_id)
        return context

    def form_valid(self, form):
        agendamento_id = self.kwargs.get('agendamento_id')
        agendamento = get_object_or_404(Agendamento, id=agendamento_id)
        
        if agendamento.usuario != self.request.user:
            messages.error(self.request, "Você não tem permissão para avaliar este agendamento.")
            return redirect('agendamento_list')

        form.instance.agendamento = agendamento
        messages.success(self.request, "Avaliação enviada com sucesso!")
        return super().form_valid(form)
