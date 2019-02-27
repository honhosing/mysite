from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.html import strip_tags
from notifications.signals import notify
from .models import LikeRecord


@receiver(post_save, sender=LikeRecord)
def send_notificaton(sender, instance, **kwargs):
    # 发送站内消息
    if instance.content_type.model == 'article':
        article = instance.content_object
        verb = '{0} 点赞了你的《{1}》'.format(instance.user.get_nickname_or_username(), article.title)
    if instance.content_type.model == 'comment':
        comment = instance.content_object
        verb = '{0} 点赞了你的评论“{1}”'.format(instance.user.get_nickname_or_username(), strip_tags(comment.text))
    url = instance.content_object.get_url()
    recipient = instance.content_object.get_user()
    notify.send(instance.user, recipient=recipient, verb=verb, action_object=instance, url=url)
