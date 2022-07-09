from django.db import models
from django.contrib.auth.models import User, Group
from django.utils import timezone
import uuid

"""
# The Keeper Table
# 保管人資料表
"""
class Keeper(models.Model):
    id = models.AutoField(
            primary_key=True,
            editable=False
        )
    
    name = models.CharField(
            max_length=100,
            verbose_name='管理人',
            help_text='Enter Keeper',
            blank=True,
            null=False,
            unique=True,
            default='None'
        )

    # Metadata
    class Meta:
        verbose_name = '管理人'
        verbose_name_plural = '管理人'

    def __str__(self):
        return f'{self.name}'

"""
# The Position Table
# 位置資料表
"""
class Position(models.Model):
    id = models.AutoField(
            primary_key=True,
            editable=False
        )
    name = models.CharField(
            max_length=100,
            verbose_name='位置',
            help_text='Enter Postion',
            null=False,
            unique=True,
            default='None'
        )

    # Metadata
    class Meta:
        verbose_name = '位置'
        verbose_name_plural = '位置'
    
    def __str__(self):
        return f'{self.name}'

"""
# The Unit Table
# 單位資料表
"""
class Unit(models.Model):
    id = models.AutoField(
            primary_key=True,
            editable=False
        )
    name = models.CharField(
            max_length=100,
            verbose_name='單位',
            help_text='Enter Unit',
            null=False,
            unique=True,
            default='None'
        )

    # Metadata
    class Meta:
        verbose_name = '單位'
        verbose_name_plural = '單位'
    
    def __str__(self):
        return f'{self.name}'

"""
# The Brand Table
# 品牌資料表
"""
class Brand(models.Model):
    id = models.AutoField(
            primary_key=True,
            editable=False
        )
    name = models.CharField(
            max_length=100,
            verbose_name='品牌',
            help_text='Enter Unit',
            null=False,
            unique=True,
            default='None'
        )

    # Metadata
    class Meta:
        verbose_name = '品牌'
        verbose_name_plural = '品牌'
    
    def __str__(self):
        return f'{self.name}'

"""
# The Property Image
# 財產圖片
"""
class PropertyImage(models.Model):
    id = models.AutoField(
            primary_key=True,
            editable=False
        )
    image_name = models.CharField(
            max_length=100,
            verbose_name='財產圖片名稱',
            help_text='Enter Image Name',
            null=False,
            unique=True,
            default='None'
        )
    image = models.ImageField(
            upload_to='static/PropertyImage',
            verbose_name='財產圖片',
        )

    # Metadata
    class Meta:
        verbose_name = '財產圖片'
        verbose_name_plural = '財產圖片'

    def __str__(self):
        return f'{self.image_name}'

"""
# The Property Table
# 財產資料表
"""
class Property(models.Model):
    # Property ID
    id = models.AutoField(
            primary_key=True,
        )
    # Is Checked or not
    CHECK_STATUS = (
        ('v', 'Checked'),
        ('x', 'NotChecked'),
        )
    check = models.CharField(
        max_length=1,
        choices=CHECK_STATUS,
        verbose_name='盤點',
        default='x',
        help_text='Property is checked',
        )
    property_number = models.CharField(
            max_length=50,
            verbose_name='財產編號',
            help_text='Enter property number',
            null=False,
            default="",
        )
    serial_number = models.CharField(
        max_length=50,
        verbose_name='序號',
        help_text='Enter serial number',
        null=False,
        )
    name = models.CharField(
            max_length=100,
            verbose_name='財產名稱',
            help_text='Enter property name',
            null=False
        )
    get_date = models.DateField(
            auto_created=True,
            verbose_name='獲取日期',
            default=timezone.now,
            null=False,
            help_text='The day that you get the property'
        )
    expiry_date = models.PositiveIntegerField(
            default=1,
            verbose_name='年限',
            null=False,
            help_text='years',
        )
    keeper = models.ForeignKey(
            'Keeper',
            verbose_name='管理人',
            help_text='Choose Keeper',
            null=True,
            blank=True,
            on_delete=models.SET_NULL,
        )
    label_position = models.ForeignKey(
            'Position',
            verbose_name='產貼位置',
            on_delete=models.PROTECT,
            default=1,
            related_name='label_position'
        )
    position = models.ForeignKey(
            'Position',
            verbose_name='位置',
            on_delete=models.PROTECT,
            default=1,
            related_name='position'
        )
    quantity = models.PositiveIntegerField(
            verbose_name='數量',
            default=1,
        )
    quantity_unit = models.ForeignKey(
            'Unit',
            verbose_name='單位',
            on_delete=models.PROTECT,
            help_text='Choose Quantity Unit',
            default=1,
        )
    brand = models.ForeignKey(
            'Brand',
            verbose_name='品牌',
            on_delete=models.PROTECT,
            help_text='Choose Brand',
            default=1,
        )
    price = models.PositiveIntegerField(
            verbose_name='價格',
            default=0,
        )
    tips  = models.TextField(
            verbose_name='Tips',
            null=True,
            blank=True,
            default="",
        )
    fill_date = models.DateTimeField(
            auto_created=True,
            verbose_name='填寫日期',
            auto_now_add=True
        )
    # The property status
    LOAN_STATUS = (
            ('o', 'On loan'),
            ('a', 'Available'),
            ('r', 'Reserved'),
        )
    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        verbose_name='現在狀態',
        default='a',
        help_text='Property availability',
        )
    image = models.ForeignKey(
        'PropertyImage',
        verbose_name='財產圖片',
        on_delete=models.CASCADE,
        null=True,
        blank=True
        )

    # Metadata
    class Meta:
        ordering = ['serial_number']
        verbose_name = '財產信息'
        verbose_name_plural = '財產'

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.name}'

"""
# The Lease Table
# 租借表(等待歸還後便會存至永久記錄)
"""
class LeaseProperty(models.Model):
    id = models.AutoField(
            primary_key=True,
        )
    leaseProperty = models.ForeignKey(
            'Property',
            verbose_name='財產',
            on_delete=models.CASCADE,
            help_text='Choose Property',
            default=1,
        )
    borrower = models.CharField(
            max_length=100,
            verbose_name='借用者',
            help_text='借用者名稱',
            null=False
        )
    borrow_administrator = models.CharField(
            max_length=100,
            verbose_name='借用管理員',
            help_text='借用管理員名稱',
            null=True,
            blank=True
        )
    returner = models.CharField(
            max_length=100,
            verbose_name='歸還者',
            help_text='歸還者名稱',
            null=True,
            blank=True
        )
    returner_administrator = models.CharField(
            max_length=100,
            verbose_name='歸還管理員',
            help_text='歸還管理員名稱',
            null=True,
            blank=True
        )
    borrow_date = models.DateTimeField(
            auto_created=True,
            verbose_name='借用日期',
            auto_now_add=True,
        )
    agree_date = models.DateTimeField(
            auto_created=True,
            verbose_name='同意日期',
            null=True,
            blank=True
        )
    return_date = models.DateTimeField(
            auto_created=True,
            verbose_name='歸還日期',
            null=True,
            blank=True
        )

    # The property status
    LOAN_STATUS = (
        ('w', 'Waiting'),
        ('l', 'Loaning'),
        ('c', 'checkReturn'),
        ('r', 'Returned'),
        )
    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        verbose_name='現在狀態',
        default='w',
        help_text='Now Status',
        )

    # Metadata
    class Meta:
        ordering = ['borrow_date']
        verbose_name = '租借'
        verbose_name_plural = '租借清單'

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.borrower}, {self.leaseProperty}'

"""
# The Lease History
# 租借紀錄(永久)
"""
class LeaseHistory(models.Model):
    id = models.AutoField(
            primary_key=True,
        )
    leaseProperty = models.CharField(
            max_length=100,
            verbose_name='財產',
            help_text='財產名稱',
            default="",
        )
    leasePropertyID = models.IntegerField(
            verbose_name='財產ID',
            help_text='財產ID',
            default=1,
        )
    borrower = models.CharField(
            max_length=100,
            verbose_name='借用者',
            help_text='借用者名稱',
            default="",
        )
    borrow_administrator = models.CharField(
            max_length=100,
            verbose_name='借用管理員',
            default="",
            help_text='借用管理員名稱',
        )
    returner = models.CharField(
            max_length=100,
            verbose_name='歸還者',
            help_text='歸還者名稱',
            default="",
        )
    returner_administrator = models.CharField(
            max_length=100,
            verbose_name='歸還管理員',
            help_text='歸還管理員名稱',
            default="",
        )
    borrow_date = models.DateTimeField(
            auto_created=True,
            verbose_name='借用日期',
            default=timezone.now
        )
    agree_date = models.DateTimeField(
            auto_created=True,
            verbose_name='同意日期',
            default=timezone.now
        )
    return_date = models.DateTimeField(
            auto_created=True,
            verbose_name='歸還日期',
            default=timezone.now
        )

    # Metadata
    class Meta:
        ordering = ['borrow_date']
        verbose_name = '租借歷史'
        verbose_name_plural = '租借歷史紀錄'

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.borrower}, {self.leaseProperty}'

"""
# The Notification
# 提醒資料表，儲存用戶近期各種動作
"""
class Notification(models.Model):
    id = models.AutoField(
            primary_key=True,
        )
    # 動作代碼
    USER_ACTION = (
        ('n', 'notknown'),
        ('d', 'deleteData'),
        ('a', 'addData'),
        ('m', 'modifyData'),
        ('l', 'loanProperty'),
        ('r', 'ReturnProperty'),
        ('i', 'importExcel'),
        ('y', 'agreeLoan'),
        ('x', 'notAgreeLoan'),
        ('q', 'resetCheckProp'),
        ('w', 'loadCheckProp'),
        )
    # 用戶動作
    action = models.CharField(
            max_length=1,
            choices=USER_ACTION,
            verbose_name='用戶動作',
            default='n',
        )
    notify_group = models.ForeignKey(
        Group,
        verbose_name='群組',
        on_delete=models.CASCADE,
        default=1,
        )
    action_user = models.ForeignKey(
            User,
            verbose_name='用戶',
            on_delete=models.CASCADE,
            default=1,
        )
    action_date = models.DateTimeField(
            auto_created=True,
            verbose_name='動作日期',
            default=timezone.now
        )
    # 訊息狀態
    READ_STATUS = (
        ('r', 'Read'),
        ('n', 'notRead'),
        )
    status = models.CharField(
            max_length=1,
            choices=READ_STATUS,
            verbose_name='訊息狀態',
            default='n',
        )
    group_status = models.CharField(
            max_length=1,
            choices=READ_STATUS,
            verbose_name='群體訊息狀態',
            default='n',
        )

"""
# The CurrentCheckProperty
# 當前盤點儲存表單
"""
class CurrentCheckProperty(models.Model):
    id = models.AutoField(
            primary_key=True,
        )
    # 哪項產品
    prop = models.ForeignKey(
            'Property',
            verbose_name='產品',
            on_delete=models.CASCADE,
            default=1,
        )
    # 狀態代碼
    STATUS_CODE = (
            ('v', 'Checked'),
            ('x', 'NotChecked'),
            ('m', 'Missing'),
            ('b', 'Broken'),
            ('o', 'Obsolete'),
        )
    status = models.CharField(
            max_length=1,
            choices=STATUS_CODE,
            verbose_name='當前盤點物品狀態',
            default='x',
        )
    # 最後做動作的使用者
    action_user = models.ForeignKey(
            User,
            verbose_name='用戶',
            on_delete=models.SET_NULL,
            null=True,
            blank=True,
        )

"""
# The Status of everyCheck
# 每一次盤點的統計狀態
"""
class CheckPropertyStatisticHistory(models.Model):
    id = models.AutoField(
            primary_key=True,
        )
    save_date = models.DateTimeField(
            auto_now_add=True,
        )
    modify_date = models.DateTimeField(
            auto_created=True,
            verbose_name='最後修改日期',
            default=timezone.now
        )
    tips = models.CharField(
            max_length=50,
            verbose_name='備註',
            null=True,
            blank=True,
        )

"""
# The CheckPropertyHistory
# 歷史盤點表單
"""
class CheckPropertyHistory(models.Model):
    id = models.AutoField(
            primary_key=True,
        )
    # 哪項產品
    prop = models.ForeignKey(
            'Property',
            verbose_name='產品',
            on_delete=models.CASCADE,
            default=1,
        )
    # 狀態代碼
    STATUS_CODE = (
            ('v', 'Checked'),
            ('x', 'NotChecked'),
            ('m', 'Missing'),
            ('b', 'Broken'),
            ('o', 'Obsolete'),
        )
    status = models.CharField(
            max_length=1,
            choices=STATUS_CODE,
            verbose_name='當前盤點物品狀態',
            default='x',
        )
    # 最後做動作的使用者
    action_user = models.ForeignKey(
            User,
            verbose_name='用戶',
            on_delete=models.SET_NULL,
            null=True,
            blank=True,
        )
    # 第幾次盤點
    checkID = models.ForeignKey(
            CheckPropertyStatisticHistory,
            verbose_name='盤點第幾次',
            on_delete=models.CASCADE,
        )
