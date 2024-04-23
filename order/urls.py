from django.urls import path
from .import views
urlpatterns=[
    path('place-order/<int:id>/',views.cancel_order,name='placeorder'),
    path('orderslist/', views.orders_page, name='orderslist'),
    path('ordersummary/<int:id>/', views.order_summary, name='ordersummary'),
]
