from django.contrib.auth.admin import UserAdmin
from ghu_web.admin import admin_site
from .models import User

admin_site.register(User, UserAdmin)
