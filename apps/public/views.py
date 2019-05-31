from django.views.generic import View
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator

from django.core.cache import cache

from apps.public.models import Image, IndexCarousel
from apps.user.models import Article, Comment, Category, Tag


# 主页
class IndexView(View):

    def get(self, request):

        article_type = request.GET.get('article_type', '0')  # 文章类型
        article_tag = request.GET.get('article_tag', '0')
        page = request.GET.get('page', '1')  # 页码

        user = request.user

        # 获取轮播信息
        carousels = IndexCarousel.objects.all()

        # 获取热门文章（浏览量最多的文章）
        hot_articles = Article.objects.all().order_by('-click_count')[:10]

        # 标题内容
        if article_type == '0' and article_tag == '0':
            articles = Article.objects.all()
            top_title = '全部文章'

        elif article_type != '0':
            articles = Article.objects.filter(category=article_type)
            # 分类信息
            category = Category.objects.get(id=article_type)
            top_title = '%s类型的所有文章' % category.name

        elif article_tag != '0':
            articles = Article.objects.filter(tag=article_tag)
            # 获取当前标签信息
            tag = Tag.objects.get(id=article_tag)
            top_title = '%s标签的所有文章' % tag.name
        else:
            articles = Article.objects.all()
            top_title = '全部文章'




        for article in articles:
            # 解决封面图片问题

            if article.image == '':
                article.image_default = '/static/tx/fengmian.jpg'

            # 获取评论次数
            comment = Comment.objects.filter(article=article)
            # print(articles) 增加浏览次数记录在 article 中
            article.comment_count = comment.count()
            article.tags = article.tag.all()

        # todo： 进行分页
        paginator = Paginator(articles, 10)
        # 获取第page页的内容(要进行数据校验，安全处理)c
        try:
            page = int(page)
        except Exception as e:
            page = 1

        if page > paginator.num_pages:
            page = 1

        # 获取第page页的Page的实例化对象
        articles_page = paginator.get_page(page)

        # todo: 进行页码的控制，页面上最多显示5个页码
        # 1、总页数小于5页，页面上显示所有页码
        # 2、如果当前页是前3页，显示1-5页
        # 3、如果当前页是后3页，显示后5页
        # 4、其他情况，显示当前页的前2页，当前页 和 当前页的后2页
        num_pages = paginator.num_pages
        if num_pages < 5:
            pages = range(1, num_pages + 1)
        elif page <= 3:
            pages = range(1, 6)
        elif num_pages - page <= 2:
            pages = range(num_pages - 4, num_pages + 1)
        else:
            pages = range(page - 2, page + 3)



        context = {
            'user': user,
            'top_title': top_title,  # 标题写什么
            'carousels': carousels,  # 轮播暂时没用
            'hot_articles': hot_articles,  # 热门文章
            'articles_page': articles_page,  # 该分页商品
            'pages': pages,  # 分页格式
        }

        return render(request, 'index.html', context)


# 上传图片
class InputImageView(View):

    def post(self, request):

        # 接受数据
        image = request.FILES.get('image')
        # 校验数据

        # 业务处理
        image = Image.objects.create(image=image)
        image.save()

        # 返回应答
        # 将 image的格式转化为字符串
        image_str = '%s' % image

        # return HttpResponse('{"errno": 0, "data": [%s, ]}' % image)
        # 返回的格式
        # {
        #     // errno 即错误代码，0 表示没有错误。
        #     //       如果有错误，errno != 0，可通过下文中的监听函数 fail 拿到该错误码进行自定义处理
        #     "errno": 0,
        #
        #     // data 是一个数组，返回若干图片的线上地址
        #     "data": [
        #         "图片1地址",
        #         "图片2地址",
        #         "……"
        #     ]
        # }

        return JsonResponse({"errno": 0, "data": [image_str, ]})


# 分类信息页面和标签搜索结果页面













