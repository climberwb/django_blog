from __future__ import unicode_literals

from django.conf import settings
from django.db import models

## import generic foreign keys
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
# Create your models here.


class CommentManager(models.Manager):
    
    def all(self):
        qs = super(CommentManager,self).filter(parent = None)
        return qs
    def filter_by_instance(self, instance):
        content_type= ContentType.objects.get_for_model( instance.__class__)
        return super(CommentManager, self).filter(content_type=content_type, object_id=instance.id).filter(parent = None)


class Comment(models.Model):
    user        = models.ForeignKey(settings.AUTH_USER_MODEL, default=1) 
    # post        = models.ForeignKey(Post )
    
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    parent    = models.ForeignKey("self", null=True, blank=True)
    
    content     = models.TextField()
    timestamp   = models.DateTimeField(auto_now_add=True)
    
    objects = CommentManager()
    
    def __unicode__(self):
        return str(self.user.username)
    
    class Meta:
        ordering = ['-timestamp']
      
    def __str__(self):
        return str(self.user.username)
        
    def children(self):#replies
        return Comment.objects.filter(parent=self)
    def get_absolute_url(self):
        return reverse("comments:thread", kwargs={"id":self.id})
    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True