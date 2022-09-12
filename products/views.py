from django.shortcuts import render, get_object_or_404
from .models import Product

def all_products(request):
    """ A view to show all products, including sorting and search queries """

    products = Product.objects.all()    # return all products from database

    context = {              # make products available in the template
        'products': products,
    }

    return render(request, 'products/products.html', context)  
    # context is needed to send things back to the template


def product_detail(request, product_id):
    """ A view to show individual product details """

    products = get_object_or_404(Product, pk=product_id)

    context = {              # make products available in the template
        'products': product,
    }

    return render(request, 'products/products.html', context)  
    # context is needed to send things back to the template