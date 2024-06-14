from django.urls import path

from fluxo.views import index, ad_despesa, ad_receita, lancamentos, ed_despesa, ed_receita


app_name = 'fluxo'

urlpatterns = [
    path('', index, name='index'),
    path('despesa/', ad_despesa, name='ad_despesa'),
    path('receita/', ad_receita, name='ad_receita'),
    path('lancamentos/', lancamentos, name='lancamentos'),
    path('despesa/edit/<int:despesa_id>', ed_despesa, name='ed_despesa'),
    path('receita/edit/<int:receita_id>', ed_receita, name='ed_receita'),
]