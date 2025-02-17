from .views import first_view, markets_single_view, product_view, seller_view, seller_single_view
from django.urls import path


urlpatterns = [
    path('market/', first_view),
    path('market/<int:pk>/', markets_single_view, name='market-detail'),
    path('sellers/', seller_view),
    path('sellers/<int:pk>', seller_single_view, name='seller_single'),
    path('products/', product_view),
    # path('product/<int:pk>', product_delete_view),
]
