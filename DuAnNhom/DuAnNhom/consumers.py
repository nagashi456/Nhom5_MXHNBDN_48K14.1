import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone
from django.contrib.auth.models import User
from MXHNBDN.models import CuocTroChuyen, TinNhanChiTiet, NguoiDung, ThanhVienCuocTroChuyen


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.get('type', 'message')

        if message_type == 'message':
            message = data['message']
            user_id = self.scope['user'].id
            conversation_id = int(self.room_name)

            # Save message to database
            message_id = await self.save_message(
                user_id=user_id,
                conversation_id=conversation_id,
                message=message,
                attachment=data.get('attachment', None),
                image=data.get('image', None)
            )

            # Get user info
            user_info = await self.get_user_info(user_id)

            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'user_id': user_id,
                    'username': user_info['username'],
                    'avatar': user_info['avatar'],
                    'message_id': message_id,
                    'timestamp': timezone.now().isoformat(),
                    'attachment': data.get('attachment', None),
                    'image': data.get('image', None)
                }
            )

    # Receive message from room group
    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'user_id': event['user_id'],
            'username': event['username'],
            'avatar': event['avatar'],
            'message_id': event['message_id'],
            'timestamp': event['timestamp'],
            'attachment': event.get('attachment', None),
            'image': event.get('image', None)
        }))

    @database_sync_to_async
    def save_message(self, user_id, conversation_id, message, attachment=None, image=None):
        user = NguoiDung.objects.get(user_id=user_id)
        conversation = CuocTroChuyen.objects.get(id=conversation_id)

        # Check if user is a member of this conversation
        is_member = ThanhVienCuocTroChuyen.objects.filter(
            MaCuocTroChuyen=conversation,
            MaNguoiDung=user
        ).exists()

        if not is_member:
            raise Exception("User is not a member of this conversation")

        # Create and save the message
        message = TinNhanChiTiet.objects.create(
            NgayTao=timezone.now(),
            NoiDung=message,
            TepDinhKem=attachment,
            HinhAnh=image,
            MaCuocTroChuyen=conversation,
            NguoiDung=user
        )

        return message.id

    @database_sync_to_async
    def get_user_info(self, user_id):
        user = NguoiDung.objects.get(user_id=user_id)
        return {
            'username': user.HoTen,
            'avatar': user.Avatar.url if user.Avatar else None
        }
