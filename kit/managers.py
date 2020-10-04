from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.apps import apps

from .forms import KitProductForm


class KitProductManager(models.Manager):
    def create_all(self, kit_products, kit):
        for kit_product in kit_products:
            kit_product_form = KitProductForm(kit_product)
            if not kit_product_form.is_valid():
                return kit_product_form.errors
            super().get_queryset().create(kit=kit, **kit_product)

        return None

    def update_all(self, kit_products, kit):
        for kit_product in kit_products:
            kit_product_form = KitProductForm(kit_product)
            if not kit_product_form.is_valid():
                return kit_product_form.errors
            kit_product_id = kit_product.get('id', None)
            if kit_product_id:
                try:
                    kit_product_persistent = super().get_queryset().get(id=kit_product_id, kit=kit)
                    kit_product_persistent.quantity = kit_product.get(
                        'quantity', None)
                    kit_product_persistent.discount = kit_product.get(
                        'discount', None)
                    kit_product_persistent.save()

                except ObjectDoesNotExist as error:
                    return {'Error: {}'.format(error)}

            else:
                super().get_queryset().create(kit=kit, **kit_product)

        return None

    def delete_all(self, kit_products, kit):
        for kit_product in kit_products:
            kit_product_id = kit_product.get('id', None)
            try:
                kit_product_persistent = super().get_queryset().get(
                    id=kit_product_id, kit=kit)
                kit_product_persistent.delete()
            except ObjectDoesNotExist as error:
                return {'Error: {}.'.format(error)}

        return None
