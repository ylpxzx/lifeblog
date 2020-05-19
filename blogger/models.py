from django.db import models
from ckeditor.fields import RichTextField
# Create your models here.
class Blogger(models.Model):
    name = models.CharField('博主名',default='狼性书生',max_length=20)
    head_photo = models.ImageField('头像', upload_to='blog_img',null=True,blank=True,default='/cover_img/default.jpg')
    blog_major = models.CharField('职业',default='程序猿',max_length=20)
    autograph = RichTextField('个性签名',default='个性签名')
    blog_email = models.EmailField('博主邮箱',default='794859685@qq.com')

    def __str__(self):
        return self.name

class Link(models.Model):
    icon_name = models.CharField("链接图标",max_length=50,default='fa fa-dribbble')
    link_name = models.CharField("链接",max_length=50)
    blogger = models.ForeignKey('Blogger',on_delete=models.CASCADE,related_name='blogger_link')

    def __str__(self):
        return self.link_name


class Layout(models.Model):
    # main_image = models.ImageField("首页图",upload_to='layout_img',default='/layout_img/home-banner.jpg')
    logo_image = models.ImageField("Logo",upload_to='layout_img',default='/layout_img/favicon.ico')
    website_name = models.CharField("网站标题名",max_length=20,default='Mr Wolf Blog')

    def __str__(self):
        return self.website_name