from django.db import models
from common.models import CommonModel
# Create your models here.
# coursereview_id : 총 수강평 아이디(PK)
# user_id : 유저 아이디(FK)
# score : 별점
# comment : 내용
# created_date : 생성 날짜

class CourseReview(CommonModel):
    rating = ((1,1),(2,2),(3,3),(4,4),(5,5),)
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="coursereviews"
    )
    
    score = models.PositiveIntegerField(choices=rating)
    comment = models.TextField(null=True, blank=True, max_length=1000)
    