from shop.models import ProductModel, ProductStatusType
from .models import CartModel, CartItemModel

class CartSession:
    total_payment_price = 0
    def __init__(self, session):
        self.session = session
        # search for get cart "cart"
        # if cart is not found, make a new one 
        # whith setdefault we get and update the session 
        self._cart = self.session.setdefault("cart", {"items": []})
        
    def add_product(self, product_id):
        for item in self._cart["items"]:
            if product_id == item["product_id"]:
                item["quantity"] += 1
                break
        else: 
            new_item = {
                "product_id":product_id,
                "quantity":1
            }
            self._cart["items"].append(new_item)
        self.save()

    def get_cart_dict(self):
        return self._cart
    
    def get_total_quantity(self):
        total_quantity = 0
        for item in self._cart["items"]:
            total_quantity += item["quantity"]
        return total_quantity
        # if we need return quantity of item:
        # total_quantity = len(self._cart["items"])


    def get_cart_items(self):
        cart_items = self._cart["items"]
        self.total_payment_price = 0
        for item in cart_items:
            # the object of product in session
            product_obj = ProductModel.objects.get(id=item["product_id"], status=ProductStatusType.publish.value)
            item["product_obj"] = product_obj
            total_price = int(item["quantity"]) * product_obj.get_int_price()
            item["total_price"] = total_price
            self.total_payment_price += total_price
        return cart_items
    
    def get_total_payment_amount(self):
        return self.total_payment_price
    
    def update_product_quantity(self,product_id, quantity):
        for item in self._cart["items"]:
            if product_id == item["product_id"]:
                item["quantity"] = int(quantity)
                break
        else:
            return
        self.save()

    def remove_product(self, product_id):
        for item in self._cart["items"]:
            if product_id == item["product_id"]:
                self._cart["items"].remove(item)
                break
        else:
            return
        self.save()

    def sync_cart_items_from_db(self,user):
        # get_or_create return tuple then we need two variables
        cart,created = CartModel.objects.get_or_create(user=user)
        cart_items = CartItemModel.objects.filter(cart=cart)
        for cart_item in cart_items:
            # look like update quantity function
            for item in self._cart["items"]:
                if str(cart_item.product.id) == item["product_id"]:
                    cart_item.quantity = item["quantity"]
                    cart_item.save()
                    break
            else:
                new_item = {
                "product_id":str(cart_item.product.id),
                "quantity":cart_item.quantity
                }
                self._cart["items"].append(new_item)
        # for keep the session after login again, because they update session after logout only
        self.merge_session_cart_in_db(user)
        self.save()


    def merge_session_cart_in_db(self,user):
        cart,created = CartModel.objects.get_or_create(user=user)
        for item in self._cart["items"]:
            # the object of product in session
            product_obj = ProductModel.objects.get(id=item["product_id"], status=ProductStatusType.publish.value)
            
            # get or create a cart_item if exist get if not create
            cart_item, created = CartItemModel.objects.get_or_create(cart=cart, product=product_obj)
            
            # after create cart_item or get cart_item need to sync quantity
            cart_item.quantity = item["quantity"]
            cart_item.save()
        
        # some data existed in database but not in session
        # get session existed item
        session_product_ids = [item['product_id'] for item in self._cart["items"]]
        # get all item of this user
        # exclude items are existed in database and session, if have another production in database delete them
        CartItemModel.objects.filter(cart=cart).exclude(product__id__in=session_product_ids).delete()

    def clear(self):
        self._cart = self.session["cart"] = {"items": []}
        self.save()

    def save(self):
        self.session.modified = True