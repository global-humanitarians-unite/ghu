from django.conf.urls import url
from ghu_main import views

app_name = 'ghu_main'

urlpatterns = [
    url('^$', views.page, name='home'),
    url('^toolkits/$', views.toolkits, name='toolkits'),
    url('^(?P<slug>.+)/$', views.page, name='page'),
]
