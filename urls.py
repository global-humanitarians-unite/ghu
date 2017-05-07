from django.conf.urls import url
from hu_browser import views

app_name = 'ghu-toolkits'

urlpatterns = [
    url('^toolkits/$', views.home, name='home'),
]
