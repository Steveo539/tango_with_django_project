from django.conf.urls import url
from django.contrib import admin
from rango import views
admin.autodiscover()
urlpatterns = [
url(r'^$', views.index, name='index'),
url(r'^$')
]
