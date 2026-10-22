
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('shop/', views.shop_page, name='shop_page'),
     path('files-folders/', views.files_folders, name='files_folders'),
    path('paper-notebooks/', views.paper_notebooks, name='paper_notebooks'),
    path('pens-writing/', views.pens_writing, name='pens_writing'),
    path('school-supplies/', views.school_supplies, name='school_supplies'),
    path("about/", views.about, name="about"),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('payment/', views.payment, name='payment'),
path('payment-details/', views.payment_details, name='payment_details'),
path(
    'bill-download/<int:order_id>/',
    views.bill_download,
    name='bill_download'
),
path(
    'order-tracking/<int:order_id>/',
    views.order_tracking,
    name='order_tracking'
),
path(
    'product/<slug:product_slug>/',
    views.product_details,
    name='product_details'
),
path('my-orders/', views.my_orders, name='my_orders'),
path('my-addresses/', views.my_addresses, name='my_addresses'),
path(
    'my-addresses/edit/<int:address_id>/',
    views.edit_address,
    name='edit_address'
),
path(
    'my-addresses/delete/<int:address_id>/',
    views.delete_address,
    name='delete_address'
),
path('my-account/', views.my_account, name='my_account'),
path(
        'search/',
        views.global_product_search,
        name='global_product_search'
    ),
      
]
