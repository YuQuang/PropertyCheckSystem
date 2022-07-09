from django.contrib import admin
from .models import Property, Position, Keeper, Unit, Brand, PropertyImage, LeaseProperty, LeaseHistory

# Register your models here.

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    # Display on the admin index
    list_display = [
        'check',
        'property_number',
        'serial_number',
        'name',
        'label_position',
        'position',
        'keeper',
        'brand',
        'get_date',
        'expiry_date',
        'quantity',
        'quantity_unit',
        'price',
        'fill_date',
        'status',
        ]
    # Search will be use
    search_fields = [
        'serial_number',
        'name'
        ]
    # Filter set
    list_filter = ['position','status',]
    # Defalt order by
    ordering = ['serial_number', 'name']
    # The field show in website
    fieldsets = (
        (None, {
            'fields': (
                    ('check', 'name',),
                    ('property_number','serial_number',),
                    ('label_position','position',),
                    ('keeper', 'brand',),
                    ('get_date','expiry_date',),
                )
        }),
        ('Quantiy Stauts', {
            'fields': (('quantity','quantity_unit','price'),),
        }),
        ('Tips', {
            'fields': (('tips',),),
        }),
        ('Reant Status', {
            'fields': ('status',)
        }),
        ('Property Image', {
            'fields': ('image',)
        }),
    )

@admin.register(LeaseProperty)
class LeasePropertyAdmin(admin.ModelAdmin):
    # Display on the admin index
    list_display = [
        'leaseProperty',
        'borrower',
        'borrow_administrator',
        'returner',
        'returner_administrator',
        'borrow_date',
        'agree_date',
        'return_date',
        ]
    # Search will be use
    search_fields = [
        'leaseProperty',
        'borrower',
        'borrow_administrator',
        'returner',
        'returner_administrator',
        ]
    # Defalt order by
    ordering = ['borrow_date', 'agree_date', 'return_date']

@admin.register(LeaseHistory)
class LeaseHistoryAdmin(admin.ModelAdmin):
        # Display on the admin index
    list_display = [
        'leaseProperty',
        'borrower',
        'borrow_administrator',
        'returner',
        'returner_administrator',
        'borrow_date',
        'agree_date',
        'return_date',
        ]
    # Search will be use
    search_fields = [
        'leaseProperty',
        'borrower',
        'borrow_administrator',
        'returner',
        'returner_administrator',
        ]
    # Defalt order by
    ordering = ['borrow_date', 'agree_date', 'return_date']
    
@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']
    # list_filter = ['name']
    ordering = ['id']

@admin.register(Keeper)
class KeeperAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']
    # list_filter = ['name']
    ordering = ['id']

@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']
    # list_filter = ['name']
    ordering = ['id']

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']
    # list_filter = ['name']
    ordering = ['id']

@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'image_name']
    ordering = ['id', 'image_name']

