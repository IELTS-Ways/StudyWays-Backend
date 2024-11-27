from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.views.permissions import IsInstitute, IsFreelance, IsStudent
from rest_framework.permissions import IsAuthenticated
from accounts.models import MarketerWallet, FreelanceWallet
from accounts.models import InstituteProfile, StudentProfile, User, StudentWallet, InstituteWallet
from subscription.serializers import SubscriptionSerializer, WithdrawRequestSerializer
from subscription.models import Subscription, DefaultPrice
import json
import requests
from django.conf import settings
from django.db import transaction
from config.responses import bad_request, SuccessResponse, UnsuccessfulResponse
from django.http import HttpResponse,JsonResponse
from datetime import datetime
from django.shortcuts import redirect
import decimal



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



class WithdrawRequest(APIView):
    serializer_class = WithdrawRequestSerializer
    permission_classes = [IsAuthenticated]
    def post(self, *args, **kwargs):
        data = self.request.data.copy()
        user = self.request.user
        data["user"] = user.id
        price = self.request.data.get('price') 

        if user.user_type == 'marketer':
            wallet = MarketerWallet.objects.get(user__user=user)
        elif user.user_type == 'student':
            wallet = StudentWallet.objects.get(user__user=user)
        elif user.user_type == 'freelance':
            wallet = FreelanceWallet.objects.get(user__user=user)
        elif user.user_type == 'institute':
            wallet = InstituteWallet.objects.get(user__user=user)
        else:
            return Response({"error": "Invalid user type."}, status=status.HTTP_400_BAD_REQUEST)

        if wallet.balance < price:
            return Response(
                {"error": "Insufficient wallet balance.", "current_balance": wallet.balance},
                status=status.HTTP_400_BAD_REQUEST,
            )
            
        serializer = self.serializer_class(data=data)
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

            if User.objects.filter(id=self.request.user.invite_code).exists():
                inviter = User.objects.get(id=self.request.user.invite_code)
                if inviter.user_type == "student":
                    #sales_percentage = 0.10
                    sales_percentage = decimal.Decimal('0.10')
                else:
                    #sales_percentage = 0.08
                    sales_percentage = decimal.Decimal('0.08')
            else:
                sales_percentage = decimal.Decimal('0.0')


            sub = Subscription.objects.get(id=serializer.data['id'])
            default_price = DefaultPrice.objects.all().last()

            if student.parent_type() == "Institute":
                sub.institute = student.institute
                sub.save()
                ZP_MERCHANT_ID = student.institute.ZP_MERCHANT_ID
                appor_percent = default_price.apportionment_percentage
                apportionment = sub.price * appor_percent
                inviter_price = float(apportionment) * float(sales_percentage)   #share with inviter
                studyways_price = float(apportionment) - inviter_price           #send to us
                institute_price = float(sub.price) - float(apportionment)        #send to institute
                sub.institute_price = institute_price

            else:
                sub.freelance = student.freelance
                sub.save()                                                       #send to us
                studyways_price = 0
                ZP_MERCHANT_ID = default_price.ZP_MERCHANT_ID
                appor_percent = default_price.freelance_apportionment_percentage
                freelance_price = sub.price * appor_percent                      #share with freelance
                apportionment = float(sub.price) - float(freelance_price)
                sub.freelance_price = freelance_price
                inviter_price = apportionment * float(sales_percentage)          #share with inviter

            sub.inviter_sales_percentage = sales_percentage
            sub.inviter_price = inviter_price
            sub.apportionment_percentage = appor_percent
            sub.save()

            data = {
                "MerchantID": ZP_MERCHANT_ID,
                "Amount": int(sub.price),
                "Description": "خریداری اشتراک آنلاین استادی ویز",
                "Authority": authority,
                "Phone": student.user.phone_number,
                "CallbackURL": settings.ZARIN_CALL_BACK + str(sub.id) + "/",
                "OrderID": sub.id,
                "wages": [{
                    "iban": default_price.shaba_number,
                    "amount": int(studyways_price),
                    "description": "تسهیم سود فروش از سرویس"
                }],
            }
            data = json.dumps(data)

            headers = {'content-type': 'application/json', 'content-length': str(len(data))}

            try:
                response = requests.post(settings.ZP_API_REQUEST, data=data, headers=headers, timeout=10)
                response.raise_for_status()

                if response.status_code == 200:
                    response = response.json()
                    print('---------------')
                    print(response)
                    if response['Status'] == 100:
                        sub.authority = response['Authority']
                        sub.save()
                        sub_serializer = SubscriptionSerializer(sub)
                        data = {'status': True, 'url': settings.ZP_API_STARTPAY + str(response['Authority']),
                                'order': sub.id, 'authority': response['Authority']}
                        return SuccessResponse(sub_serializer.data, data)
                    else:
                        return Response(response['errors'], status=400)
                        #return {'status': False, 'code': str(response['Status'])}
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
        id = self.kwargs.get("id")
        #student = StudentProfile.objects.get(user=self.request.user)

        if not authority or status != "OK":
            return redirect('https://app.studyways.ir/dashboard/student/callback?success=notok')
            #return HttpResponse("payment faild...", content_type='text/plain')

        try:
            sub = Subscription.objects.get(id=id)
        except Subscription.DoesNotExist:
            return bad_request("Subscription does not exist...")

        if sub.user.parent_type() == "Institute":
            ZP_MERCHANT_ID = sub.user.institute.ZP_MERCHANT_ID
        else:
            default_price = DefaultPrice.objects.all().last()
            ZP_MERCHANT_ID = default_price.ZP_MERCHANT_ID

        data = {
            "MerchantID": ZP_MERCHANT_ID,
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

                # update wallet
                if User.objects.filter(id=sub.user.user.invite_code).exists():
                    inviter = User.objects.get(id=sub.user.user.invite_code)

                    if inviter.user_type == 'marketer':
                        wallet, created = MarketerWallet.objects.get_or_create(user__user=inviter)
                    elif inviter.user_type == 'student':
                        wallet, created  = StudentWallet.objects.get_or_create(user__user=inviter)
                    elif inviter.user_type == 'freelance':
                        wallet, created  = FreelanceWallet.objects.get_or_create(user__user=inviter)
                    elif inviter.user_type == 'institute':
                        wallet, created  = InstituteWallet.objects.get_or_create(user__user=inviter)
                    wallet.balance += sub.inviter_price
                    wallet.save()

                return redirect(f'https://app.studyways.ir/dashboard/student/callback?success=ok&payment_id={response["RefID"]}')
                #return HttpResponse("payment done, RefID={}".format(response['RefID']), content_type='text/plain')
            else:
                return SuccessResponse(data={'status': False, 'details': 'Subscription already paid' })
        return SuccessResponse(data=response.content)




class Membership(APIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsStudent]
    def get(self, *args, **kwargs):
        try:
            student = StudentProfile.objects.get(user=self.request.user)
            subs = Subscription.objects.filter(user=student)

            for sub in subs:
                if sub.paid:
                    if sub.expired():
                        sub.status = "Expired"
                    else:
                        sub.status = "Active"
                else:
                    sub.status = "Canceled"
                sub.save()

            active_subs = Subscription.objects.filter(user=student,status="Active")

            audio_video_scripter = active_subs.filter(type="Audio-Video-Scripter").last()
            if audio_video_scripter:
                audio_video_scripter_remaining_days = audio_video_scripter.remaining_days()
            else:
                audio_video_scripter_remaining_days = 0

            memory_mirror = active_subs.filter(type="Memory-Mirror").last()
            if memory_mirror:
                memory_mirror_remaining_days = memory_mirror.remaining_days()
            else:
                memory_mirror_remaining_days = 0

            final_data = {"Audio-Video-Scripter":audio_video_scripter_remaining_days, "Memory-Mirror":memory_mirror_remaining_days}
            return Response(final_data, status=status.HTTP_200_OK)
        except:
            return Response("Subscription not found or something went wrong, try again", status=status.HTTP_400_BAD_REQUEST)
