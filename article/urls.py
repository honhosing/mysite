from django.urls import path
from . import views

urlpatterns = [
    # http://localhost:8000/article/
    path('', views.article_list, name='article_list'),
    # http://localhost:8000/article/1
    path('<int:article_pk>', views.article_detail, name='article_detail'),
    path('type/<int:article_type_pk>', views.articles_with_type, name='articles_with_type'),
    path('data/<int:year>/<int:month>', views.articles_with_date, name='articles_with_date'),
]
