from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from searchNews.documents import sentAnalysis, dailySentAnalysis, displayNews

def searchForNews(request):

    data = sentAnalysis()
    print(data)
    return JsonResponse(data)

def searchForDates(request):

    template_name = 'news/base.html'
    data = dailySentAnalysis()
    return JsonResponse(data)


def viewNews(request):

    posts = displayNews()
    context = {
        'posts': posts
    }
    return render(request, 'news/base.html', context)


#  HttpResponse(res)