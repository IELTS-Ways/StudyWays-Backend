from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Service, ReportSharing
from accounts.models import StudentProfile




class CreateReportShareLink(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        report_id = request.data.get('report_id')
        access_type = request.data.get('access_type')

        report = get_object_or_404(Service, id=report_id)

        try:
            student_profile = request.user.studentprofile
        except StudentProfile.DoesNotExist:
            return Response({"error": "Student profile not found for the current user."}, status=400)

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


class AccessReportLink(APIView):
    def get(self, request, link, *args, **kwargs):
        report_sharing = get_object_or_404(ReportSharing, link=link)

        if report_sharing.access_type == 'allow_any':
            pass
        elif report_sharing.access_type == 'is_authenticated':
            if not request.user.is_authenticated:
                return Response({"error": "Authentication required."}, status=403)
        elif report_sharing.access_type == 'just_parent':
            student_profile = request.user.studentprofile
            shared_student = report_sharing.user

            if student_profile.institute and shared_student.institute:
                if student_profile.institute != shared_student.institute:
                    return Response({"error": "You are not authorized to view this report."}, status=403)
            elif student_profile.freelance and shared_student.freelance:
                if student_profile.freelance != shared_student.freelance:
                    return Response({"error": "You are not authorized to view this report."}, status=403)
            else:
                return Response({"error": "No valid parent relationship found."}, status=403)

        return Response({
            "message": "Access granted.",
            "report": {
                "report_id": report_sharing.report.id,
                "report": report_sharing.report.full_result,
            }
        })

