from django.contrib import admin
from .models import Agendamento  # Importe o modelo que deseja registrar
from django.contrib import admin
  # Importe o modelo que deseja registrar
from .models import Usuario
# Registre o modelo Agendamento no painel de administração
admin.site.register(Agendamento)



# Registre o modelo CustomUser no painel de administração

admin.site.register(Usuario)
