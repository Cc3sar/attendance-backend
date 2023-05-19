from datetime import datetime, time, timedelta

from django.db.models import Count
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from api.models import Schedule, User
from api.serializers import ScheduleSaveSerializer


class ScheduleViewset(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSaveSerializer
    permission_classes = (AllowAny,)

    @action(methods=['post'], detail=False)
    def entry_date(self, request):
        dpi = request.data.get('dpi')
        entry_datetime = datetime.now()
        user = User.objects.get(dpi=dpi)
        data = {
            'user': user.id,
            'entry_datetime': entry_datetime
        }
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(methods=['post'], detail=False)
    def exit_date(self, request):
        dpi = request.data.get('dpi')
        exit_datetime = datetime.now()
        user = User.objects.get(dpi=dpi)
        # Buscar el ultimo registro de entrada de la persona con la fecha de entrada actual
        schedule = Schedule.objects.filter(user=user, entry_datetime__date=exit_datetime.date()).last()
        schedule.exit_datetime = exit_datetime
        schedule.save()
        serializer = self.get_serializer(schedule)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False)
    def get_report(self, request):
        # Obtener la fecha actual y establecer el rango del mes actual
        current_date = timezone.now().date()
        start_of_month = datetime(current_date.year, current_date.month, 1, tzinfo=timezone.utc)
        end_of_month = start_of_month.replace(day=28) + timezone.timedelta(days=4)

        # Obtener las llegadas tempranas y tardías del usuario en el mes actual
        early_arrivals = Schedule.objects.filter(
            entry_datetime__gte=start_of_month,
            entry_datetime__lt=end_of_month,
            entry_datetime__time__lte=time(8, 10)  # Filtrar llegadas antes o a las 8:10 am
        ).values('user__first_name').annotate(count=Count('id')).order_by('count')

        late_arrivals = Schedule.objects.filter(
            entry_datetime__gte=start_of_month,
            entry_datetime__lt=end_of_month,
            entry_datetime__time__gt=time(8, 10)  # Filtrar llegadas después de las 8:10 am
        ).values('user__first_name').annotate(count=Count('id')).order_by('-count')

        # Obtener los DPI de los empleados y los valores de las llegadas tempranas y tardías
        early_employees = [arrival['user__dpi'] for arrival in early_arrivals]
        early_counts = [arrival['count'] for arrival in early_arrivals]

        late_employees = [arrival['user__dpi'] for arrival in late_arrivals]
        late_counts = [arrival['count'] for arrival in late_arrivals]

        # Crear el objeto de respuesta con las listas de llegadas tempranas y tardías
        response = {
            "early": {
                "labels": early_employees,
                "datasets": [ {"data": early_counts} ]
            },
            "late": {
                "labels": late_employees,
                "datasets": [ {"data": late_counts} ]
            }
        }

        return Response(response, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False)
    def rellenar_datos(self, request):
        user_id = 2  # ID del usuario
        start_date = datetime(2023, 5, 16)  # Fecha de inicio
        end_date = datetime(2023, 5, 26)  # Fecha de fin
        entry_time = datetime.strptime("8:11 AM", "%I:%M %p").time()  # Hora de entrada

        current_date = start_date
        while current_date <= end_date:
            entry_datetime = datetime.combine(
                current_date.date(),  # Obtener solo la fecha
                entry_time  # Utilizar la hora de entrada
            )
            data = {
                'user': user_id,
                'entry_datetime': entry_datetime
            }
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            current_date += timedelta(days=1)

        return Response({"message": "Fechas de entrada registradas."}, status=status.HTTP_201_CREATED)       
    
    @action(methods=['get'], detail=False)
    def test_fechas(self, request):
        # obtener todos los registros de entrada
        schedules = Schedule.objects.all()
        for schedule in schedules:
            print(schedule.entry_datetime)
        return Response({"message": "Fechas de entrada registradas."}, status=status.HTTP_201_CREATED)