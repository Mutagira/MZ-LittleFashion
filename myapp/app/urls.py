from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.home, name = 'home'),
    path('index', views.home, name = 'home'),
    path('about/', views.about, name='about'),
    path('faq/', views.faq, name='faq'),
    path('products/', views.products, name='products'),
    path('product-detail/<int:id>/', views.product_detail, name='product-detail'),

    path('login/', views.log_in, name='login'),
    path('logout/', views.log_out, name='logout'),
    path('sign-up/', views.sign_up, name='sign_up'),
    path('contact/', views.contact, name='contact'),
   
    path('profile/', views.profile_view, name='profile'),
    path('address/', views.address_view, name='address'),
    path('address/update/', views.update_address, name='update-address'),
    path('address/add/', views.add_address, name='add-address'),

    path('add-to-cart/', views.add_to_cart, name='cart'),
    path('view-cart/', views.view_cart, name='view_cart'),
    path('cart/increase/<int:cart_id>/', views.increase_quantity, name='increase_quantity'),
    path('cart/decrease/<int:cart_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('cart/delete/<int:cart_id>/', views.delete_cart_item, name='delete_cart_item'),
    
    path('checkout/', views.checkout, name='checkout'),
    path('place-order/', views.place_order, name='place_order'),
    path('orders/', views.user_orders, name='user_orders'),
]