from django import forms
from django.contrib import admin
from ghu_web.admin import admin_site
from ghu_global.forms import RichTextField, CheckboxBlanker
from .models import Page, PageTemplate, NavbarEntry
from ordered_model.admin import OrderedModelAdmin

class PageForm(forms.ModelForm):
    # Use CKEditor and hide the label
    contents = RichTextField()
    make_home_page = CheckboxBlanker()

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
