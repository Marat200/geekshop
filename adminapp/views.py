from datetime import datetime

from django.contrib.auth.decorators import user_passes_test
from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from adminapp.forms import ShopUserAdminEditForm, ProductEditForm, ProductCategoryEditForm
from authapp.forms import ShopUserRegisterForm
from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product


class AccessMixin:
    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class UserCreateView(AccessMixin, CreateView):
    model = ShopUser
    template_name = 'adminapp/user_form.html'
    form_class = ShopUserRegisterForm

    def get_success_url(self):
        return reverse('adminapp:user_list')


class UserListView(AccessMixin, ListView):
    model = ShopUser
    template_name = 'adminapp/users.html'


class UserUpdateView(AccessMixin, UpdateView):
    model = ShopUser
    template_name = 'adminapp/user_form.html'
    form_class = ShopUserAdminEditForm

    def get_success_url(self):
        return reverse('adminapp:user_list')


class UserDeactivateView(AccessMixin, DeleteView):
    model = ShopUser
    template_name = 'adminapp/user_deactivate.html'

    def get_success_url(self):
        return reverse('adminapp:user_list')

    def delete(self, *args, **kwargs):
        self.object = self.get_object()
        if self.object.is_active:
            self.object.is_active = False
        else:
            self.object.is_active = True
        self.object.save()
        return HttpResponseRedirect(reverse('adminapp:user_list'))


class UserDeleteView(AccessMixin, DeleteView):
    model = ShopUser
    template_name = 'adminapp/user_delete.html'

    def get_success_url(self):
        return reverse('adminapp:user_list')


class ProductCategoryCreateView(AccessMixin, CreateView):
    model = ProductCategory
    template_name = 'adminapp/category_form.html'
    form_class = ProductCategoryEditForm

    def get_success_url(self):
        return reverse('adminapp:category_list')


class ProductCategoryListView(AccessMixin, ListView):
    model = ProductCategory
    template_name = 'adminapp/categories.html'


class ProductCategoryUpdateView(AccessMixin, UpdateView):
    model = ProductCategory
    template_name = 'adminapp/category_form.html'
    form_class = ProductCategoryEditForm

    def get_success_url(self):
        return reverse('adminapp:category_list')

    def form_valid(self, form):
        if 'discount' in form.cleaned_data:
            discount = form.cleaned_data.get('discount')
            if discount:
                new_price = F('price') * (1 - discount / 100)
                with open('/logs/discount.log', 'a+', encoding='utf-8') as file:
                    file.seek(0)
                    file.write(
                        f"{datetime.now()}: old price - {F('price')}: discount - {discount}%: new price - {new_price}")
                self.object.product_set.update(price=new_price)
        return super().form_valid(form)


class ProductCategoryDeactivateView(DeleteView):
    model = ProductCategory
    template_name = 'adminapp/category_deactivate.html'

    def get_success_url(self):
        return reverse('adminapp:category_list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.is_active:
            self.object.is_active = False
        else:
            self.object.is_active = True
        self.object.save()
        return HttpResponseRedirect(reverse('adminapp:category_list'))


class ProductCategoryDeleteView(DeleteView):
    model = ProductCategory
    template_name = 'adminapp/category_delete.html'

    def get_success_url(self):
        return reverse('adminapp:category_list')


class ProductCreateView(AccessMixin, CreateView):
    model = Product
    template_name = 'adminapp/product_form.html'
    form_class = ProductEditForm

    def get_success_url(self):
        return reverse('adminapp:product_list', args=[self.kwargs['pk']])


class ProductListView(AccessMixin, ListView):
    model = Product
    template_name = 'adminapp/products.html'

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['category'] = get_object_or_404(ProductCategory, pk=self.kwargs.get('pk'))
        return context_data

    def get_queryset(self):
        return Product.objects.filter(category__pk=self.kwargs.get('pk'))


class ProductDetailView(AccessMixin, DetailView):
    model = Product
    template_name = 'adminapp/product_detail.html'


class ProductUpdateView(AccessMixin, UpdateView):
    model = Product
    template_name = 'adminapp/product_form.html'
    form_class = ProductEditForm

    def get_success_url(self):
        product_item = Product.objects.get(pk=self.kwargs['pk'])
        return reverse('adminapp:product_list', args=[product_item.category.pk])


class ProductDeactivateView(DeleteView):
    model = Product
    template_name = 'adminapp/product_deactivate.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object = self.get_object()

    def get_success_url(self):
        product_item = Product.objects.get(pk=self.kwargs['pk'])
        return reverse('adminapp:product_list', args=[product_item.category.pk])

    def delete(self, request, *args, **kwargs):
        if self.object.is_active:
            self.object.is_active = False
        else:
            self.object.is_active = True
        self.object.save()
        return HttpResponseRedirect(reverse('adminapp:product_list', args=[self.object.category.pk]))


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'adminapp/product_delete.html'

    def get_success_url(self):
        product_item = Product.objects.get(pk=self.kwargs['pk'])
        return reverse('adminapp:product_list', args=[product_item.category.pk])
