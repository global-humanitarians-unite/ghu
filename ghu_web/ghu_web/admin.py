from django.contrib.admin import AdminSite

class GHUAdminSite(AdminSite):
    """
    A subclass of AdminSite (of which django.contrib.admin.site is an
    instance) which customizes branding constants that the built-in
    admin templates use. Without this approach, I'd have to override an
    admin/ template to change the values the template inserts, which
    would duplicate a lot of code for little benefit. But unfortunately,
    taking the subclassing approach means we need to register models in
    the admin.py of each app with:

        from ghu_web.admin import admin_site
        admin_site.register(...)

    instead of the standard:

        from django.contrib import admin
        admin.site.register(...)

    so, for example, because django.contrib.auth.admin has the latter
    rather than the former, we'll need to manually register the
    django.contrib.auth.Group model below. (But not the
    django.contrib.auth.User, since we subclass that in
    ghu_global.models and register it in ghu_global.admin in the first
    way.)
    """

    site_title = 'GHU Admin'
    site_header = 'Global Humanitarians Unite Administration'
    index_title = 'GHU Administration'

admin_site = GHUAdminSite()

# Register our admin site with the built-in Django Group model.
# (ghu_global.admin will register its own subclass of User, so we don't
#  need to do it here.)
from django.contrib.auth.models import Group
from django.contrib.auth.admin import GroupAdmin
admin_site.register(Group, GroupAdmin)
