from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from searchNews.documents import sentAnalysis, dailySentAnalysis, displayNews

def searchForNews(request):

    data = sentAnalysis()
    return JsonResponse(data)

def searchForDates(request):

    data = dailySentAnalysis()
    return JsonResponse(data)

def viewNews(request):

    posts = displayNews()
    context = {
        'posts': posts
    }
    return render(request, 'news/base.html', context)


#  HttpResponse(res)