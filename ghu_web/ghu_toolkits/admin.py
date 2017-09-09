from django.contrib import admin
from ghu_web.admin import admin_site
from .models import ToolkitSection, Toolkit

@admin.register(Toolkit, site=admin_site)
class ToolkitAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

@admin.register(ToolkitSection, site=admin_site)
class ToolkitSectionAdmin(admin.ModelAdmin):
    pass
