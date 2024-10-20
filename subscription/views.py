from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.views.permissions import IsInstitute, IsFreelance, IsStudent
from accounts.models import InstituteProfile, StudentProfile
from subscription.serializers import SubscriptionSerializer
from subscription.models import Subscription
import json
import requests
from django.conf import settings
from django.db import transaction
from config.responses import bad_request, SuccessResponse
from django.http import HttpResponse


class StudentSubs(APIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsStudent]
    def get(self, *args, **kwargs):
        try:
            student = StudentProfile.objects.get(user=self.request.user)
            sub = Subscription.objects.filter(user=student)
            serializer = self.serializer_class(sub, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response("Subscription not found or something went wrong, try again", status=status.HTTP_400_BAD_REQUEST)




class AddSub(APIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsStudent]
    def post(self, *args, **kwargs):
        data = self.request.data
        student = StudentProfile.objects.get(user=self.request.user)
        data["user"] = student.id
        serializer = self.serializer_class(data=data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)





class AddSubPay(APIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsStudent]

    def post(self, *args, **kwargs):
        authority = self.request.query_params.get("Authority")
        status = self.request.query_params.get("Status")

        data = self.request.data
        student = StudentProfile.objects.get(user=self.request.user)
        data["user"] = student.id
        serializer = self.serializer_class(data=data, partial=True)
        if serializer.is_valid():
            serializer.save()

            sub = Subscription.objects.get(id=serializer.data['id'])
            try:
                price = student.institute.memory_mirror_price
            except:
                price = 230000
            sub.price = price
            sub.save()

            data = {
                "MerchantID": student.institute.ZP_MERCHANT_ID,
                "Amount": sub.price,
                "Description": "خریداری اشتراک آنلاین استادی ویز",
                "Authority": authority,
                "CallbackURL": settings.ZARIN_CALL_BACK + str(sub.id) + "/",
                "OrderID": sub.id,
            }
            data = json.dumps(data)
            headers = {'content-type': 'application/json', 'content-length': str(len(data))}

            try:
                response = requests.post(settings.ZP_API_REQUEST, data=data, headers=headers, timeout=10)

                if response.status_code == 200:
                    response = response.json()
                    if response['Status'] == 100:
                        sub.authority = response['Authority']
                        sub.save()
                        sub_serializer = SubscriptionSerializer(sub)
                        data = {'status': True, 'url': settings.ZP_API_STARTPAY + str(response['Authority']),
                                'order': sub.id, 'authority': response['Authority']}
                        return SuccessResponse(sub_serializer.data, data)
                    else:
                        return {'status': False, 'code': str(response['Status'])}
                return response

            except requests.exceptions.Timeout:
                return {'status': False, 'code': 'timeout'}
            except requests.exceptions.ConnectionError:
                return {'status': False, 'code': 'connection error'}


        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)









class SubPayVerify(APIView):
    @transaction.atomic
    def get(self, *args, **kwargs):
        status = self.request.query_params.get("Status")
        authority = self.request.query_params.get("Authority")
        id = kwargs.get("id")
        student = StudentProfile.objects.get(user=self.request.user)

        if not authority or status != "OK":
            #return redirect('https://ioc.ieltsways.com/orders')
            return HttpResponse("payment faild...", content_type='text/plain')

        try:
            sub = Subscription.objects.get(id=id)
        except Subscription.DoesNotExist:
            return bad_request("Subscription does not exist...")

        data = {
            "MerchantID": student.institute.ZP_MERCHANT_ID,
            "Amount": sub.price,
            "Authority": authority,
        }
        data = json.dumps(data)
        headers = {'content-type': 'application/json', 'content-length': str(len(data))}
        response = requests.post(settings.ZP_API_VERIFY, data=data, headers=headers)

        if response.status_code == 200:
            response = response.json()
            if response['Status'] == 100:
                sub.paid = True
                sub.authority = authority
                sub.ref_id = response['RefID']
                sub.save()
                #return redirect('https://ioc.ieltsways.com/orders?RefID={}'.format(response['RefID']))
                return HttpResponse("payment done, RefID={}".format(response['RefID']), content_type='text/plain')
            else:
                return SuccessResponse(data={'status': False, 'details': 'Subscription already paid' })
        return SuccessResponse(data=response.content)


