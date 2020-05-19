# from django.shortcuts import render,HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
# from django.views.generic import View
from .models import Post,Category
from blogger.models import Blogger,Layout,Link
from urllib import parse
from haystack.views import SearchView
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.conf import settings
from django.shortcuts import render,redirect
from django.db.models import Q,Count
# Create your views here.


class IndexView(ListView):
    model = Post
    template_name = "index.html"
    context_object_name = "post_list"
    paginate_by = 6
    def get_queryset(self):
        # 判断urls是否携带category参数来确定是否选中分类
        url_args = self.request.GET.dict()

        if url_args != {}:  # 判断是否在首页/index/,无参数
            # 判断是否处于分类下
            if 'category' not in url_args:
                post_list = Post.objects.filter(is_publish=True).order_by("-id")
            else:
                # 选中分类，获取指定分类文章
                category_obj = Category.objects.get(post_category = url_args['category'])
                post_list = Post.objects.filter(is_publish=True,category_id=category_obj.id).order_by("-id")
        else:
            # 未选中分类，获取全部文章
            post_list = Post.objects.filter(is_publish=True).order_by("-id")
        return post_list

    def get_context_data(self,object_list=None, **kwargs):

        if 'category' in self.request.get_full_path():
            url = self.request.get_full_path()
            params = parse.parse_qs(parse.urlparse(url).query)
            kwargs['category'] = params['category'][0]
        else:
            kwargs['category'] = None
        kwargs['website'] = Layout.objects.get(id=2)
        kwargs['author_list'] = Blogger.objects.all()
        # kwargs['category_list'] = Category.objects.filter(post__is_publish=True).order_by('post_category')

        # 分组、聚合查询：过滤出允许发布的文章，按post_category分组 , 将post下的is_publish字段计数，返回结果是post_category字段和计数结果
        kwargs['category_list'] = Category.objects.filter(post__is_publish=True).values("post_category").annotate(c=Count('post__is_publish')).values('post_category','c').order_by('post_category')


        kwargs['new_post'] = Post.objects.filter(is_publish=True).order_by("-create_time")[:4]
        kwargs['popular_post'] = Post.objects.filter(is_publish=True).order_by('-total_views')[:4]
        kwargs['link_list'] = Link.objects.all()
        content = super(IndexView,self).get_context_data(**kwargs)
        return content


class PostDetailView(DetailView):
    model = Post
    template_name = 'detail_post.html'
    context_object_name = "post"
    pk_url_kwarg = 'post_id'

    def get_object(self, queryset=None):
        obj = super(PostDetailView,self).get_object()
        obj.total_views += 1
        obj.save(update_fields=['total_views'])

        return obj

    def get_context_data(self, **kwargs):
        kwargs['link_list'] = Link.objects.all()
        kwargs['author_list'] = Blogger.objects.all()
        # kwargs['category_list'] = Category.objects.filter(post__is_publish=True).order_by('post_category')
        kwargs['category_list'] = Category.objects.filter(post__is_publish=True).values("post_category").annotate(c=Count('post__is_publish')).values('post_category', 'c').order_by('post_category')

        kwargs['popular_post'] = Post.objects.filter(is_publish=True).order_by('-total_views')[:4]
        content = super(PostDetailView, self).get_context_data(**kwargs)


        num = content['post'].id
        # 下一篇 ，如果想实现分类状态下的上下一篇，可自行过滤
        next_post = Post.objects.filter(id__gt=num,is_publish=True).order_by("id")[:1]
        if len(next_post) == 0:
            content['next_post'] = 0
        else:
            for next in next_post:
                content['next_post'] = next

        # 上一篇
        prev_post = Post.objects.filter(id__lt=num,is_publish=True).order_by("-id")[:1]
        if len(prev_post) == 0:
            content['prev_post'] = 0
        else:
            for prev in prev_post:
                content['prev_post'] = prev

        return content


class MySearchIndex(SearchView):

    # template = 'search.html'

    def extra_context(self):
        context = super(MySearchIndex,self).extra_context()
        # context['category_list'] = Category.objects.filter(post__is_publish=True).order_by('post_category')
        context['category_list'] = Category.objects.filter(post__is_publish=True).values("post_category").annotate(c=Count('post__is_publish')).values('post_category', 'c').order_by('post_category')

        context['popular_post'] = Post.objects.filter(is_publish=True).order_by('-total_views')[:4]
        return context

    def create_response(self):
        if self.request.GET.get('q'):
            keyword = self.request.GET.get('q')
            # post_info = Post.objects.filter(title__contains=keyword)
            post_info = Post.objects.filter(Q(title__icontains=keyword)|Q(content__icontains=keyword)).filter(is_publish=True).order_by("id")  # 搜索标题和文章内容
            # post_info = Post.objects.all()
            paginator = Paginator(post_info, settings.HAYSTACK_SEARCH_RESULTS_PER_PAGE)
            try:
                page = paginator.page(int(self.request.GET.get('page', 1)))
            except PageNotAnInteger:
                page = paginator.page(1)
            except EmptyPage:
                page = paginator.page(paginator.num_pages)

            context = {
                'query': self.query,
                'form': self.form,
                'page': page,
                'paginator': paginator,
                'suggestion': None,
            }
            context.update(self.extra_context())
            return render(self.request, self.template, context)
        else:
            qs = super(MySearchIndex, self).create_response()
            return qs

def page_not_found(request,exception):
    return render(request, '404.html')