from django.test import TestCase, SimpleTestCase, Client
# from django.shortcuts import reverse
from django.urls import reverse 




class HomePageTest(SimpleTestCase):

    def test_staus_code(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_correct_news_template(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'news/news.html')

    def test_correct_about_template(self):
        response = self.client.get('/about/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'news/about.html')

    # test the json response
    def test_success_when_not_added_before(self):
        data = {'positive': 122, 'negative': 178}
        response = self.client.post('/newsBySentiment')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            data
        )

# class TestViews(TestCase):

#     def test_project(self):
#         client = Client()

#         response = self.client.get('/')


    # def test_newsBySentiment(self):
    #     response = self.client.get('/newsBySentiment/')
    #     self.assertEqual(response.status_code, 200)

    # def test_newsByDate(self):
    #     response = self.client.get('/newsByDate/')
    #     self.assertEqual(response.status_code, 200)

# from elasticutils.contrib.django.estestcase import ESTestCase
# from elasticsearch import Elasticsearch
# from nose.tools import eq_

# from elasticutils import get_es, _cached_elasticsearch

# class TestQueries(ESTestCase):
#     # This class holds tests that do elasticsearch things

#     def test_query(self):
#         # Test code ...

#     def test_locked_filters(self):
#         # Test code .