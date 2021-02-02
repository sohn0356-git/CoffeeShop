from django.contrib import admin
from cfboard.models import Cfboard, Boardcate, Boardcode, Boardcomment

# Register your models here.

class CfboardAdmin(admin.ModelAdmin):
    list_display = ('title','writer')

class BoardcodeAdmin(admin.ModelAdmin):
    list_display = ('boardname',)

class BoardcateAdmin(admin.ModelAdmin):
    list_display = ('catename',)

class BoardcommentAdmin(admin.ModelAdmin):
    list_display = ('board', 'user')


admin.site.register(Cfboard,CfboardAdmin)
admin.site.register(Boardcode,BoardcodeAdmin)
admin.site.register(Boardcate,BoardcateAdmin)
admin.site.register(Boardcomment,BoardcommentAdmin)
