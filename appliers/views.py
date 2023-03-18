from rest_framework import viewsets, exceptions, status
from rest_framework.response import Response
from rest_framework.views    import APIView
from .serializers import ApplierSerializer
from .models import Applier


class ApplierView(APIView):
    def get(self, request):
        applier = Applier.objects.all()
        serializer = ApplierSerializer(applier, many=True)
        return Response(status=status.HTTP_200_OK,data=serializer.data)
        
    def post(self, request):        
        serializer = ApplierSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED,data=serializer.data)
        
