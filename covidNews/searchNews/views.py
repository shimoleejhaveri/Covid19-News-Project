from django.shortcuts import render
from django.http import HttpResponse
from searchNews.documents import displayNews

def viewNews(request):

	posts = displayNews()
	context = {
		'posts': posts
	}
	return render(request, 'news/base.html', context)
