from django.urls import path
from . import views
from btcbrowser.express import express
from btcbrowser.invitation import invitation, invitation2

urlpatterns = [
    path('', views.btcbrowser, name='btcbrowser'),
    path('get_blockchain_data', views.get_blockchain_data, name='get_blockchain_data'),
    path('test', views.test, name='test'),
    path('express', views.express, name="express"),
    path(r'^image/$', express.express_img, name="express_img"),
    path('halving', views.halving, name="halving"),
    path('bitcoin_orange', views.bitcoin_orange, name="bitcoin_orange"),
    # path('7gkd', views.qgkd, name="7gkd"),
    path('invitation',views.invitation, name="invitation"),
    path(r'^image2/$', invitation.invitation_img, name="invitation_img"),
    path('invitation2',views.invitation2, name="invitation2"),
    path(r'^image3/$', invitation2.invitation2_img, name="invitation2_img"),
]
