from django.shortcuts import render
from django.http import HttpResponse
from searchNews.documents import addarticle

def searchForNews(request):
    
    searchDate="2020-06-11"
    res = addarticle()
    return HttpResponse(res)

