from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def index(request):
    #dictionary to pass to the template engine as its context
    context_dict = {'boldmessage': "Crunchy, creamy, cookie, candy, cupcake!"}
    #return a rendered response to the client
    return render(request, 'rango/index.html', context=context_dict)

def about(request):
    context_dict = {'boldmessage': "Crunchy, creamy, cookie, candy, cupcake!"}
    
    return render(request, 'rango/about.html', context=context_dict)
