from django.contrib import admin
from .models import Post,Category
from django.utils.safestring import mark_safe
# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title','image_data','create_time','short_detail','is_publish','is_comment','category','id']
    list_editable = ['is_publish','is_comment','category']
    list_filter = ['title','create_time','is_publish','is_comment','category']
    # readonly_fields = ('image_data',)  # 必须加这行 否则访问编辑页面会报错

    # 缩略图显示
    def image_data(self,obj):
        return mark_safe(u'<img src="%s" width="100px" />' % obj.cover.url)
    image_data.short_description = u'封面'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id','post_category']
    list_editable = ['post_category']