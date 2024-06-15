"""srvmedical URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from srvmedical import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
     path('', views.homePage, name="homepage"),
    path('cart/', views.cart, name="cart"),
    path('create/account/', views.createAccount, name="create-account"),
    path('signup/', views.signup, name="signup"),
    path('user/', views.userHomepage, name="user-index"),
    path('user/cart/', views.userCart, name="user-cart"),
    path('user/attach-prescription/',
         views.attachPrescription, name="user-prescription"),
    path('user/profile/', views.userProfile, name="user-profile"),
    path('update/profile/', views.updateProfile, name="update-profile"),
    path('review/order/', views.reviewOrder, name="review-order"),
    path('upload/', views.upload, name="upload"),
    path('search/', views.product_search, name='product_search'),
    path('user/search/', views.user_product_search, name='user_search'),
    path('category/<str:category>/', views.category_product, name='category_product'),
    path('orders/', views.orders, name="orders"),
    path('orders/placed/', views.placed_orders, name="placed_orders"),
    path('signin/', views.signin, name="signin"),
    path('user/logout/', views.userLogout, name="logout"),
    path('add/<int:product_id>/',views.add_to_cart, name="add_cart"),
    path('remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)