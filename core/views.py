from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages # <--- OLHA O NOSSO IMPORT AQUI!
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.contrib.auth.models import User
from .models import Procedure, Appointment
from .serializers import UserSerializer, ProcedureSerializer, AppointmentSerializer

# --- PÁGINA INICIAL ---
def index(request):
    procedures = Procedure.objects.all()
    return render(request, 'index.html', {'procedures': procedures})

# --- PÁGINA DE AGENDAMENTO (Agora só temos uma, e com a mensagem!) ---
@login_required(login_url='/admin/login/')
def agendar(request, procedure_id):
    procedure = get_object_or_404(Procedure, id=procedure_id)

    if request.method == 'POST':
        data_hora_escolhida = request.POST.get('data_hora')
        specialist = User.objects.filter(is_staff=True).first()

        # Salvamos o agendamento
        Appointment.objects.create(
            client=request.user,
            specialist=specialist,
            procedure=procedure,
            date_time=data_hora_escolhida
        )

        # 👇 ESTA É A LINHA QUE CRIA O BANNER VERDE 👇
        messages.success(request, f'Agendamento para {procedure.name} realizado com sucesso!')

        return redirect('index')

    return render(request, 'agendar.html', {'procedure': procedure})


# --- VIEWSETS DA API ---
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ProcedureViewSet(viewsets.ModelViewSet):
    queryset = Procedure.objects.all()
    serializer_class = ProcedureSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class AppointmentViewSet(viewsets.ModelViewSet):
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Appointment.objects.all()
        return Appointment.objects.filter(client=user)