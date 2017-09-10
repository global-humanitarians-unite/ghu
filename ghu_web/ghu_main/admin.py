from django import forms
from django.contrib import admin
from ghu_web.admin import admin_site
from ghu_global.forms import RichTextField
from .models import Page

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
