from django.contrib import admin
from apps.public.models import IndexCarousel


class IndexCarouselAdmin(admin.ModelAdmin):
    # listdisplay设置要显示在列表中的字段（id字段是Django模型的默认主键）
    list_display = ('id', 'name', 'index')

    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 50


admin.site.register(IndexCarousel, IndexCarouselAdmin)
