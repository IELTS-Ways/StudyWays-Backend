from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from subscription.serializers import SubscriptionSerializer, WithdrawRequestSerializer
from rest_framework import status
from accounts.models import StudentWallet, StudentProfile
from subscription.models import Subscription, DefaultPrice


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
