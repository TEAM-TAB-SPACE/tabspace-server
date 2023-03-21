from django.db import models
from common.models import CommonModel
# lecturecomments_id : 강의 댓글 아이디(PK)
# user_id : 유저 아이디(FK)
# comment : 내용


class LectureComment(CommonModel):
    
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="lecturecomments"
    )
    lecture = models.ForeignKey(
        "lectures.Lecture",
        on_delete=models.CASCADE
    )
    comment = models.TextField(max_length=1000)
    


# commentsreplies_id : 강의 대댓글 아이디(PK)
# user_id : 유저 아이디(FK)
# lecturecomments_id : 유저 아이디(FK)
# reply : 내용


class CommentReply(CommonModel):
    
    
    user= models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="replies"
    )
    
    lecture_comment = models.ForeignKey(
        "lecture_comments.LectureComment",
        on_delete=models.CASCADE,
        related_name="replies"
    )
    
    comment = models.CharField(max_length=255)
    