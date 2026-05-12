from django.contrib import admin
from .models import Procedure, Appointment

# Registrando os modelos para que apareçam no painel de administração
admin.site.register(Procedure)
admin.site.register(Appointment)