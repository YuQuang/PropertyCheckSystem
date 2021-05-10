from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from django.urls import reverse
from django.contrib.auth.models import User, Permission, Group
from django.contrib.auth.decorators import login_required
#
import json
import sys, os, datetime, asyncio, re, os.path
#
from .models import Property, Brand, Position, Unit, LeaseProperty, LeaseHistory, Notification, PropertyImage, CurrentCheckProperty
#
from .consumers import NotifyConsumer
from .consumers import sendToAllGroup, sendToGroup

"""
# HomePage
"""
# 瀏覽功能首頁
# browse every function
# (不用登入)
# (no need login)
def index(request):
    return render(request, 'index.html')

"""
# Web Appearance
"""

# 查找資料頁面
# (需要登入)
# (need login)
@login_required
def search(request):
    return render(request, 'search.html')

# 查找資料頁面
# (需要登入)
# (need login)
@login_required
def oldSearch(request):
    return render(request, 'old_search.html')

# 查找資料頁面
# (需要登入)
# (need login)
@login_required
def newPropertyDetail(request):
    return render(request, 'new_propertyDetail.html')

# 導入Excel表格的網頁
# (需要登入)
# (need login)
@login_required
def importExcel(request):
    return render(request, 'importExcel.html')

# 新增一筆資料
# (需要登入)
# (need login)
@login_required
def addData(request):
    return render(request, 'addData.html')

# 關於我們
# (不用登入)
# (no need login)
def aboutUs(request):
    return render(request, 'aboutUs.html')

# 借用財產頁面
# (需要登入)
# (need login)
# (需要觀看租借財產權限)
# (Need index.view_lease_property)
@login_required
def leaseProperty(request):
    user = request.user
    # 用戶於群組內的權限
    all_permissions_in_groups = user.get_group_permissions()
    # 用戶自己的權限
    all_permissions = user.get_all_permissions()
    # 檢查用戶是否有借用的權限
    if not request.user.has_perm('index.view_leaseproperty'):
        return redirect('/')
    return render(request, 'leaseProperty.html')

# 盤點功能
# (需要登入)
# (need login)
@login_required
def stockTaking(request):
    return render(request, "stockTaking.html")

# 使用者詳細訊息
# (需要登入)
# (need login)
@login_required
def profile(request):
    return render(request, "profile.html")

"""
#   Web API部分
#   Restfull API
#   WebAPI Part
"""

"""
# 裝飾函數
"""
# 檢查登陸狀態
def API_CheckLogin(func):
    """
        屬於API的用戶登陸檢查
    """
    def wrapper(request):
        if not request.user.is_authenticated:
            return HttpResponse(status=403)
        return func(request)
    
    return wrapper

# 用戶是否於群組
def UserInGroup(user, groupName: str):
    return user.groups.filter(name = groupName).exists()

"""
# 取得用戶資訊
"""
# 取得該用戶基本資訊
@API_CheckLogin
def getUserInfo(request):
    user = request.user

    userGroup = []
    for group in user.groups.all():
        userGroup.append(group.__str__())
    
    userName = user.username

    return JsonResponse({"userName": userName, "userGroup": userGroup})

# 取得所有位置
@API_CheckLogin
def getPosition(request):
    position = Position.objects.all()
    
    positionList = []
    for p in position:
        positionList.append(p.name.__str__())
    
    return JsonResponse({"position":positionList})

# 取得所有廠牌
@API_CheckLogin
def getBrand(request):
    brand = Brand.objects.all()

    brandList = []
    for b in brand:
        brandList.append(b.name.__str__())
    
    return JsonResponse({"brand": brandList})

"""
# 租借與歸還、同意租借與同意歸還
"""
# 查詢租借財產
# (需要租用財產權限 index.view_lease_property)
@API_CheckLogin
def getLoanProperty(request):
    user = request.user
    
    # 檢查用戶是否有借用的權限
    if not user.has_perm('index.view_leaseproperty'):
        return JsonResponse({'result': 'permission_deny'})

    waiting_data = []
    loaning_data = []
    waiting_return_data = []
    returned_data = []

    loaning_list = None
    waiting_list = None
    waiting_return_list = None
    returned_list = None
    if user.has_perm('index.change_leaseproperty') and user.has_perm('index.delete_leaseproperty'):
        waiting_list = LeaseProperty.objects.filter(status='w').all()
        loaning_list = LeaseProperty.objects.filter(status='l').all()
        waiting_return_list = LeaseProperty.objects.filter(status='c').all()
        returned_list = LeaseHistory.objects.all()
    else:
        waiting_list = LeaseProperty.objects.filter(status='w', borrower=user.__str__()).all()
        loaning_list = LeaseProperty.objects.filter(status='l', borrower=user.__str__()).all()
        waiting_return_list = LeaseProperty.objects.filter(status='c', returner=user.__str__()).all()
        returned_list = LeaseHistory.objects.filter(returner=user.__str__()).all()
    
    # 等待核准清單
    for waiting in waiting_list:
        waiting_dict = {}
        waiting_dict.setdefault("id", waiting.id.__str__())
        waiting_dict.setdefault("borrower", waiting.borrower.__str__())
        waiting_dict.setdefault("leaseProperty", waiting.leaseProperty.__str__())
        waiting_dict.setdefault("leasePropertyId", waiting.leaseProperty.id.__str__())
        waiting_dict.setdefault("serial_number", waiting.leaseProperty.serial_number.__str__())
        waiting_dict.setdefault("product_number", waiting.leaseProperty.property_number.__str__())
        waiting_dict.setdefault("borrow_administrator", waiting.borrow_administrator.__str__())
        waiting_dict.setdefault("borrow_date", waiting.borrow_date.strftime("%Y-%m-%d"))

        waiting_data.append(waiting_dict)

    # 正在租借中的物品清單
    for loaning in loaning_list:
        loaning_dict = {}
        loaning_dict.setdefault("id", loaning.id.__str__())
        loaning_dict.setdefault("leaseProperty", loaning.leaseProperty.__str__())
        loaning_dict.setdefault("leasePropertyId", loaning.leaseProperty.id.__str__())
        loaning_dict.setdefault("serial_number", loaning.leaseProperty.serial_number.__str__())
        loaning_dict.setdefault("product_number", loaning.leaseProperty.property_number.__str__())
        loaning_dict.setdefault("borrow_administrator", loaning.borrow_administrator.__str__())
        loaning_dict.setdefault("borrower", loaning.borrower.__str__())
        loaning_dict.setdefault("returner_administrator", loaning.returner_administrator.__str__())
        loaning_dict.setdefault("returner", loaning.returner.__str__())
        loaning_dict.setdefault("agree_date", loaning.agree_date.strftime("%Y-%m-%d"))
        loaning_dict.setdefault("borrow_date", loaning.borrow_date.strftime("%Y-%m-%d"))

        loaning_data.append(loaning_dict)
    
    # 等待核准清單
    for waiting_return in waiting_return_list:
        waiting_return_dict = {}
        waiting_return_dict.setdefault("id", waiting_return.id.__str__())
        waiting_return_dict.setdefault("leaseProperty", waiting_return.leaseProperty.__str__())
        waiting_return_dict.setdefault("leasePropertyId", waiting_return.leaseProperty.id.__str__())
        waiting_return_dict.setdefault("serial_number", waiting_return.leaseProperty.serial_number.__str__())
        waiting_return_dict.setdefault("product_number", waiting_return.leaseProperty.property_number.__str__())
        waiting_return_dict.setdefault("borrow_administrator", waiting_return.borrow_administrator.__str__())
        waiting_return_dict.setdefault("borrower", waiting_return.borrower.__str__())
        waiting_return_dict.setdefault("returner_administrator", waiting_return.returner_administrator.__str__())
        waiting_return_dict.setdefault("returner", waiting_return.returner.__str__())
        waiting_return_dict.setdefault("agree_date", waiting_return.agree_date.strftime("%Y-%m-%d"))
        waiting_return_dict.setdefault("borrow_date", waiting_return.borrow_date.strftime("%Y-%m-%d"))

        waiting_return_data.append(waiting_return_dict)

    # 已歸還物品清單
    for returned in returned_list:
        returned_dict = {}
        returned_dict.setdefault("id", returned.id.__str__())
        returned_dict.setdefault("leaseProperty", returned.leaseProperty.__str__())
        returned_dict.setdefault("leasePropertyID", returned.leasePropertyID.__str__())
        returned_dict.setdefault("borrow_administrator", returned.borrow_administrator.__str__())
        returned_dict.setdefault("borrower", returned.borrower.__str__())
        returned_dict.setdefault("returner_administrator", returned.returner_administrator.__str__())
        returned_dict.setdefault("returner", returned.returner.__str__())
        returned_dict.setdefault("agree_date", returned.agree_date.strftime("%Y-%m-%d"))
        returned_dict.setdefault("borrow_date", returned.borrow_date.strftime("%Y-%m-%d"))
        returned_dict.setdefault("return_date", returned.return_date.strftime("%Y-%m-%d"))

        returned_data.append(returned_dict)

    perm = {
        'change_leaseproperty': user.has_perm('index.change_leaseproperty'),
        'delete_leaseproperty': user.has_perm('index.delete_leaseproperty'),
        'add_leaseproperty': user.has_perm('index.add_leaseproperty'),
        'view_leaseproperty': user.has_perm('index.view_leaseproperty'),
    }
    return HttpResponse(json.dumps({'result': 'success', 'waiting_data': waiting_data, 'loaning_data': loaning_data,
                         'waiting_return_data': waiting_return_data, 'returned_data': returned_data,
                         'perm': perm}),content_type="application/json")

# 借用財產
# (需要租用財產權限 index.add_lease_property)
# 會留下提醒
@API_CheckLogin
def loanProperty(request):
    user = request.user
    # 用戶於群組內的權限
    all_permissions_in_groups = user.get_group_permissions()
    # 用戶自己的權限
    all_permissions = user.get_all_permissions()

    # 檢查用戶是否有借用的權限
    if not user.has_perm('index.add_leaseproperty'):
        return JsonResponse({'result': 'permission_deny'})

    # 取得序號以及產品編號
    product_id = request.GET.get('id')

    # 檢查序號以及編號
    if product_id == None:
        return JsonResponse({'result': 'empty'})

    # 查詢
    result = Property.objects.filter(id=product_id).first()
    if result == None:
        return JsonResponse({'result': 'empty'})

    # 被借走了
    if result.status == 'o':
        return JsonResponse({'result': 'loaning'})
    
    # 申請過了
    if LeaseProperty.objects.filter(borrower=user.__str__(), leaseProperty=result, status='w').first() != None:
        return JsonResponse({'result': 'duplicate'})

    leasing = LeaseProperty()
    leasing.leaseProperty = result
    leasing.borrower = user.__str__()
    leasing.save()

    """
        將提醒事件添加至資料表內
    """
    noti = Notification()
    noti.action = 'l'
    noti.action_user = user
    noti.action_date = datetime.datetime.now()
    noti.notify_group = Group.objects.filter(name="admin").first()
    noti.save()

    # 通知前端
    sendToAllGroup({"action": "newNotify"})

    return JsonResponse({'result': 'success'})

# 同意租借財產
# (需要租用財產權限 index.view_leaseproperty, index.change_leaseproperty, index.delete_leaseproperty, index.add_leaseproperty)
@API_CheckLogin
def agreeLoanProperty(request):
    user = request.user

    if not user.has_perm('index.view_leaseproperty') and not user.has_perm('index.change_leaseproperty') and not user.has_perm('index.delete_leaseproperty') and not user.has_perm('index.add_leaseproperty'):
        return JsonResponse({'result': 'permissionDeny'})

    # 取得序號以及產品編號
    leaseId = request.GET.get('id')
    agree = request.GET.get('agree')
    leasePropertyId = request.GET.get('leasePropertyId')

    print("財產:", leasePropertyId)

    if agree == "True":
        leasing = LeaseProperty.objects.filter(id=leaseId).first()
        leasing.borrow_administrator = user.__str__()
        leasing.agree_date = datetime.datetime.now()
        leasing.leaseProperty.status = 'o'
        leasing.status = 'l'
        leasing.leaseProperty.save()
        leasing.save()

        other_leasing = LeaseProperty.objects.exclude(id=leaseId).filter(leaseProperty__id=leasePropertyId)
        other_leasing.delete()
    else:
        leasing = LeaseProperty.objects.filter(id=leaseId).first()
        leasing.delete()



    return JsonResponse({'result': 'success'})

# 歸還財產
# (需要租用財產權限 index.add_lease_property)
# 會留下提醒
@API_CheckLogin
def returnProperty(request):
    user = request.user

    if not user.has_perm('index.add_leaseproperty'):
        return JsonResponse({'result': 'permissionDeny'})

    product_id = request.GET.get('id')
    
    if product_id == None:
        return JsonResponse({'result': 'empty'})

    leasing = LeaseProperty.objects.filter(id=product_id).first()
    
    if leasing == None:
        return JsonResponse({'result': 'empty'})

    if not(user.has_perm('index.change_leaseproperty') and user.has_perm('index.delete_leaseproperty') and user.has_perm('index.add_leaseproperty')) and not(user.__str__() == leasing.borrower.__str__()):
        return JsonResponse({'result': 'Unknow Error'})
    leasing.returner = user.__str__()
    leasing.status = 'c'
    leasing.save()

    """
        將提醒事件添加至資料表內，並通知所有前端管理員
    """
    noti = Notification()
    noti.action = 'r'
    noti.action_user = user
    noti.action_date = datetime.datetime.now()
    noti.notify_group = Group.objects.filter(name="admin").first()
    noti.save()

    # 通知前端
    sendToAllGroup({"action": "newNotify"})

    return JsonResponse({'result': 'success'})

# 同意歸還財產
# (需要租用財產權限)
@API_CheckLogin
def agreeReturnProperty(request):
    user = request.user
    
    if not user.has_perm('index.change_leaseproperty') and not user.has_perm('index.delete_leaseproperty') and not user.has_perm('index.add_leaseproperty'):
        return JsonResponse({'result': 'permissionDeny'})

    # 取得序號以及產品編號
    product_id = request.GET.get('id')
    agree = request.GET.get('agree')

    if product_id == None:
        return JsonResponse({'result': 'Failed'})

    # 將財產狀態改成可使用，並刪除當前借閱資料表中的資料
    # 將資料存到借閱歷史紀錄中
    if agree == "True":
        leasing = LeaseProperty.objects.filter(id=product_id).first()
        leasing.leaseProperty.status = 'a'
        leasing.leaseProperty.save()

        leaseHistory = LeaseHistory()
        leaseHistory.leasePropertyID = leasing.leaseProperty.id
        leaseHistory.leaseProperty = leasing.leaseProperty.__str__()
        leaseHistory.borrower = leasing.borrower.__str__()
        leaseHistory.borrow_date = leasing.borrow_date.__str__()
        leaseHistory.borrow_administrator = leasing.borrow_administrator.__str__()
        leaseHistory.agree_date = leasing.agree_date.__str__()
        leaseHistory.returner = leasing.returner.__str__()
        leaseHistory.returner_administrator = user.__str__()
        leaseHistory.return_date = datetime.datetime.now()
        leaseHistory.save()

        leasing.delete()
    else:
        leasing = LeaseProperty.objects.filter(id=product_id).first()
        leasing.status = 'l'
        leasing.save()
        return JsonResponse({'result': 'Disagree'})

    return JsonResponse({'result': 'success'})


"""
# 儲存檔案、刪除、取得全部、取得單一檔案
"""
# 儲存檔案
# (需要新增財產權限 index.add_property)
# 會留下提醒
@API_CheckLogin
def saveData(request):
    """
    # 儲存資料
    # (需要登入)
    # (need login)
    """
    user = request.user
    if not user.has_perm('index.add_property'):
        return HttpResponse(status=403)

    if request.POST.get('data') is None:
        # Check the data that client send is empty or not
        data = {'result': 'empty'}
        return JsonResponse(data)

    # try:
    print(f"\n{saveData.__name__ }() Loading data...")
    # Change the data format to json
    data = json.loads(request.POST.get('data'))
    duplicatePropertyList = []
    totalSaveData = []
    for singleProperty in data:
        product_number = singleProperty.get('product_number', -1)
        product_name   = singleProperty.get('product_name', 'None')
        is_check       = singleProperty.get('is_check', 'x')
        tip            = singleProperty.get('tip', '')
        number         = singleProperty.get('number', -1)
        get_date       = singleProperty.get('get_date', -1)
        quantity       = singleProperty.get('quantity', 1)
        age_limit      = singleProperty.get('age_limit', 0)
        single_value   = singleProperty.get('single_value', 0)

        # Foreign Key Part
        position       = singleProperty.get('position', 'None')
        label_position = singleProperty.get('label_position', 'None')
        brand          = singleProperty.get('brand', 'None')
        unit           = singleProperty.get('unit', 'None')

        try:
            int(age_limit)
        except:
            continue

        """
        # 檢查number以及product_number是否為空
        """
        if number == -1 or product_number == -1:
            raise Exception

        """
        # 若為不為V或X
        """
        if is_check != 'v' and is_check != 'x' and is_check != 'V' and is_check != 'X':
            is_check = 'x'
        

        """
        # 產品重複
        # 更新資訊
        """
        duplicate = Property.objects.filter(serial_number=number, property_number=product_number).first()
        if duplicate != None:
            # 檢查重複產品是否有盤點資料(沒有則創建)
            checkProp = CurrentCheckProperty.objects.filter(prop=duplicate)
            if not checkProp.exists():
                preCheckProp = CurrentCheckProperty()
                preCheckProp.status = 'x'
                preCheckProp.prop = duplicate
                preCheckProp.save()
            # 印出重複產品
            print(f"{ saveData.__name__ }() duplicated property { number } - { product_number } { product_name } found, update info...")
            # 更新的財產資訊添加至更新清單
            duplicatePropertyList.append({'number': number, 'product_number': product_number, 'product_name': product_name})
            continue
        
        """
        # 檢查品牌是否存在於資料庫內
        # 若無則新增品牌
        """
        if Brand.objects.filter(name=brand).first().__str__() == "None":
            print(f"{ saveData.__name__ }() Found new Brand { brand }, Adding to Database...")
            newBrand      = Brand()
            newBrand.name = brand
            newBrand.save()

        """
        # 檢查位置是否存在於資料庫內
        # 若無則新增位置
        """
        if Position.objects.filter(name=position).first().__str__() == "None":
            print(f"{ saveData.__name__ }() Found new Position { position }, Adding to Database...")
            newPosition      = Position()
            newPosition.name = position
            newPosition.save()
        if Position.objects.filter(name=label_position).first().__str__() == "None":
            print(f"{ saveData.__name__ }() Found new Position { label_position }, Adding to Database...")
            newPosition      = Position()
            newPosition.name = label_position
            newPosition.save()

        """
        # 檢查單位是否存在於資料庫內
        # 若無則新增單位
        """
        if Unit.objects.filter(name=unit).first().__str__() == "None":
            print(f"{ saveData.__name__ }() Found new Unit { unit }, Adding to Database...")
            newUnit      = Unit()
            newUnit.name = unit
            newUnit.save()

        """
        # 建立PreProperty物件存入資料
        """
        preSaveData = Property()
        preSaveData.property_number = product_number
        preSaveData.name            = product_name
        preSaveData.check           = is_check.lower()
        preSaveData.tips            = tip
        preSaveData.serial_number   = number
        preSaveData.quantity        = quantity

        # Change the day to isoformat
        try:
            if(len(get_date) == 6):
                preSaveData.get_date = f"{ int(get_date[0:2])+1911 }-{ get_date[2:4] }-{ get_date[4:6] }"
            else:
                preSaveData.get_date = f"{ int(get_date[0:3])+1911 }-{ get_date[3:5] }-{ get_date[5:7] }"
        except Exception as e:
            nowIosDate = datetime.datetime.now().strftime("%Y-%m-%d")
            preSaveData.get_date = nowIosDate
            print(f"{ saveData.__name__ }() 未知日期資料 { product_number } - { number } , { get_date }...使用目前日期{ nowIosDate }")

        preSaveData.expiry_date     = age_limit
        preSaveData.price           = single_value.replace(",", "")

        # Foreign key part
        preSaveData.position        = Position.objects.filter(name=position).first()
        preSaveData.label_position  = Position.objects.filter(name=label_position).first()
        preSaveData.brand           = Brand.objects.filter(name=brand).first()
        preSaveData.quantity_unit   = Unit.objects.filter(name=unit).first()
        totalSaveData.append(preSaveData)

        """
        # 建立盤點部分關聯資料
        """
        preCheckProp = CurrentCheckProperty()
        preCheckProp.status = is_check
        preCheckProp.prop = preSaveData
        preCheckProp.save()

    Property.objects.bulk_create(totalSaveData)
    # except Exception as e:
    #     exc_type, exc_obj, exc_tb = sys.exc_info()
    #     fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    #     print(exc_type, fname, exc_tb.tb_lineno)
    #     return JsonResponse({'result': 'failed'})

    """
        將提醒事件添加至資料表內
    """
    noti = Notification()
    noti.action = 'a'
    noti.action_user = user
    noti.action_date = datetime.datetime.now()
    noti.notify_group = Group.objects.filter(name="admin").first()
    noti.save()

    sendToAllGroup({"action": "newNotify"})

    print(f"{saveData.__name__ }() Done!\n")
    return JsonResponse({'result': 'success', 'duplicatelist': duplicatePropertyList})

# 儲存單一檔案帶圖片
# (需要新增財產權限 index.add_property)
# 會留下提醒
@API_CheckLogin
def saveSingleData(request):
    user = request.user
    if not user.has_perm('index.add_property'):
        return HttpResponse(status=403)

    # 從前端接收檔案
    files = request.FILES.get('file')
    # 必要訊息
    name = request.POST.get('name')
    number = request.POST.get('number')
    serial = request.POST.get('serial')
    # 附加詳細資料
    brand = request.POST.get('brand', '')
    position = request.POST.get('position', '')
    realPosition = request.POST.get('realPosition', '')
    tips = request.POST.get('tips', '')
    getDate = request.POST.get('getDate', '')
    expiryDate = request.POST.get('expiryDate', '')
    amount = request.POST.get('amount', '')
    price = request.POST.get('price', '')

    """""""""""""""""""""""""""""""""
        檢查重要資訊
    """""""""""""""""""""""""""""""""
    # 檢查名稱、流水號、編號
    Importantform = PropertyImportantForm(request.POST, request.FILES)
    if not Importantform.is_valid():
        # 資料缺失或格式不符
        return JsonResponse({
            'result': 'failed',
            'reason': 'InfoEmpty'
        })

    """""""""""""""""""""""""""""""""""""""""""""
        檢查重複
    """""""""""""""""""""""""""""""""""""""""""""
    if Property.objects.filter(property_number=number, serial_number=serial).exists():
        # 產品重複
        return JsonResponse({
            'result': 'failed',
            'reason': 'Duplicated'
        })
    
    """""""""""""""""""""""""""""""""""""""""""""
        檢查有外鍵之部分，外鍵是否存在
    """""""""""""""""""""""""""""""""""""""""""""
    brand = brand.replace(' ','')   # 去掉空白
    # 檢查品牌是否存在
    b = Brand.objects.filter(name=brand)
    if not b.exists():
        print(f"品牌不存在創建{brand}.")
        b = Brand.objects.create(name=brand)
        b.save()
    else: b = b.first()
    
    position = position.replace(' ','') # 去掉空白
    # 檢查位置是否存在
    p = Position.objects.filter(name=position)
    if not p.exists():
        print(f"位置不存在創建{position}.")
        p = Position.objects.create(name=position)
        p.save()
    else: p = p.first()
    
    realPosition = realPosition.replace(' ','') # 去掉空白
    # 檢查真實位置是否存在
    rp = Position.objects.filter(name=realPosition)
    if not rp.exists():
        print(f"真實位置不存在創建{realPosition}.")
        rp = Position.objects.create(name=realPosition)
        rp.save()
    else: rp = rp.first()
    
    """""""""""""""""""""""""""""""""""""""""""""
        檢查數字是否正確
    """""""""""""""""""""""""""""""""""""""""""""
    try:
        expiryDate = float(expiryDate)
        amount = float(amount)
        price = float(price)
    except Exception as e:
        expiryDate = 0
        amount = 0
        price = 0
        print("數字轉換錯誤...使用預設都為0")
    
    """""""""""""""""""""""""""""""""""""""""""""
        檢查日期是否正確
    """""""""""""""""""""""""""""""""""""""""""""
    try:
        year = int(getDate[:4])
        month = int(getDate[5:7])
        day = int(getDate[8:10])
        datetime.date(year, month, day)
    except Exception as e:
        getDate = datetime.datetime.now().strftime("%Y-%m-%d")
        print("日期格式不正確...使用預設當前日期")

    """""""""""""""""""""""""""""""""""""""""""""
    # 資訊暫時儲存
    """""""""""""""""""""""""""""""""""""""""""""
    prop = Property()
    prop.name = name
    prop.serial_number = serial
    prop.property_number = number
    prop.tips = tips
    prop.brand = b
    prop.position = rp
    prop.label_position = p
    prop.expiry_date = expiryDate
    prop.quantity = amount
    prop.price = price
    prop.get_date = getDate

    """""""""""""""""""""""""""""""""""""""""""""
    # 圖片檢查、確定有圖片上傳
    """""""""""""""""""""""""""""""""""""""""""""
    Imageform = PropertyImageForm(request.POST, request.FILES)
    # 若圖片不存在則上傳圖片，若重複則更新舊圖片
    if Imageform.is_valid():
        # 副檔名
        extension = re.findall(r".[a-zA-Z]+$", files._name)
        # 若檔案沒有副檔名
        if not extension:
            extension = ['.jpg']
        # 圖片於資料庫內的名稱
        imageName = name + serial + number
        # 更改檔名
        files._name = imageName + extension[0]
        imagePosition = os.path.abspath(os.getcwd()) + "/static/PropertyImage/"
        if os.path.isfile(imagePosition + files._name):
            os.remove(imagePosition + files._name)
            print(f"刪除原有圖檔{files._name}")

        pi = PropertyImage.objects.filter(image_name=imageName)
        if not pi.exists():
            pi = PropertyImage()
            pi.image = files
            pi.image_name = imageName
            pi.save()
        else:
            pi = pi.first()
            pi.image = files
            pi.save()
        prop.image = pi
    else: 
        print('沒有上傳圖片')

    """""""""""""""""""""""""""""""""""""""""""""
    # 寫入資料庫
    """""""""""""""""""""""""""""""""""""""""""""
    prop.save()

    """""""""""""""""""""""""""""""""""""""""""""
    # 建立盤點部分關聯資料
    """""""""""""""""""""""""""""""""""""""""""""
    preCheckProp = CurrentCheckProperty()
    preCheckProp.status = 'x'
    preCheckProp.prop = prop
    preCheckProp.save()

    """
        將提醒事件添加至資料表內
    """
    noti = Notification()
    noti.action = 'a'
    noti.action_user = user
    noti.action_date = datetime.datetime.now()
    noti.notify_group = Group.objects.filter(name="admin").first()
    noti.save()

    sendToAllGroup({"action": "newNotify"})

    return JsonResponse({'result': 'success'})

# 刪除財產
# (需要租刪除財產權限 index.delete_property)
# 會留下提醒
@API_CheckLogin
def deleteData(request):
    """
    # 取得單一資料
    # (需要登入以及可以刪除資料的權限)
    # (need login and permission)
    """
    
    user = request.user
    if not user.has_perm('index.delete_property'):
        return JsonResponse({'result': 'Permission Deny!'})

    # 取得序號以及產品編號
    property_id = request.GET.get('id')

    if property_id == None:
        return JsonResponse({'result': 'ID Error!'})

    result = Property.objects.filter(id=property_id).first()

    if result == None:
        return JsonResponse({'result': 'Not Found Property!'})

    if result.status.__str__() == 'o':
        return JsonResponse({'result': 'Property not return yet!'})

    result.delete()

    """
        將提醒事件添加至資料表內
    """
    noti = Notification()
    noti.action = 'd'
    noti.action_user = user
    noti.action_date = datetime.datetime.now()
    noti.notify_group = Group.objects.filter(name="admin").first()
    noti.save()

    sendToAllGroup({"action": "newNotify"})

    return JsonResponse({'result': 'success'})

# 取得財產資訊
@API_CheckLogin
def getData(request):
    """
    # 取得資料
    # (需要登入)
    # (need login)
    """
    # 獲取搜尋關鍵字
    searchKeyWord = request.GET.get('search')

    data = []
    # Change Property to python dictionary
    newsdata = Property.objects.all()
    # 檢查前端傳過來的資料
    # 根據關鍵字搜索欄位
    if(searchKeyWord != None and searchKeyWord != ''):
        # 搜索名稱、位置、產品編號、序號、備註、品牌
        qs1 = Property.objects.all().filter(name__icontains=searchKeyWord).all()
        qs2 = Property.objects.all().filter(position__name__icontains=searchKeyWord).all()
        qs3 = Property.objects.all().filter(property_number__icontains=searchKeyWord).all()
        qs4 = Property.objects.all().filter(serial_number__icontains=searchKeyWord).all()
        qs5 = Property.objects.all().filter(brand__name__icontains=searchKeyWord).all()
        qs6 = Property.objects.all().filter(tips__icontains=searchKeyWord).all()

        # 合并到一起
        qs = qs1 | qs2 | qs3 | qs4 | qs5 | qs6
        
        # 去重方法
        newsdata = qs.distinct()

    # Wrapper the data in json
    for singleProperty in newsdata:
        singleDict = {}
        # Wrapper the data
        singleDict.setdefault('id', singleProperty.id.__str__())
        singleDict.setdefault('is_check', singleProperty.check.__str__())
        singleDict.setdefault('product_name', singleProperty.name.__str__())
        singleDict.setdefault('number', singleProperty.serial_number.__str__())
        singleDict.setdefault('product_number', singleProperty.property_number.__str__())
        singleDict.setdefault('tip', singleProperty.tips.__str__())
        singleDict.setdefault('get_date', singleProperty.get_date.__str__())
        singleDict.setdefault('age_limit', singleProperty.expiry_date.__str__())
        singleDict.setdefault('quantity', singleProperty.quantity.__str__())
        singleDict.setdefault('single_value', singleProperty.price.__str__())

        # With foreign key filter
        singleDict.setdefault('position', singleProperty.position.__str__())
        singleDict.setdefault('brand', singleProperty.brand.__str__())
        singleDict.setdefault('label_position', singleProperty.label_position.__str__())
        singleDict.setdefault('unit', singleProperty.quantity_unit.__str__())
        singleDict.setdefault('status', singleProperty.status.__str__())

        if singleProperty.image != None:
            singleDict.setdefault('image', singleProperty.image.image.__str__())
        else:
            # https://i.imgur.com/3ZTDX.jpeg
            # https://i.imgur.com/WNL6utH.jpeg
            singleDict.setdefault('image', "https://i.imgur.com/WNL6utH.jpeg")

        data.append(singleDict)
    result = {'result': 'success', 'data': data}

    return JsonResponse(result)

# 取得單一財產資訊
@API_CheckLogin
def getSingleData(request):
    """
    # 取得單一資料
    # (需要登入)
    # (need login)
    """
    # 取得序號以及產品編號
    product_id = request.GET.get('id')

    if(product_id == '' or product_id == None):
        return JsonResponse({'result': 'error'})

    result = Property.objects.filter(id=product_id).first()
    if result == None:
        # 未找到資料
        return JsonResponse({'result': 'empty'})
    

    data = {}
    data.setdefault('id', result.id.__str__())
    data.setdefault('is_check', result.check.__str__())
    data.setdefault('product_name', result.name.__str__())
    data.setdefault('serial_number', result.serial_number.__str__())
    data.setdefault('property_number', result.property_number.__str__())
    data.setdefault('tip', result.tips.__str__())
    data.setdefault('status', result.status.__str__())
    data.setdefault('keeper', result.keeper.__str__())
    data.setdefault('price', result.price.__str__())
    data.setdefault('quantity', result.quantity.__str__())
    data.setdefault('get_date', result.get_date.__str__())
    data.setdefault('expiry_date', result.expiry_date.__str__())
    data.setdefault('position', result.position.__str__())
    data.setdefault('label_position', result.label_position.__str__())
    data.setdefault('brand', result.brand.__str__())
    data.setdefault('unit', result.quantity_unit.__str__())

    if result.image != None:
        data.setdefault('image', result.image.image.__str__())
    else:
        data.setdefault('image', "https://i.imgur.com/WNL6utH.jpeg")

    return JsonResponse({'result': 'success', 'data': data})

"""
# 盤點API
"""
@API_CheckLogin
def getCheckProperty(request):
    # Change Property to python dictionary
    newsdata = CurrentCheckProperty.objects.all()
    data = []
    for singleCheck in newsdata:
        singleProperty = singleCheck.prop
        singleDict = {}
        # Wrapper the data
        singleDict.setdefault('id', singleCheck.id.__str__())
        singleDict.setdefault('is_check', singleCheck.status.__str__())
        singleDict.setdefault('action_user', singleCheck.action_user.__str__())
        singleDict.setdefault('product_name', singleProperty.name.__str__())
        singleDict.setdefault('number', singleProperty.serial_number.__str__())
        singleDict.setdefault('product_number', singleProperty.property_number.__str__())
        singleDict.setdefault('tip', singleProperty.tips.__str__())
        singleDict.setdefault('get_date', singleProperty.get_date.__str__())
        singleDict.setdefault('age_limit', singleProperty.expiry_date.__str__())
        singleDict.setdefault('quantity', singleProperty.quantity.__str__())
        singleDict.setdefault('single_value', singleProperty.price.__str__())

        # With foreign key filter
        singleDict.setdefault('position', singleProperty.position.__str__())
        singleDict.setdefault('brand', singleProperty.brand.__str__())
        singleDict.setdefault('label_position', singleProperty.label_position.__str__())
        singleDict.setdefault('unit', singleProperty.quantity_unit.__str__())
        singleDict.setdefault('status', singleProperty.status.__str__())

        if singleProperty.image != None:
            singleDict.setdefault('image', singleProperty.image.image.__str__())
        else:
            singleDict.setdefault('image', "https://i.imgur.com/WNL6utH.jpeg")

        data.append(singleDict)
    result = {'result': 'success', 'data': data}

    return JsonResponse(result)

# 更改盤點狀態
# (需要登入)
# need Login
@API_CheckLogin
def changePropStatus(request):
    user = request.user
    data = json.loads(request.body.decode('utf-8'))
    checkProp = data['data']

    for check in checkProp:
        preSave = CurrentCheckProperty.objects.filter(id=check.get('id', 0))
        if not preSave.exists():
            continue

        preSave = preSave.first()
        preSave.action_user = user
        preSave.status = check.get('is_check', 'x')
        preSave.save()

    return JsonResponse({'result': 'success'})

@API_CheckLogin
def resetCheckProp(request):
    user = request.user
    if not UserInGroup(user, "admin"):
        return HttpResponse(status=403)

    allCheckProp = CurrentCheckProperty.objects.all()
    for checkProp in allCheckProp:
        checkProp.status = 'x'
        checkProp.action_user = None
        checkProp.save()

    return JsonResponse({'result': 'success'})