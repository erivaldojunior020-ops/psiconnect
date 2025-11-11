from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as login_django
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import CustomUser
from django.contrib.auth import get_user_model
User = get_user_model()


def cadastro_paciente(request):
    if request.method == "GET":
        return render(request, 'cadastro_paciente.html')
    else:
        username = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        # Verifica se já existe usuário com esse username
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Já existe um usuário com esse nome.')
            return render(request, 'cadastro_paciente.html')

        # Verifica se o e-mail já está sendo usado (opcional)
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Já existe um usuário com esse e-mail.')
            return render(request, 'cadastro_paciente.html')

        # Cria o novo usuário
        user = User.objects.create_user(username=username, email=email, password=senha)
        messages.success(request, 'Cadastro realizado com sucesso!')
        return redirect('/auth/login_paciente/')



def login_paciente(request):
    if request.method == "GET":
        return render(request, 'login_paciente.html')

    email = request.POST.get('email')
    senha = request.POST.get('senha')

    user = authenticate(request, email=email, password=senha)

    if user:
        if user.user_type == 'paciente':
            login_django(request, user)
            return redirect('inicio_paciente')
        else:
            messages.error(request, 'Apenas pacientes podem acessar esta área.')
    else:
        messages.error(request, 'Email ou senha inválidos.')

    return render(request, 'login_paciente.html')

def inicio_paciente(request):
    if request.user.is_authenticated:
        return render(request, 'inicio_paciente.html')
    messages.warning(request, 'Você precisa estar logado para acessar esta página.')
    return redirect('login_paciente')

def lista_psicologos(request):
    if request.user.is_authenticated:
        return render(request, 'lista_psicologos.html')
    return redirect('login_paciente')

def agendamento_paciente(request):
    return render(request, 'agendamento_paciente.html')
    
def sessoes_paciente(request):
    return render(request,'sessoes_paciente.html')



# --- LOGIN PROFESSOR (somente superusuário) ---
def login_professor(request):
    if request.method == "GET":
        return render(request, 'login_professor.html')

    email = request.POST.get('email')
    senha = request.POST.get('password')

    user = authenticate(request, username=email, password=senha)

    if user:
        if user.user_type == 'professor' and user.is_superuser:
            login_django(request, user)
            return redirect('cadastrar_aluno')
        else:
            messages.error(request, 'Apenas superusuários (professores) podem acessar esta área.')
    else:
        messages.error(request, 'Email ou senha inválidos.')

    return render(request, 'login_professor.html')  



# --- CADASTRAR ALUNO (somente superusuário) ---
@login_required
def cadastrar_aluno(request):
    if not request.user.is_superuser:
        return redirect('login_professor')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        if not username or not password or not email:
            messages.error(request, "Preencha todos os campos.")
            return redirect('cadastrar_aluno')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Já existe um psicologo com esse nome de usuário.")
            return redirect('cadastrar_aluno')

        # Cria o aluno
        psicologo = CustomUser.objects.create_user(
            username=username,
            password=password,
            email=email,
            user_type='psicologo'
        )
        psicologo.save()

        messages.success(request, f"psicologo '{username}' cadastrado com sucesso!")
        return redirect('cadastrar_aluno')

    return render(request, 'cadastrar_aluno.html')



# --- LOGIN PSICÓLOGO (ALUNO) ---
def login_psicologo(request):
    if request.method == "GET":
        return render(request, 'login_psicologo.html')

    email = request.POST.get('email')
    senha = request.POST.get('password')
    print("Tentando login:", email, senha)

    user = authenticate(request, email=email, password=senha)
    print("Resultado do authenticate:", user)

    if user:
        print("User type:", user.user_type)
        if user.user_type == 'psicologo':
            login_django(request, user)
            print("Login bem-sucedido!")
            return redirect('inicio_psicologo')
        else:
            messages.error(request, 'Apenas psicólogos podem acessar esta área.')
    else:
        messages.error(request, 'Email ou senha inválidos.')

    return render(request, 'login_psicologo.html')


# --- INÍCIO PSICÓLOGO (ALUNO) ---
@login_required
def inicio_psicologo(request):
    if getattr(request.user, 'user_type', '') != 'psicologo':
        return redirect('login_psicologo')
    return render(request, 'inicio_psicologo.html')




    
