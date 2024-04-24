class CartSession:
    def __init__(self, session):
        self.session = session
        # search for get cart "cart"
        # if cart is not found, make a new one 
        self.cart = self.session.get("cart", 
        {
            "items": [],
            "total_price": 0,
            "total_items": 0,
        })
        self.session["cart"] = self.cart