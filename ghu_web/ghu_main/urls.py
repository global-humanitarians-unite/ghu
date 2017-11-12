from django.conf.urls import url
from ghu_main import views
from django.contrib.auth import views as auth_views

app_name = 'ghu_main'

urlpatterns = [
    url(r'^$', views.page, name='home'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^register/$', views.register, name='register'),
    url(r'^register/activate/(?P<uid>[0-9A-Za-z_\-]+)/'
        r'(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    url(r'^organizations/$', views.organizations, name='organizations'),
    url(r'^toolkits/$', views.toolkits, name='toolkits'),
    url(r'^toolkit/(?P<slug>[a-zA-Z0-9_\-]+)/$', views.toolkit, name='toolkit'),
    url(r'^toolkit/(?P<toolkit_slug>[a-zA-Z0-9_\-]+)/(?P<toolkitpage_slug>[a-zA-Z0-9_\-]+)/$', views.toolkitpage, name='toolkitpage'),
    url(r'^profiles/(?P<slug>.+)/$', views.org_profile, name='profile'),
    url(r'^(?P<slug>.+)/$', views.page, name='page'),
]
