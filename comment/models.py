import threading
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from user.models import get_nickname_or_username

# Create your models here.
class SendMail(threading.Thread):
    def __init__(self, subject, text, email, fail_silently=False):
        self.subject = subject
        self.text = text
        self.email = email
        self.fail_silently = fail_silently
        threading.Thread.__init__(self)


    def run(self):
        send_mail(
            self.subject,  # Subject here
            '',  # Here is the message
            settings.EMAIL_HOST_USER,  # from@example.com
            [self.email],  # to@example.com
            html_message=self.text,
            fail_silently=self.fail_silently,
        )

class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    text = models.TextField()
    comment_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)

    root = models.ForeignKey('self', null=True, related_name="root_comment", on_delete=models.CASCADE)
    parent = models.ForeignKey('self', null=True, related_name="parent_comment", on_delete=models.CASCADE)
    reply_to = models.ForeignKey(User, related_name="replies", null=True, on_delete=models.CASCADE)

    def send_email(self):
        # 发送邮件通知
        if self.parent is None:
            # 有人评论我的文章
            subject = '[有人评论了你的文章]'
            email = self.content_object.get_email()
        else:
            # 回复评论
            subject = '[有人回复了你的评论]'
            email = self.reply_to.email
        if email != '':
            context = {}
            context['comment_user'] = str(self.user.get_nickname_or_username())
            context['article_title'] = self.content_object.title
            context['comment_text'] = self.text
            context['url'] = self.content_object.get_url()
            text = render_to_string('comment/send_mail.html', context)
            send_email = SendMail(subject, text, email)
            send_email.start()


    def __str__(self):
        return self.text

    class Meta:
        ordering = ['comment_time']

