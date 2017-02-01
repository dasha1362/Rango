from django.shortcuts import render
from django.http import HttpResponse
# Import Category model
from rango.models import Category
# Import Page model
from rango.models import Page
from rango.forms import CategoryForm
from rango.forms import PageForm

def add_category(request):
    form = CategoryForm()
    # A HTTP post?
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        # Valid form?
        if form.is_valid():
            # Save new category to database
            form.save(commit=True)
            return index(request)
        else:
            print(form.errors)
    return render(request, 'rango/add_category.html', {'form': form})

def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)
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
    return render(request,'rango/add_page.html', context_dict)

def show_category(request, category_name_slug):
    context_dict = {}

    try:
        # Get a category name slug with given name
        category = Category.objects.get(slug=category_name_slug)

        # Retrieve all of associated pages
        pages = Page.objects.filter(category=category)

        # Adds results list to template context under name pages
        context_dict['pages'] = pages
        # Also add category object from database to context dic
        # Used in template to verify existence of category
        context_dict['category'] = category
    except Category.DoesNotExist:
        # Template will display 'no category' message
        context_dict['category'] = None
        context_dict['pages'] = None

    return render(request, 'rango/category.html', context_dict)

def index(request):
    # Query database for list of all current categories
    # Order by likes in non-ascending order
    # Retrieve top 5 only
    category_list = Category.objects.order_by('-likes')[:5]
    # Put into dictionary to be passed to template
    context_dict = {'categories': category_list}
    page_list = Page.objects.order_by('-views')[:5]
    context_dict['pages'] = page_list
    return render(request, 'rango/index.html', context_dict)

def about(request):
    return render(request, 'rango/about.html')


#return HttpResponse(
    #"Rango says here is the about page!<br/> This tutorial has been put together by Darya Shumitskiy<br />  <a href='/rango/'>Index</a>")
