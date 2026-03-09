# here you store a series of functions to handle requests and return responses
from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import (
    render,  #streamlines the process of combining given template with a context dictionary.Automates a threee step process i.e, loading the template, merging data into it and creating the HttpResponse object.
)
from django.urls import reverse

from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from rango.models import Category, Page


def index(request):
    # request.session.set_test_cookie()
    category_list = Category.objects.order_by('-likes')[:5]
    top_pages =  Page.objects.order_by('-views')[:5]

    context_dict = {"categories": category_list,
                    "top_pages": top_pages
                        }

    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']

    response = render(request, 'rango/index.html', context = context_dict)
    return response



def show_category(request, category_name_slug):
    context_dict = {}
    try:
        category = Category.objects.get(slug = category_name_slug) #.get() method commonly used with dictionary objects has the parameters :key, default_value,
        pages = Page.objects.filter(category = category)
        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['pages'] = None
        context_dict['category'] = None

    return render(request, 'rango/category.html', context_dict)


def add_category(request):
    context_dict = {}
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST)

        #server checks==>have we been provided with a valid form?
        if form.is_valid():
            cat = form.save(commit = True )
            print (cat)
            return index(request)
        else:
            print (form.errors)

    context_dict['form'] = form

    return render (request, 'rango/add_category.html', context_dict)


def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug = category_name_slug)
    except Category.DoesNotExist:
        category = None

    form = PageForm()

    if request.method =='POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                page = form.save(commit = False)
                page.category = category
                page.views = 0
                page.save ()
                return show_category(request, category_name_slug)
        else:
            print(form.errors)

    context_dict = {'form': form, 'category': category}

    return render(request, 'rango/add_page.html', context_dict)


def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data = request.POST)
        profile_form = UserProfileForm(data = request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit = False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()

            registered = True

        else:
            print(user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request,'rango/register.html', {'user_form':user_form,
                                                'profile_form': profile_form,
                                                'registered' : registered})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username = username, password = password)#returns a user object if one is found and None if none exists

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))#httpresponseredirect class tells the client's web browser to redirect to the URL you provide as the argument
            else:
                return HttpResponse('Your Rango Account is Disabled')
        else:
            print(f"Invalid login details:{username}, {password}")
            return HttpResponse("Invalid login details supplied")
    else:
        return render(request, 'rango/login.html', {})

def about(request):
    if request.session.test_cookie_worked():
        print("TEST COOKIE WORKED!")
        request.session.delete_test_cookie()

    visitor_cookie_handler(request)
    visits = request.session['visits']
    return render(request, 'rango/about.html', {'visits' : visits})


@login_required
def restricted(request):
    return HttpResponse('You are logged in pal')

def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


# helper functions
def get_server_side_cookie(request, cookie, default_val = None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val

def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request,'visits', '1'))

    last_visit_cookie = get_server_side_cookie(request,'last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')

    # check if it's been more than a day since the last visit...
    if (datetime.now() - last_visit_time).seconds > 0:
        visits = visits + 1
        request.session['last_visit'] = str(datetime.now())
    else:
        visits = 1
        request.session['last_visit'] = last_visit_cookie

    request.session['visits'] = visits