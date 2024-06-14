from django.contrib import admin
from .models import FornecedorCliente

@admin.register(FornecedorCliente)
class FornecedorClienteAdmin(admin.ModelAdmin):
    pass
