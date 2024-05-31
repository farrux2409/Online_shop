from typing import Optional

from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from app.forms import ProductModelForm, CommentModelForm, OrderModelForm
from app.models import Product, Category, Order


# Create your views here.

# 1-version
# def index_page(request, cat_id=None):
#     filter_type = request.GET.get('filter', '')
#     categories = Category.objects.all()
#     if cat_id:
#         products = Product.objects.filter(category=cat_id)
#         if filter_type == 'expensive':
#             products = products.filter(price__gte=10000)
#         elif filter_type == 'cheap':
#             products = products.filter(price__lt=10_000)
#     else:
#         products = Product.objects.all()
#         if filter_type == 'expensive':
#             products = products.filter(price__gte=10000)
#         elif filter_type == 'cheap':
#             products = products.filter(price__lt=10_000)
#
#     context = {
#         'products': products,
#         'categories': categories
#
#     }
#     return render(request, 'app/home.html', context)
#
def index_page(request, cat_id=None):
    filter_type = request.GET.get('filter', '')
    search = request.GET.get('search', '')
    categories = Category.objects.all()
    if cat_id:
        products = Product.objects.filter(category=cat_id)
        if filter_type == 'expensive':
            products = products.order_by('-price')[:4]
        elif filter_type == 'cheap':
            products = products.order_by('price')[:4]
    else:
        products = Product.objects.all()
        if filter_type == 'expensive':
            products = products.order_by('-price')[:4]
        elif filter_type == 'cheap':
            products = products.order_by('price')[:4]
    if search:
        products = Product.objects.filter(
            Q(name__icontains=search) | Q(description__icontains=search) | Q(price__contains=search) | Q(
                category__title__search=search))

    context = {
        'products': products,
        'categories': categories

    }
    return render(request, 'app/home.html', context)


def detail_product(request, pk):
    product = Product.objects.get(id=pk)
    comments = product.comments.filter(is_active=True)
    search = request.GET.get('search', '')
    price_lower_bound = product.price * 0.8
    price_upper_bound = product.price * 1.2
    similar_products = Product.objects.filter(Q(price__lte=price_upper_bound) &
                                              Q(price__gte=price_lower_bound)).exclude(id=pk)

    # comments = product.comments.all().order_by('-created_at')
    # comments = product.comments.all().order_by('-created_at')[:3]
    if search:
        products = Product.objects.filter(
            Q(name__icontains=search) | Q(description__icontains=search) |
            Q(price__contains=search))

    count = product.comments.count()
    context = {
        'product': product,
        'comments': comments,
        'count': count,
        'similar_products': similar_products
    }

    return render(request, 'app/detail.html', context)


def order_product(request, pk):
    product = get_object_or_404(Product, id=pk)
    form = OrderModelForm()
    if request.method == 'POST':
        form = OrderModelForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.product = product
            order.save()
            return redirect('detail', pk)
        context = {
            'form': form,
            'product': product
        }
        return render(request, 'app/detail.html', context)


# def add_product(request):
#     if request.method == 'POST':
#         form = ProductForm(request.POST, request.FILES)
#         if form.is_valid():
#             name = request.POST['name']
#             description = request.POST['description']
#             price = request.POST['price']
#             image = request.FILES['image']
#             rating = request.POST['rating']
#             discount = request.POST['discount']
#             product = Product(name=name, description=description, price=price, image=image, rating=rating,
#                               discount=discount)
#             product.save()
#             return redirect('index')
#
#     else:
#         form = ProductForm()
#     return render(request, 'app/add-product.html', {'form': form})


def add_product(request):
    if request.method == 'POST':
        form = ProductModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')

    else:
        form = ProductModelForm()

    context = {
        'form': form,
    }
    return render(request, 'app/add-product.html', context)


def add_comment(request, product_id):
    # product = Product.objects.get(id=product_id)
    product = get_object_or_404(Product, id=product_id)
    form = CommentModelForm()
    if request.method == 'POST':
        form = CommentModelForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = product
            comment.save()
            return redirect('detail', product_id)

    context = {
        'form': form,
        'product': product
    }

    return render(request, 'app/detail.html', context)


def delete_product(request, pk):
    product = Product.objects.filter(id=pk).first()
    if product:
        product.delete()
        return redirect('index')
    return render('app/detail.html', {'product': product})


def edit_product(request, pk):
    product = Product.objects.get(id=pk)
    form = ProductModelForm(instance=product)
    if request.method == 'POST':
        form = ProductModelForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('detail', pk)
    context = {
        'form': form,
        'product': product
    }

    return render(request, 'app/update-product.html', context)
