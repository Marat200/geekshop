from django.urls import path
from ordersapp import views as ordersapp

app_name = 'ordersapp'

urlpatterns = [
    path('', ordersapp.OrderListView.as_view(), name='list'),
    path('create/', ordersapp.OrderCreateView.as_view(), name='create'),
    path('detail/<int:pk>/', ordersapp.OrderDetailView.as_view(), name='detail'),
    path('update/<int:pk>/', ordersapp.OrderUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', ordersapp.OrderDeleteView.as_view(), name='delete'),
    path('forming/<int:pk>/', ordersapp.order_forming_complete, name='forming_complete'),
    path('product/price/<int:pk>/', ordersapp.get_product_price, name='get_product_price'),
]
