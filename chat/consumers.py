from channels.generic.websocket import AsyncWebsocketConsumer
import json


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(
            'all',
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_send(
            'all',
            {
                'type': 'chat_message',
                'data': {
                    'type': 'disconnect',
                    'data': {
                        'name': self.name
                    }
                }
            }
        )

        await self.channel_layer.group_discard(
            'all',
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)

        if data['type'] == 'connect':
            self.name = data['data']['name']

        await self.channel_layer.group_send(
            'all',
            {
                'type': 'chat_message',
                'data': data,
                'senderChannel': self.channel_name
            }
        )

    async def chat_message(self, event):
        if self.channel_name != event['senderChannel']:
            await self.send(
                text_data=json.dumps(event['data'])
            )