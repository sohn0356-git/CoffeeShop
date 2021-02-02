from django.contrib import admin
from cfproduct.models import *
# Register your models here.

class BuyAdmin(admin.ModelAdmin):
    list_display = ('buy_info',)

class BuyInfoAdmin(admin.ModelAdmin):
    list_display = ('buyer',)

class CoffeecodeAdmin(admin.ModelAdmin):
    list_display = ('cfcode',)

class CfproductAdmin(admin.ModelAdmin):
    list_display = ('name', )


admin.site.register(Buy,BuyAdmin)
admin.site.register(BuyInfo,BuyInfoAdmin)
admin.site.register(Coffeecode,CoffeecodeAdmin)
admin.site.register(Cfproduct,CfproductAdmin)