from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
# Create your models here.


class Category(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    name = models.CharField(max_length=255)
    slug_name = models.SlugField(max_length=255, blank=True, default='')
    owners = models.ManyToManyField(User, related_name='categories')
    #feeds = models.ManyToManyField(Feed)
    #objects = PostManager()

    class Meta:
        ordering = ["created_at", "name"]

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug_name:
            self.slug_name = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

class Feed(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    #updated_at = models.DateTimeField(auto_now=True, editable=False)
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
    fetched_at = models.DateTimeField(auto_now_add=True, editable=False)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, blank=True, default='')
    content = models.TextField()
    readed = models.BooleanField(default=False)
    link = models.CharField(max_length=255, blank=True, default='')
    reader = models.ForeignKey(User, related_name="articles")
    source = models.ForeignKey(Feed, related_name="articles") #feed 
    category = models.ForeignKey(Category, related_name="articles") #category 
    #objects = PostManager()

    class Meta:
        ordering = ["-fetched_at", "title"]

    #def set_title(self, title):
    #    self.title = title

    #def set_content(self, content):
    #    self.

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.link)
        super(Article, self).save(*args, **kwargs)

    #@models.permalink
    #def get_absolute_url(self):
    #    return ("infoholic:detail", (), {'slug': self.slug})
