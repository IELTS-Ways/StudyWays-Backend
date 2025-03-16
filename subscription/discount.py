from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.views.permissions import IsInstitute, IsFreelance, IsStudent
from rest_framework.permissions import IsAuthenticated
import requests
from .models import DiscountCode
from .serializers import DiscountCodeSerializer
from rest_framework import status
from accounts.models import InstituteProfile, StudentProfile
from rest_framework import permissions

class Discount(APIView):
    serializer_class = DiscountCodeSerializer
    permission_classes = [IsInstitute]
    def post(self, *args, **kwargs):
        institute = InstituteProfile.objects.get(user=self.request.user)
        data=self.request.data.copy()
        data['institute'] = institute.id
        
        serializer = DiscountCodeSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, *args, **kwargs):
        institute = InstituteProfile.objects.get(user=self.request.user)
        codes = DiscountCode.objects.filter(institute=institute)
        serializer = DiscountCodeSerializer(codes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
   
   
    
class DiscountItem(APIView):
    serializer_class = DiscountCodeSerializer
    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsStudent()]
        elif self.request.method == 'DELETE':
            return [IsInstitute()]
        return super().get_permissions() or [permissions.AllowAny()]

    
    def get(self, *args, **kwargs):
        try:
            code_param = self.kwargs.get("code")
            code = DiscountCode.objects.get(code=code_param)
            serializer = self.serializer_class(code)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response("discount code not found or something went wrong, try again", status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, *args, **kwargs):
        try:
            institute = InstituteProfile.objects.get(user=self.request.user)
            if institute:
                code = DiscountCode.objects.get(code=self.kwargs["code"], institute=institute)
                code.delete()
                return Response("discount code deleted.", status=status.HTTP_200_OK)
        except:
            return Response("discount code not found or something went wrong, try again", status=status.HTTP_400_BAD_REQUEST)