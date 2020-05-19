"""lifeblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('post/', include('post.urls'))
"""
import haystack.urls
from django.contrib import admin
from django.urls import path
from django.conf.urls import include,url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns  # 加入该行,如若不加，在生产环境下无法加载样式
from post.views import page_not_found
from django.views.static import serve   # 加入该行,如若不加，在生产环境下无法加载样式

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'', include('ckeditor_uploader.urls')),
    url(r'',include('post.urls')),
    url(r'^search/', include(haystack.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()  # # 加入该行,如若不加，在生产环境下无法加载样式

if settings.DEBUG == False:
    print('当前处于生产环境下')
    urlpatterns += [
        url(r'^static/(?P<path>.*)$',serve,{'document_root':settings.STATIC_ROOT}), # 加入该行,如若不加，在生产环境下无法加载样式
        url(r'^media/(?P<path>.*)$',serve,{'document_root':settings.MEDIA_ROOT}),  # 加入该行,如若不加，在生产环境下无法显示图片
        ]
else:
    print('当前处于开发环境下')


handler404 = page_not_found