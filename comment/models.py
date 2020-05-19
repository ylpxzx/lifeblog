from django.db import models
# from life_blog.posts.models import Post

# Create your models here.

class Comment(models.Model):
    name = models.CharField('姓名',max_length=50)
    email = models.EmailField('邮箱',unique=True, blank=False)
    major = models.CharField('专业',max_length=50)
    comment_content = models.TextField('评论内容')
    is_examine = models.BooleanField("是否审核通过",default=False)
    post_comment = models.ForeignKey('post.Post',on_delete=models.CASCADE,related_name='user_comment')

    def __str__(self):
        return self.email