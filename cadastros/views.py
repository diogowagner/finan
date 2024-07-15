from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import Http404
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required

@login_required
def usuario(request):
    register_form_data = request.session.get('register_form_data', None)
    form = RegisterForm(register_form_data)

    context = {
        'form': form,
    }

    return render(request, 'usuario.html', context)

@login_required
def cria_usuario(request):
    if not request.POST:
        raise Http404()

    POST = request.POST
    request.session['register_form_data'] = POST
    form = RegisterForm(POST)

    if form.is_valid():
        form.save()
        messages.success(request, 'Seu usuário foi criado, por favor faça login.')

        del(request.session['register_form_data'])

    return redirect('cadastro:usuario')