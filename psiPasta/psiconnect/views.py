from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as login_django

def cadastro(request):
    if request.method == "GET":
        return render(request, 'cadastro.html')
    else:
        username = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        user = User.objects.filter(username=username).first()

        if user:
            return HttpResponse('Já existe usuário com esse nome.')

        user = User.objects.create_user(username=username, email=email, password=senha)
        user.save()

        return HttpResponse('Usuário cadastrado com sucesso.')


def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    else:
        username = request.POST.get('username')
        senha = request.POST.get('senha')

        user = authenticate(username=username, password=senha)

        if user:
            login_django(request, user)

            return redirect('inicio')
        else:
            return HttpResponse('Usuário ou senha inválidos.')


def inicio(request):
    if request.user.is_authenticated:
        return render(request, 'inicio.html')
    return HttpResponse('Você precisa estar logado para acessar esta página.')

