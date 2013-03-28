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


class HomepageView(TemplateView):
    template_name = 'infoholic/index.html'

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            user_guest = User.objects.get(username='guest')
            for category in user_guest.categories.all():
                category.owners.add(new_user)
                for feed in user_guest.feeds.filter(category=category):
                    feed.owners.add(new_user)
            new_user.save()
            username = request.POST.get('username', '')
            password = request.POST['password1']
            user = authenticate(username=username,
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
        form = UserCreationForm()
    return render(request, "infoholic/register.html", {
        'form': form,
    })

def user_default(request):
    template_name = "infoholic/user_default.html"
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
        'default_cat'  : default_cat,
        'feed_list'    : feed_list,
        'default_feed' : default_feed,
        'article_list' : article_list
    }
    return render(request, template_name, context)

def category_detail(request, slug):
    template_name = "infoholic/category_detail.html"
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
            
    """    
    post_list = temp_post_list[:]
    post = temp_post_list[0]
    if len(temp_post_list) > 10:
        show_posts = 10
    else:
        show_posts = len(temp_post_list)
    for j in range(show_posts):
        post = post_list[j]
        for temp_post in temp_post_list:
            if post.created_at <= temp_post.created_at:
                post = temp_post
                
        post_list[j] = post
        temp_post_list.remove(post)
    """
    
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
    template_name = "infoholic/feed_detail.html"
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
