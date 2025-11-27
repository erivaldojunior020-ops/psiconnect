
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from datetime import datetime
from datetime import date
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import PerfilPsicologo, Sessao, HorarioDisponivel, Mensagem
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as login_django
from django.contrib import messages
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

@login_required
def inicio_paciente(request):
    # Pega os 3 primeiros psicólogos cadastrados
    destaques = PerfilPsicologo.objects.filter(
        user__user_type='psicologo'
    ).order_by('-id')[:3]

    return render(request, 'inicio_paciente.html', {
        "destaques": destaques
    })


def lista_psicologos(request):
    psicologos = PerfilPsicologo.objects.filter(user__user_type='psicologo')
    return render(request, 'lista_psicologos.html', {'psicologos': psicologos})


@login_required
def agendamento_paciente(request, psicologo_id):
    psicologo = get_object_or_404(PerfilPsicologo, id=psicologo_id)

    horarios = HorarioDisponivel.objects.filter(
        psicologo=psicologo,
        disponivel=True
    ).order_by("data", "hora")

    if request.method == "POST":
        horario_id = request.POST.get("horario_id")
        horario = get_object_or_404(HorarioDisponivel, id=horario_id)

        Sessao.objects.create(
            paciente=request.user,
            psicologo=psicologo,
            data=horario.data,
            hora=horario.hora,
        )

        # Marcar o horário como ocupado
        horario.disponivel = False
        horario.save()

        messages.success(request, "Sessão agendada com sucesso!")
        return redirect("sessoes_paciente")

    return render(request, "agendamento_paciente.html", {
        "psicologo": psicologo,
        "horarios_disponiveis": horarios
    })


@login_required
def serviços_paciente(request):
    if request.user.user_type != "paciente":
        return redirect("login_paciente")

    return render(request, "serviços_paciente.html")



@login_required
def suporte_paciente(request):
    if request.user.user_type != "paciente":
        return redirect("login_paciente")

    return render(request, "suporte_paciente.html")



@login_required
def sobre_paciente(request):
    if request.user.user_type != "paciente":
        return redirect("login_paciente")

    return render(request, "sobre_paciente.html")



@login_required(login_url="/auth/login_psicologo/")
def cadastrar_horario(request):

    if request.user.user_type != "psicologo":
        messages.error(request, "Apenas psicólogos podem cadastrar horários.")
        return redirect("login_psicologo")

    psicologo, created = PerfilPsicologo.objects.get_or_create(user=request.user)

    if request.method == "POST":
        data = request.POST.get("data")
        hora = request.POST.get("hora")

        if HorarioDisponivel.objects.filter(psicologo=psicologo, data=data, hora=hora).exists():
            messages.error(request, "Este horário já está cadastrado!")
            return redirect("cadastrar_horario")

        HorarioDisponivel.objects.create(
            psicologo=psicologo,
            data=data,
            hora=hora,
            disponivel=True
        )

        messages.success(request, "Horário cadastrado com sucesso!")
        return redirect("cadastrar_horario")

    # Data e hora atual
    agora = timezone.now()

    # Query filtrando:
    # 1. Horários do psicólogo
    # 2. Disponíveis (não cancelados)
    # 3. Datas futuras ou hoje com horário ainda não passado
    horarios = HorarioDisponivel.objects.filter(
        psicologo=psicologo,
        disponivel=True
    ).order_by("data", "hora")

    # Remover horários passados
    horarios = [
        h for h in horarios
        if h.data > agora.date() or (h.data == agora.date() and h.hora > agora.time())
    ]

    return render(request, "cadastrar_horario.html", {
        "horarios": horarios
    })


@login_required
def sessoes_paciente(request):
    # Filtra apenas sessões futuras e que não foram canceladas
    agora = timezone.now()
    sessoes = Sessao.objects.filter(
        paciente=request.user,
        data__gte=agora.date()
    ).exclude(
        status='cancelado'
    ).order_by("data", "hora")
    
    return render(request, "sessoes_paciente.html", {"sessoes": sessoes})



@login_required
def cancelar_sessao_ajax(request, sessao_id):
    if request.method == "POST":
        sessao = get_object_or_404(Sessao, id=sessao_id, paciente=request.user)
        sessao.status = "cancelado"
        sessao.save()
        return JsonResponse({"success": True})
    return JsonResponse({"success": False}, status=400)





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



# --- LOGIN PSICÓLOGO ---
def login_psicologo(request):
    if request.method == "GET":
        return render(request, 'login_psicologo.html')

    email = request.POST.get('email')
    senha = request.POST.get('senha')

    user = authenticate(request, email=email, password=senha)

    if user:
        if user.user_type == 'psicologo':

            # 🔥 Se o psicólogo NÃO tem perfil, cria automaticamente
            from .models import PerfilPsicologo
            PerfilPsicologo.objects.get_or_create(
                user=user,
                defaults={"nome_completo": user.username}
            )

            login_django(request, user)
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

def consultas_psicologo(request):
    if not request.user.is_authenticated or request.user.user_type != "psicologo":
        return redirect("login_psicologo")

    psicologo = request.user.perfil_psicologo
    agora = timezone.now()

    # Só consultas futuras e que não foram canceladas
    consultas = Sessao.objects.filter(
        psicologo=psicologo,
        data__gte=agora.date()
    ).exclude(status='cancelado').order_by("data", "hora")

    return render(request, "consultas_psicologo.html", {"consultas": consultas})


def confirmar_consulta(request, id):
    consulta = Sessao.objects.get(id=id)

    if request.user.perfil_psicologo != consulta.psicologo:
        return redirect("inicio_psicologo")

    consulta.status = "confirmado"
    consulta.save()
    return redirect("consultas_psicologo")


@login_required
def cancelar_consulta(request, id):
    if request.method == "POST":
        consulta = get_object_or_404(Sessao, id=id)

        # Verifica se quem cancela é paciente da sessão ou psicólogo responsável
        if request.user == consulta.paciente or getattr(request.user, 'perfil_psicologo', None) == consulta.psicologo:
            consulta.status = "cancelado"
            consulta.save()
            return JsonResponse({"success": True})
        else:
            return JsonResponse({"success": False, "error": "Sem permissão"}, status=403)

    return JsonResponse({"success": False, "error": "Método inválido"}, status=400)


def pendente_consulta(request, id):
    consulta = Sessao.objects.get(id=id)

    if request.user.perfil_psicologo != consulta.psicologo:
        return redirect("inicio_psicologo")

    consulta.status = "pendente"
    consulta.save()
    return redirect("consultas_psicologo")


def chat(request, consulta_id):
    consulta = get_object_or_404(Sessao, id=consulta_id)

    # Apenas paciente e psicólogo da consulta podem acessar
    if request.user not in [consulta.paciente, consulta.psicologo.user]:
        return redirect("inicio_paciente")

    # Busca histórico de mensagens da consulta
    mensagens = Mensagem.objects.filter(consulta=consulta).order_by("data_envio")

    return render(request, "chat.html", {
        "consulta": consulta,
        "mensagens": mensagens
    })

from django.shortcuts import redirect

def home(request):
    return redirect('login_paciente')
