from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q    # if query is not blank, this generates search query
from .models import Product

def all_products(request):
    """ A view to show all products, including sorting and search queries """

    products = Product.objects.all()    # return all products from database
    query = None                  # none ensure user doesn't get error when searching without inputting search term

    if request.GET:                      # check if request.get exists
        if 'q' in request.GET:           # name attrib in form is 'q', 
            query = request.GET['q']
            if not query:                # if query blank = no results, so display message, then redirect
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))
            
            # name or description can contain the query that is searched
            queries = Q(name__icontains=query) | Q(description__icontains=query)  # 'i' makes query case INsensitive
            products = products.filter(queries)  # then pass to filter mehtod to filter products

    context = {              # make products available in the template
        'products': products,
        'search_term': query,  # in template, query is called 'search term'
    }

    return render(request, 'products/products.html', context)  
    # context is needed to send things back to the template


def product_detail(request, product_id):
    """ A view to show individual product details """

    product = get_object_or_404(Product, pk=product_id)

    context = {              # make products available in the template
        'product': product,
    }

    return render(request, 'products/product_detail.html', context)  
    # context is needed to send things back to the template