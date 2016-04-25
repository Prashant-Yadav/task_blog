
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-
    updating ``created`` and ``modified`` fields.
    """
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Blog(TimeStampedModel):
    title = models.CharField(max_length=40, default=None)
    blog_text = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    def __unicode__(self):
        return self.blog_text


class Comment(TimeStampedModel):
    comment_text = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    blog = models.ForeignKey(Blog)

    def __unicode__(self):
        return self.comment_text
