# we can show this content just call key like this {{key}} on html file
# we add this function to settings.TEMPLATES.OPTIOND.context_processor
from .cart import CartSession


def cart_processor(request):
    cart = CartSession(request.session)
    return {"cart": cart}