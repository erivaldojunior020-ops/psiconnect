import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from .models import Mensagem, Sessao
from django.utils import timezone

User = get_user_model()

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

        mensagem = data.get("mensagem") or data.get("texto")
        horario = data.get("horario") or data.get("hora")

        remetente = self.scope["user"]
        remetente_username = remetente.username

        consulta = Sessao.objects.get(id=self.consulta_id)

        destinatario = (
            consulta.paciente
            if remetente == consulta.psicologo.user
            else consulta.psicologo.user
        )

        # Salvar no banco
        Mensagem.objects.create(
            remetente=remetente,
            destinatario=destinatario,
            consulta=consulta,
            texto=mensagem,
            data_envio=timezone.now(),
        )

        # Broadcast
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "texto": mensagem,
                "remetente": remetente_username,
                "hora": horario,
            }
        )


    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "texto": event["texto"],
            "remetente": event["remetente"],
            "hora": event["hora"],
        }))
