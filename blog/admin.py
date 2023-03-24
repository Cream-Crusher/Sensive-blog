from django.contrib import admin
from blog.models import Post, Tag, Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    raw_id_fields = ['likes', 'tags', ]
    pass

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    raw_id_fields = ['post', 'author', ]
    list_display = ['text', ]
    pass
