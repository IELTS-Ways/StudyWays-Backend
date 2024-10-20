from rest_framework import viewsets, filters, status, pagination, mixins
from rest_framework.response import Response
from file.serializers import FileSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import GenericAPIView
from accounts.models import User
from file.models import File
from django.db.models import Q
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from service.models import Service
from accounts.models import InstituteProfile, StudentProfile
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 200


class Search(GenericAPIView):
    permission_classes = [AllowAny]
    pagination_class = CustomPagination
    serializer_class = FileSerializer
    queryset = File.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['book','unit','page','cd','track','CEFR','language','skill_type','book_type']
    ordering_fields = ['id','skill_type','book_type','book','unit','page','cd']
    filterset_fields = ['CEFR', 'id', 'language', 'skill_type', 'book_type','unit','cd','track','lyrics','test','section','passage','episode','unit_opener','article_title','unit_title']

    @swagger_auto_schema()
    def get(self, request, format=None):
        query = self.filter_queryset(File.objects.all().order_by('id'))
        page = self.paginate_queryset(query)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.serializer_class(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)




class Library1(GenericAPIView):
    permission_classes = [AllowAny]
    pagination_class = CustomPagination
    serializer_class = FileSerializer
    queryset = File.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['book','unit','page','cd','track','CEFR','language','skill_type','book_type']
    ordering_fields = ['id','skill_type','book_type','book','unit','page','cd']
    filterset_fields = ['CEFR', 'id', 'language', 'skill_type', 'book_type','unit','cd','track','lyrics','test','section','passage','episode','unit_opener','article_title','unit_title']

    def get(self, request, format=None):
        queryset = self.filter_queryset(File.objects.all().order_by('id'))
        book_types = set(queryset.values_list('book_type', flat=True))
        return Response(book_types, status=status.HTTP_200_OK)



class Library2(GenericAPIView):
    permission_classes = [AllowAny]
    pagination_class = CustomPagination
    serializer_class = FileSerializer
    queryset = File.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['book','unit','page','cd','track','CEFR','language','skill_type','book_type']
    ordering_fields = ['id','skill_type','book_type','book','unit','page','cd']
    filterset_fields = ['CEFR', 'id', 'language', 'skill_type', 'book_type','unit','cd','track','lyrics','test','section','passage','episode','unit_opener','article_title','unit_title']

    def get(self, request, format=None):
        queryset = self.filter_queryset(File.objects.all().order_by('id'))
        cds = set(queryset.values_list('cd', flat=True))
        units = set(queryset.values_list('unit', flat=True))
        sections = set(queryset.values_list('section', flat=True))
        passages = set(queryset.values_list('passage', flat=True))
        episodes = set(queryset.values_list('episode', flat=True))
        pages = set(queryset.values_list('page', flat=True))
        tracks = set(queryset.values_list('track', flat=True))
        resp = {"cds":cds,"units":units,"sections":sections,"passages":passages,"episodes":episodes,"pages":pages,"tracks":tracks}
        return Response(resp, status=status.HTTP_200_OK)





class MoreUsedFile(APIView):
    serializer_class = FileSerializer
    permission_classes = [IsAuthenticated]
    def get(self, *args, **kwargs):
        try:
            student = StudentProfile.objects.get(user=self.request.user)
            more_used_files = Service.objects.filter(user=student).values_list('file', flat=True).distinct()
            files = File.objects.filter(id__in=more_used_files)
            serializer = self.serializer_class(files, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except StudentProfile.DoesNotExist:
            return Response("Student profile not found", status=status.HTTP_404_NOT_FOUND)
        except Service.DoesNotExist:
            return Response("No services found for this student", status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(f"An error occurred: {str(e)}", status=status.HTTP_400_BAD_REQUEST)



class AddPhotoUrl(APIView):
    permission_classes = [AllowAny]
    def put(self, *args, **kwargs):
        global img_url
        try:
            files = File.objects.all()
            for item in files:
                if (item.language, item.book_type) == ("English", "Cambridge"):
                    if "Cambridge 10" in item.book:
                        img_url = "https://studyways02.s3.ir-thr-at1.arvanstorage.ir/IELTS%20Academic%20Covers%2FIELTS%20Academic%20Cover%2010%2FIELTS%20Academic%2010%20Cover.jpg"
                    elif "Cambridge 11" in item.book:
                        img_url = "https://studyways02.s3.ir-thr-at1.arvanstorage.ir/IELTS%20Academic%20Covers%2FIELTS%20Academic%20Cover%2011%2FIELTS%20Academic%2011%20Cover.jpg.png"
                    elif "Cambridge 12" in item.book:
                        img_url = "https://studyways02.s3.ir-thr-at1.arvanstorage.ir/IELTS%20Academic%20Covers%2FIELTS%20Academic%20Cover%2012%2FIELTS%20Academic%2012%20Cover%20%281%29.jpg"
                    elif "Cambridge 13" in item.book:
                        img_url = "https://studyways02.s3.ir-thr-at1.arvanstorage.ir/IELTS%20Academic%20Covers%2FIELTS%20Academic%20Cover%2013%2FIELTS%20Academic%2013%20Cover.jpg"
                    elif "Cambridge 14" in item.book:
                        img_url = "https://studyways02.s3.ir-thr-at1.arvanstorage.ir/IELTS%20Academic%20Covers%2FIELTS%20Academic%20Cover%2014%2FIELTS%20Academic%2014%20Cover%20%281%29.jpg"
                    elif "Cambridge 15" in item.book:
                        img_url = "https://studyways02.s3.ir-thr-at1.arvanstorage.ir/IELTS%20Academic%20Covers%2FIELTS%20Academic%20Cover%2015%2FIELTS%20Academic%2015%20Cover%20%281%29.jpg"
                    elif "Cambridge 16" in item.book:
                        img_url = "https://studyways02.s3.ir-thr-at1.arvanstorage.ir/IELTS%20Academic%20Covers%2FIELTS%20Academic%20Cover%2016%2FIELTS%20Academic%2016%20Cover%20%281%29.jpg"
                    elif "Cambridge 17" in item.book:
                        img_url = "https://studyways02.s3.ir-thr-at1.arvanstorage.ir/IELTS%20Academic%20Covers%2FIELTS%20Academic%20Cover%2017%2FIELTS%20Academic%2017%20Cover%20%281%29.jpg"
                    elif "Cambridge 18" in item.book:
                        img_url = "https://studyways02.s3.ir-thr-at1.arvanstorage.ir/IELTS%20Academic%20Covers%2FIELTS%20Academic%20Cover%2018%2FIELTS%20Academic%2018%20Cover.jpg"
                    elif "Cambridge 19" in item.book:
                        img_url = "https://studyways02.s3.ir-thr-at1.arvanstorage.ir/IELTS%20Academic%20Covers%2FIELTS%20Academic%20Cover%2019%2FIELTS%20Academic%2019%20Cover.jpg"
                elif (item.language, item.book_type) == ("English", "Tactics for Listening"):
                    if "Basic Tactics for Listening" in item.book:
                        img_url = "https://studyways02.s3.ir-thr-at1.arvanstorage.ir/CourseBook%20Covers%2FBasic%20Tactics.jpg"
                    elif "Developing Tactics for Listening" in item.book:
                        img_url = "https://studyways02.s3.ir-thr-at1.arvanstorage.ir/CourseBook%20Covers%2FDeveloping%20Tactics%20Cover.jpg"
                    elif "Expanding Tactics for Listening" in item.book:
                        img_url = "https://studyways02.s3.ir-thr-at1.arvanstorage.ir/CourseBook%20Covers%2FExpanding%20Tactics%20Cover.jpg"
                elif (item.language, item.book_type) == ("English", "Inside Reading"):
                    if "Inside Reading Intro" in item.book:
                        img_url = "https://studyways02.s3.ir-thr-at1.arvanstorage.ir/CourseBook%20Covers%2FInside%20Reading%2FInside%20Reading%20Intro%20Cover.jpg"
                    elif "Inside Reading 1" in item.book:
                        img_url = "https://studyways02.s3.ir-thr-at1.arvanstorage.ir/CourseBook%20Covers%2FInside%20Reading%2FInside%20Reading%201%20Cover.jpg"
                    elif "Inside Reading 2" in item.book:
                        img_url = "https://studyways02.s3.ir-thr-at1.arvanstorage.ir/CourseBook%20Covers%2FInside%20Reading%2FInside%20Reading%202%20Cover.jpg"
                    elif "Inside Reading 3" in item.book:
                        img_url = "https://studyways02.s3.ir-thr-at1.arvanstorage.ir/CourseBook%20Covers%2FInside%20Reading%2Finside%20reading%203%20Cover.png"
                    elif "Inside Reading 4" in item.book:
                        img_url = "https://studyways02.s3.ir-thr-at1.arvanstorage.ir/CourseBook%20Covers%2FInside%20Reading%2FInside%20Reading%204%20Cover.png"
                elif (item.language, item.book_type) == ("English", "Inside Writing"):
                    if "Inside Writing Intro" in item.book:
                        img_url = "https://studyways02.s3.ir-thr-at1.arvanstorage.ir/CourseBook%20Covers%2FInside%20Writing%2FInside%20Writing%20Intro%20Cover.png"
                    elif "Inside Writing 1" in item.book:
                        img_url = "https://studyways02.s3.ir-thr-at1.arvanstorage.ir/CourseBook%20Covers%2FInside%20Writing%2FInside%20Writing%201%20Cover.jpg"
                    elif "Inside Writing 2" in item.book:
                        img_url = "https://studyways02.s3.ir-thr-at1.arvanstorage.ir/CourseBook%20Covers%2FInside%20Writing%2FInside%20Writing%202%20Cover.png"
                    elif "Inside Writing 3" in item.book:
                        img_url = "https://studyways02.s3.ir-thr-at1.arvanstorage.ir/CourseBook%20Covers%2FInside%20Writing%2FInside%20Writing%203%20Cover.png"
                    elif "Inside Writing 4" in item.book:
                        img_url = "https://studyways02.s3.ir-thr-at1.arvanstorage.ir/CourseBook%20Covers%2FInside%20Writing%2FInside%20Writing%204%20Cover.png"
                elif (item.language, item.book_type) == ("English", "Evolve"):
                    if "Evolve 1 Student's Book" in item.book:
                        img_url = "https://studyways02.s3.ir-thr-at1.arvanstorage.ir/CourseBook%20Covers%2FEvolve%20Covers%2FEvolve%201%20Cover.jpg"
                    elif "Evolve 2 Student's Book" in item.book:
                        img_url = "https://studyways02.s3.ir-thr-at1.arvanstorage.ir/CourseBook%20Covers%2FEvolve%20Covers%2FEvolve%202%20Cover.jpg"
                    elif "Evolve 3 Student's Book" in item.book:
                        img_url = "https://studyways02.s3.ir-thr-at1.arvanstorage.ir/CourseBook%20Covers%2FEvolve%20Covers%2FEvolve%203%20Cover.jpg"
                    elif "Evolve 4 Student's Book" in item.book:
                        img_url = "https://studyways02.s3.ir-thr-at1.arvanstorage.ir/CourseBook%20Covers%2FEvolve%20Covers%2FEvolve%204%20Cover.jpg"
                    elif "Evolve 5 Student's Book" in item.book:
                        img_url = "https://studyways02.s3.ir-thr-at1.arvanstorage.ir/CourseBook%20Covers%2FEvolve%20Covers%2FEvovle%205%20Cover.jpg"
                    elif "Evolve 6 Student's Book" in item.book:
                        img_url = "https://studyways02.s3.ir-thr-at1.arvanstorage.ir/CourseBook%20Covers%2FEvolve%20Covers%2FEvovle%206%20Cover.jpg"
                else:
                    img_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS4pNg-HwTm_WImVeVUgDnRSXU8awW_xMoN85BhqrsRpzMlywHe31eyadJ-zbs7PFFtidE&usqp=CAU"

                item.book_cover_photo_url = img_url
                item.save()
            return Response("All files book_cover_photo_url updated.", status=status.HTTP_200_OK)

        except Exception as e:
            return Response(f"Error: {str(e)}", status=status.HTTP_400_BAD_REQUEST)