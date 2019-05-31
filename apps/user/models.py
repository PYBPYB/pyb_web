from django.db import models
from db.base_model import BaseModel
from django.contrib.auth.models import AbstractUser
import django.utils.timezone as timezone
from tinymce.models import HTMLField

'''
############ 本地模型用到的字段类型和和参数的含义

max_length：最大长度
blank：True可以为空
null：可以为null
verbose_name：admin显示名称
default：默认值
unique：True表示唯一
【ImageField】：upload_to表示MEDIA_ROOT的子目录，用来存放上传的文件
【CharField】
【URLField】
【IntegerField】
【DateTimeField】：auto_now_add表示自动设置当前时间
【TextField】
【BooleanField】
【EmailField】
'''


# 用户(User)模型
# 采用的继承方式扩展用户信息
class User(AbstractUser, BaseModel):
    avatar = models.ImageField(upload_to='static/avatar/default.png', default=None, max_length=200, blank=True,
                               null=True, verbose_name='用户头像')
    qq = models.CharField(max_length=20, blank=True, null=True, verbose_name='QQ号码')
    weixin = models.CharField(max_length=50, blank=True, null=True, verbose_name='微信')
    mobile = models.CharField(max_length=11, blank=True, null=True, unique=True, verbose_name='手机号码')
    url = models.URLField(max_length=100, blank=True, null=True, verbose_name='个人网页地址')
    creed = models.CharField(max_length=300, blank=True, default='好好学习，天天向上！', verbose_name='个人信条')

    # 使用内部的class Meta 定义模型的元数据
    class Meta:
        # verbose_name：数据库表名名称，这里表名称为“用户”
        verbose_name = '用户'
        # verbose_name_plural：人类可读的单复数名称，这里“用户”复数名称为“用户”
        verbose_name_plural = verbose_name
        # ordering：如排序选项，这里以id降序来排序
        ordering = ['-id']

    # 对象的字符串表达式(unicode格式)
    def __str__(self):
        return self.username


# 文章标签(tag)模型
class Tag(BaseModel):
    name = models.CharField(max_length=30, unique=True, verbose_name='标签名称')

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 分类(category)模型
class Category(BaseModel):
    name = models.CharField(max_length=30, verbose_name='分类名称')
    index = models.IntegerField(default=999, verbose_name='优先级')

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name
        ordering = ['index', 'id']

    def __str__(self):
        return self.name


# 自定义一个文章Model的管理器  新加一个数据处理的方法
# 2、改变原有的queryset
class ArticleManager(BaseModel):
    def distinct_date(self):
        distinct_date_list = []
        date_list = self.values('date_publish')
        for date in date_list:
            date = date['date_publish'].strftime('%Y/%m文章存档')
            if date not in distinct_date_list:
                distinct_date_list.append(date)
        return distinct_date_list


# 文章(aticle)模型
class Article(BaseModel):
    title = models.CharField(max_length=50, verbose_name='文章标题')
    desc = models.CharField(max_length=1000, verbose_name='文章描述')
    image = models.ImageField(upload_to='static/avatar/fengmian.jpg', default=None, blank=True, null=True, verbose_name='封面图片')
    content = models.TextField(verbose_name='文章内容', blank=True)
    click_count = models.IntegerField(default=0, verbose_name='点击次数')
    is_recommend = models.BooleanField(default=False, verbose_name='是否推荐')
    date_publish = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    mod_date = models.DateTimeField(auto_now=True, verbose_name='最后修改日期')
    user = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name='用户')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, blank=True, null=True, verbose_name='分类')
    tag = models.ManyToManyField(Tag, verbose_name='标签')

    objects = ArticleManager()

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-date_publish']

    def __str__(self):
        return self.title


# 评论(comment)模型
class Comment(BaseModel):
    content = models.TextField(verbose_name='评论内容', blank=True)
    username = models.CharField(max_length=30, blank=True, null=True, verbose_name='用户名')
    email = models.EmailField(max_length=50, blank=True, null=True, verbose_name='邮箱地址')
    url = models.URLField(max_length=100, blank=True, null=True, verbose_name='个人网页地址')
    date_publish = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    # 目标文章信息
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='文章')
    pid = models.IntegerField(default=0, verbose_name='父级评论id')

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.content)


# 友情链接(links)模型
class Links(BaseModel):
    title = models.CharField(max_length=50, verbose_name='标题')
    description = models.CharField(max_length=200, verbose_name='友情链接描述')
    callback_url = models.URLField(verbose_name='url地址')
    date_publish = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    index = models.IntegerField(default=999, verbose_name='排列顺序(从小到大)')

    class Meta:
        verbose_name = '友情链接'
        verbose_name_plural = verbose_name
        ordering = ['index', 'id']

    def __str__(self):
        return self.title


# 广告(ad)模型
class Ad(BaseModel):
    title = models.CharField(max_length=50, verbose_name='广告标题')
    description = models.CharField(max_length=200, verbose_name='广告描述')
    image_url = models.ImageField(upload_to='ad/%Y/%m', verbose_name='图片路径')
    callback_url = models.URLField(null=True, blank=True, verbose_name='回调url')
    date_publish = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    index = models.IntegerField(default=999, verbose_name='排列顺序(从小到大)')

    class Meta:
        verbose_name = '广告'
        verbose_name_plural = verbose_name
        ordering = ['index', 'id']

    def __str__(self):
        return self.title
