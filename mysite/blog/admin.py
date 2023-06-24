from django.contrib import admin
from .models import Post, Message, Topic

# Register your models here.


# admin.site.register(Post)
# admin.site.register(Message)
admin.site.register(Topic)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['author', 'title', 'created', 'updated']
    search_fields = ['title', 'author']
    list_filter = ['topic']
    ordering = ['-updated', 'created']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['post', 'user', 'parent', 'body']
    list_filter = ['parent']
    ordering = ['-created']


admin.site.site_header = 'My Blogpost Administration Page'
admin.site.site_title = 'My Blogpost'
admin.site.index_title = 'Welcome To The Admin Area'
