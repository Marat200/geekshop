import random

from django.conf import settings
from django.core.cache import cache
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from django.views.decorators.cache import cache_page, never_cache

from mainapp.models import Product, ProductCategory


def get_links_menu():
    if settings.LOW_CACHE:
        key = 'categories'
        links_menu = cache.get(key)
        if links_menu is None:
            links_menu = ProductCategory.objects.filter(is_active=True)
            cache.set(key, links_menu)
        return links_menu
    return ProductCategory.objects.filter(is_active=True)


def get_category(pk):
    if settings.LOW_CACHE:
        key = f'category_{pk}'
        category_item = cache.get(key)
        if category_item is None:
            category_item = get_object_or_404(ProductCategory, pk=pk)
            cache.set(key, category_item)
        return category_item
    return get_object_or_404(ProductCategory, pk=pk)


@never_cache
def main(request):
    context = {
        'title': 'Главная',
        'products': Product.objects.all()[:4]
    }
    return render(request, 'mainapp/index.html', context=context)


# @never_cache
def get_hot_product():
    return random.sample(list(Product.objects.all()), 1)[0]


def get_same_products(hot_product):
    return Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk).select_related()[:3]


@cache_page(3600)
def products(request, pk=None, page=1):
    links_menu = get_links_menu()
    products_list = Product.objects.all()
    if pk is not None:
        if pk == 0:
            category_item = {
                'name': 'все',
                'pk': 0
            }
        else:
            category_item = get_category(pk)
            products_list = Product.objects.filter(category__pk=pk).select_related()

        paginator = Paginator(products_list, 2)
        try:
            product_paginator = paginator.page(page)
        except PageNotAnInteger:
            product_paginator = paginator.page(1)
        except EmptyPage:
            product_paginator = paginator.page(paginator.num_pages)
        context = {
            'links_menu': links_menu,
            'title': 'Продукты',
            'category': category_item,
            'products': product_paginator,
            'paginator_range': range(1, paginator.num_pages + 1)
        }
        return render(request, 'mainapp/products_list.html', context)

    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)
    context = {
        'links_menu': links_menu,
        'title': 'Продукты',
        'products': products_list,
        'hot_product': hot_product,
        'same_products': same_products
    }

    return render(request, 'mainapp/products.html', context=context)


def product(request, pk):
    context = {
        'product': get_object_or_404(Product, pk=pk),
        'links_menu': get_links_menu()
    }
    return render(request, 'mainapp/product.html', context)


def contact(request):
    context = {
        'title': 'Контакты'
    }
    return render(request, 'mainapp/contact.html', context=context)
