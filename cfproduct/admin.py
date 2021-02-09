from django.contrib import admin
from cfproduct.models import *
# Register your models here.


class CoffeecodeAdmin(admin.ModelAdmin):
    list_display = ('cfcode',)

class CfproductAdmin(admin.ModelAdmin):
    list_display = ('name', )

class OpcodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', )
    
class CftoOptionAdmin(admin.ModelAdmin):
    list_display = ('id','option_id', 'amount', 'coffee_id')

class CfoptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'code_option', 'option')

class CfcommentAdmin(admin.ModelAdmin):
    list_display = ('coffee', 'user')


admin.site.register(Coffeecode,CoffeecodeAdmin)
admin.site.register(Cfproduct,CfproductAdmin)
admin.site.register(Cfoption,CfoptionAdmin)
admin.site.register(CftoOption,CftoOptionAdmin)
admin.site.register(Opcode,OpcodeAdmin)
admin.site.register(Cfcomment,CfcommentAdmin)
