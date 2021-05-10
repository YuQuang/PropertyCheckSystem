# index/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User, AnonymousUser, Group
from .consumer_async_db import get_user, is_member
from channels.layers import get_channel_layer
import json
from asgiref.sync import async_to_sync


##################
# 盤點時連線
##################
class CheckConsumer(AsyncWebsocketConsumer):
    userGroup = {
        "admin": "admin",
        "user":  "user",
        "guest": "guest",
    }
    now_group = userGroup["guest"]
    now_user = ''
    now_user_id = 0

    #################
    # 用戶連線時觸發
    ##################
    async def connect(self):
        """
            連線時檢查用戶是否為登陸用戶
        """
        user = await get_user(self.scope['user'].id)
        if await is_member(user, self.userGroup["admin"]):
            self.now_group = self.userGroup["admin"]
        elif await is_member(user, self.userGroup["user"]):
            self.now_group = self.userGroup["user"]

        # 紀錄使用者資訊
        self.now_user_id = self.scope['user'].id
        self.now_user = user

        # 驗證使用者是否已經登陸
        if user.is_anonymous:
            await self.close()
        await self.accept()

        await self.channel_layer.group_add(
            self.now_group,
            self.channel_name
        )

    #################
    # 斷開連接時觸發
    ##################
    async def disconnect(self, close_code):
        """
            斷線
        """
        print("disconnect", close_code)
        await self.channel_layer.group_discard(self.now_group, self.channel_name)

    #################
    # 接收訊息
    ##################
    async def receive(self, text_data):
        """
            接收資料
        """
        data = json.loads(text_data)
        print(data)
        # await self.sendToAllGroup({"action": "check", "id": 3, "status": "c"})

    #################
    # 傳送給全部人
    ##################
    async def sendToAllGroup(self, msg):
        for key in CheckConsumer.userGroup:
            await self.channel_layer.group_send(
                CheckConsumer.userGroup[key],
                {
                    'type': 'Check.sendMsg',
                    'message': msg,
                }
            )
    
    #################
    # 傳送訊息給該消費者
    ##################
    async def Check_sendMsg(self, event):
        message = event['message']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
        }))
