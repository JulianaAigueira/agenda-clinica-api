from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.contrib.auth.models import User
from .models import Procedure, Appointment
from .serializers import UserSerializer, ProcedureSerializer, AppointmentSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ProcedureViewSet(viewsets.ModelViewSet):
    queryset = Procedure.objects.all()
    serializer_class = ProcedureSerializer
    # Qualquer um pode ver (Ler), mas só logados podem criar/editar
    permission_classes = [IsAuthenticatedOrReadOnly]

class AppointmentViewSet(viewsets.ModelViewSet):
    # Retirámos a linha 'queryset = Appointment.objects.all()'
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    # NOVA FUNÇÃO: O filtro inteligente de autorização
    def get_queryset(self):
        # A variável 'user' descobre quem está logado fazendo a requisição
        user = self.request.user

        # Regra 1: Se o usuário for um administrador da clínica (staff), ele pode ver tudo
        if user.is_staff:
            return Appointment.objects.all()

        # Regra 2: Se for um cliente normal, filtramos a tabela para mostrar apenas os dele
        return Appointment.objects.filter(client=user)