"""
    與資料庫非同步連線函數
"""

from channels.db import database_sync_to_async
from django.contrib.auth.models import User, AnonymousUser, Group
from .models import Notification

@database_sync_to_async
def get_user(user_id):
    """
        檢查用戶是否存在資料庫內
    """
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return AnonymousUser()

@database_sync_to_async
def is_member(user, group_name):
    """
        檢查用戶是否在某群組內
    """
    try:
        return user.groups.filter(name=group_name).exists()
    except Group.DoesNotExist:
        return False

@database_sync_to_async
def get_recentNotify(user_id, group_name):
    """
        取得用戶近期通知
    """
    group_id = Group.objects.filter(name=group_name).first().pk
    qs1 = Notification.objects.filter(action_user=user_id, status='n').all()
    gqs1 = Notification.objects.filter(notify_group=group_id, group_status='n').exclude(action_user=user_id).all()
    qs2 = Notification.objects.filter(action_user=user_id, status='r').order_by("-action_date").all()
    gqs2 = Notification.objects.filter(notify_group=group_id, group_status='r').exclude(action_user=user_id).order_by("-action_date").all()
    
    # 群組與個人的未讀訊息
    r1 = qs1 | gqs1
    
    # 群組與自己的已讀訊息
    qs2 = list(qs2)
    gqs2 = list(gqs2)
    if qs2.__len__() > 3:
        qs2 = qs2[:3]
    if gqs2.__len__() > 3:
        gqs2 = gqs2[:3]
    r2 = qs2 + gqs2

    r3 = list(r1) + list(r2)

    notify_list = []
    for item in r3:
        notify_dict = {}
        ACTION_DICT = dict(item.USER_ACTION)
        notify_dict.setdefault("action", str(ACTION_DICT[item.action]))
        notify_dict.setdefault("user", str(item.action_user))
        notify_dict.setdefault("time", str(item.action_date.strftime("%Y-%m-%d %H:%M:%S")))
        STATUS_DICT = dict(item.READ_STATUS)
        notify_dict.setdefault("status", str(STATUS_DICT[item.status]))
        notify_dict.setdefault("group_status", str(STATUS_DICT[item.group_status]))
        notify_dict.setdefault("group_name", str(item.notify_group.name))

        notify_list.append(notify_dict)

    return {"action": "onNewNotify", "data": notify_list}

@database_sync_to_async
def userReadNotify(user_id, group_name):
    """
        取得用戶新訊息
    """
    group = Group.objects.filter(name=group_name).first()
    Notification.objects.filter(notify_group=group, group_status='n').update(group_status="r")
    Notification.objects.filter(action_user=user_id, status='n').update(status="r")
    return 0