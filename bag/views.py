from django.shortcuts import render


def view_bag(request):
    """ A view that rendera the bag """

    return render(request, 'bag/bag.html')