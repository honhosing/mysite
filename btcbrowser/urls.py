from django.urls import path
from . import views

urlpatterns = [
    path('', views.btcbrowser, name='btcbrowser'),
    path('get_blockchain_data', views.get_blockchain_data, name='get_blockchain_data')
]
