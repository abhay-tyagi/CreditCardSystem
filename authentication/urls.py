from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
	url(r'^signin/(?P<arg>[\w\-]+)/$', views.signin, name='signin'),
	url(r'^signup/$', views.signup, name='signup'),
	url(r'^signout/$', views.signout, name='signout'),
]
