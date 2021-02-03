from django.contrib import admin
from cfproduct.models import *
# Register your models here.


class CoffeecodeAdmin(admin.ModelAdmin):
    list_display = ('cfcode',)

class CfproductAdmin(admin.ModelAdmin):
    list_display = ('name', )

class CfoptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', )
    
class CftoOptionAdmin(admin.ModelAdmin):
    list_display = ('id','option_id', 'coffee_id')

class OptiondetailAdmin(admin.ModelAdmin):
    list_display = ('id', 'option_id', 'option')


admin.site.register(Coffeecode,CoffeecodeAdmin)
admin.site.register(Cfproduct,CfproductAdmin)
admin.site.register(Cfoption,CfoptionAdmin)
admin.site.register(CftoOption,CftoOptionAdmin)
admin.site.register(Optiondetail,OptiondetailAdmin)
