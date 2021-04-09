from django.urls import path
from .import views


urlpatterns = [
    path('', views.main),
    path('create', views.create),
    path('login', views.login),
    path('wall', views.wall),
    path('new_message', views.message),
    path('new_comment', views.comment),
    path('delete/<msgid>', views.delete_msg),
    path('delete/<cmtid>', views.delete_cmt)
]
