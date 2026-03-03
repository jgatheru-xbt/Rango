# here you store a series of functions to handle requests and return responses  
from django.shortcuts import render #streamlines the process of combining given template with a context dictionary.Automates a threee step process i.e, loading the template, merging data into it and creating the HttpResponse object.
from django.http import HttpResponse
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm

def index(request):

    category_list = Category.objects.order_by('-likes')[:5]
    top_pages =  Page.objects.order_by('-views')[:5]

    context_dict = {"categories": category_list,
                    "top_pages": top_pages
                        }
    return render(request, 'rango/index.html', context = context_dict)



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

def about(request):
    return HttpResponse('this is the about page <br> Go back to home  http://127.0.0.1:8000/rango/')