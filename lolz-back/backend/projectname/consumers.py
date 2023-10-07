from channels.generic.websocket import AsyncWebsocketConsumer
import json

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = "chat_room"
        self.room_group_name = f"chat_{self.room_name}"

        # Add the user to the group when they connect
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Remove the user from the group when they disconnect
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        username = text_data_json['username']  # Assuming you have user authentication
        message = text_data_json['message']

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username  # Include the sender's username
            }
        )

    async def chat_message(self, event):
        message = event['message']
        username = event['username']  # Get the sender's username from the event

        await self.send(text_data=json.dumps({
            'message': message,
            'username': username  # Include the sender's username in the message
        }))
