from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages


def bem_vindo(request):
    return render(request, 'usuarios/bem_vindo.html')

def cadastrar_usuario(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        login = request.POST.get('login')
        senha = request.POST.get('senha')
        confirmar = request.POST.get('confirmar')

        if senha != confirmar:
            messages.error(request, "As senhas não coincidem.")
            return redirect('cadastro')

        if User.objects.filter(login=login).exists():
            messages.error(request, "Este login já existe.")
            return redirect('cadastro')

        user = User.objects.create_user(login=login, password=senha, first_name=nome)
        user.save()
        messages.success(request, "Conta criada com sucesso!")
        return redirect('login')

    return render(request, 'usuarios/cadastro.html')

def login_usuario(request):
    if request.method == 'POST':
        login = request.POST.get('login')
        senha = request.POST.get('senha')
        user = authenticate(request, login=login, password=senha)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Login ou senha inválidos.")
            return redirect('login')

    return render(request, 'usuarios/login.html')

def logout_usuario(request):
    logout(request)
    return redirect('bem_vindo')

