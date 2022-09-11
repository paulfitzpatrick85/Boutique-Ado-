from django.shortcuts import render
from .models import Product

def all_products(request):
    """ A view to show all products, including sorting and search queries """

    products = Product.objects.all()    # return all products from database

    context = {              # make products available in the template
        'products': products,
    }

    return render(request, 'products/products.html', context)  
    # context is needed to send things back to the template