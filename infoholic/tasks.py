from celery import task
from feedparser import parse
#from multiprocessing import Process
import time
#from heroku import heroku

from .models import Article
from my1stsite import settings

if settings.DEBUG == False:
    import heroku

#worker_start_time = 0
@task()
def fetch_article(user, category, feed):
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
'''
def start_time():
    start = time.time()
    print "update timer = %r" % start
    while (time.time() - start) < 30:
        pass

    print "Time's Up!"
    print "Now, it is %r" % time.time()


    
def start_count():
    p = Process(target=start_time)
    p.start()
'''
"""
def update_worker_start_time():
    worker_start_time = time.time()
"""
def start_worker():
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
        #while (time.time() - worker_start_time) < 60:
        #    pass

        #if 'worker' in app.processes:
        #    cloud._http_resource(method='POST', resource=(
        #        'apps', 'theinfoholic', 'ps', 'scale'),
        #                         data={'type': 'worker', 'qty': 0})
            
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