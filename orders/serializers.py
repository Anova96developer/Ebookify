from rest_framework import serializers

from orders.models import Order


class AllOrdersSerializer(serializers.ModelSerializer):
    """Serializer to get all orders of customers"""

    username = serializers.StringRelatedField(source="user.username")
    book_category = serializers.StringRelatedField(source="book.book_category")
    book_title = serializers.StringRelatedField(source="book.title")

    class Meta:
        model = Order
        fields = "__all__"
        read_only_fields = [
            "username",
            "book_category",
            "book_title",
            "price_wrt_quantity",
            "order_status",
            "user",
        ]

    def create(self, validated_data):
        book = validated_data["book"]
        quantity = validated_data["quantity"]

        validated_data["price_wrt_quantity"] = book.price * quantity
        return super().create(validated_data)

    def update(self, instance, validated_data):
        order = super().update(instance, validated_data)

        order.price_wrt_quantity = order.book.price * order.quantity
        order.save()
        return order


class UpdateOrderStatus(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["order_status", "order_Id"]
