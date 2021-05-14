from django.urls import path
from django.conf.urls import include
from . import views
from django.urls import re_path
from . import consumers, CheckConsumers


urlpatterns = [
    # Account Part
    path('accounts/', include('django.contrib.auth.urls')),


    # HomePage
    path('', view=views.index, name='index'),
    

    # 網頁部分
    path('importExcel/', views.importExcel, name='importExcel'),
    path('search', view=views.search, name='search'),
    path('addData/', views.addData, name='addData'),
    path('aboutUs/', views.aboutUs, name='aboutUs'),
    path('leaseProperty/', views.leaseProperty, name='leaseProperty'),
    path('stockTaking/', views.stockTaking, name='stockTaking'),
    path('profile/', views.profile, name='profile'),


    # 新版介面
    path('newpropertydetail', view=views.newPropertyDetail, name='newpropertydetail'),

    # 舊版搜尋介面
    path('oldsearch', view=views.oldSearch, name='oldsearch'),


    ###########
    # API部分 #
    ###########
    
    # 取得所有位置
    path('getPosition/', views.getPosition, name='getPosition'),
    path('getBrand/', views.getBrand, name='getBrand'),
    # 取得用戶資料
    path('getUserInfo/', views.getUserInfo, name='getUserInfo'),
    # 儲存資料
    path('saveData/', views.saveData, name='saveData'),
    path('saveSingleData', views.saveSingleData, name='saveSingleData'),
    # 取得資料、取得單一資料、刪除單筆資料
    path('getData/', views.getData, name='getData'),
    path('getSingleData/', views.getSingleData, name='getSingleData'),
    path('deleteData/', views.deleteData, name='deleteData'),
    # 取得 等待審核租借、租借中、等待審核歸還、已歸還
    path('getLoanProperty/', views.getLoanProperty, name='getLoanProperty'),
    # 歸還與租借
    path('loanProperty/', views.loanProperty, name='loanProperty'),
    path('returnProperty/', views.returnProperty, name='returnProperty'),
    # 同意歸還與同意租借
    path('agreeLoanProperty/', views.agreeLoanProperty, name='agreeLoanProperty'),
    path('agreeReturnProperty/', views.agreeReturnProperty, name='agreeReturnProperty'),
    # 盤點相關
    path('getCheckProperty/', views.getCheckProperty, name='getCheckProperty'),
    path('changePropStatus/', views.changePropStatus, name='changePropStatus'),
    path('resetCheckProp/', views.resetCheckProp, name='resetCheckProp'),
]
