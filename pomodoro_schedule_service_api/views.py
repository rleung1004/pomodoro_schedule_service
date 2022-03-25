from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ScheduleSerializer


class ScheduleApiView(APIView):

    def update(self, request, *args, **kwargs):
        '''
        Create/Update the Schedule with given schedule data
        '''
        data = {
            'userId': request.data.get('userId'),
            'scheduleObj': request.data.get('scheduleObj'),
        }
        serializer = ScheduleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)