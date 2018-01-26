from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category, Page
# Create your views here.
def index(request):
    #dictionary to pass to the template engine as its context
    category_list =Category.objects.order_by('-likes')[:5]
    context_dict = {'categories': category_list}
    #return a rendered response to the client
    return render(request, 'rango/index.html', context=context_dict)

def about(request):
    context_dict = {'boldmessage': "Crunchy, creamy, cookie, candy, cupcake!"}

    return render(request, 'rango/about.html', context=context_dict)

def show_category(request, category_name_slug):
    context_dict = {}

    try:
        category = Category.objects.get(slug=category_name_slug)

        pages = Page.pobjects.filter(category=category)

        context_dict['pages'] = pages

        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['page'] = None


    return render(request, 'rango/category.html', context_dict)
