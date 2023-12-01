from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

from cart.forms import CartAddProductForm
from shop.models import Category, Product
from shop.recommender import Recommender


def product_list_view(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    if category_slug:
        category = get_object_or_404(Category,
                                     slug=category_slug)
        products = products.filter(category=category)

    return render(request,
                  'shop/product/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products, })


def product_detail_view(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    r = Recommender()
    recommended_products = r.suggest_products_for([product], 4)
    return render(
        request,
        'shop/product/detail.html',
        {'product': product,
         'cart_product_form': cart_product_form,
         'recommended_products': recommended_products})


def health(request):
    return JsonResponse({'status': 'ok'})
