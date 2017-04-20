from django.conf.urls import url
from hu_browser import views

app_name = 'hu_browser'

urlpatterns = [
    url('^$', views.home, name='home'),
    url('^about/$', views.about, name='about'),
    url('^orgs/$', views.orgs, name='orgs'),
    url('^forum/$', views.forum, name='forum'),
]
