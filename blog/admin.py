from django.contrib import admin

from blog.models import Comment, Category, Post


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0




@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'author', 'created_at', 'modified_at')
    list_filter = ('status', 'created_at', 'modified_at',)
    list_editable = ('status',)
    search_fields = ('title', 'description',)
    inlines = [CommentInline]


class SocialMediaAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
