from rest_framework.views    import APIView
from rest_framework.response import Response
from rest_framework import exceptions, decorators, permissions, status
from . import serializers 
from .models import Weekday


class ProductsView(APIView):
    def get(self, request):
        weekday = Weekday.objects.last()
        serializer = serializers.WeekdaySerializer(weekday)
        return Response(status=status.HTTP_200_OK, data=serializer.data)
