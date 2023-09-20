from django.urls import path, include
from rest_framework.routers import DefaultRouter
from app.views import PizzaViewSet, OrderViewSet

router = DefaultRouter()
app_name = "app"
router.register(r'pizzas', PizzaViewSet)
router.register(r'orders', OrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('orders/', OrderViewSet.as_view({'get': 'list'}), name='order-list'),
    path('create_order/', OrderViewSet.create_order_view, name='create-order'),
    path('get_order_status/<int:order_id>/', OrderViewSet.get_order_status, name='get-order-status'),
]
