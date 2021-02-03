from django.contrib import admin
from cfbuy.models import *
# Register your models here.


class BuyAdmin(admin.ModelAdmin):
    list_display = ('buyer', 'address', 'buy_date' )

class BuydetailAdmin(admin.ModelAdmin):
    list_display = ('id', )

class ShoppingbasketAdmin(admin.ModelAdmin):
    list_display = ('id', )
    
class BasketdetailAdmin(admin.ModelAdmin):
    list_display = ('id', )

class CfselectAdmin(admin.ModelAdmin):
    list_display = ('id', )


admin.site.register(Buy,BuyAdmin)
admin.site.register(Buydetail,BuydetailAdmin)
admin.site.register(Shoppingbasket,ShoppingbasketAdmin)
admin.site.register(Basketdetail,BasketdetailAdmin)
admin.site.register(Cfselect,CfselectAdmin)
