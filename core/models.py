from django.db import models
from django.contrib.auth.models import User


# Modelo que representa os serviços/procedimentos oferecidos pela clínica
class Procedure(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    estimated_duration = models.DurationField(help_text="Format: HH:MM:SS")

    def __str__(self):
        return self.name


# Modelo que gerencia os agendamentos do sistema
class Appointment(models.Model):
    # Lista com as opções de status (Valor no Banco de Dados, Valor exibido no sistema)
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('COMPLETED', 'Completed'),
        ('CANCELED', 'Canceled'),
    ]

    # Cliente que fez o agendamento (relacionado ao modelo User do Django)
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='client_appointments')

    # Profissional que fará o atendimento
    specialist = models.ForeignKey(User, on_delete=models.CASCADE, related_name='specialist_appointments')

    # Procedimento escolhido (PROTECT impede que um procedimento seja apagado se houver agendamentos atrelados a ele)
    procedure = models.ForeignKey(Procedure, on_delete=models.PROTECT)

    # Data e hora exatas do agendamento
    date_time = models.DateTimeField()

    # Status atual do agendamento, começando sempre como 'PENDING'
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='PENDING')

    def __str__(self):
        # Exibe uma string legível no painel de administração
        return f"{self.client.username} - {self.procedure.name} ({self.date_time})"