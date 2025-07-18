from order.models import Cart, Order, OrderItem


class OrderService:
    @staticmethod
    def create_order(user_id, cart_id):
        cart = Cart.objects.get(pk=cart_id)
        cart_item = cart.items.select_related("product").all()

        total_price = sum([item.product.price * item.quantity for item in cart_item])
        order = Order.objects.create(user_id=user_id, total_price=total_price)

        order_items = [
            OrderItem(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price,
                total_price=item.product.price * item.quantity,
            )
            for item in cart_item
        ]
        OrderItem.objects.bulk_create(order_items)

        cart.delete()

        return order
