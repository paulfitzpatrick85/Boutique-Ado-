from django.shortcuts import render, redirect


def view_bag(request):
    """ A view that rendera the bag """

    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):  # id of product being added to bag
    """ Add a quantity of the specified product to the shopping bag """

    quantity = int(request.POST.get('quantity'))       # get quatity from form. will come from template as string, so convert to int
    redirect_url = request.POST.get('redirect_url')   # where to redirect once process is finished
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    bag = request.session.get('bag', {})             # session allows info to be stored until client and server are done communicating
                                                    # in the case of e-commerce, allows cart items to be stored while user browses website
    
    if size:           # check if prod with size being added
        if item_id in list(bag.keys()):                     # if item in bag
            if size in bag[item_id]['items_by_size'].keys(): # check if item of same id and size already exists
                bag[item_id]['items_by_size'][size] += quantity # if so, increment item for that size
            else:
                bag[item_id]['items_by_size'][size] = quantity # otherwise, if new size for same item, set to quantity
        else:
            bag[item_id] = {'items_by_size': {size: quantity}} # if not in bag, add it. by size used over id in case same item different size is bought
    
    else: # if no size, run logic below
    
        if item_id in list(bag.keys()):
            bag[item_id] += quantity    # if item already in bag/key already in dict mathcing product id, then increment quantity
        else:
            bag[item_id] = quantity       # set key of item id to quantity

    request.session['bag'] = bag          # put 'bag' variable into session: overwrite variable in session with updated version
   #  print(request.session['bag'])         #just for testing that products are adding to, only seen in terminal though
    return redirect(redirect_url)   # redirect user back to redirect url
    