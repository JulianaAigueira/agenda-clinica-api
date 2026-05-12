from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, ProcedureViewSet, AppointmentViewSet

# O Router cria automaticamente os links para os nossos ViewSets
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'procedures', ProcedureViewSet)
# Adicionamos o basename='appointments' na linha abaixo:
router.register(r'appointments', AppointmentViewSet, basename='appointments')

# Todas as rotas geradas pelo router serão incluídas aqui
urlpatterns = [
    path('', include(router.urls)),
]