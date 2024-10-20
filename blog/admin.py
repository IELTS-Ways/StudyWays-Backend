from django.contrib import admin
from blog.models import Category,Post
from import_export.admin import ImportExportModelAdmin

''' 
class PostCommentAdmin(admin.ModelAdmin):
    list_display = ('sender', 'create_at')
admin.site.register(PostComment, PostCommentAdmin)
'''

class CategoryAdmin(ImportExportModelAdmin):
    list_display = ('name',)
admin.site.register(Category, CategoryAdmin)


class PostAdmin(ImportExportModelAdmin):
    list_display = ('title', 'author', 'category', 'post_date')
    list_filter = ("title", "author", "category", "post_date")
    search_fields = ['title', 'author', 'category']
admin.site.register(Post, PostAdmin)