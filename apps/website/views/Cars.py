
from rest_framework.views import APIView
from apps.website.models import CarRegistration
from rest_framework import status
from apps.website.Serilaizers.Rides_serializer import car_serializer
from django.http import JsonResponse

class CarsView(APIView):

    def get(self, request, *args, **kwargs):

        requests = CarRegistration.Car.objects.all()

        data_serialized = car_serializer(requests, many=True).data
        statusc =''
        if data_serialized:
            content = {"Cars": data_serialized }
            statusc=status.HTTP_200_OK
        else:
            content = {"Cars": "No Cars."}
            statusc=status.HTTP_204_NO_CONTENT

       

        return JsonResponse(content ,status=statusc)