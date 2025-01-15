from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.views.permissions import IsInstitute, IsFreelance, IsStudent
from rest_framework.permissions import IsAuthenticated
import requests
from .models import DiscountCode
from .serializers import DiscountCodeSerializer
from rest_framework import status


class Discount(APIView):
    serializer_class = DiscountCodeSerializer
    permission_classes = [IsAuthenticated]
    def post(self, *args, **kwargs):
        serializer = DiscountCodeSerializer(data=self.request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, *args, **kwargs):
        codes = DiscountCode.objects.all()
        serializer = DiscountCodeSerializer(codes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
   
   
    
class DiscountItem(APIView):
    serializer_class = DiscountCodeSerializer
    permission_classes = [IsAuthenticated]
    def get(self, *args, **kwargs):
        try:
            code = DiscountCode.objects.get(code=self.kwargs["code"])
            serializer = self.serializer_class(code)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response("discount code not found or something went wrong, try again", status=status.HTTP_400_BAD_REQUEST)

    def delete(self, *args, **kwargs):
        try:
            code = DiscountCode.objects.get(code=self.kwargs["code"])
            code.delete()
            return Response("discount code deleted.", status=status.HTTP_200_OK)
        except:
            return Response("discount code not found or something went wrong, try again", status=status.HTTP_400_BAD_REQUEST)