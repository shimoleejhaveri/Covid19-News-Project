from django.shortcuts import render
from django.http import HttpResponse
from searchNews.documents import sentAnalysis

def searchForNews(request):

    res = sentAnalysis()
    return HttpResponse(res)

