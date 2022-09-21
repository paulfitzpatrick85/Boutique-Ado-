from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product

def bag_contents(request):

    bag_items = []
    total = 0        # intialize to zero
    product_count = 0
    bag = request.session.get('bag', {})           #access bag in session, session allows info to be stored until client and server are done communicating
                                                     #gets bag if it exists or intialize to empty dict if not

    # iterate through items in bag and get quantity and cost and add to bag_items array
    for item_id, quantity in bag.items():                   #bag from session
        product = get_object_or_404(Product, pk=item_id)     #get the product
        total += quantity * product.price                     # add quantity times the price to the total
        product_count += quantity                     # increment product count by quantity
        bag_items.append({                          # add dict to list of bag item
            'item_id': item_id,
            'quantity': quantity,
            'product': product,            # adding product object give access to all its related info when iterating through bag items in templates
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