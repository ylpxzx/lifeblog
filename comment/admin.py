from django.contrib import admin
from .models import Comment
# Register your models here.

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id','name','email','major','comment_content','is_examine','post_comment']
    list_editable = ['is_examine']
    list_filter = ['is_examine','email','major','name']