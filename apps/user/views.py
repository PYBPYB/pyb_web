from django.urls import reverse
from django.http import JsonResponse
from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from apps.user.models import User, Article, Category, Tag, Comment
import re

from utils.mixin import LoginRequiredMixin


# 个人中心
class UserView(LoginRequiredMixin, View):
    # 文章类型（莫认为0，表示所有类型） 文章访问页码
    def get(self, request, articles_type, page):
        user = request.user
        # 获取该用户所有的文章 和 评论
        if articles_type == '0':
            articles = Article.objects.filter(user=user)
        else:
            articles = Article.objects.fileter(user=user, type=articles_type)

        for article in articles:
            comment = Comment.objects.filter(article=article)

            # print(articles) 增加浏览次数记录在 article 中
            article.comment_count = comment.count()
            article.tags = article.tag.all()

        # todo： 进行分页
        paginator = Paginator(articles, 6)
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
            # 'articles': articles,
            'articles_page': articles_page,  # 该分页商品
            'pages': pages,  # 分页格式
        }

        return render(request, 'user.html', context)


# 登录
class UserLoginView(View):
    """登录"""
    def get(self, request):
        # 显示登录页面
        if 'username' in request.COOKIES:
            username = request.COOKIES.get('username')
            checked = 'checked'
        else:
            username = ''
            checked = ''
        # 使用模板
        return render(request, 'login.html',
                      {'username': username,
                       'checked': checked})

    def post(self, request):
        # 登录校验
        # 接收数据
        username = request.POST.get('username')
        password = request.POST.get('pwd')
        # 校验数据
        if not all([username, password]):
            return render(request, 'login.html', {'errmsg': '数据不完整'})

        # 业务处理：登录校验
        # try:
        #     user1 = User.objects.get(username=username)
        #     print(user1)
        #     user2 = User.objects.get(password=password)
        #     print(user2)
        # except:
        #     pass

        user = authenticate(username=username, password=password)
        # print('------------------', user, '------------------')

        if user is not None:

            login(request, user)

            # 获取登录后所要跳转的地址，默认跳转到首页（重定向）
            next_url = request.GET.get('next', reverse('public:index'))  # None

            # 跳转到next_url
            # response = render(request, 'user_center_info.html')
            # response = render(reverse(next_url))  # 不是重定向
            response = redirect(next_url)

            # 判断是否需要记住用户名
            remember = request.POST.get('remember')

            if remember == 'on':
                # 记住用户名
                response.set_cookie('username', username, max_age=7*24*3600)
            else:
                response.delete_cookie('username')
            # 返回 response
            return response
        else:
            #  用户名或密码错误
            print(username, '---', password, '---', user)
            return render(request, 'login.html', {'errmsg': '用户名或密码错误'})


# 退出当前登录用户用户
class UserLogoutView(View):
    def get(self, request):
        # 清除用户的session信息
        logout(request)
        return redirect(reverse('public:index'))


# 注册
class UserRegisterView(View):

    def get(self, request):
        # 显示注册页面
        return render(request, 'register.html')

    def post(self, request):
        # 进行注册处理
        # 接受数据
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        email = request.POST.get('email')

        # print(username, password, email)

        # 进行数据的校验
        if not all([username, password, email]):
            # 数据不完整
            return render(request, 'register.html',
                          {'errmsg': '数据不完整'})

        # 校验用户名是否重复
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            # 用户名不存在
            user = None
        if user:
            # 用户名已存在
            return render(request, 'register.html',
                          {'errmsg': '用户名已存在'})

        # 校验邮箱是否已经被注册
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # 邮箱不存在
            user = None

        if user:
            # 邮箱已存在
            return render(request, 'register.html',
                          {'errmsg': '该邮箱已被注册'})


        # print('到了这马？1')
        # 进行业务处理：进行用户注册
        user = User.objects.create_user(username, email, password)
        user.is_active = 0  # 默认绑定邮箱
        user.save()

        # print('到了这马？2')
        # 返回应答,跳转首页
        return redirect(reverse('public:index'))  # 反向解析，需要目标设置的自己的 name属性


# 写博客
class UserWriteBlogView(LoginRequiredMixin, View):

    #
    def get(self, request):

        # 获取所有的文章分类信息
        categorys = Category.objects.all()

        # 获取所有的文章标签


        # 返回应答
        context = {
            'categorys': categorys,
        }

        return render(request, 'blog_write.html', context)


    def post(self, request):
        """

        :param request:
        title：    文章标题
        category： 文章类型
        image:     文章封面图片文件对象
        tag:       文章标签
        desc:      描述信息
        文章内容
        :return:内容审核页面（博客详情显示页面）博文效果
        """
        # 接受数据
        title = request.POST.get('title')
        category = request.POST.get('category')
        image = request.FILES.get('image')
        tag = request.POST.get('tag')
        desc = request.POST.get('desc')
        content = request.POST.get('content')

        # 校验数据
        # print('----->', image, '<-----')

        # 获取当前登录用户的实例对象
        user = request.user
        # 获取当前文章分类对应的分类信息的实例对象
        category = Category.objects.get(name=category)

        # 业务处理 增加一条博客信息信息
        blog = Article.objects.create(
            title=title,
            category=category,
            image=image,
            desc=desc,
            content=content,
            user=user,

            # tag=tag,
        )

        # 处理标签信息
        tags = re.split(r'[ ]+', tag)
        # print(tags)
        for tag in tags:
            try:
                tag_object = Tag.objects.get(name=tag)
            except:
                tag_object = Tag.objects.create(name=tag)
                tag_object.save()

            blog.tag.add(tag_object)

        blog.save()

        # 返回应答

        return JsonResponse({'res': 0, 'article_id': blog.id})


# 博客详情页面
class UserDetailsView(View):

    def get(self, request, article_id):

        # 接受数据，该文的id
        id = article_id

        # 数据校验


        # 业务处理


        article = Article.objects.get(id=id)

        article.click_count += 1

        article.save()


        context = {
            'article': article,
        }

        return render(request, 'blog_details.html', context)








