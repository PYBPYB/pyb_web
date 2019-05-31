from django.urls import path
from apps.user.views import UserView, UserLoginView, UserLogoutView, UserRegisterView, UserWriteBlogView, UserDetailsView, UserInformationView

urlpatterns = [
    path('login', UserLoginView.as_view(), name='login'),  # 登录
    path('register', UserRegisterView.as_view(), name='register'),  # 注册
    path('logout', UserLogoutView.as_view(), name='logout'),  # 退出账号

    path('write', UserWriteBlogView.as_view(), name='write'),  # 写博客
    path('details/<article_id>', UserDetailsView.as_view(), name='details'),  # 博客详情页面

    path('information', UserInformationView.as_view(), name='information'),  # 个人信息
    path('center', UserView.as_view(), name='center'),  # 用户中心
]
