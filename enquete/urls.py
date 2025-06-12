from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EnqueteViewSet

# O roteador é instanciado aqui, no nível do app
router = DefaultRouter()
router.register(r'enquetes', EnqueteViewSet, basename='enquete')

# As urlpatterns do app apontam para as rotas geradas pelo roteador
urlpatterns = [
    path('', include(router.urls)),
]