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

        # Kiểm tra người dùng có thuộc cuộc trò chuyện không
        is_participant = await self.is_room_participant(self.room_id, self.user.id)
        if not is_participant:
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
        message_type = data.get('type')

        if message_type == 'chat_message':
            message = data.get('message', '')
            attachment_id = data.get('attachment_id', None)  # ID của tệp đã tải lên
            image_id = data.get('image_id', None)  # ID của hình ảnh đã tải lên

            # Lưu tin nhắn với tệp đính kèm hoặc hình ảnh nếu có
            message_obj = await self.save_message(
                self.room_id,
                self.user.id,
                message,
                attachment_id,
                image_id
            )

            # Chuẩn bị dữ liệu để gửi
            message_data = {
                'type': 'chat_message',
                'message': message,
                'sender_id': self.user.id,
                'sender_name': self.user.username,
                'timestamp': message_obj.NgayTao.isoformat(),
                'message_id': message_obj.id,
            }

            # Thêm thông tin về tệp đính kèm nếu có
            if message_obj.TepDinhKem:
                message_data['attachment'] = {
                    'url': message_obj.TepDinhKem.url,
                    'name': message_obj.TepDinhKem.name.split('/')[-1],
                    'size': message_obj.TepDinhKem.size
                }

            # Thêm thông tin về hình ảnh nếu có
            if message_obj.HinhAnh:
                message_data['image'] = {
                    'url': message_obj.HinhAnh.url,
                    'name': message_obj.HinhAnh.name.split('/')[-1],
                    'size': message_obj.HinhAnh.size
                }

            # Gửi tin nhắn cho tất cả thành viên trong phòng
            await self.channel_layer.group_send(
                self.room_group_name,
                message_data
            )

    async def chat_message(self, event):
        # Tạo bản sao của event để tránh thay đổi dữ liệu gốc
        message_data = event.copy()

        # Loại bỏ trường 'type' vì nó được sử dụng bởi channel layer
        message_type = message_data.pop('type')

        # Thêm lại trường 'type' với giá trị 'chat_message' cho client
        message_data['type'] = 'chat_message'

        # Gửi dữ liệu đến client
        await self.send(text_data=json.dumps(message_data))

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

        # Tạo tin nhắn mới
        message = TinNhanChiTiet(
            MaCuocTroChuyen=room,
            NguoiDung=user,
            NgayTao=timezone.now(),
            NoiDung=content
        )

        # Nếu có ID tệp đính kèm, lấy tệp từ bảng tạm và gán cho tin nhắn
        if attachment_id:
            from MXHNBDN.models import TempFile  # Import tại đây để tránh circular import
            try:
                temp_file = TempFile.objects.get(id=attachment_id, user=user)
                message.TepDinhKem = temp_file.file
                temp_file.delete()  # Xóa tệp tạm sau khi đã gán cho tin nhắn
            except TempFile.DoesNotExist:
                pass

        # Nếu có ID hình ảnh, lấy hình ảnh từ bảng tạm và gán cho tin nhắn
        if image_id:
            from MXHNBDN.models import TempImage  # Import tại đây để tránh circular import
            try:
                temp_image = TempImage.objects.get(id=image_id, user=user)
                message.HinhAnh = temp_image.image
                temp_image.delete()  # Xóa hình ảnh tạm sau khi đã gán cho tin nhắn
            except TempImage.DoesNotExist:
                pass

        message.save()
        return message