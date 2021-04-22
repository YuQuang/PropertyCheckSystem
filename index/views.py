from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from django.urls import reverse
from django.contrib.auth.models import User, Permission, Group
from django.contrib.auth.decorators import login_required
#
import json
import sys, os, datetime, asyncio
#
from .models import Property, Brand, Position, Unit, LeaseProperty, LeaseHistory, Notification
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
def stockTaking(request):
    return render(request, "stockTaking.html")


"""
#   Web API部分
#   Restfull API
#   WebAPI Part
"""


"""
# 租借與歸還、同意租借與同意歸還
"""
# 查詢租借財產
# (需要租用財產權限 index.view_lease_property)
@login_required
def getLoanProperty(request):
    user = request.user
    
    # 檢查用戶是否有借用的權限
    if not user.has_perm('index.view_leaseproperty'):
        return JsonResponse({'result': 'permission_deny'})

    waiting_data = []
    loaning_data = []
    waiting_return_data = []
    returned_data = []

    # 等待核准清單
    waiting_list = None
    if user.has_perm('index.change_leaseproperty') and user.has_perm('index.delete_leaseproperty'):
        waiting_list = LeaseProperty.objects.filter(status='w').all()
    else:
        waiting_list = LeaseProperty.objects.filter(status='w', borrower=user.__str__()).all()
    for waiting in waiting_list:
        waiting_dict = {}
        waiting_dict.setdefault("id", waiting.id.__str__())
        waiting_dict.setdefault("borrower", waiting.borrower.__str__())
        waiting_dict.setdefault("leaseProperty", waiting.leaseProperty.__str__())
        waiting_dict.setdefault("serial_number", waiting.leaseProperty.serial_number.__str__())
        waiting_dict.setdefault("product_number", waiting.leaseProperty.property_number.__str__())
        waiting_dict.setdefault("borrow_administrator", waiting.borrow_administrator.__str__())
        waiting_dict.setdefault("borrow_date", waiting.borrow_date.strftime("%Y-%m-%d"))

        waiting_data.append(waiting_dict)

    # 正在租借中的物品清單
    loaning_list = None
    if user.has_perm('index.change_leaseproperty') and user.has_perm('index.delete_leaseproperty'):
        loaning_list = LeaseProperty.objects.filter(status='l').all()
    else:
        loaning_list = LeaseProperty.objects.filter(status='l', borrower=user.__str__()).all()
    for loaning in loaning_list:
        loaning_dict = {}
        loaning_dict.setdefault("id", loaning.id.__str__())
        loaning_dict.setdefault("leaseProperty", loaning.leaseProperty.__str__())
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
    waiting_return_list = None
    if user.has_perm('index.change_leaseproperty') and user.has_perm('index.delete_leaseproperty'):
        waiting_return_list = LeaseProperty.objects.filter(status='c').all()
    else:
        waiting_return_list = LeaseProperty.objects.filter(status='c', returner=user.__str__()).all()
    for waiting_return in waiting_return_list:
        waiting_return_dict = {}
        waiting_return_dict.setdefault("id", waiting_return.id.__str__())
        waiting_return_dict.setdefault("leaseProperty", waiting_return.leaseProperty.__str__())
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
    returned_list = None
    if user.has_perm('index.change_leaseproperty') and user.has_perm('index.delete_leaseproperty'):
        returned_list = LeaseHistory.objects.all()
    else:
        returned_list = LeaseHistory.objects.filter(returner=user.__str__()).all()
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
@login_required
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
    sendToGroup({"action": "newNotify"}, "admin")

    return JsonResponse({'result': 'success'})

# 同意租借財產
# (需要租用財產權限 index.view_lease_property)
@login_required
def agreeLoanProperty(request):
    user = request.user

    if not user.has_perm('index.change_leaseproperty') and not user.has_perm('index.delete_leaseproperty') and not user.has_perm('index.add_leaseproperty'):
        return JsonResponse({'result': 'permissionDeny'})

    # 取得序號以及產品編號
    product_id = request.GET.get('id')
    agree = request.GET.get('agree')

    if agree == "True":
        leasing = LeaseProperty.objects.filter(id=product_id).first()
        leasing.borrow_administrator = user.__str__()
        leasing.agree_date = datetime.datetime.now()
        leasing.leaseProperty.status = 'o'
        leasing.status = 'l'
        leasing.leaseProperty.save()
        leasing.save()
    else:
        leasing = LeaseProperty.objects.filter(id=product_id).first()
        leasing.delete()


    return JsonResponse({'result': 'success'})

# 歸還財產
# (需要租用財產權限 index.add_lease_property)
# 會留下提醒
@login_required
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
    sendToGroup({"action": "newNotify"}, "admin")

    return JsonResponse({'result': 'success'})

# 同意歸還財產
# (需要租用財產權限)
@login_required
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
@login_required
def saveData(request):
    """
    # 儲存資料
    # (需要登入)
    # (need login)
    """
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
        # 產品重複
        # 更新資訊
        """
        if Property.objects.filter(serial_number=number, property_number=product_number).first() != None:
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
    Property.objects.bulk_create(totalSaveData)
    # except Exception as e:
    #     exc_type, exc_obj, exc_tb = sys.exc_info()
    #     fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    #     print(exc_type, fname, exc_tb.tb_lineno)
    #     return JsonResponse({'result': 'failed'})



    print(f"{saveData.__name__ }() Done!\n")
    return JsonResponse({'result': 'success', 'duplicatelist': duplicatePropertyList})

# 刪除財產
# (需要租刪除財產權限 index.delete_property)
@login_required
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

    return JsonResponse({'result': 'success'})

# 取得財產資訊
@login_required
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
@login_required
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
