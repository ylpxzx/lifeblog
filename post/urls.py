from django.conf.urls import url
from django.urls import path
from .views import IndexView,PostDetailView,MySearchIndex
app_name = 'post'
urlpatterns = [
    # 不要使用在根url使用：r'index/', 在应用app中使用：r'' 。   会导致页面无法跳转，
    url(r'^index/',IndexView.as_view(),name="index"),
    url(r'^detail/(?P<post_id>\d+)$',PostDetailView.as_view(),name='detail'),
    url(r'^search/$', MySearchIndex(), name='haystack_search'),
]

