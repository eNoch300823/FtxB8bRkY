# 代码生成时间: 2025-09-23 08:12:10
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from typing import Dict, List

# Shopping cart item data model
class CartItem:
    def __init__(self, product_id: int, quantity: int):
        self.product_id = product_id
        self.quantity = quantity

# Shopping cart data model
class ShoppingCart:
    def __init__(self):
        self.items: Dict[int, CartItem] = {}

    def add_item(self, product_id: int, quantity: int) -> None:
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")
        if product_id in self.items:
            self.items[product_id].quantity += quantity
        else:
            self.items[product_id] = CartItem(product_id, quantity)

    def remove_item(self, product_id: int) -> None:
        if product_id in self.items:
            del self.items[product_id]
        else:
            raise ValueError("Product not found in the cart.")

    def get_cart_items(self) -> List[CartItem]:
        return list(self.items.values())

# Shopping cart service
class ShoppingCartService:
    def __init__(self):
        self.carts: Dict[str, ShoppingCart] = {}

    def create_cart(self, user_id: str) -> str:
        self.carts[user_id] = ShoppingCart()
        return user_id

    def get_cart(self, user_id: str) -> JSONResponse:
        if user_id not in self.carts:
            return JSONResponse({'error': 'Cart not found'}, status_code=HTTP_404_NOT_FOUND)
        return JSONResponse({'cart': [{'product_id': item.product_id, 'quantity': item.quantity} for item in self.carts[user_id].get_cart_items()]}, status_code=HTTP_200_OK)

    def add_item_to_cart(self, user_id: str, product_id: int, quantity: int) -> JSONResponse:
        if user_id not in self.carts:
            return JSONResponse({'error': 'Cart not found'}, status_code=HTTP_404_NOT_FOUND)
        try:
            self.carts[user_id].add_item(product_id, quantity)
        except ValueError as e:
            return JSONResponse({'error': str(e)}, status_code=HTTP_400_BAD_REQUEST)
        return JSONResponse({'message': 'Item added to cart'}, status_code=HTTP_200_OK)

    def remove_item_from_cart(self, user_id: str, product_id: int) -> JSONResponse:
        if user_id not in self.carts:
            return JSONResponse({'error': 'Cart not found'}, status_code=HTTP_404_NOT_FOUND)
        try:
            self.carts[user_id].remove_item(product_id)
        except ValueError as e:
            return JSONResponse({'error': str(e)}, status_code=HTTP_400_BAD_REQUEST)
        return JSONResponse({'message': 'Item removed from cart'}, status_code=HTTP_200_OK)

# Create the Starlette application
app = Starlette(debug=True, routes=[
    Route('/cart', endpoint=ShoppingCartService(), methods=['POST']),
    Route('/cart/{user_id}', endpoint=ShoppingCartService(), methods=['GET']),
    Route('/cart/{user_id}/add', endpoint=ShoppingCartService(), methods=['POST']),
    Route('/cart/{user_id}/remove/{product_id}', endpoint=ShoppingCartService(), methods=['POST'])
])

# Documentation
"""
Shopping Cart Service API Documentation

Endpoints:
- POST /cart: Create a new shopping cart for a user
- GET /cart/{user_id}: Retrieve a user's shopping cart
- POST /cart/{user_id}/add: Add an item to a user's shopping cart
- POST /cart/{user_id}/remove/{product_id}: Remove an item from a user's shopping cart
"""