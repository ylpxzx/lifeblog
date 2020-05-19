from django.contrib import admin
from .models import Blogger,Link,Layout
from django.utils.safestring import mark_safe
# Register your models here.
admin.site.site_title="Mr Wolf Blog"
admin.site.site_header="Mr Wolf博客管理系统"

@admin.register(Blogger)
class BloggerAdmin(admin.ModelAdmin):
    list_display = ['id','name','image_data','blog_major','autograph','blog_email']
    list_editable = ['name','blog_major','blog_email']

    # 缩略图，后台展示页显示缩略图
    def image_data(self,obj):
        return mark_safe(u'<img src="%s" width="100px" />' % obj.head_photo.url)
    image_data.short_description = u'头像'

@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ['id','link_name','icon_name']
    # list_editable = ['link_name']

@admin.register(Layout)
class LayoutAdmin(admin.ModelAdmin):
    list_display = ['id', 'logo_img', 'website_name']
    list_editable = ['website_name']

    # 缩略图，后台展示页显示缩略图
    # def main_img(self,obj):
    #     return mark_safe(u'<img src="%s" width="100px" />' % obj.main_image.url)
    # main_img.short_description = u'首页图'

    def logo_img(self,obj):
        return mark_safe(u'<img src="%s" width="100px" />' % obj.logo_image.url)
    logo_img.short_description = u'logo'