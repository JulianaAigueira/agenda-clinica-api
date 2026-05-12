from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, ProcedureViewSet, AppointmentViewSet, index, agendar

# O Router cria automaticamente os links para os nossos ViewSets
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'procedures', ProcedureViewSet)
router.register(r'appointments', AppointmentViewSet, basename='appointments')

urlpatterns = [
    path('site/', index, name='index'),

    # 2. ADICIONE ESTA NOVA LINHA:
    path('site/agendar/<int:procedure_id>/', agendar, name='agendar'),

    path('', include(router.urls)),
]