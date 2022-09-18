from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q    # if query is not blank, this generates search query
from .models import Product, Category

def all_products(request):
    """ A view to show all products, including sorting and search queries """

    products = Product.objects.all()    # return all products from database
    query = None                  # none ensure user doesn't get error when searching without inputting search term
    categories = None

    
    if request.GET:                 # check if category exists in request.get
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')  # if it does, split into list at the commas
            products = products.filter(category__name__in=categories) # use list to filter current queryset of all products down to products whose category name is in the list
            categories = Category.objects.filter(name__in=categories) # display to user categories they have selected, filter categories down to the ones whose name is in the url

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
        'current_categories': categories  # list of category objects rerurned to context to use in template
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