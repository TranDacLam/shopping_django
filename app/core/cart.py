from models import Product

class Cart:

    def __init__(self, old_cart):
        self.old_cart = old_cart
        self.total = old_cart.total
        self.quantity = old_cart.quantity
        self.items = old_cart.items

    def add(product_id, quantity, price):
        index = self.items.find(lambda x: x.id == product_id)



# {
#     quantity: 10,
#     total: 40000,
#     items:[
#         {
#             id: 1,
#             quantity: 2,
#             unit_price: 3000
#         },
#         {
#             id: 2,
#             quantity: 3,
#             unit_price: 4000
#         }
#     ]
# }