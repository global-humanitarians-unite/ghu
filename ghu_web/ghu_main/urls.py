from django.conf.urls import url
from ghu_main import views
from django.contrib.auth import views as auth_views

app_name = 'ghu_main'

urlpatterns = [
    url('^$', views.page, name='home'),
    url('^login/$', auth_views.login, name='login'),
    url('^logout/$', auth_views.logout, name='logout'),
    url('^register/$', views.register, name='register'),
    url('^organizations/$', views.organizations, name='organizations'),
    url('^toolkits/$', views.toolkits, name='toolkits'),
    url('^toolkit/(?P<slug>[a-zA-Z0-9_\-]+)/$', views.toolkit, name='toolkit'),
    url('^toolkit/(?P<toolkit_slug>[a-zA-Z0-9_\-]+)/(?P<toolkitpage_slug>[a-zA-Z0-9_\-]+)/$', views.toolkitpage, name='toolkitpage'),
    url('^profiles/(?P<slug>.+)/$', views.org_profile, name='profile'),
    url('^(?P<slug>.+)/$', views.page, name='page'),


]
