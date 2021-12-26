from django.urls import path
from adminapp import views as admin_views

app_name = 'adminapp'

urlpatterns = [
    path('users/create/', admin_views.UserCreateView.as_view(), name='user_create'),
    path('users/', admin_views.UserListView.as_view(), name='user_list'),
    path('users/update/<int:pk>/', admin_views.UserUpdateView.as_view(), name='user_update'),
    path('users/deactivate/<int:pk>/', admin_views.UserDeactivateView.as_view(), name='user_deactivate'),
    path('users/delete/<int:pk>/', admin_views.UserDeleteView.as_view(), name='user_delete'),

    path('categories/create/', admin_views.ProductCategoryCreateView.as_view(), name='category_create'),
    path('categories/', admin_views.ProductCategoryListView.as_view(), name='category_list'),
    path('categories/update/<int:pk>/', admin_views.ProductCategoryUpdateView.as_view(), name='category_update'),
    path('categories/deactivate/<int:pk>/', admin_views.ProductCategoryDeactivateView.as_view(), name='category_deactivate'),
    path('categories/delete/<int:pk>/', admin_views.ProductCategoryDeleteView.as_view(), name='category_delete'),

    path('products/create/<int:pk>/', admin_views.ProductCreateView.as_view(), name='product_create'),
    path('products/<int:pk>/', admin_views.ProductListView.as_view(), name='product_list'),
    path('products/detail/<int:pk>/', admin_views.ProductDetailView.as_view(), name='product_detail'),
    path('products/update/<int:pk>/', admin_views.ProductUpdateView.as_view(), name='product_update'),
    path('products/deactivate/<int:pk>/', admin_views.ProductDeactivateView.as_view(), name='product_deactivate'),
    path('products/delete/<int:pk>/', admin_views.ProductDeleteView.as_view(), name='product_delete'),
]
