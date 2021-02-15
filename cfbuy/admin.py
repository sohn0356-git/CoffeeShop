from django.contrib import admin
from cfbuy.models import *
# Register your models here.


class CfbuyAdmin(admin.ModelAdmin):
    list_display = ('id', 'buyer', 'address')

class BuydetailAdmin(admin.ModelAdmin):
    list_display = ('id', 'buy_info')
    
class BasketdetailAdmin(admin.ModelAdmin):
    list_display = ('id',)

class CfselectAdmin(admin.ModelAdmin):
    list_display = ('id', 'cfoption', 'buy', 'basket')


admin.site.register(Cfbuy,CfbuyAdmin)
admin.site.register(Buydetail,BuydetailAdmin)
admin.site.register(Basketdetail,BasketdetailAdmin)
admin.site.register(Cfselect,CfselectAdmin)
