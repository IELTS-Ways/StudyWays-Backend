from django.shortcuts import render, redirect
from django.conf import settings
from django.views.generic.base import View
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from accounts.models import User,StudentProfile
from config import responses
from rest_framework import status
import requests
from accounts.functions import get_user_data, login
from config.settings import ACCESS_TTL, SOCIAL_AUTH_GOOGLE_OAUTH2_KEY, SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET
from accounts.serializers import UserSerializer
from accounts.utils import random_with_N_digits
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from urllib.parse import urlencode



def index(request):
    return render(request, 'index.html')




class GoogleAuthRedirect(View):
    permission_classes = [AllowAny]
    def get(self, request):
        redirect_url = f"https://accounts.google.com/o/oauth2/v2/auth?client_id={SOCIAL_AUTH_GOOGLE_OAUTH2_KEY}&response_type=code&scope=https://www.googleapis.com/auth/userinfo.profile%20https://www.googleapis.com/auth/userinfo.email&access_type=offline&redirect_uri=https://api.studyways.ir/google-redirect/"
        return redirect(redirect_url)




class GoogleRedirectURIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        # Extract the authorization code from the request URL
        code = self.request.GET.get('code')

        if code:
            # Prepare the request parameters to exchange the authorization code for an access token
            token_endpoint = 'https://oauth2.googleapis.com/token'
            token_params = {
                'code': code,
                'client_id': SOCIAL_AUTH_GOOGLE_OAUTH2_KEY,
                'client_secret': SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET,
                'redirect_uri': 'https://api.studyways.ir/google-redirect/',
                'grant_type': 'authorization_code',
            }

            # Make a POST request to exchange the authorization code for an access token
            response = requests.post(token_endpoint, data=token_params)

            if response.status_code == 200:
                access_token = response.json().get('access_token')

                if access_token:
                    # Make a request to fetch the user's profile information
                    profile_endpoint = 'https://www.googleapis.com/oauth2/v1/userinfo'
                    headers = {'Authorization': f'Bearer {access_token}'}
                    profile_response = requests.get(profile_endpoint, headers=headers)

                    if profile_response.status_code == 200:
                        data = {}
                        profile_data = profile_response.json()
                        if User.objects.filter(email=profile_data["email"]).exists():
                            user = User.objects.get(email=profile_data["email"])
                        else:
                            user = User.objects.create_user(first_name=profile_data["given_name"],
                                                            email=profile_data["email"],
                                                            username=profile_data["email"],
                                                            user_type="unknown",
                                                            phone_number="09{}".format(random_with_N_digits(9)))
                            if "family_name" in profile_data:
                                user.last_name = profile_data["family_name"]
                                user.save()
                            user.save()

                        access, refresh = login(user)


                        data = {
                            "refresh_token": refresh,
                            "access_token": access,
                            "user_id": user.id,
                            "user_user_type": user.user_type,
                            "user_first_name": user.first_name,
                            "user_last_name": user.last_name,
                            "user_email": user.email,
                            "is_profile_fill": user.is_profile_fill()
                        }
                        '''   
                        response = Response(
                            {
                                "success": True,
                                "data": data,
                            },
                            status=status.HTTP_200_OK,
                        )
                        response.set_cookie(
                            "HTTP_ACCESS",
                            f"Bearer {access}",
                            max_age=ACCESS_TTL * 24 * 3600,
                            secure=True,
                            httponly=True,
                            samesite="None",)
                        #return response
                        '''

                        query_string = urlencode(data)
                        request.session['data'] = data
                        redirect_url = "https://app.studyways.ir/check-user?" + query_string
                        return redirect(redirect_url)

