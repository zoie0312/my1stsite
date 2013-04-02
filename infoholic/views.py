# Create your views here.
from django.views.generic import TemplateView
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Article, Category, Feed
from django.shortcuts import render
import feedparser
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.hashers import check_password


class HomepageView(TemplateView):
    template_name = 'infoholic/index.html'

def register(request):
    if request.method == 'POST':
        new_user = User()
        new_user.username = request.POST['username']
        new_user.email = request.POST['email']
        new_user.set_password(request.POST['password'])
        new_user.save()
        user_guest = User.objects.get(username='guest')
        for category in user_guest.categories.all():
            category.owners.add(new_user)
            for feed in user_guest.feeds.filter(category=category):
                feed.owners.add(new_user)
            
        username = request.POST.get('username', '')
        password = request.POST['password']
        user = authenticate(username=new_user.username,
                            password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('infoholic:user_default'))
            else:
                return HttpResponseRedirect(reverse('home'))
        else:
            return HttpResponseRedirect(reverse('infoholic:signup'))
      
    else:
        return HttpResponseRedirect(reverse('infoholic:home'))

def user_profile(request):
    template_name = "infoholic/user_profile.html"
    if request.method == 'POST':
        if request.POST['inputEmail'] is not None:
            request.user.email = request.POST['inputEmail']
            request.user.save()
        if check_password(request.POST['currentPassword'], request.user.password):
            if (request.POST['newPassword'] is not None) and \
               (request.POST['confirmPassword'] is not None) and \
               (request.POST['newPassword'] == request.POST['confirmPassword']):
                request.user.set_password(request.POST['newPassword'])
                request.user.save()
                                
        return HttpResponseRedirect(reverse('infoholic:user_default'))
    else:
        return render(request, template_name)
            
def edit_source(request):
    template_name = "infoholic/edit_source.html"
    if request.method == 'POST':
        if request.POST['new_cat_name'] != '':
            new_cat_added = False
            for category in Category.objects.all():
                if category.name == request.POST['new_cat_name']:
                    if category not in request.user.categories.all():
                        category.owners.add(request.user)
                        new_cat_added = True
            if not new_cat_added:
                new_category = Category(name=request.POST['new_cat_name'])
                new_category.save()
                new_category.owners.add(request.user)
                
        if request.POST['new_feed_title'] != '':
            new_feed_added = False
            for feed in Feed.objects.all():
                if feed.link == request.POST['new_feed_link']:
                    if feed not in request.user.feeds.all():
                        feed.owners.add(request.user)
                        new_feed_added = True
            if not new_feed_added:
                new_feed = Feed(title=request.POST['new_feed_title'],
                                category=request.POST['new_feed_cat'],
                                link=request.POST['new_feed_link'])
                new_feed.save()
                new_feed.owners.add(request.user)
            
        return HttpResponseRedirect(reverse('infoholic:user_default'))
    else:
        return render(request, template_name)

def user_default(request):
    template_name = "infoholic/read_article.html"
    if request.user.is_authenticated():
        user = request.user        
    else:
        user = User.objects.get(username='guest')
    username = user.username
    category_list = user.categories.all().order_by('created_at')
    default_cat = category_list[0]
    feed_list = user.feeds.filter(category=default_cat).order_by(
                'created_at')
    default_feed = feed_list[0]
    d = feedparser.parse(default_feed.link)
    article_titles = []
    for article in user.articles.all():
        article_titles.append(article.title)
        
    parse_len = len(d.entries)
    num_save_article = 0
    for i in range(parse_len-1, -1, -1):
        if d.entries[i].title not in article_titles:
            new_article = Article()
            new_article.title = d.entries[i].title
            new_article.content = d.entries[i].description
            new_article.link = d.entries[i].link
            new_article.source = default_feed
            new_article.category = default_cat
            new_article.reader = user
            if num_save_article < 10:
                new_article.save()
            num_save_article += 1
    
    article_list = user.articles.filter(category=default_cat,
                                    source=default_feed)[:10]
        

    context = {
        'username'     : username,
        'category_list': category_list,
        'cat_selected'  : default_cat,
        'feed_list'    : feed_list,
        'feed_selected' : default_feed,
        'article_list' : article_list
    }
    return render(request, template_name, context)

def category_detail(request, slug):
    template_name = "infoholic/read_article.html"
    if request.user.is_authenticated():
        user = request.user        
    else:
        user = User.objects.get(username='guest')
    username = user.username
    category_list = user.categories.all().order_by('created_at')
    cat_selected = user.categories.get(name=slug)
    feed_list = user.feeds.filter(category=cat_selected).order_by(
                'created_at')

    article_titles = []
    for article in user.articles.all():
        article_titles.append(article.title)

    #temp_post_list = []
    for feed in feed_list:
        d = feedparser.parse(feed.link)
        parse_len = len(d.entries)
        num_save_article = 0
                    
        for i in range(parse_len-1, -1, -1):
            if d.entries[i].title not in article_titles:
                new_article = Article()
                new_article.title = d.entries[i].title
                new_article.content = d.entries[i].description
                new_article.link = d.entries[i].link
                new_article.source = feed
                new_article.category = cat_selected
                new_article.reader = user
                if num_save_article < 100:
                    new_article.save()
                num_save_article += 1
            
        
    article_list = user.articles.filter(category=cat_selected)
    context = {
        'username'      : username,
        'category_list' : category_list,
        'cat_selected'  : cat_selected,
        'feed_list'     : feed_list,
        'article_list'  : article_list
    }
    return render(request, template_name, context)

def feed_detail(request, slug1, slug2):
    template_name = "infoholic/read_article.html"
    if request.user.is_authenticated():
        user = request.user        
    else:
        user = User.objects.get(username='guest')
    username = user.username
    category_list = user.categories.all().order_by('created_at')
    cat_selected = user.categories.get(slug_name=slug1)
    feed_list = user.feeds.filter(category=cat_selected).order_by(
                'created_at')
    feed_selected = user.feeds.get(slug=slug2)
    d = feedparser.parse(feed_selected.link)
    article_titles = []
    #user = User
    for article in user.articles.all():
        article_titles.append(article.title)
        
    parse_len = len(d.entries)
    num_save_article = 0    
    for i in range(parse_len-1, -1, -1):
            if d.entries[i].title not in article_titles:
                new_article = Article()
                new_article.title = d.entries[i].title
                new_article.content = d.entries[i].description
                new_article.link = d.entries[i].link
                new_article.source = feed_selected
                new_article.category = cat_selected
                new_article.reader = user
                if num_save_article < 100:
                    new_article.save()
                num_save_article += 1
    
    num_feed_articles = user.articles.filter(category=cat_selected,
                                    source=feed_selected).count()
    if num_feed_articles > parse_len:
        for j in range(num_feed_articles-1, parse_len+9, -1):
            user.articles.filter(category=cat_selected,
                                 source=feed_selected)[j].delete()
        
    article_list = user.articles.filter(category=cat_selected,
                                    source=feed_selected)
    """
    for i in range(10):
        post_list.append(Post())
        post_list[i].title = d.entries[i].title
        post_list[i].content = d.entries[i].description
        post_list[i].link = d.entries[i].link
        #post_list[i].created_at = d.entries[i].published_parsed
    """
    context = {
        'username'     : username,
        'category_list': category_list,
        'cat_selected' : cat_selected,
        'feed_list'    : feed_list,
        'feed_selected': feed_selected,
        'article_list' : article_list
    }
    return render(request, template_name, context)   
