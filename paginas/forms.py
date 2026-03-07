from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Usuario, Cuidador, Pet, Agendamento, Avaliacao, Servico

User = get_user_model()


class TutorForm(UserCreationForm):
    first_name = forms.CharField(
        label="Nome",
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            "placeholder": "João da Silva"
        })
    )
    
    email = forms.EmailField(
        label="E-mail",
        required=True,
        widget=forms.EmailInput(attrs={
            "placeholder": "seu@email.com"
        })
    )
    
    telefone = forms.CharField(
        label="Celular",
        max_length=11,
        required=True,
        widget=forms.TextInput(attrs={
            "placeholder": "(00) 00000-0000"
        })
    )

    class Meta:
        model = Usuario
        fields = ("first_name", "email", "telefone", "password1", "password2")

    def clean_email(self):
        """Validar se o email já está registrado"""
        email = self.cleaned_data.get('email')
        if email and Usuario.objects.filter(username=email).exists():
            raise forms.ValidationError(
                "Este email já está registrado. Use outro email ou faça login."
            )
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data["email"]
        user.email = self.cleaned_data["email"]
        user.tipo_usuario = "TUTOR"
        if commit:
            user.save()
        return user


class PetFormTutor(forms.ModelForm):
    
    class Meta:
        model = Pet
        fields = ["nome", "especie", "raca", "data_nascimento"]
        labels = {
            "especie": "Espécie",
            "raca": "Raça",
            "data_nascimento": "Data de nascimento"
        }
        widgets = {
            "nome": forms.TextInput(attrs={
                "placeholder": "Ex: Mel, Thor"
            }),
            "especie": forms.Select(),
            "raca": forms.TextInput(attrs={
                "placeholder": "Ex: Golden, Persa, SRD"
            }),
            "data_nascimento": forms.DateInput(attrs={
                "type": "date"
            }),
        }
    
    def __init__(self, *args, required=False, **kwargs):
        super().__init__(*args, **kwargs)
        # Todos os campos são opcionais
        for field in self.fields:
            self.fields[field].required = False


class CuidadorRegistroForm(UserCreationForm):
    first_name = forms.CharField(
        label="Nome Completo",
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            "placeholder": "João da Silva"
        })
    )
    
    email = forms.EmailField(
        label="E-mail",
        required=True,
        widget=forms.EmailInput(attrs={
            "placeholder": "seu@email.com"
        })
    )
    
    telefone = forms.CharField(
        label="Celular",
        max_length=11,
        required=True,
        widget=forms.TextInput(attrs={
            "placeholder": "(00) 00000-0000"
        })
    )

    class Meta:
        model = Usuario
        fields = ("first_name", "email", "telefone", "password1", "password2")

    def clean_email(self):
        """Validar se o email já está registrado"""
        email = self.cleaned_data.get('email')
        if email and Usuario.objects.filter(username=email).exists():
            raise forms.ValidationError(
                "Este email já está registrado. Use outro email ou faça login."
            )
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data["email"]
        user.email = self.cleaned_data["email"]
        user.tipo_usuario = "CUIDADOR"
        if commit:
            user.save()
        return user


class CuidadorForm(forms.ModelForm):
   
    servicos = forms.ModelMultipleChoiceField(
        queryset=Servico.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={
        "class": "checkbox-servicos"
        }),
        label="Serviços que você oferece",
        required=False
    )

    class Meta:
        model = Cuidador
        fields = ["uf", "cidade", "descricao", "valor_diaria", "foto", "servicos"]
        labels = {
            "uf": "UF",
            "descricao": "Descrição",
            "valor_diaria": "Valor diária",
            "foto": "Foto de Perfil"
        }
        widgets = {
            "uf": forms.Select(),
            "cidade": forms.TextInput(attrs={
                "placeholder": "São Paulo"
            }),
            "descricao": forms.Textarea(attrs={
                "placeholder": "Conte sobre sua experiência...",
                "rows": 4
            }),
            "valor_diaria": forms.NumberInput(attrs={
                "placeholder": "100.00",
                "step": "0.01"
            }),
            "foto": forms.FileInput(attrs={
                "accept": "image/*"
            }),
        }


class AgendamentoForm(forms.ModelForm):
    
    class Meta:
        model = Agendamento
        fields = ["pet", "forma_pagamento", "data_inicio", "data_fim"]
        widgets = {
            "pet": forms.Select(),
            "forma_pagamento": forms.Select(),
            "data_inicio": forms.DateTimeInput(attrs={
                "type": "datetime-local"
            }),
            "data_fim": forms.DateTimeInput(attrs={
                "type": "datetime-local"
            }),
        }
    
    def __init__(self, *args, user=None, cuidador=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields["pet"].queryset = Pet.objects.filter(usuario=user)


class AvaliacaoForm(forms.ModelForm):
    
    class Meta:
        model = Avaliacao
        fields = ["nota", "comentario"]
        widgets = {
            "nota": forms.RadioSelect(choices=[(i, f"{i} ★") for i in range(1, 6)]),
            "comentario": forms.Textarea(attrs={
                "placeholder": "Compartilhe sua experiência...",
                "rows": 4
            }),
        }