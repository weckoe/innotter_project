from django.contrib import admin
from apps.content.models import (
    Page,
    Post
)


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    pass


@admin.register(Post)
class PageAdmin(admin.ModelAdmin):
    pass
