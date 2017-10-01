from django.conf.urls import url
from ghu_main import views

app_name = 'ghu_main'

urlpatterns = [
    url('^$', views.page, name='home'),
    url('^toolkits/$', views.toolkits, name='toolkits'),
    url('^toolkit/(?P<slug>[a-zA-Z0-9_\-]+)/$', views.toolkit, name='toolkit'),
    url('^toolkit/(?P<toolkit_slug>[a-zA-Z0-9_\-]+)/(?P<toolkitpage_slug>[a-zA-Z0-9_\-]+)/$', views.toolkitpage, name='toolkitpage'),
    url('^(?P<slug>.+)/$', views.page, name='page'),
]
