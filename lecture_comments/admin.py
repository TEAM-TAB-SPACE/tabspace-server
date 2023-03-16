from django.contrib import admin
from .models import LectureComment, CommentReply

@admin.register(LectureComment)
class LectureCommentAdmin(admin.ModelAdmin):  
    pass

@admin.register(CommentReply)
class CommentReplyAdmin(admin.ModelAdmin):  
    pass
    
