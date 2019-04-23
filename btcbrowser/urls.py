from django.urls import path
from . import views
from btcbrowser.express import express

urlpatterns = [
    path('', views.btcbrowser, name='btcbrowser'),
    path('get_blockchain_data', views.get_blockchain_data, name='get_blockchain_data'),
    path('test', views.test, name='test'),
    path('express', views.express, name="express"),
    path(r'^image/$', express.express_img, name="express_img"),
    path('halving', views.halving, name="halving"),
    path('bitcoin_orange', views.bitcoin_orange, name="bitcoin_orange"),
    path('7gkd', views.qgkd, name="7gkd"),
]
