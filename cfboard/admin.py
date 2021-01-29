from django.contrib import admin
from cfboard.models import Cfboard, Boardcate, Boardcode
# Register your models here.

class CfboardAdmin(admin.ModelAdmin):
    list_display = ('title','writer')

class BoardcodeAdmin(admin.ModelAdmin):
    list_display = ('boardname',)

class BoardcateAdmin(admin.ModelAdmin):
    list_display = ('catename',)


admin.site.register(Cfboard,CfboardAdmin)
admin.site.register(Boardcode,BoardcodeAdmin)
admin.site.register(Boardcate,BoardcateAdmin)
