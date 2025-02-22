from .views import MarketDetailView, MarketsView, MarketsViewSet, ProductDetailView, ProductView, ProductsViewset, SellerDetailView, SellerOfMarketsView, SellersView, SellersViewSet
from django.urls import path, include
from rest_framework import routers


router = routers.SimpleRouter()
router.register(r'products', ProductsViewset)
router.register(r'markets', MarketsViewSet)
router.register(r'sellers', SellersViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('market/', MarketsView.as_view()),
    # path('market/<int:pk>/', MarketDetailView.as_view(), name='market-detail'),
    path('market/<int:pk>/seller/', SellerOfMarketsView.as_view(), name='market-sellers'),
    # path('sellers/', SellersView.as_view()),
    # path('sellers/<int:pk>/', SellerDetailView.as_view(), name='seller-detail'),
    # path('products/', ProductView.as_view()),
    # path('products/<int:pk>/', ProductDetailView.as_view(), name='product_single')
    # path('product/<int:pk>', product_delete_view),
]
