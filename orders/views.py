from rest_framework import viewsets, filters, status
from rest_framework.response import Response


from orders.serializers import AllOrdersSerializer, UpdateOrderStatus
from .models import Order
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from django.conf import settings


class AllOrderViewSets(viewsets.ModelViewSet):

    user = settings.AUTH_USER_MODEL
    queryset = Order.objects.all().order_by("-date_created")
    serializer_class = AllOrdersSerializer
    permission_classes = [AllowAny]
    http_method_names = ["get", "post", "patch", "put", "delete"]
    permission_classes = [IsAuthenticated]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    search_fields = [
        "order_Id",
        "book__book_category",
        "book__title",
        "user__username",
        "order_status",
    ]
    ordering_fields = ["created_at"]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def paginate_results(self, queryset):
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(
        methods=["GET"],
        detail=False,
        url_path="single-customer-orders",
        permission_classes=[IsAuthenticated],
        url_name="single_customer_orders",
    )
    def single_customer_orders(self, request, *args, **kwargs):
        """This end points get all the orders made by a single customer"""

        queryset = Order.objects.all().filter(user=request.user.id)
        serializer = AllOrdersSerializer(queryset, many=True)
        return Response(
            data={"success": True, "data": serializer.data}, status=status.HTTP_200_OK
        )

    @action(
        methods=["POST"],
        detail=True,
        url_path="update-order-status",
        permission_classes=[IsAuthenticated],
        serializer_class=UpdateOrderStatus,
        url_name="update_order_status",
    )
    def update_order_status(self, request, *args, **kwargs):
        order = self.get_object()

        serializer = UpdateOrderStatus(data=request.data)
        if serializer.is_valid():
            order.order_status = serializer.data["order_status"]
            order.save()
            return Response(
                data={"success": True, "data": serializer.data},
                status=status.HTTP_200_OK,
            )
