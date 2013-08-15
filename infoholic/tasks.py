import time

from .models import Article
from my1stsite import settings

from celery import task
from feedparser import parse

if settings.DEBUG == False:
    import heroku

"""
worker_start_time = 0
"""

@task()
def fetch_article(user, category, feed):
    """
    to parse articles of feeds
    """
    if settings.DEBUG == False:
        cloud = heroku.from_key(settings.HEROKU_APIKEY)
        app = cloud.apps['theinfoholic']
        try:
            app.processes['worker']
        except KeyError, e:
            cloud._http_resource(method='POST', resource=(
                'apps', 'theinfoholic', 'ps', 'scale'),
                                data={'type': 'worker', 'qty': 1})

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

    if settings.DEBUG == False:
        #update_worker_start_time()
               
        time.sleep(30)
        if app.processes['worker']:
            cloud._http_resource(method='POST', resource=(
                'apps', 'theinfoholic', 'ps', 'scale'),
                                 data={'type': 'worker', 'qty': 0})
        
    return

"""
def update_worker_start_time():
    worker_start_time = time.time()
"""

def start_worker():
    """
    wake up worker
    """
    if settings.DEBUG == False:
        import heroku
        cloud = heroku.from_key(settings.HEROKU_APIKEY)
        app = cloud.apps['theinfoholic']
        #worker_start_time = time.time()        
        try:
            app.processes['worker']
        except KeyError, e:
            cloud._http_resource(method='POST', resource=(
                'apps', 'theinfoholic', 'ps', 'scale'),
                                 data={'type': 'worker', 'qty': 1})
                    
    return


"""
def check_worker():
    import heroku
    cloud = heroku.from_key(settings.HEROKU_APIKEY)
    app = cloud.apps['theinfoholic']
    try:
            app.processes['worker']
    except KeyError, e:
            cloud._http_resource(method='POST', resource=(
                'apps', 'theinfoholic', 'ps', 'scale'),
                                 data={'type': 'worker', 'qty': 1})     
"""