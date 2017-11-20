from django.conf.urls import url
from . import views
 
urlpatterns = [
    url(r'^$', views.index),
    url(r'^keyboard/', views.keyboard),
    url(r'^message', views.message),
    #url(r'^action', views.action),
]