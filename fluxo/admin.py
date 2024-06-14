from django.contrib import admin
from .models import Lancamento, Item

@admin.register(Lancamento)
class LancamentoAdmin(admin.ModelAdmin):
    pass

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    pass