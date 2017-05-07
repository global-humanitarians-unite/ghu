from django.conf.urls import url
from ghu_toolkits import views

app_name = 'ghu-toolkits'

urlpatterns = [
    url('^$', views.home, name='home'),
]
