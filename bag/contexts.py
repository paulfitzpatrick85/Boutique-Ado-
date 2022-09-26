from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product

def bag_contents(request):

    bag_items = []
    total = 0        # intialize to zero
    product_count = 0
    bag = request.session.get('bag', {})           # access bag in session, session allows info to be stored until client and server are done communicating
                                                     # gets bag if it exists or intialize to empty dict if not

    # iterate through items in bag and get quantity and cost and add to bag_items array
    for item_id, item_data in bag.items():                   # bag from session, item with no size-item will just be quantity, otherwise will be dict of item by size
       # only use this code if no sizes, evident by checking if item is int 
        if isinstance(item_data, int):                    # if is int, then item data = quantity, otherwise its a dict
            product = get_object_or_404(Product, pk=item_id)     # get the product
            total += item_data * product.price                     # add quantity times the price to the total
            product_count += item_data                     # increment product count by quantity
            bag_items.append({                          # add dict to list of bag item
                'item_id': item_id,
                'quantity': item_data,
                'product': product,            # adding product object give access to all its related info when iterating through bag items in templates
            })
        else:
            product = get_object_or_404(Product, pk=item_id)
            for size, quantity in item_data['items_by_size'].items(): # iterate through inner dict by items_by_size
                total += quantity * product.price  
                product_count += quantity         # increment product and total
                bag_items.append({   #for each item, add size to bag items returned to the template, this is how to render the sizes in the template
                    'item_id': item_id,
                    'quantity': quantity,
                    'product': product,
                    'size': size,
                })


    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100) # if total is less than free trehold - calcaulate total * SDP/100 (10%)
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total  # tells user how much more there need to spend to get free delivery
        
    else:          # if total is greater or equal to threshold
        delivery = 0    
        free_delivery_delta = 0
    
    grand_total = delivery + total
    
    context = {                              #returns a dict. this is a context processor. it make the dict available to all templates in app(boutiqe ado)
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
    }

    return context