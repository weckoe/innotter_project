from django.contrib import admin
from apps.content.models import (
    Page,
    Post,
    Tag,
)


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    pass


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass
