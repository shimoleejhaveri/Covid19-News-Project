from django.shortcuts import render
# from django.http import HttpResponse
# from searchNews.documents import sentAnalysis

posts = [
	{
		'author': 'CoreyMS',
		'title': 'Blog Post 1',
		'content': 'First Post',
		'date_posted': 'July 23, 2020'
	},
	{
		'author': 'Jane Doe',
		'title': 'Blog Post 2',
		'content': 'Second Post',
		'date_posted': 'July 24, 2020'
	}
]

def home(request):
	context = {
		'posts': posts
	}
	return render(request, 'news/base.html', context)

# def searchForNews(request):

#     res = sentAnalysis()
#     return HttpResponse(res)

