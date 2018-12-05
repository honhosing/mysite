from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from ckeditor_uploader.fields import RichTextUploadingField
from read_statistics.models import ReadNumExpandMethod, ReadDetail
from django.urls import reverse
from user.models import get_nickname_or_username


# Create your models here.

class ArticleType(models.Model):
    type_name = models.CharField(max_length=15)

    def __str__(self):
        return self.type_name

class Article(models.Model, ReadNumExpandMethod):
    title = models.CharField(verbose_name='标题', max_length=50)
    article_type = models.ForeignKey(ArticleType, on_delete=models.CASCADE, verbose_name='文章类型')
    content = RichTextUploadingField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作者')
    read_details = GenericRelation(ReadDetail)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建日期')
    last_updated_time = models.DateTimeField(auto_now=True, verbose_name='更新日期')

    def get_url(self):
        return reverse('article_detail', kwargs={'article_pk': self.pk})

    def get_email(self):
        return self.author.email

    def get_name_showed(self):
        return self.author.get_nickname_or_username()

    def __str__(self):
        return "<Article: %s>" % self.title

    class Meta:
        ordering = ['-created_time']


