from models import Product

class Cart:

    def __init__(self, old_cart):
        self.total_price = old_cart[
            'total_price'] if 'total_price' in old_cart else 0
        self.total_quantity = old_cart[
            'total_quantity'] if 'total_quantity' in old_cart else 0
        self.items = old_cart[
            'items'] if 'items' in old_cart else []


    def add(self, product, quantity):
        # find_product = next((item for (index, item) in self.old_cart if item["id"] == product.id), None)
        index = self.find_index(id=product.id)
        if index is not None:
            self.items[index]['quantity'] += quantity
        else:
            self.items.append({
                    'id': product.id,
                    'quantity': quantity,
                    'price': product.unit_price,
                    'image': str(product.image),
                    'category': product.category.name,
                    'name': product.name
                })
        self.total_quantity += quantity
        self.total_price += quantity * product.unit_price


    def remove(self, id):
        index = self.find_index(id=id)
        if self.items and index is not None:
            product = self.items[index]
            self.total_quantity -= product['quantity']
            self.total_price -= product['quantity'] * product['price']
            self.items.pop(index)


    def find_index(self, id):
        index = next((index for (index, item) in enumerate(self.items) if item['id'] == id), None)
        print 'index', index
        return index



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