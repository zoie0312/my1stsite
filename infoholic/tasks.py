from celery import task
from feedparser import parse

from .models import Article

@task()
def chk_task():
    print "This is to check task"
    return

@task()
def fetch_article(user, category, feed):
    d = parse(feed.link)
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
                new_article.source = feed
                new_article.category = category
                new_article.reader = user
                if num_save_article < 100:
                    new_article.save()
                num_save_article += 1

    return
    
