from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^makepost$', views.makePost, name='makePost'),
    url(r'^makecomment$', views.makeComment, name='makeComment'),
    url(r'^deletepost$', views.deletePost, name="deletePost")
]