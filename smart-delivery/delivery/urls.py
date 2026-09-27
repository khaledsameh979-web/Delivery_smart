from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.index,name='home'),
   
  path('request/', views.add, name='request_shipment'),
  path('login/', views.login, name='login'),
  path('register/', views.register, name='register'),
  path('track/', views.track, name='track'),
  path('driver/', views.driver_home, name='driver_home'),
  path('dashboard/', views.customer_dashboard, name='customer_dashboard'),
  path("api/chat/", views.chat_api, name="chat_api"),
  
]