from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render

from .context_processors import get_cart_counter

from .models import Cart
from menu.models import Category, FoodItem
from vendor.models import Vendor
from django.db.models import Prefetch

def marketplace(request):
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)
    vendor_count = vendors.count()
    context = {
        'vendors': vendors,
        'vendor_count': vendor_count,
    }
    return render(request, 'marketplace/listings.html', context)


def vendor_detail(request, vendor_slug):
    vendor = get_object_or_404(Vendor, vendor_slug = vendor_slug)
    categories = Category.objects.filter(vendor=vendor).prefetch_related(
        Prefetch(
            'fooditems',
            queryset = FoodItem.objects.filter(is_available=True)
        )
    )
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items = None
    context = {
        'vendor': vendor,
        'categories': categories,
        'cart_items': cart_items,

    }
    return render(request, 'marketplace/vendor_detail.html', context)



def add_to_cart(request, food_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Check if the food item mexist
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                # Check if the user has already added that food item to the cart
                try:
                    checkCart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    # Increase Cart quantity
                    checkCart.quantity += 1
                    checkCart.save()
                    return JsonResponse({'status': 'success', 'message': 'Increased Cart quantity', 'cart_counter': get_cart_counter(request), 'qty': checkCart.quantity})
                except:
                    checkCart = Cart.objects.create(user=request.user, fooditem=fooditem, quantity=1,)
                    return JsonResponse({'status': 'success', 'message': 'Added the food to the Cart', 'cart_counter': get_cart_counter(request), 'qty': checkCart.quantity})

            except:
                return JsonResponse({'status': 'failed', 'message': 'This food does not exist'})
        else:
            return JsonResponse({'status': 'failed', 'message': 'Invalid request'})
        
    else:
        return JsonResponse({'status': 'failed', 'message': 'Please, login to continue'})

