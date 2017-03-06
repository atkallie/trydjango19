from __future__ import unicode_literals

from django.db import models
from django.core.urlresolvers import reverse
from django.conf import settings
from django.utils import timezone

#Django uses the Model-View-Controller (MVC) principal, much like in iOS development
#Define how you wish to map data from Posts to your database in this class (model)
#Note that Posts inherits from the Model Class, so it does not need an explicit __init__ function

def uploadLoc(instance,filename):
    return 'user_{0}/{1}'.format(instance.id, filename)

class PostManager(models.Manager):
    # new method that you can use to manipulate model
    def active(self,*args,**kwargs):
        return super(PostManager, self).filter(draft=False).filter(publishDate__lte=timezone.now())

class Post(models.Model):
    objects = PostManager()

    #a foreign key points to the primary key of another table, which is AUTH_USER_MODEL in this case
    #we set the default user for all posts to the first AUTH_USER in our system unless otherwise specified (see view)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)

    title = models.CharField(max_length=120) #needs a 'max_length' parameter
    content = models.TextField() #larger than CharField by default
    lastUpdated = models.DateTimeField(auto_now=True) #False by default
    created = models.DateTimeField(auto_now_add=True) #False by default

    draft = models.BooleanField(default=False) #boolean field to indicate whether post is a draft or not
    publishDate = models.DateField(auto_now=False, auto_now_add=False) #date we wish to publish the post

    #width field and height field are automatically populated with the image width and height when an image is uploaded
    width_Field = models.IntegerField(default=0)
    height_Field = models.IntegerField(default=0)
    image = models.ImageField(null=True, blank=True,
                              width_field="width_Field", #this is the name of the width field that is displayed in the admin site
                              height_field="height_Field", #this is the name of the height field that is displayed in the admin site
                              upload_to=uploadLoc) #'null=True' means that your DB can store a null value, whereas 'blank=True' means that the field is not required

    #this is __str__ for Python 3
    #provides a unicode string representation of the model
    #this gets displayed on the admin site as a description of the post after you add a post
    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("posts:single_post", kwargs={"id":self.id})

    class Meta:
        #first orders by id, then by creation time, and then finally by last updated time
        ordering = ["-id","-created","-lastUpdated"]