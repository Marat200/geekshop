from django import forms

from authapp.forms import ShopUserEditForm
from authapp.models import ShopUser
from mainapp.models import Product, ProductCategory


class ShopUserAdminEditForm(ShopUserEditForm):
    class Meta:
        model = ShopUser
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
            if field_name == 'password':
                field.widget = forms.HiddenInput()


class ProductEditForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ('is_active',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''


class ProductCategoryEditForm(forms.ModelForm):
    discount = forms.IntegerField(label='скидка', min_value=0, max_value=90, initial=0, required=False)

    class Meta:
        model = ProductCategory
        exclude = ('is_active',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
