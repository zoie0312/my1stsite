from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User


class TimeStampedModel(models.Model):
    '''
    An abstract base class model that provides self-updating
    "created_at" and "updated_at" fields.
    '''
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        abstract = True


class Category(TimeStampedModel):
    """
    category of articles, such as News, Business etc
    """
    name = models.CharField(max_length=255)
    slug_name = models.SlugField(max_length=255, blank=True, default='')
    owners = models.ManyToManyField(User, related_name='categories')
    
    class Meta:
        ordering = ["created_at", "name"]

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug_name:
            self.slug_name = slugify(self.name)
        super(Category, self).save(*args, **kwargs)


class Feed(TimeStampedModel):
    """
    an RSS feed
    """
    title = models.CharField(max_length=255)
    link = models.CharField(max_length=255) #ex, http://www.theverge.com/rss/index.xml
    slug = models.SlugField(max_length=255, blank=True, default='')
    owners = models.ManyToManyField(User, related_name='feeds')
    category = models.ForeignKey(Category)
    
    class Meta:
        ordering = ["created_at", "title"]

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Feed, self).save(*args, **kwargs)


class Article(models.Model):
    """
    articles parsed from an RSS feed
    """
    fetched_at = models.DateTimeField(auto_now_add=True, editable=False)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, blank=True, default='')
    content = models.TextField()
    readed = models.BooleanField(default=False)
    link = models.CharField(max_length=255, blank=True, default='')
    reader = models.ForeignKey(User, related_name="articles")
    source = models.ForeignKey(Feed, related_name="articles") #feed 
    category = models.ForeignKey(Category, related_name="articles") #category 
    
    class Meta:
        ordering = ["-fetched_at", "title"]

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.link)
        super(Article, self).save(*args, **kwargs)

    
