# from django.contrib import admin
# from modeltranslation.admin import TranslationAdmin
# from .models import Post
#
# @admin.register(Post)
# class PostAdmin(TranslationAdmin):
#     list_display = ('title', 'slug', 'is_published', 'created_at')
#     search_fields = ('title', 'content')
#     list_filter = ('is_published', 'created_at')


from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):  # <--- admin عادي
    list_display = ('title', 'slug', 'language', 'is_published', 'created_at')
    search_fields = ('title', 'content')
    list_filter = ('is_published', 'language', 'created_at')
    prepopulated_fields = {'slug': ('title',)}
