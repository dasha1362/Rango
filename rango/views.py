from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
# Import Category model
from rango.models import Category
# Import Page model
from rango.models import Page
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse

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

def register(request):
    # When registration succeeds, this will be changed to true
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If forms are valid
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            # Hash password
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            # Did user provide a profile picture?
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()
            registered = True

        else:
            print(user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'rango/register.html', {'user_form': user_form, 'profile_form': profile_form, 'registered':registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'rango/login.html', {})
