import os
import time
import datetime
from django.db import models
# from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.

def modify_path(instance, filename):
    '''
    重定义封面保存路径
    :param instance: self
    :param filename: 文件名
    :return: 新路径
    '''
    ext = filename.split('.').pop()
    now_date = datetime.datetime.now().strftime('%Y%m%d')
    now_time = int(time.time())
    filename = '{0}{1}.{2}'.format(now_date, now_time, ext)
    return os.path.join('cover_img', now_date, filename) # 系统路径分隔符差异，增强代码重用性

class Post(models.Model):
    '''
    文章模型
    '''
    title = models.CharField('标题',max_length=100,default='无标题名',null=True,blank=True)
    cover = models.ImageField('封面', upload_to=modify_path,null=True,blank=True,default='/cover_img/default.jpg')
    create_time = models.DateTimeField('创建时间',auto_now=True)
    content = RichTextUploadingField('文章内容',default='文章内容')
    is_publish = models.BooleanField(default=False)
    is_comment = models.BooleanField(default=False)
    total_views = models.PositiveIntegerField('文章浏览量',default=0)
    category = models.ForeignKey('Category',on_delete=models.CASCADE,related_name='post')

    def __str__(self):
        return self.title

    # 完善后台数据显示过长情况
    def short_detail(self):
        if len(str(self.content)) > 30:
            return '{}...'.format(str(self.content)[0:29])
        else:
            return str(self.content)
    short_detail.allow_tags = True
    short_detail.short_description = u'文章内容'

class Category(models.Model):
    post_category = models.CharField('文章类别',max_length=20,default='杂记')
    def __str__(self):
        return self.post_category

