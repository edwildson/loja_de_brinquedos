from rest_framework.routers import DefaultRouter
from interface_adapters.views.cliente_view import ClienteViewSet
from interface_adapters.views.venda_view import VendaViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path

router = DefaultRouter()
router.register(r'clientes', ClienteViewSet, basename='cliente')
router.register(r'vendas', VendaViewSet, basename='venda')

# Adicionar rotas de estatísticas explicitamente
urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Rotas de estatísticas
    path('vendas/estatisticas/vendas-por-dia/', VendaViewSet.as_view({'get': 'vendas_por_dia'}), name='estatisticas-vendas-por-dia'),
    path('vendas/estatisticas/clientes-destaque/', VendaViewSet.as_view({'get': 'clientes_destaque'}), name='estatisticas-clientes-destaque'),
] + router.urls
