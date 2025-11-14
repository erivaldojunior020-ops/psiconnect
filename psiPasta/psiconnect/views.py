from django.shortcuts import render, redirect
from .models import PerfilPsicologo, Sessao  # certifique-se de importar
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as login_django
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
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
    psicologos = PerfilPsicologo.objects.filter(user__user_type='psicologo')
    return render(request, 'lista_psicologos.html', {'psicologos': psicologos})


@login_required
def agendamento_paciente(request, psicologo_id):
    psicologo = get_object_or_404(PerfilPsicologo, id=psicologo_id)

    if request.method == "POST":
        data = request.POST.get("data")
        hora = request.POST.get("hora")

        Sessao.objects.create(
            paciente=request.user,
            psicologo=psicologo,
            data=data,
            hora=hora
        )

        messages.success(request, "Sessão agendada com sucesso!")
        return redirect("sessoes_paciente")

    return render(request, "agendamento_paciente.html", {"psicologo": psicologo})

    
@login_required
def sessoes_paciente(request):
    sessoes = Sessao.objects.filter(paciente=request.user).order_by("data", "hora")
    return render(request, "sessoes_paciente.html", {"sessoes": sessoes})




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
    senha = request.POST.get('senha')
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


@login_required
def perfil_psicologo(request):
    # Pega (ou cria) o perfil do psicólogo logado
    perfil, created = PerfilPsicologo.objects.get_or_create(user=request.user)

    if request.method == "POST":
        perfil.nome_completo = request.POST.get("nome_completo")
        perfil.crp = request.POST.get("crp")
        perfil.telefone = request.POST.get("telefone")
        perfil.especializacao = request.POST.get("especializacao")
        perfil.bio = request.POST.get("bio")

        if "foto" in request.FILES:
            perfil.foto = request.FILES["foto"]

        perfil.save()
        messages.success(request, "Perfil atualizado com sucesso!")
        return redirect("perfil_psicologo")

    context = {
        "perfil": perfil
    }
    return render(request, "perfil_psicologo.html", context)


