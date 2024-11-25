"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from .import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login/', views.login_user, name='login'),
    path('register/', views.register_user, name='register'),
    path('profile/', views.profile_user, name='profile'),
    path('logout/', views.logout_user, name='logout'),
    path('product/<int:pk>/', views.product, name='product'),
    path('category/<int:pk>/', views.category_products, name='category_products'),
    path('search/', views.searched_products, name='search'),
    path('cart/', views.cart, name='cart'),
    path('cart_action/<int:pk>/', views.cart_action, name='cart_action'),
    path('cart_quantity/<int:pk>/', views.cart_quantity, name='cart_quantity'),
    path('complete_order/', views.complete_order, name='complete_order'),
    path('opinion/<int:pk>/', views.opinion_action, name='opinion'),
    path('user_order/<int:pk>/', views.user_order, name='user_order'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

