from channels.generic.websocket import AsyncWebsocketConsumer
import json

names = []


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
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

        names.pop(names.index(self.name))

    async def receive(self, text_data):
        data = json.loads(text_data)

        if data['type'] == 'connect':
            self.name = data['data']['name']
            names.append(self.name)
            await self.channel_layer.group_add(
                'all',
                self.channel_name
            )
        elif data['type'] == 'names':
            return await self.send(text_data=json.dumps({
                'type': 'names',
                'data': names
            }))

        await self.channel_layer.group_send(
            'all',
            {
                'type': 'chat_message',
                'data': data,
                'senderChannel': self.channel_name
            }
        )

    async def chat_message(self, event):
        data = event['data']

        if data['type'] != 'disconnect' and self.channel_name == event['senderChannel']:
            return

        await self.send(
            text_data=json.dumps(event['data'])
        )
