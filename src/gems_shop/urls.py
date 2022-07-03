"""gems_shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.conf.urls.static import static
from gems_shop import settings


from django.contrib import admin
from django.urls import path, include
from store.views import home, shop, gem_detail
from accounts.views import login, register, logout, activate, dashboard, forgotPassword, resetpassword_validate, resetPassword
from carts.views import cart, add_cart, remove_cart, remove_cart_item, checkout
from orders.views import place_order, payments


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('shop/', shop, name='shop'),
    path('category/<slug:category_slug>/', shop, name='gem_by_category'),
    path('category/<slug:category_slug>/<slug:gem_slug>/', gem_detail, name='gem_detail'),

    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('register/', register, name='register'),
    path('dashboard/', dashboard, name='dashboard'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('forgotPassword/', forgotPassword, name='forgotPassword'),
    path('resetpassword_validate/<uidb64>/<token>/', resetpassword_validate, name='resetpassword_validate'),
    path('resetPassword/', resetPassword, name='resetPassword'),

    path('cart/', cart, name='cart'),
    path('add_cart/<int:gem_id>/', add_cart, name='add_cart'),
    path('remove_cart/<int:gem_id>/<int:cart_item_id>/', remove_cart, name='remove_cart'),
    path('remove_cart_item/<int:gem_id>/<int:cart_item_id>/', remove_cart_item, name='remove_cart_item'),
    path('checkout/', checkout, name='checkout'), 
    
    # ORDERS
    path('place_order/', place_order, name='place_order'),
    path('payments/', payments, name='payments'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
