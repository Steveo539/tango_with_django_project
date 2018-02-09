from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from rango.models import Category
from rango.models import Page
from rango.forms import CategoryForm, PageForm, UserProfileForm, UserForm
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from datetime import datetime

# Create your views here.
def index(request):
    request.session.set_test_cookie()
    #dictionary to pass to the template engine as its context
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {'categories': category_list, 'pages': page_list}

    #obtain our response object early so we can add cookie information

    #call the helper func to handle the COOKIES
    visitor_cookie_handler(request)

    context_dict['visits'] = request.session['visits']

    response = render(request, 'rango/index.html', context_dict)

    #return response back to the user, updating any cookies that needed changing
    return response

def about(request):
    if request.session.test_cookie_worked():
        print("TEST COOKIE WORKED")
        request.session.delete_test_cookie()

    context_dict = {'categories': category_list, 'pages': page_list}


    visitor_cookie_handler(request)

    context_dict['visits'] = request.session['visits']
    #context_dict = {'boldmessage': "Crunchy, creamy, cookie, candy, cupcake!"}
    #return HttpResponse('Rango says here is the about page.')
    return render(request, 'rango/about.html', {})

def show_category(request, category_name_slug):
    context_dict = {}

    try:
        category = Category.objects.get(slug=category_name_slug)

        pages = Page.objects.filter(category=category)

        context_dict['pages'] = pages
        context_dict['category'] = category

    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['page'] = None


    return render(request, 'rango/category.html', context_dict)
@login_required
def add_category(request):
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print(form.errors)
    return render(request, 'rango/add_category.html', {'form': form})

@login_required
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = NONE

    form = PageForm()
    if request.method == 'POST':
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                return show_category(request, category_name_slug)
        else:
            print(form.errors)
    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context_dict)

def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            #hash the password with the set_password method and save the user object.
            user.set_password(user.password)
            user.save()

            profile= profile_form.save(commit=False)
            profile.user = user

            #if the user provided a profile picture
            #then get it from the input form and put it in the UserProfile model
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()

            registered = True

        else:
            #invalid form
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request,
                    'rango/register.html',
                    {'user_form': user_form,
                    'profile_form': profile_form,
                    'registered': registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                #If the account is valid and active,
                #log them in and send them to the homepage
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                #An inactive account was used
                return HttpResponse("Your Rango account is disabled.")
        else:

            #if username != :
            #Bad login details provided
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")
    #The request method is not POST so display the login form
    else:
        return render(request, 'rango/login.html', {})

@login_required
def restricted(request):
    return render(request, 'rango/restricted.html', {})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val


def visitor_cookie_handler(request):
    #gets the number of visits to the website
    #usese cookies.get() to obtain the visits cookies
    #if cookie exists -> value is casted to an int: otherwise default to 1
    visits = int(get_server_side_cookie(request, 'visits', 1))

    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')
    #if its been more than a day since the last visit...
    if(datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        #update the last visit cookie now that we have updated the count
        request.session['last_visit'] = str(datetime.now())
    else:
        visits = 1
        #set the last visit cookie
        request.session['visits'] = last_visit_cookie
    #update or set the visits cookie
    request.session['visits'] = visits
