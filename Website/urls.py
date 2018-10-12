from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
import views

urlpatterns = [
	url(r'^$', views.index, name = 'index'),
	url(r'^scanCard/$', views.scanCard, name = 'scanCard'),
	url(r'^transactionFinal/$', views.transactionFinal, name = 'transactionFinal'),
	url(r'^pendingFunds/$', views.pendingFunds, name = 'pendingFunds'),
	url(r'^payPending/$', views.payPending, name = 'payPending'),
]
