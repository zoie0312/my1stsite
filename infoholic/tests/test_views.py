from django.test import TestCase
from ..models import *
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test.client import Client
from django.utils.http import urlencode
from django.contrib.auth.hashers import check_password


class InfoholicViewsTests(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='test')
        self.category = Category.objects.create(
            name='test_Cat'
            )
        self.category.owners.add(self.user)

        self.feed = Feed.objects.create(
            title='test_Feed',
            category=self.category,
            link='infoholic/tests/test_rss.xml'
            )
        self.feed.owners.add(self.user)
        self.article = Article.objects.create(
            title='test aritcle',
            content='this is a test article',
            reader=self.user,
            source=self.feed,
            category=self.category
            )
    '''
    def create_article(self, title='test_article'):
        return Article.objects.create(
            title=title,
            content='for testing purpose',
            link='http://test.html',
            reader=self.user,
            category=self.category,
            source=self.feed
            )
    '''
    def test_home_view(self):
        url = reverse('infoholic:home')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'infoholic/index.html')
        self.assertIn('The Infoholic', resp.rendered_content)
        
    def test_user_default_view(self):
        url = reverse('infoholic:user_default')
        user_guest = User.objects.create(username='guest')
        self.category.owners.add(user_guest)
        self.feed.owners.add(user_guest)
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'infoholic/read_article.html')
        self.assertEqual(resp.context['username'], 'guest')

    def test_category_detail_view(self):
        url = reverse('infoholic:category_detail',
                      kwargs={'slug': self.category.slug_name})
        user_guest = User.objects.create(username='guest')
        self.category.owners.add(user_guest)
        self.feed.owners.add(user_guest)
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'infoholic/read_article.html')
        self.assertEqual(resp.context['username'], 'guest')

    def test_feed_detail_view(self):
        url = reverse('infoholic:feed_detail',
                      kwargs={'slug1': self.category.slug_name,
                              'slug2': self.feed.slug})
        user_guest = User.objects.create(username='guest')
        self.category.owners.add(user_guest)
        self.feed.owners.add(user_guest)
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'infoholic/read_article.html')
        self.assertEqual(resp.context['username'], 'guest')
        #print 'article num = %u' %len(resp.context['article_list'])

    def test_edit_source_get_view(self):
        url = reverse('infoholic:edit_source')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'infoholic/edit_source.html')

    def test_register_view(self):
        url = reverse('infoholic:signup')
        resp = self.client.get(url)
        self.assertRedirects(resp, reverse('infoholic:home'),
                             status_code=302, target_status_code=200)

    def test_register(self):
        url = reverse('infoholic:signup')
        User.objects.create_user('guest', 'guest@abc.com', 'guest123')
        guest_user = User.objects.get(username='guest')
        guest_cat = Category.objects.create(
            name='test_Cat'
            )
        guest_cat.owners.add(guest_user)
        guest_feed = Feed.objects.create(
            title='test_Feed',
            category=guest_cat,
            link=''
            )
        guest_feed.owners.add(guest_user)
        resp = self.client.post(url, {
            'username': 'test_user',
            'email': 'test_user@abc.com',
            'password': 'test123'})
        self.assertRedirects(resp, reverse('infoholic:user_default'),
                         status_code=302, target_status_code=200)
        #self.assertEqual(resp.context['user'].username, 'test_user')

    def test_user_profile_view(self):
        url = reverse('infoholic:user_profile')
        resp = self.client.get(url)
        #self.assertEqual(resp.status_code, 200)
        self.assertRedirects(resp, reverse('infoholic:home'),
                             status_code=302, target_status_code=200)
        #self.assertEqual(resp.context['user'].username, 'john')
    

class SessionTestCase(TestCase):
    def setUp(self):
        # http://code.djangoproject.com/ticket/10899
        #settings.SESSION_ENGINE = 'django.contrib.sessions.backends.file'
        #engine = import_module(settings.SESSION_ENGINE)
        #store = engine.SessionStore()
        #store.save()
        #self.session = store
        #self.client.cookies[settings.SESSION_COOKIE_NAME] = store.session_key
        self.client = Client()
        User.objects.create_user('john', 'john@gmail.com', 'johnpassword')
        self.client.login(username='john', password='johnpassword')
        self.user = User.objects.get(username='john')
        self.category = Category.objects.create(
            name='test_Cat'
            )
        self.category.owners.add(self.user)
        self.feed = Feed.objects.create(
            title='test_Feed',
            category=self.category,
            link='infoholic/tests/test_rss.xml'
            )
        self.feed.owners.add(self.user)
        self.article = Article.objects.create(
            title='test aritcle',
            content='this is a test article',
            reader=self.user,
            source=self.feed,
            category=self.category
            )
    
class InfoholicUserViewsTests(SessionTestCase):

    def test_user_default_view(self):
        #session = self.client.session
        #session['user'] = self.user
        #session.save()
        url = reverse('infoholic:user_default')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'infoholic/read_article.html')
        self.assertEqual(resp.context['username'], 'john')
        self.assertIn('More', resp.content)
        self.assertIn(self.category.name, resp.content)
        self.assertIn(self.feed.title, resp.content)

    def test_category_detail_view(self):
        url = reverse('infoholic:category_detail',
                      kwargs={'slug': self.category.slug_name})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'infoholic/read_article.html')
        self.assertEqual(resp.context['username'], 'john')

    def test_feed_detail_view(self):
        url = reverse('infoholic:feed_detail',
                      kwargs={'slug1': self.category.slug_name,
                              'slug2': self.feed.slug})
        ori_user_article_num = self.user.articles.filter(
            category=self.category,
            source=self.feed).count()
        resp = self.client.get(url)
        #print 'article num = %u' %len(resp.context['article_list'])
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'infoholic/read_article.html')
        self.assertEqual(resp.context['username'], 'john')
        self.assertEqual(ori_user_article_num+1, self.user.articles.filter(
            category=self.category,
            source=self.feed).count())

    def test_control_article_num(self):
        url = reverse('infoholic:feed_detail',
                      kwargs={'slug1': self.category.slug_name,
                              'slug2': self.feed.slug})
        for i in range(0, 21):
            Article.objects.create(
                title='test aritcle'+str(i),
                content='this is a test article',
                reader=self.user,
                source=self.feed,
                category=self.category
            )
        ori_user_article_num = self.user.articles.filter(
            category=self.category,
            source=self.feed).count()
        resp = self.client.get(url)
        #print 'article num = %u' %len(resp.context['article_list'])
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'infoholic/read_article.html')
        self.assertEqual(resp.context['username'], 'john')
        self.assertNotEqual(ori_user_article_num+1, self.user.articles.filter(
            category=self.category,
            source=self.feed).count())
        #self.assertEqual(11, self.user.articles.filter(
        #    category=self.category,
        #    source=self.feed).count())

    def test_add_new_category(self):
        #session = self.client.session
        #session['user'] = self.user
        #session.save()
        cat_count = self.user.categories.count()
        url = reverse('infoholic:edit_source')
        resp = self.client.post(url, {'new_cat_name': 'new_cat',
                                      'new_feed_title': ''})
        self.assertRedirects(resp, reverse('infoholic:user_default'),
                             status_code=302, target_status_code=200)
        self.assertNotEqual(cat_count, self.user.categories.count())
        new_cat = Category.objects.get(name='new_cat')
        self.assertIn(self.user, new_cat.owners.all())

    def test_add_user_owned_category(self):
        #session = self.client.session
        #session['user'] = self.user
        #session.save()
        cat_count = self.user.categories.count()
        url = reverse('infoholic:edit_source')
        resp = self.client.post(url, {'new_cat_name': 'test_Cat',
                                      'new_feed_title': ''})
        self.assertRedirects(resp, reverse('infoholic:user_default'),
                             status_code=302, target_status_code=200)
        self.assertEqual(cat_count, self.user.categories.count())

    def test_add_existing_category(self):
        url = reverse('infoholic:edit_source')
        new_cat = Category.objects.create(name='new_cat')
        self.assertNotIn(self.user, new_cat.owners.all())
        resp = self.client.post(url, {'new_cat_name': 'new_cat',
                                      'new_feed_title': ''})
        self.assertRedirects(resp, reverse('infoholic:user_default'),
                             status_code=302, target_status_code=200)
        self.assertIn(self.user, new_cat.owners.all())
        
    def test_add_new_feed(self):        
        url = reverse('infoholic:edit_source')
        feed_count = self.user.feeds.count()        
        resp = self.client.post(url, {
            'new_cat_name': '',
            'new_feed_title': 'new_feed',
            'new_feed_cat': self.category.name,
            'new_feed_link': '123.com'})
        self.assertRedirects(resp, reverse('infoholic:user_default'),
                         status_code=302, target_status_code=200)
        new_feed = Feed.objects.get(title='new_feed')
        self.assertIn(self.user, new_feed.owners.all())
        self.assertEqual(self.user.feeds.count(), feed_count+1)
        #self.assertIn(new_feed.title, resp.content)

    def test_add_user_owned_feed(self):        
        #session = self.client.session
        #session['user'] = self.user
        #session.save()
        url = reverse('infoholic:edit_source')
        feed_count = self.user.feeds.count()        
        resp = self.client.post(url, {
            'new_cat_name': '',
            'new_feed_title': 'new_feed',
            'new_feed_cat': self.category.name,
            'new_feed_link': 'infoholic/tests/test_rss.xml'})
        self.assertRedirects(resp, reverse('infoholic:user_default'),
                         status_code=302, target_status_code=200)
        self.assertEqual(self.user.feeds.count(), feed_count)

    def test_add_existing_feed(self):
        url = reverse('infoholic:edit_source')
        new_feed = Feed.objects.create(
            title='new_Feed',
            category=self.category,
            link='new_feed.abc.com')
        self.assertNotIn(self.user, new_feed.owners.all())
        resp = self.client.post(url, {
            'new_cat_name': '',
            'new_feed_title': 'feed',
            'new_feed_cat': self.category.name,
            'new_feed_link': 'new_feed.abc.com'})
        self.assertRedirects(resp, reverse('infoholic:user_default'),
                         status_code=302, target_status_code=200)
        self.assertIn(self.user, new_feed.owners.all())
        
        
    def test_user_profile_view(self):
        #session = self.client.session
        #session['user'] = self.user
        #session.save()
        url = reverse('infoholic:user_profile')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'infoholic/user_profile.html')
        self.assertEqual(resp.context['user'].username, 'john')

    '''    
    def test_profile(self):
        c = Client()
        #test_user = User.objects.create(username='test123',
        #                                email='test@abc.com',
        #                                password='testpassword')
        User.objects.create_user('test123', 'test@abc.com', 'testpassword')
        #test_user.save()
        c.login(username='test123', password='testpassword')
        url = reverse('infoholic:user_profile')
        resp = c.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'infoholic/user_profile.html')
        self.assertEqual('test123', resp.context['user'].username)
    '''

    def test_change_user_email(self):
        #session = self.client.session
        #session['user'] = self.user
        #session.save()
        url = reverse('infoholic:user_profile')
        resp = self.client.get(url)
        self.assertEqual(resp.context['user'].email, 'john@gmail.com')
        #print resp.context['user'].username
        #print resp.context['user'].email
        resp = self.client.post(url, {
            'newEmail': 'xxx@123.com',
            'currentPassword': '11'})
        self.assertRedirects(resp, reverse('infoholic:user_default'),
                         status_code=302, target_status_code=200)
        
        resp = self.client.get(url)
        self.assertEqual(resp.context['user'].email, 'xxx@123.com')
        #print resp.context['user'].username
        #print resp.context['user'].email
        
    def test_change_user_password(self):
        url = reverse('infoholic:user_profile')
        resp = self.client.get(url)
        pwd1 = resp.context['user'].password
        self.assertEqual(pwd1, self.user.password)
        resp = self.client.post(url, {
            'newEmail': None,
            'currentPassword': 'johnpassword',
            'newPassword': '1111',
            'confirmPassword': '1111'})
        self.assertRedirects(resp, reverse('infoholic:user_default'),
                         status_code=302, target_status_code=200)
        resp = self.client.get(url)
        pwd2 = resp.context['user'].password
        self.assertNotEqual(pwd1, pwd2)
        chk_pwd = check_password('1111' ,pwd2)
        self.assertEqual(chk_pwd, True)

    

    
        
        
        


        
