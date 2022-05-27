import uuid

from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)


class Page(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    name = models.CharField(max_length=80)
    description = models.TextField()
    tags = models.ManyToManyField('content.Tag', related_name='pages')
    owner = models.ForeignKey('authentication.User', on_delete=models.CASCADE,
                              related_name='pages')
    followers = models.ManyToManyField('authentication.User',
                                       related_name='follows')
    image = models.URLField(null=True, blank=True)
    is_private = models.BooleanField(default=False)
    follow_requests = models.ManyToManyField('authentication.User',
                                             related_name='requests')
    unblock_date = models.DateTimeField(null=True, blank=True)


class Post(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE,
                             related_name='posts')
    content = models.CharField(max_length=180)
    reply_to = models.ForeignKey('content.Post', on_delete=models.SET_NULL,
                                 null=True, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
