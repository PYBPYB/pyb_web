from django.urls import path
from apps.public.views import IndexView, InputImageView, InputCommentView

urlpatterns = [
    path('comment', InputCommentView.as_view(), name='comment'),  # 评论信息上传
    path('image', InputImageView.as_view(), name='image'),  # 图片上传视图
    path('', IndexView.as_view(), name='index'),  # 网站主页

]
