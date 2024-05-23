from cart_app.models import Cart


def context_processors(request):
    try:
        if request.user.is_authenticated:
            cart = Cart.objects.get(user=request.user)
        else:
            session_id = request.session.get("anonymous_user")
            cart = Cart.objects.get(session_id=session_id)
    except:
        cart = {"total_quantity": 0,
                "len": 0,
                "total_cart_price": 0
                }

    return {"cart": cart}
