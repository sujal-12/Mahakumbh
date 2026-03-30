
from django.urls import path
from app import views


urlpatterns = [
    path('', views.index, name='index'),   
    path('shopkeeper_register', views.shopkeeper_register, name='shopkeeper_register.html'),
    path('admin_dashboard', views.admin_dashboard, name='admin_dashboard.html'),
    path('visitor_dashboard', views.visitor_dashboard, name='visitor_dashboard.html'),
    path('shopkeeper_dashboard', views.shopkeeper_dashboard, name='shopkeeper_dashboard.html'),
    path('dashboard', views.dashboard, name='dashboard.html'),
    path('admin_login', views.admin_login, name='admin_login.html'),
    path('visitor_register', views.visitor_register, name='visitor_register.html'),
    path('log_in', views.log_in, name='log_in'),
    path('log_out/', views.log_out, name='log_out.html'), 
    path("shop/<int:shop_id>/", views.shop_products, name="shop_products"),
    path('camera/', views.open_camera, name='open_camera'),
]