from django.contrib import admin
from .models import ToolkitSection, Toolkit

class ToolkitAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(ToolkitSection)
admin.site.register(Toolkit, ToolkitAdmin)
