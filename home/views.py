import json

from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from content.models import Menu, Content, CImages
from home.forms import SearchForm, SignUpForm
from home.models import Setting, ContactForm, ContactFormMessage, UserProfile
from order.models import ShopCart
from product.models import Product, Category, Images, Comment


def index(request):
    setting = Setting.objects.get(pk=1)
    sliderdata = Product.objects.all()[:4]
    category = Category.objects.all()
    menu = Menu.objects.all()
    dayproducts = Product.objects.all().order_by('?')[:6]
    lastproducts_active = Product.objects.all().order_by('-id')[:3]
    lastproducts_passive = Product.objects.all().order_by('-id')[:7]
    randomproducts = Product.objects.all().order_by('?')[:3]
    request.session['cart_items'] = ShopCart.objects.filter(user_id=request.user.id).count()
    news = Content.objects.filter(type='haber').order_by('-id')[:4]
    announcements = Content.objects.filter(type='haber').order_by('-id')[:4]

    context = {'setting': setting,
               'category': category,
               'page': 'home',
               'sliderdata': sliderdata,
               'dayproducts': dayproducts,
               'lastproducts_active': lastproducts_active,
               'lastproducts_passive': lastproducts_passive,
               'randomproducts': randomproducts,
               'menu': menu,
               'news': news,
               'announcements': announcements,
               }
    return render(request, 'index.html', context)


def hakkimizda(request):
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting, 'page': 'hakkimizda'}
    return render(request, 'hakkimizda.html', context)


def referanslar(request):
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting, 'page': 'referanslar'}
    return render(request, 'referanslar.html', context)


def iletisim(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            data = ContactFormMessage()
            data.name = form.cleaned_data['name']
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            messages.success(request, "Mesajınız başarıyla kaydedilmiştir. Teşekkür ederiz.")
            return HttpResponseRedirect('/iletisim')

    setting = Setting.objects.get(pk=1)
    form = ContactForm()
    context = {'setting': setting, 'form': form, 'page': 'iletisim'}
    return render(request, 'iletisim.html', context)


def category_products(request, id, slug):
    category = Category.objects.all()
    categorydata = Category.objects.get(pk=id)
    sliderdata = Product.objects.all().order_by('?')[:4]
    products = Product.objects.filter(category_id=id)
    context = {'products': products,
               'category': category,
               'categorydata': categorydata,
               'sliderdata': sliderdata
               }
    return render(request, 'products.html', context)


def product_detail(request, id, slug):
    category = Category.objects.all()
    product = Product.objects.get(pk=id)
    images = Images.objects.filter(product_id=id)
    comments = Comment.objects.filter(product_id=id, status='True')

    context = {'product': product,
               'category': category,
               'images': images,
               'comments': comments,
               }
    return render(request, 'product_detail.html', context)


def product_search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            category = Category.objects.all()
            query = form.cleaned_data['query']
            products = Product.objects.filter(title__icontains=query)
            context = {'products': products,
                       'category': category,
                       }
            return render(request, 'product_search.html', context)

    return HttpResponseRedirect('/')


def product_search_auto(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        product = Product.objects.filter(title__icontains=q)
        results = []
        for rs in product:
            product_json = {}
            product_json = rs.title
            results.append(product_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'

    return HttpResponse(data, mimetype)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            userprofile = UserProfile.objects.get(user_id=request.user.id)
            request.session['userimage'] = userprofile.image.url
            return HttpResponseRedirect('/')
        else:
            messages.warning(request, "Giriş Hatası! Kullanıcı adı ya da parolası yanlış.")
            return HttpResponseRedirect('/login')
    return render(request, 'login.html')


def join_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = request.POST['username']
            password = request.POST['password1']
            user = authenticate(request, username=username, password=password)
            login(request, user)
            current_user = request.user
            data = UserProfile()
            data.user_id = current_user.id
            data.image = 'images/users/user.png'
            data.save()
            return HttpResponseRedirect('/')

    form = SignUpForm()
    context = {
        'form': form,
    }
    return render(request, 'signup.html', context)

def menu(request, id):
    content = Content.objects.get(menu_id=id)

    if content:
        link = '/content/' + str(content.id) + '/menu'
        return HttpResponseRedirect(link)
    else:
        messages.warning(request, "Hata! İlgili içerik Bulunamadı")
        link = '/'
        return HttpResponseRedirect(link)

def content_detail(request, id, slug):
    menu = Menu.objects.all()
    content = Content.objects.get(pk=id)
    images = CImages.objects.filter(content_id=id)
    category = Category.objects.all()
    context = {
        'content': content,
        'menu': menu,
        'images': images,
        'category': category,
    }
    return render(request, 'content_detail.html', context)

