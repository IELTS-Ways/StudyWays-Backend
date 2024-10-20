from django.urls import path, re_path
from blog.views import PostList, PostItem, InstitutePosts, StudentPosts, AddPost, upload_photo, download_photo, delete_photo


urlpatterns = [
    path("posts", PostList.as_view(), name="posts"),
    path('post-item/<int:id>', PostItem.as_view(), name='post-item'),
    path("institute-posts", InstitutePosts.as_view(), name="institute-posts"),
    path("student-institute-posts", StudentPosts.as_view(), name="student-institute-posts"),
    path("add-post", AddPost.as_view(), name="add-post"),
    path('', upload_photo, name='upload_photo'),
    re_path(r'^download/(?P<photo_name>.+)/$', download_photo, name='download_photo'),
    re_path(r'^delete/(?P<photo_name>.+)/$', delete_photo, name='delete_photo'),  # Update this line
]

