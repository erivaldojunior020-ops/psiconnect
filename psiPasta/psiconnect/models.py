from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('O email é obrigatório')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('user_type', 'professor')
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('professor', 'Professor'),
        ('psicologo', 'Psicologo'),
        ('paciente', 'Paciente'),
    )

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=False, blank=True, null=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='paciente')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.email} ({self.get_user_type_display()})"


# perfil do psicólogo
class PerfilPsicologo(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='perfil_psicologo')
    nome_completo = models.CharField(max_length=150)
    crp = models.CharField(max_length=20, unique=True, blank=True, null=True)
    especializacao = models.CharField(max_length=150, blank=True, null=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    foto = models.ImageField(upload_to='perfil_fotos/', blank=True, null=True)

    def __str__(self):
        return f"Perfil de {self.user.email}"


class Sessao(models.Model):
    paciente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    psicologo = models.ForeignKey('PerfilPsicologo', on_delete=models.CASCADE)
    data = models.DateField()
    hora = models.TimeField()
    observacoes = models.TextField(blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    STATUS_CHOICES = (
        ('pendente', 'Pendente'),
        ('confirmado', 'Confirmado'),
        ('cancelado', 'Cancelado'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')

    def __str__(self):
        return f"{self.paciente.email} com {self.psicologo.nome_completo} em {self.data} às {self.hora}"


class HorarioDisponivel(models.Model):
    psicologo = models.ForeignKey(PerfilPsicologo, on_delete=models.CASCADE)
    data = models.DateField()
    hora = models.TimeField()
    disponivel = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.psicologo.user.username} - {self.data} {self.hora}"
    
User = get_user_model()

class Mensagem(models.Model):
    remetente = models.ForeignKey(User, on_delete=models.CASCADE, related_name="mensagens_enviadas")
    destinatario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="mensagens_recebidas")
    consulta = models.ForeignKey(Sessao, on_delete=models.CASCADE)
    texto = models.TextField()
    data_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.remetente} → {self.destinatario} ({self.consulta.id})"








class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.consulta_id = self.scope["url_route"]["kwargs"]["consulta_id"]
        self.room_group_name = f"chat_{self.consulta_id}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        texto = data.get("texto")
        remetente_id = data.get("remetente")

        from .models import Sessao, Mensagem, User
        consulta = await database_sync_to_async(Sessao.objects.get)(id=self.consulta_id)
        remetente = await database_sync_to_async(User.objects.get)(id=remetente_id)

        # Descobrir destinatário
        if remetente == consulta.psicologo.user:
            destinatario = consulta.paciente
        else:
            destinatario = consulta.psicologo.user

        # SALVA NO BANCO (AGORA FUNCIONA!)
        msg = await database_sync_to_async(Mensagem.objects.create)(
            remetente=remetente,
            destinatario=destinatario,
            consulta=consulta,
            texto=texto
        )

        # Envia mensagem ao grupo
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "texto": msg.texto,
                "hora": msg.data_envio.strftime("%H:%M"),
                "remetente": remetente.email
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))
