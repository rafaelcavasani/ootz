from django import forms


class KitForm(forms.Form):
    sku = forms.CharField(max_length=50, required=True)
    name = forms.CharField(max_length=100, required=True)


class KitProductForm(forms.Form):
    product_id = forms.CharField(max_length=50, required=True)
    quantity = forms.IntegerField(required=True)
    discount = forms.DecimalField(required=True)
