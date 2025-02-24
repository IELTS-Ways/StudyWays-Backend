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
from django.shortcuts import redirect
from django.http import JsonResponse
from rest_framework.views import APIView



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
        code = request.GET.get('code')

        if not code:
            return Response({"error": "Authorization code not provided"}, status=status.HTTP_400_BAD_REQUEST)

        token_endpoint = 'https://oauth2.googleapis.com/token'
        token_params = {
            'code': code,
            'client_id': SOCIAL_AUTH_GOOGLE_OAUTH2_KEY,
            'client_secret': SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET,
            'redirect_uri': 'https://api.studyways.ir/google-redirect/',
            'grant_type': 'authorization_code',
        }

        response = requests.post(token_endpoint, data=token_params)

        if response.status_code != 200:
            return Response({"error": "Failed to exchange code for token"}, status=status.HTTP_400_BAD_REQUEST)

        access_token = response.json().get('access_token')
        if not access_token:
            return Response({"error": "No access token received"}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch user profile
        profile_endpoint = 'https://www.googleapis.com/oauth2/v1/userinfo'
        headers = {'Authorization': f'Bearer {access_token}'}
        profile_response = requests.get(profile_endpoint, headers=headers)

        if profile_response.status_code != 200:
            return Response({"error": "Failed to fetch user profile"}, status=status.HTTP_400_BAD_REQUEST)

        profile_data = profile_response.json()
        user, created = User.objects.get_or_create(email=profile_data["email"], defaults={
            "first_name": profile_data.get("given_name", ""),
            "username": profile_data["email"],
            "user_type": "unknown",
            "phone_number": "09{}".format(random_with_N_digits(9))
        })

        if "family_name" in profile_data:
            user.last_name = profile_data["family_name"]
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

        query_string = urlencode(data)
        request.session['data'] = data
        redirect_url = "https://app.studyways.ir/check-user?" + query_string

        return redirect(redirect_url)
