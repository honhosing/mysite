from django.contrib import admin
from .models import ArticleType, Article#, ReadNum

# Register your models here.
@admin.register(ArticleType)
class ArticleTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'type_name')

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'article_type', 'get_read_num', 'author', 'created_time', 'last_updated_time')

