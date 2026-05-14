from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.contrib.auth.models import User
from .models import Procedure, Appointment
from .serializers import UserSerializer, ProcedureSerializer, AppointmentSerializer
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone


# --- PÁGINA INICIAL ---
def index(request):
    procedures = Procedure.objects.all()
    return render(request, 'index.html', {'procedures': procedures})

# --- PÁGINA DE AGENDAMENTO ---
@login_required(login_url='/admin/login/')
def agendar(request, procedure_id):
    procedure = get_object_or_404(Procedure, id=procedure_id)

    # 1. Buscamos TODOS os usuários que são marcados como equipe (staff)
    especialistas = User.objects.filter(is_staff=True)

    if request.method == 'POST':
        data_hora_escolhida = request.POST.get('data_hora')
        especialista_id = request.POST.get('specialist')  # 2. Pegamos o ID que o cliente escolheu no form

        # 3. Buscamos exatamente o médico que o cliente selecionou
        specialist = get_object_or_404(User, id=especialista_id, is_staff=True)

        try:
            Appointment.objects.create(
                client=request.user,
                specialist=specialist,
                procedure=procedure,
                date_time=data_hora_escolhida
            )
            messages.success(request, f'Agendamento para {procedure.name} realizado com sucesso!')
            return redirect('index')

        except Exception as e:
            messages.error(request, str(e))
            # Se der erro de validação (ex: data no passado), devolvemos a lista de médicos para a tela não quebrar
            return render(request, 'agendar.html', {'procedure': procedure, 'especialistas': especialistas})

    # 4. Enviamos a lista de especialistas para o template HTML
    return render(request, 'agendar.html', {'procedure': procedure, 'especialistas': especialistas})


def cadastro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Conta criada com sucesso! Agora pode fazer login.')
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'registration/cadastro.html', {'form': form})


@login_required(login_url='/admin/login/')
def meus_agendamentos(request):
    # Buscamos apenas os agendamentos onde o cliente é o usuário atual
    agendamentos = Appointment.objects.filter(client=request.user).order_by('-date_time')
    return render(request, 'meus_agendamentos.html', {'agendamentos': agendamentos})


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


@login_required(login_url='/admin/login/')
def cancelar_agendamento(request, appointment_id):
    # Busca o agendamento garantindo que pertence ao usuário logado
    agendamento = get_object_or_404(Appointment, id=appointment_id, client=request.user)

    # Por segurança, deleções devem ser feitas via método POST
    if request.method == 'POST':
        agendamento.delete()
        messages.success(request, 'Sua consulta foi cancelada com sucesso.')

    return redirect('meus_agendamentos')

@login_required(login_url='/login/')
def painel_recepcao(request):
    # Trava de Segurança: Se não for da equipe, é expulso de volta pra home
    if not request.user.is_staff:
        messages.error(request, 'Acesso negado. Apenas membros da equipe podem ver o painel.')
        return redirect('index')

    # Busca todos os agendamentos de HOJE em diante, ordenados pela data e hora
    agendamentos = Appointment.objects.filter(
        date_time__gte=timezone.now()
    ).order_by('date_time')

    return render(request, 'painel.html', {'agendamentos': agendamentos})