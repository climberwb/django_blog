from django.conf.urls import url
from django.contrib import admin


from .views import (
   
    # comment_delete,
    comment_thread,
)

urlpatterns = [
 
    url(r'^(?P<id>\d+)/$', comment_thread, name='thread'),
 
    # url(r'^(?P<slug>[\w-]+)/delete/$', comment_delete),
    #     #url(r'^comments/$', "<appname>.views.<function_name>"),
]


