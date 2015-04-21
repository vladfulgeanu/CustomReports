from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns('',

    url(r'^$', views.index, name='index'),
    url(r'^dashboard$', views.dashboard, name='dashboard'),
)