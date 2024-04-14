from django.contrib import admin
from .models import Categoria, Conta, Empresa

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['categoria_pai'].widget.can_add_related = False
        form.base_fields['categoria_pai'].widget.can_change_related = False
        form.base_fields['categoria_pai'].widget.can_delete_related = False
        return form
    list_display = ['descricao','categoria_pai','ativo']
    list_filter = ['ativo', 'is_categoria_filha', 'classificacao']
    # list_editable = ['is_categoria_filha']
    exclude = ['slug']
    ordering = ['descricao']

    class Media:
        js = ('js/admin.js',)

@admin.register(Conta)
class AdminConta(admin.ModelAdmin):
    pass


@admin.register(Empresa)
class AdminEmpresa(admin.ModelAdmin):
    pass


