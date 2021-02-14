from django.shortcuts import render, redirect
from django.http import HttpResponse
from collections import defaultdict

from .models import Article

def index(request):
    articles = Article.objects.all()
    years = list(map(lambda a: a.publish_date.year,articles))
    categories = list(map(lambda a: a.category, articles))
    set_categories = list(set(categories))
    categorical = defaultdict(list)
    for article in articles:
        categorical[article.category].append(article)

    # sorting articles in descending order
    for article in categorical.values():
        article.sort(key = lambda a: -a.publish_date.year)

    params = {'articles': dict(categorical), 'years': sorted(set(years), reverse=True), 'count': len(articles), 'categories': set_categories}
    return render(request, 'publish/index.html', params)

def years(request, id):
    all_articles = Article.objects.all()
    articles = list(filter(lambda a: a.publish_date.year == id, all_articles))
    categories = list(map(lambda a: a.category, articles))
    set_categories = list(set(categories))
    categorical = defaultdict(list)
    for article in articles:
        categorical[article.category].append(article)
    # sorting articles in descending order
    for article in articles:
        categorical[article.category].sort(reverse = True, key = lambda a: a.publish_date)
    params = {'articles': dict(categorical), 'count': len(articles), 'categories': set_categories,'id':id}
    return render(request, 'publish/year.html', params)

def search(request):
    query = request.GET.get('search', '')
    if query == '':
        return redirect('/inst/')
    articles = Article.objects.filter(name__icontains = query)
    years = list(map(lambda a: a.publish_date.year,articles))
    
    if list(articles) == []:
        return render(request, 'publish/search.html', {'res' : 0})

    categories = list(map(lambda a: a.category, articles))
    set_categories = list(set(categories))
    categorical = defaultdict(list)
    
    for article in articles:
        categorical[article.category].append(article)
    
    # sorting articles in descending order
    for article in articles:
        categorical[article.category].sort(reverse = True, key = lambda a: a.publish_date)
    params = {'articles': dict(categorical), 'categories': set_categories, 'res': 1, 'years': sorted(set(years), reverse=True), 'year': query}
    return render(request, 'publish/search.html', params)
