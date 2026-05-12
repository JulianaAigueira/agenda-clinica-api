from rest_framework import serializers
from django.utils import timezone  # <-- ADICIONADO (para lidar com datas)
from django.contrib.auth.models import User
from .models import Procedure, Appointment

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']

class ProcedureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Procedure
        fields = '__all__'

class AppointmentSerializer(serializers.ModelSerializer):
    client_name = serializers.ReadOnlyField(source='client.username')
    specialist_name = serializers.ReadOnlyField(source='specialist.username')
    procedure_name = serializers.ReadOnlyField(source='procedure.name')

    class Meta:
        model = Appointment
        fields = [
            'id',
            'client', 'client_name',
            'specialist', 'specialist_name',
            'procedure', 'procedure_name',
            'date_time', 'status'
        ]

    # <-- ESSA PARTE TODA ABAIXO É A NOVIDADE PROFISSIONAL -->
    def validate(self, data):
        specialist = data.get('specialist')
        date_time = data.get('date_time')
        procedure = data.get('procedure')

        # Validação 1: Bloqueia datas no passado
        if date_time < timezone.now():
            raise serializers.ValidationError({
                "date_time": "Não é possível realizar um agendamento em uma data ou hora no passado."
            })

        # Validação 2: Bloqueia conflito de horários (mesmo especialista no mesmo horário)
        new_end_time = date_time + procedure.estimated_duration
        existing_appointments = Appointment.objects.filter(
            specialist=specialist,
            status__in=['PENDING', 'CONFIRMED']
        )

        for appt in existing_appointments:
            existing_start = appt.date_time
            existing_end = appt.date_time + appt.procedure.estimated_duration

            # Se houver sobreposição, impede o salvamento
            if date_time < existing_end and new_end_time > existing_start:
                raise serializers.ValidationError({
                    "specialist": "Conflito: Este especialista já possui um atendimento neste horário."
                })

        return data