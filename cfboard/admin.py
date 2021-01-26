from django.contrib import admin
from cfboard.models import Cfboard, Boardcate, Boardcode
# Register your models here.

class CfboardAdmin(admin.ModelAdmin):
    list_display = (Cfboard.title,)

# class BoardcodeAdmin(admin.ModelAdmin):
#     list_display = (Boardcode.boardname,)

# class BoardcateAdmin(admin.ModelAdmin):
#     list_display = (Boardcate.catename,)


# admin.site.register(Cfboard,CfboardAdmin)
