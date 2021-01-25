from django.contrib import admin
from cfuser.models import Cfuser

# Register your models here.

class CfuserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')
    list_filter = ('register_date',)

admin.site.register(Cfuser, CfuserAdmin)
