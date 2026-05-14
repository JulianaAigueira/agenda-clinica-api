from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, ProcedureViewSet, AppointmentViewSet, index, agendar, meus_agendamentos, cadastro,cancelar_agendamento, painel_recepcao

# O Router cria automaticamente os links para os nossos ViewSets
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'procedures', ProcedureViewSet)
router.register(r'appointments', AppointmentViewSet, basename='appointments')

urlpatterns = [
    path('site/', index, name='index'),

    # 2. ADICIONE ESTA NOVA LINHA:
    path('site/agendar/<int:procedure_id>/', agendar, name='agendar'),

    path('site/meus-agendamentos/', meus_agendamentos, name='meus_agendamentos'),

    path('site/cadastro/', cadastro, name='cadastro'),

    path('site/cancelar/<int:appointment_id>/', cancelar_agendamento, name='cancelar_agendamento'),

    path('site/painel/', painel_recepcao, name='painel_recepcao'),

    path('', include(router.urls)),


]