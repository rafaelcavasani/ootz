from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Kit, KitProduct
from product.serializers import ProductSerializer


class KitProductSerializer(ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = KitProduct
        fields = '__all__'


class KitSerializer(ModelSerializer):
    products = KitProductSerializer(source='kitproduct_set', many=True)

    class Meta:
        model = Kit
        fields = '__all__'
