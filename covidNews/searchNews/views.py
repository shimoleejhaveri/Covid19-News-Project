from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from elasticsearch import Elasticsearch
from searchNews.documents import sent_analysis, daily_sent_analysis, display_news
import os

def search_for_news(request):

    data = sent_analysis()
    return JsonResponse(data)

def search_for_dates(request):

    data = daily_sent_analysis()
    return JsonResponse(data)

def view_news(request):

	ip = os.environ.get('IP')
	es = Elasticsearch(['http://' + ip])

	posts = display_news(es)
	context = {
		'posts': posts
	}
	return render(request, 'news/news.html', context)

def about(request):

	return render(request, 'news/about.html')