# import json
# from channels.generic.websocket import AsyncWebsocketConsumer
# from channels.db import database_sync_to_async
# from django.contrib.auth.models import User
# from django.utils import timezone
# from MXHNBDN.models import CuocTroChuyen, TinNhanChiTiet

# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.user = self.scope["user"]

#         if not self.user.is_authenticated:
#             await self.close()
#             return

#         self.room_id = self.scope['url_route']['kwargs']['room_id']
#         self.room_group_name = f'chat_{self.room_id}'

#         # Kiểm tra người dùng có thuộc cuộc trò chuyện không
#         is_participant = await self.is_room_participant(self.room_id, self.user.id)
#         if not is_participant:
#             await self.close()
#             return

#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )

#         await self.accept()

#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )

#     async def receive(self, text_data):
#         data = json.loads(text_data)
#         message_type = data.get('type')

#         if message_type == 'chat_message':
#             message = data.get('message')

#             # Lưu tin nhắn
#             message_obj = await self.save_message(self.room_id, self.user.id, message)

#             # Gửi tin nhắn cho tất cả thành viên trong phòng
#             await self.channel_layer.group_send(
#                 self.room_group_name,
#                 {
#                     'type': 'chat_message',
#                     'message': message,
#                     'sender_id': self.user.id,
#                     'sender_name': self.user.username,
#                     'timestamp': message_obj.NgayTao.isoformat(),
#                     'message_id': message_obj.id
#                 }
#             )

#     async def chat_message(self, event):
#         await self.send(text_data=json.dumps({
#             'type': 'chat_message',
#             'message': event['message'],
#             'sender_id': event['sender_id'],
#             'sender_name': event['sender_name'],
#             'timestamp': event['timestamp'],
#             'message_id': event['message_id']
#         }))

#     @database_sync_to_async
#     def is_room_participant(self, room_id, user_id):
#         try:
#             room = CuocTroChuyen.objects.get(id=room_id)
#             return room.ThanhVien.filter(id=user_id).exists()
#         except CuocTroChuyen.DoesNotExist:
#             return False

#     @database_sync_to_async
#     def save_message(self, room_id, user_id, content):
#         room = CuocTroChuyen.objects.get(id=room_id)
#         user = User.objects.get(id=user_id)
#         message = TinNhanChiTiet.objects.create(
#             MaCuocTroChuyen=room,
#             NguoiDung=user,
#             NgayTao=timezone.now(),
#             NoiDung=content
#         )
#         return message

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from django.utils import timezone
from MXHNBDN.models import CuocTroChuyen, TinNhanChiTiet

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        if not self.user.is_authenticated:
            await self.close()
            return

        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_id}'

        # Kiểm tra user có trong room không
        if not await self.is_room_participant(self.room_id, self.user.id):
            await self.close()
            return

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
        if data.get('type') != 'chat_message':
            return

        # Lấy payload từ client
        content       = data.get('message', '')
        attachment_id = data.get('attachment_id')
        image_id      = data.get('image_id')

        # Lưu vào DB
        message_obj = await self.save_message(
            self.room_id, self.user.id,
            content, attachment_id, image_id
        )

        # Chuẩn bị payload gửi cho group
        payload = {
            'type': 'chat_message',
            'message_id': message_obj.id,
            'message':    message_obj.NoiDung,
            'sender_id':  self.user.id,
            'sender_name':self.user.username,
            'timestamp':  message_obj.NgayTao.isoformat(),
        }

        # Nếu có file
        if message_obj.TepDinhKem:
            payload['attachment'] = {
                'url':  message_obj.TepDinhKem.url,
                'name': message_obj.TepDinhKem.name.rsplit('/',1)[-1],
                'size': message_obj.TepDinhKem.size,
            }

        # Nếu có ảnh
        if message_obj.HinhAnh:
            payload['image'] = {
                'url':  message_obj.HinhAnh.url,
                'name': message_obj.HinhAnh.name.rsplit('/',1)[-1],
                'size': message_obj.HinhAnh.size,
            }

        # Broadcast
        await self.channel_layer.group_send(self.room_group_name, payload)

    async def chat_message(self, event):
        # gửi payload nguyên gốc (vừa thêm attachment/image)
        await self.send(text_data=json.dumps(event))

    @database_sync_to_async
    def is_room_participant(self, room_id, user_id):
        try:
            room = CuocTroChuyen.objects.get(id=room_id)
            return room.ThanhVien.filter(id=user_id).exists()
        except CuocTroChuyen.DoesNotExist:
            return False

    @database_sync_to_async
    def save_message(self, room_id, user_id, content, attachment_id=None, image_id=None):
        room = CuocTroChuyen.objects.get(id=room_id)
        user = User.objects.get(id=user_id)

        msg = TinNhanChiTiet(
            MaCuocTroChuyen=room,
            NguoiDung=user,
            NoiDung=content,
            NgayTao=timezone.now()
        )

        # Gán trực tiếp đường dẫn storage (attachment_id) vào FileField
        if attachment_id:
            msg.TepDinhKem.name = attachment_id

        # Gán đường dẫn image_id vào ImageField
        if image_id:
            msg.HinhAnh.name = image_id

        msg.save()
        return msg
