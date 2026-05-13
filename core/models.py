from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone


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

    def clean(self):
        # Garante que a data digitada tenha fuso horário para poder comparar sem erro
        if self.date_time and timezone.is_naive(self.date_time):
            self.date_time = timezone.make_aware(self.date_time)

        # 1. Verificar se a data é no passado
        if self.date_time and self.date_time < timezone.now():
            raise ValidationError("Você não pode agendar uma consulta em uma data que já passou.")


        # 2. Verificar se o médico já tem outro agendamento nesse exato horário
        # Buscamos se existe algum agendamento para o mesmo especialista e mesma hora
        conflito = Appointment.objects.filter(
            specialist=self.specialist,
            date_time=self.date_time
        ).exclude(id=self.id)  # Ignora o próprio agendamento caso seja uma edição

        if conflito.exists():
            raise ValidationError("Este especialista já possui um agendamento para este horário.")

    # Sobrescrevemos o método save para garantir que a trava seja chamada sempre
    def save(self, *args, **kwargs):
        self.full_clean()  # Isso força a execução do método clean acima
        super().save(*args, **kwargs)