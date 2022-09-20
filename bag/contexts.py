from decimal import Decimal
from django.conf import settings

def bag_contents(request):

    bag_items = []
    total = 0        # intialize to zero
    product_count = 0

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