from django.shortcuts import render
from django.http import HttpResponse
# Import Category model
from rango.models import Category
# Import Page model
from rango.models import Page

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
