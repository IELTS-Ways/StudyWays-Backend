from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from .models import Service, ReportSharing
from accounts.models import StudentProfile
from accounts.views.permissions import IsStudent
from django.urls import reverse
import requests




class ReportShareLink(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        #self.permission_classes = [IsStudent]
        #self.check_permissions(request)
          
        report_id = request.data.get('report_id')
        access_type = request.data.get('access_type')

        report = get_object_or_404(Service, id=report_id)

        try:
            student_profile = request.user.studentprofile
        except StudentProfile.DoesNotExist:
            student_profile = StudentProfile.objects.get(id=203)
           # return Response({"error": "Student profile not found for the current user."}, status=400)


        report_sharing = ReportSharing(
            user=student_profile,
            report=report,
            access_type=access_type,
        )
        report_sharing.generate_dynamic_link()
        report_sharing.save()

        return Response({
            "message": "Share link created successfully.",
            "link": report_sharing.link,
            "access_type": report_sharing.access_type,
        }, status=201)
        
     
        
    def get(self, request, link, *args, **kwargs):
        report_sharing = get_object_or_404(ReportSharing, link=link)

        if report_sharing.access_type == 'allow_any':
            pass
        elif report_sharing.access_type == 'is_authenticated':
            if not request.user.is_authenticated:
                return Response({"error": "Authentication required."}, status=403)
        elif report_sharing.access_type == 'just_parent':
            parent = request.user
            shared_student = report_sharing.user

            if report_sharing.user.user == request.user:
                pass
            elif shared_student.institute:
                if parent.id != shared_student.institute.user.id:
                    return Response({"error": "You are not authorized to view this report."}, status=403)
            elif shared_student.freelance:
                if parent.id != shared_student.freelance.user.id:
                    return Response({"error": "You are not authorized to view this report."}, status=403)
            else:
                return Response({"error": "No valid parent relationship found."}, status=403)

        report_id = report_sharing.report.id
        target_url = request.build_absolute_uri(reverse('service-correction-v3', kwargs={'id': report_id}))
        response = requests.get(target_url)

        return Response(response.json(), status=response.status_code)



class ReportShareHistory(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        
        student_profile = request.user

        report_shares = ReportSharing.objects.filter(user__user=student_profile)
        
        # filtering
        service = request.query_params.get("service")
        report_id = request.query_params.get("report_id")
        access_type = request.query_params.get("access_type")

        if service:
            report_shares = report_shares.filter(report__type=service)
        if report_id:
            report_shares = report_shares.filter(report__id=report_id)
        if access_type:
            report_shares = report_shares.filter(access_type=access_type)
        
        # ordering
        ordering = request.query_params.get("ordering", "-created_at")
        if ordering in ["created_at", "-created_at"]:
            report_shares = report_shares.order_by(ordering)

        data = [
            {
                "link": report.link,
                "report_id": report.report.id,
                "service" : report.report.type,
                "access_type": report.access_type,
                "created_at": report.created_at, 
            }
            for report in report_shares
        ]

        return Response({"links": data}, status=200)
