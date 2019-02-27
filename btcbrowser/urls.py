from django.urls import path
from . import views
from btcbrowser.express import express

urlpatterns = [
    path('', views.btcbrowser, name='btcbrowser'),
    path('get_blockchain_data', views.get_blockchain_data, name='get_blockchain_data'),
    path('test', views.test, name='test'),
    path('express', views.express, name="express"),
    # path('express_img', express.express_img, name="express_img"),
    path(r'^image/$', express.express_img, name="express_img"),

]
