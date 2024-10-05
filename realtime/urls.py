from django.contrib import admin
from django.urls import path
from pizza import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('<order_id>/', views.order, name='order'),
    path('order_pizza/<pizza_id>/', views.order_pizza, name='order_pizza'),
]
