from django.contrib import admin
from ghu_web.admin import admin_site
from .models import Page

@admin.register(Page, site=admin_site)
class PageAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
