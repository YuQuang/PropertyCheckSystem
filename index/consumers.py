# index/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Property
from django.contrib.auth.models import User, AnonymousUser, Group
from .consumer_async_db import get_user, is_member, get_recentNotify, userReadNotify
from channels.layers import get_channel_layer
import json
from asgiref.sync import async_to_sync

userAction = {
    'getRecentNotify': 'getRecentNotify',
    'getNewNotify': 'getNewNotify',
    'userReadNotify': 'userReadNotify',
}


##################
# 提醒的消費者
##################
class NotifyConsumer(AsyncWebsocketConsumer):
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
        try:
            data = json.loads(text_data)
            action = data["action"]
            if action == None or action == '':
                return

            # 用戶取得最近未讀+已讀的10則通知
            if action == userAction['getRecentNotify']:
                await self.Notify_sendMsg({
                    'message': await get_recentNotify(self.now_user_id, self.now_group)
                })
            elif action == userAction['getNewNotify']:
                await self.Notify_sendMsg({
                    'message': await get_recentNotify(self.now_user_id, self.now_group)
                })
            elif action == userAction['userReadNotify']:
                await userReadNotify(self.now_user_id, self.now_group)

        except Exception as e:
            print("Websocket接收錯誤")
            print(e)
    
    #################
    # 傳送給全部人
    ##################
    async def sendToAllGroup(self, msg):
        for key in NotifyConsumer.userGroup:
            await self.channel_layer.group_send(
                NotifyConsumer.userGroup[key],
                {
                    'type': 'Notify.sendMsg',
                    'message': msg,
                }
            )

    #################
    # 傳送訊息給該群組
    ##################
    async def sendToGroup(self, msg, groupName):
        await self.channel_layer.group_send(
            groupName,
            {
                'type': 'Notify.sendMsg',
                'message': msg,
            }
        )
    
    #################
    # 傳送訊息給該消費者
    ##################
    async def Notify_sendMsg(self, event):
        message = event['message']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
        }))


##################
# 傳送訊息給所有人
##################
def sendToAllGroup(msg):
    """
        傳送訊息給全部人
    """
    channel_layer = get_channel_layer()
    for key in NotifyConsumer.userGroup:
            async_to_sync(channel_layer.group_send)(
                NotifyConsumer.userGroup[key],
                {
                    'type': 'Notify.sendMsg',
                    'message': msg,
                }
            )

#################
# 傳送訊息給特定群組
#################
def sendToGroup(msg, groupName):
    """
        傳送訊息給特定Group
    """
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        groupName,
        {
            'type': 'Notify.sendMsg',
            'message': msg,
        }
    )