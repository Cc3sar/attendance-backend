from datetime import datetime

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
