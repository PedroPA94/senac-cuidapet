# app: cuidadores/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Cuidador
import re

User = get_user_model()

class UserForm(UserCreationForm):
    """
    Form de criação de usuário com email + password1/password2.
    Se você usa o email como username, pode ajustar o User model ou sobrescrever save().
    """
    email = forms.EmailField(
        label="E-mail",
        required=True,
        widget=forms.EmailInput(attrs={
            "placeholder": "seu@email.com",
            "class": "input-text"
        })
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("email",)  # password1/password2 vêm do UserCreationForm
        # Se seu User ainda exige username, adicione "username" aqui ou no Model.

    def save(self, commit=True):
        user = super().save(commit=False)
        # Se seu User tem username obrigatório e você quer usar o email como username:
        if hasattr(user, "username") and not user.username:
            user.username = self.cleaned_data["email"]
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class CuidadorForm(forms.ModelForm):
    class Meta:
        model = Cuidador
        fields = [
            "nome_completo",
            "cpf",
            "celular",
            "uf",
            "cidade",
            "sobre_mim",
            "servico_prestado",
            "dias_disponiveis",
        ]
        widgets = {
            "nome_completo": forms.TextInput(attrs={"placeholder": "João da Silva", "required": True}),
            "cpf": forms.TextInput(attrs={"placeholder": "000.000.000-00", "required": True}),
            "celular": forms.TextInput(attrs={"placeholder": "(00) 00000-0000", "required": True}),
            "uf": forms.TextInput(attrs={"placeholder": "SP", "maxlength": 2, "required": True}),
            "cidade": forms.TextInput(attrs={"placeholder": "São Paulo", "required": True}),
            "sobre_mim": forms.Textarea(attrs={"placeholder": "...", "rows": 4}),
            "servico_prestado": forms.Select(),
            "dias_disponiveis": forms.TextInput(attrs={"placeholder": "Ex.: Segunda-feira a Quinta-feira"}),
        }
        help_texts = {
            "dias_disponiveis": "Ex.: Segunda-feira a Quinta-feira",
        }

    # ----- Validações específicas do Brasil -----
    def clean_cpf(self):
        cpf = self.cleaned_data["cpf"].strip()
        # aceita com ou sem máscara; aqui só exigimos o formato mascarado do layout
        pattern = r"^\d{3}\.\d{3}\.\d{3}-\d{2}$"
        if not re.match(pattern, cpf):
            raise forms.ValidationError("Informe o CPF no formato 000.000.000-00.")
        return cpf

    def clean_celular(self):
        celular = self.cleaned_data["celular"].strip()
        # Aceita (00) 00000-0000 ou (00) 0000-0000
        pattern = r"^\(\d{2}\)\s?\d{4,5}-\d{4}$"
        if not re.match(pattern, celular):
            raise forms.ValidationError("Informe o celular no formato (00) 00000-0000.")
        return celular

    def clean_uf(self):
        uf = self.cleaned_data["uf"].strip().upper()
        if len(uf) != 2:
            raise forms.ValidationError("UF deve conter 2 letras, ex.: SP.")
        return uf