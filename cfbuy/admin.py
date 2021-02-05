from django.contrib import admin
from cfbuy.models import *
# Register your models here.


class CfbuyAdmin(admin.ModelAdmin):
    list_display = ('id', 'buyer', 'roadAddress', 'buy_date' )

class BuydetailAdmin(admin.ModelAdmin):
    list_display = ('id', 'buy_info')

class ShoppingbasketAdmin(admin.ModelAdmin):
    list_display = ('id', 'buyer')
    
class BasketdetailAdmin(admin.ModelAdmin):
    list_display = ('id', 'basket')

class CfselectAdmin(admin.ModelAdmin):
    list_display = ('cfoption', 'buy', 'basket')


admin.site.register(Cfbuy,CfbuyAdmin)
admin.site.register(Buydetail,BuydetailAdmin)
admin.site.register(Shoppingbasket,ShoppingbasketAdmin)
admin.site.register(Basketdetail,BasketdetailAdmin)
admin.site.register(Cfselect,CfselectAdmin)
