import math
from django.db import transaction
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework.decorators import action

from .forms import KitForm
from .models import Kit, KitProduct
from .serializers import KitSerializer, KitProductSerializer
from product.serializers import ProductSerializer


class KitViewSet(ModelViewSet):
    queryset = Kit.objects.all()
    serializer_class = KitSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        kit_form = KitForm(request.data)
        if not kit_form.is_valid():
            return Response(data=kit_form.errors, status=400)

        try:
            kit_persistent = Kit.objects.get(sku=request.data.get('sku', None))
            if kit_persistent:
                data = {"sku": [
                    "Kit com este sku já existe."
                ]}
                return Response(data=data, status=400)
        except:
            pass

        kit = Kit.objects.create(
            sku=request.data.get('sku', None),
            name=request.data.get('name', None),
        )

        kit_products = request.data.get('products', None)
        if kit_products:
            products_add = KitProduct.objects.create_all(kit_products, kit)
            if products_add is not None:
                transaction.set_rollback(True)
                return Response(data=products_add, status=404)

        serializer = KitSerializer(kit)
        return Response(data=serializer.data, status=202)

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        kit_form = KitForm(request.data)
        if not kit_form.is_valid():
            return Response(data=kit_form.errors, status=400)

        kit_sku = kwargs['pk']
        try:
            kit = Kit.objects.get(sku=kit_sku)
        except Kit.DoesNotExist:
            data = {"datail": "Kit não encontrado."}
            return Response(data=data, status=404)

        kit.name = request.data.get('name', None)
        kit.save()

        kit_products = request.data.get('products', None)
        if kit_products:
            products_add = KitProduct.objects.update_all(kit_products, kit)
            if products_add is not None:
                transaction.set_rollback(True)
                return Response(data=products_add, status=404)

        deleted_products = request.data.get('deleted_products', None)
        if deleted_products:
            products_delete = KitProduct.objects.delete_all(
                deleted_products, kit)
            if products_delete is not None:
                transaction.set_rollback(True)
                return Response(data=products_delete, status=404)

        serializer = KitSerializer(kit)
        return Response(data=serializer.data, status=200)

    @action(methods=['GET'], detail=True, url_path='price')
    def kpi(self, request, *args, **kwargs):
        kit_sku = kwargs['pk']
        try:
            kit = Kit.objects.get(sku=kit_sku)
        except Kit.DoesNotExist:
            data = {"datail": "Kit não encontrado."}
            return Response(data=data, status=404)

        kit_products = KitProduct.objects.filter(kit=kit)

        stock = 0
        cost = 0
        price = 0
        if kit_products:
            for kit_product in kit_products:
                cost = cost + (kit_product.product.cost * kit_product.quantity)
                discount = (kit_product.product.price *
                            kit_product.discount) / 100
                price = price + ((kit_product.product.price - discount) *
                                 kit_product.quantity)
                min_product_stock = kit_product.product.stock / kit_product.quantity

                if stock != 0 and min_product_stock < stock:
                    stock = min_product_stock
                else:
                    stock = min_product_stock if stock == 0 else stock

        result = {
            'name': kit.name,
            'sku': kit.sku,
            'cost': cost,
            'price': price,
            'stock': math.floor(stock),
        }
        return Response(data=result, status=200)
