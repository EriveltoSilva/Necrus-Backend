import json
from django.db.models import Count
from ..models import Order, Product, Category


def get_order_and_items(request):
    if request.user.is_authenticated:
        user = request.user
        order, created = Order.objects.get_or_create(user=user, complete=False)
        items = order.get_cart_items
    else:
        cart = json.loads(request.COOKIES['cart']) if 'cart' in request.COOKIES else {}        
        items = []
        order = {"get_total_price":0, "get_total_items":0}
        for item in cart:
            try:
                product = Product.objects.get(id=item)
                order["get_total_items"] += cart[item]['quantity']
                order["get_total_price"] += (product.price * cart[item]['quantity'])

                items.append({
                    'product':{
                        'id':product.id,
                        'name':product.name,
                        'price':product.price,
                        'imageURL':product.imageURL
                    },
                    'quantity':cart[item]['quantity'],
                    'get_total':(product.price * cart[item]['quantity'])
                })
            except:
                print("Produto no carrinho do usuário não foi encontrado! Pode ter sido deletado do db!")  
    return (order, items)


def get_categories():
    return Category.objects.filter(is_published=True).annotate(num_products=Count('product'))