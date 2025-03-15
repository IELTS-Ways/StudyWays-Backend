from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from subscription.serializers import SubscriptionSerializer, WithdrawRequestSerializer
from rest_framework import status
from subscription.models import Subscription, DefaultPrice
from accounts.models import InstituteProfile, StudentProfile, User, StudentWallet, InstituteWallet
from django.shortcuts import redirect
import decimal
from datetime import timedelta
from decimal import Decimal
import json
import requests
from django.conf import settings
from django.db import transaction
from config.responses import bad_request, SuccessResponse, UnsuccessfulResponse
from django.http import HttpResponse,JsonResponse


class CheckWallet(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, *args, **kwargs):
        try:
            price = self.request.data["price"]
            student = StudentProfile.objects.get(user=self.request.user)
            wallet = StudentWallet.objects.get(user=student)
            if wallet.balance < price:
                return Response("The price is more than your wallet balance.", status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response("You can pay with your wallet, the price is proportional to your wallet balance.", status=status.HTTP_200_OK)
        except Exception as e:
            return Response("Error - {}".format(e), status=status.HTTP_400_BAD_REQUEST)



class CheckWalletAndPay(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SubscriptionSerializer

    def post(self, *args, **kwargs):
        try:
            price = self.request.data["price"]
            day_period = self.request.data["day_period"]
            user = self.request.user
            data = self.request.data

            student = StudentProfile.objects.get(user=user)
            wallet = StudentWallet.objects.get(user=student)
            if wallet.balance < data["price"]:
                return Response("The price is more than your wallet balance.", status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                data["user"] = student.id
                data["type"] = "Audio-Video-Scripter"
                data["description"] = "Payment by wallet."
                data["paid"] = True
                serializer = self.serializer_class(data=data, partial=True)
                if serializer.is_valid():
                    serializer.save()

                    data["type"] = "Memory-Mirror"
                    serializer = self.serializer_class(data=data, partial=True)
                    if serializer.is_valid():
                        serializer.save()

                        wallet.balance -= price
                        wallet.save()

                        return Response(
                            f" {day_period} day Audio-Video-Scripter and Memory-Mirror actived for you, and {price} was deducted from your wallet. ",
                            status=status.HTTP_200_OK)

                    return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
                return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)


        except Exception as e:
            return Response("Error - {}".format(e), status=status.HTTP_400_BAD_REQUEST)





class WalletAndBOGOPay(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SubscriptionSerializer

    def post(self, *args, **kwargs):
        authority = self.request.query_params.get("Authority")
        status = self.request.query_params.get("Status")

        data = self.request.data
        student = StudentProfile.objects.get(user=self.request.user)

        if data["empty_wallet"]:
            wallet = StudentWallet.objects.get(user=student)
            wallet.balance = 0
            wallet.save()


        data["user"] = student.id
        serializer = self.serializer_class(data=data, partial=True)
        if serializer.is_valid():
            serializer.save()

            if User.objects.filter(id=self.request.user.invite_code).exists():
                inviter = User.objects.get(id=self.request.user.invite_code)
                if inviter.user_type == "student":
                    # sales_percentage = 0.10
                    sales_percentage = decimal.Decimal('0.10')
                else:
                    # sales_percentage = 0.08
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
                inviter_price = float(apportionment) * float(sales_percentage)  # share with inviter
                studyways_price = float(apportionment) - inviter_price  # send to us
                institute_price = float(sub.price) - float(apportionment)  # send to institute
                sub.institute_price = institute_price

            else:
                sub.freelance = student.freelance
                sub.save()  # send to us
                studyways_price = 0
                ZP_MERCHANT_ID = default_price.ZP_MERCHANT_ID
                appor_percent = default_price.freelance_apportionment_percentage
                freelance_price = sub.price * appor_percent  # share with freelance
                apportionment = float(sub.price) - float(freelance_price)
                sub.freelance_price = freelance_price
                inviter_price = apportionment * float(sales_percentage)  # share with inviter

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
                "CallbackURL": "https://api.studyways.ir/subscription/BOGO-verify/" + str(sub.id) + "/",
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
                        # return {'status': False, 'code': str(response['Status'])}
                return response

            except requests.exceptions.Timeout:
                return {'status': False, 'code': 'timeout'}
            except requests.exceptions.ConnectionError:
                return {'status': False, 'code': 'connection error'}

        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)






class WalletAndBOGOAutoPay(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SubscriptionSerializer

    def post(self, *args, **kwargs):
        authority = self.request.query_params.get("Authority")
        status = self.request.query_params.get("Status")

        data = self.request.data
        student = StudentProfile.objects.get(user=self.request.user)

        if data["empty_wallet"]:
            wallet = StudentWallet.objects.get(user=student)
            data["price"] -= wallet.balance
            wallet.balance = 0
            wallet.save()


        data["user"] = student.id
        serializer = self.serializer_class(data=data, partial=True)
        if serializer.is_valid():
            serializer.save()

            if User.objects.filter(id=self.request.user.invite_code).exists():
                inviter = User.objects.get(id=self.request.user.invite_code)
                if inviter.user_type == "student":
                    # sales_percentage = 0.10
                    sales_percentage = decimal.Decimal('0.10')
                else:
                    # sales_percentage = 0.08
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
                inviter_price = float(apportionment) * float(sales_percentage)  # share with inviter
                studyways_price = float(apportionment) - inviter_price  # send to us
                institute_price = float(sub.price) - float(apportionment)  # send to institute
                sub.institute_price = institute_price

            else:
                sub.freelance = student.freelance
                sub.save()  # send to us
                studyways_price = 0
                ZP_MERCHANT_ID = default_price.ZP_MERCHANT_ID
                appor_percent = default_price.freelance_apportionment_percentage
                freelance_price = sub.price * appor_percent  # share with freelance
                apportionment = float(sub.price) - float(freelance_price)
                sub.freelance_price = freelance_price
                inviter_price = apportionment * float(sales_percentage)  # share with inviter

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
                "CallbackURL": "https://api.studyways.ir/subscription/BOGO-verify/" + str(sub.id) + "/",
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
                        # return {'status': False, 'code': str(response['Status'])}
                return response

            except requests.exceptions.Timeout:
                return {'status': False, 'code': 'timeout'}
            except requests.exceptions.ConnectionError:
                return {'status': False, 'code': 'connection error'}

        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

