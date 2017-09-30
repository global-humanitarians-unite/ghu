from django import forms
from django.contrib import admin
from ghu_web.admin import admin_site
from ghu_global.forms import RichTextField
from .models import Page, PageTemplate, Toolkit, ToolkitPage, NavbarEntry
from ordered_model.admin import OrderedModelAdmin

class PageForm(forms.ModelForm):
    # Use CKEditor and hide the label
    contents = RichTextField()

    class Meta:
        model = Page
        exclude = []

@admin.register(Page, site=admin_site)
class PageAdmin(admin.ModelAdmin):
    form = PageForm
    prepopulated_fields = {'slug': ('title',)}

@admin.register(PageTemplate, site=admin_site)
class PageTemplateAdmin(admin.ModelAdmin):
    pass

@admin.register(NavbarEntry, site=admin_site)
class NavbarEntryAdmin(OrderedModelAdmin):
    list_display = ('label', 'move_up_down_links')

@admin.register(Toolkit, site=admin_site)
class ToolkitAdmin(admin.ModelAdmin):
    pass

@admin.register(ToolkitPage, site=admin_site)
class ToolkitPageAdmin(admin.ModelAdmin):
    pass
