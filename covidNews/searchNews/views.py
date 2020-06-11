from django.shortcuts import render
from django.http import HttpResponse
from searchNews.documents import addarticle

def searchForNews(request):
    
    res = addarticle()
    return HttpResponse(res)

