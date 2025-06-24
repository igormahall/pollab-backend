from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EnqueteViewSet

# Roteador que gera automaticamente as rotas do ViewSet
router = DefaultRouter()
router.register(r'enquetes', EnqueteViewSet, basename='enquete')

# As urlpatterns do app apontam para as rotas geradas pelo roteador
urlpatterns = [
    path('', include(router.urls)),
]