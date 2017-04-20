from django.conf.urls import url
from uh_browser import views

app_name = 'uh_browser'

urlpatterns = [
    url('^$', views.home, name='home'),
    url('^about/$', views.about, name='about'),
    url('^orgs/$', views.orgs, name='orgs'),
    url('^forum/$', views.forum, name='forum'),
]
