import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from asgiref.sync import sync_to_async
from .models import Sessao, Mensagem

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.consulta_id = self.scope['url_route']['kwargs']['consulta_id']
        self.room_group_name = f'chat_{self.consulta_id}'

        # Adiciona o canal ao grupo
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Remove o canal do grupo
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        user = self.scope['user']

        # Salva a mensagem no banco
        await self.salvar_mensagem(user, message)

        # Envia a mensagem para o grupo
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': user.username
            }
        )

    async def chat_message(self, event):
        # Recebe mensagem do grupo e envia para o WebSocket
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'user': event['user']
        }))

    @sync_to_async
    def salvar_mensagem(self, user, texto):
        consulta = Sessao.objects.get(id=self.consulta_id)
        destinatario = consulta.paciente if user == consulta.psicologo.user else consulta.psicologo.user
        Mensagem.objects.create(
            remetente=user,
            destinatario=destinatario,
            consulta=consulta,
            texto=texto
        )
