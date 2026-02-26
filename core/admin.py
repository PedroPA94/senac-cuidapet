from django.contrib import admin
from .models import *

admin.site.register(Usuario)
admin.site.register(Cuidador)
admin.site.register(Pet)
admin.site.register(Disponibilidade)
admin.site.register(Servico)
admin.site.register(Agendamento)
admin.site.register(Avaliacao)