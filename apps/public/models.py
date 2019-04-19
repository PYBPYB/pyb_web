from django.db import models
from db.base_model import BaseModel
from apps.user.models import User, Article


# 用户上传图片存储类
class Image(BaseModel):
    image = models.ImageField(verbose_name='用户上传的图片')

    class Meta:
        verbose_name = '图片'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.image.url


# 首页轮播控制
class IndexCarousel(BaseModel):
    name = models.CharField(max_length=50, verbose_name='轮播主题')
    url = models.URLField(verbose_name='轮播图片指向地址')
    image = models.ImageField(verbose_name='轮播图片')
    index = models.SmallIntegerField(default=0, verbose_name='展示顺序')

    class Meta:
        verbose_name = '轮播图片'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name





