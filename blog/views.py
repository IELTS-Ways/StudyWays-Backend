from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from blog.serializers import PostSerializer, PostDetailSerializer
from blog.models import Post,Category
from rest_framework.permissions import AllowAny, IsAuthenticated
from accounts.views.permissions import IsInstitute, IsFreelance
from accounts.models import InstituteProfile, StudentProfile
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import GenericAPIView
from django.shortcuts import render, redirect
from blog.forms import PostForm
from django.conf import settings as s
import boto3
import datetime
import os



class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class PostList(GenericAPIView):
    permission_classes = [AllowAny]
    pagination_class = CustomPagination
    serializer_class = PostDetailSerializer
    queryset = Post.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['post_date', 'category', 'author']
    search_fields = ['title', 'body']
    ordering_fields = ['post_date', 'category', 'author']

    def get(self, *args, **kwargs):
        posts = self.filter_queryset(Post.objects.all())
        page = self.paginate_queryset(posts)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.filter_queryset(Post.objects.all())
        return Response(serializer.data, status=status.HTTP_200_OK)


class PostItem(APIView):
    serializer_class = PostDetailSerializer
    permission_classes = [AllowAny]
    def get(self, *args, **kwargs):
        try:
            post = Post.objects.get(id=self.kwargs["id"])
            serializer = self.serializer_class(post)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response("Post not found or something went wrong, try again", status=status.HTTP_400_BAD_REQUEST)


class InstitutePosts(GenericAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    serializer_class = PostDetailSerializer
    queryset = Post.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['post_date', 'category', 'author']
    search_fields = ['title', 'body']
    ordering_fields = ['post_date', 'category', 'author']

    def get(self, *args, **kwargs):
        institute = InstituteProfile.objects.get(user=self.request.user)
        posts = self.filter_queryset(Post.objects.filter(author=institute))
        page = self.paginate_queryset(posts)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.filter_queryset(Post.objects.filter(author=institute))
        return Response(serializer.data, status=status.HTTP_200_OK)


class StudentPosts(GenericAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    serializer_class = PostDetailSerializer
    queryset = Post.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['post_date', 'category', 'author']
    search_fields = ['title', 'body']
    ordering_fields = ['post_date', 'category', 'author']

    def get(self, *args, **kwargs):
        student = Post.objects.get(user=self.request.user)
        posts = self.filter_queryset(Post.objects.filter(author=student.institute))
        page = self.paginate_queryset(posts)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.filter_queryset(Post.objects.filter(author=student.institute))
        return Response(serializer.data, status=status.HTTP_200_OK)


class AddPost(APIView):
    serializer_class = PostSerializer
    permission_classes = [IsInstitute]

    def post(self, *args, **kwargs):
        data = self.request.data.copy()
        institute = InstituteProfile.objects.get(user=self.request.user)
        data["author"] = institute.id
        serializer = self.serializer_class(data=data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)



#---------------- liara --------------



LIARA = {
    'endpoint': s.LIARA_ENDPOINT,
    'accesskey': s.LIARA_ACCESS_KEY,
    'secretkey': s.LIARA_SECRET_KEY,
    'bucket': s.LIARA_BUCKET_NAME
}


def upload_photo(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            photo_instance = form.save(commit=False)

            # Get the original filename and extension
            original_filename, file_extension = os.path.splitext(photo_instance.image.name)

            # Get current date and time
            current_date = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

            # Construct unique filename with date and original filename
            filename = f"{current_date}_{original_filename}{file_extension}"

            # Set the filename
            photo_instance.image.name = filename
            photo_instance.save()
            return redirect('upload_photo')
    else:
        form = PostForm()

    # Retrieve a list of uploaded photos from the S3 bucket
    s3 = boto3.client('s3',
                      endpoint_url=LIARA['endpoint'],
                      aws_access_key_id=LIARA['accesskey'],
                      aws_secret_access_key=LIARA['secretkey']
                      )
    bucket_name = LIARA['bucket']
    objects = s3.list_objects(Bucket=bucket_name)

    uploaded_photos = []
    if 'Contents' in objects:
        for obj in objects['Contents']:
            uploaded_photos.append({
                'name': obj['Key'],  # Assuming key name as file name
                'permanent_link': f"{LIARA['endpoint']}/{bucket_name}/{obj['Key']}",
                'temporary_link': s3.generate_presigned_url(
                    'get_object',
                    Params={'Bucket': bucket_name, 'Key': obj['Key']},
                    ExpiresIn=3600  # 1 hour expiry
                )
            })
    else:
        uploaded_photos.append({'name': 'no file', 'permanent_link': '', 'temporary_link': ''})

    return render(request, 'photos/upload_photo.html', {'form': form, 'uploaded_photos': uploaded_photos})


def download_photo(request, photo_name):
    s3 = boto3.client('s3',
                      endpoint_url=LIARA['endpoint'],
                      aws_access_key_id=LIARA['accesskey'],
                      aws_secret_access_key=LIARA['secretkey']
                      )
    bucket_name = LIARA['bucket']
    file_url = s3.generate_presigned_url(
        'get_object',
        Params={'Bucket': bucket_name, 'Key': photo_name},
        ExpiresIn=3600  # 1 hour expiry
    )
    return redirect(file_url)


def delete_photo(request, photo_name):
    s3 = boto3.client('s3',
                      endpoint_url=LIARA['endpoint'],
                      aws_access_key_id=LIARA['accesskey'],
                      aws_secret_access_key=LIARA['secretkey']
                      )
    bucket_name = LIARA['bucket']
    s3.delete_object(Bucket=bucket_name, Key=photo_name)
    return redirect('upload_photo')

