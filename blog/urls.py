from django.urls import path
from rest_framework.routers import SimpleRouter

from blog.views import CategoryListView, UserPostViewSet, CommentCreateView, CommentView, PostLike, \
    PostDetailView, PostListView

app_name = 'blog'

router = SimpleRouter()
router.register('user-posts', UserPostViewSet, basename='Post')

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('posts/', PostListView.as_view(), name='post-list'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='get-post'),
    path('comments/', CommentCreateView.as_view(), name='create-comment'),
    path('comments/<int:pk>/', CommentView.as_view(), name='get-or-update-comment'),
    path('posts/<int:pk>/likes/', PostLike.as_view(), name='post-like'),
]

urlpatterns += router.urls
