from django import forms
from django.contrib import admin
from ghu_web.admin import admin_site
from ghu_global.forms import RichTextField, CheckboxBlanker
from .models import Page, PageTemplate, Toolkit, ToolkitPage, NavbarEntry, OrgProfile
from ordered_model.admin import OrderedModelAdmin, OrderedTabularInline

class PageForm(forms.ModelForm):
    # Use CKEditor and hide the label
    contents = RichTextField()
    # for the purpose of making the slug field blank out when you're working with the homepage
    make_home_page = CheckboxBlanker(target_field='slug', source_field='title')

    class Meta:
        model = Page
        exclude = []

@admin.register(OrgProfile, site=admin_site)
class OrgProfileAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    fields = ('name', 'slug', 'email', 'location', 'phone', 'summary', 'description')

@admin.register(Page, site=admin_site)
class PageAdmin(admin.ModelAdmin):
    form = PageForm
    prepopulated_fields = {'slug': ('title',)}
    fields = ('title', 'slug', 'make_home_page', 'contents', 'template')

@admin.register(PageTemplate, site=admin_site)
class PageTemplateAdmin(admin.ModelAdmin):
    pass

@admin.register(NavbarEntry, site=admin_site)
class NavbarEntryAdmin(OrderedModelAdmin):
    list_display = ('label', 'move_up_down_links')

class ToolkitPageForm(forms.ModelForm):
    # Use CKEditor and hide the label
    contents = RichTextField()

class ToolkitPageInline(OrderedTabularInline):
    model = ToolkitPage
    fields = ('move_up_down_links', 'title', 'slug', 'contents')
    readonly_fields = ('move_up_down_links',)
    form = ToolkitPageForm
    prepopulated_fields = {'slug': ('title',)}
    extra = 1

@admin.register(Toolkit, site=admin_site)
class ToolkitAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    fields = ('title', 'slug', 'summary')
    inlines = (ToolkitPageInline,)

    # Copy-pasted from django-ordered-model README:
    # https://github.com/bfirsh/django-ordered-model/blob/master/README.md#admin-integration
    def get_urls(self):
        urls = super().get_urls()
        for inline in self.inlines:
            if hasattr(inline, 'get_urls'):
                urls = inline.get_urls(self) + urls
        return urls
