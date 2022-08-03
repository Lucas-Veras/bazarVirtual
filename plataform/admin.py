from django.contrib import admin
from .models import Usuario, Produto, Evento, Reserva
# Register your models here.
admin.site.register(Usuario)
admin.site.register(Evento)
admin.site.register(Produto)
admin.site.register(Reserva)