from rest_framework import serializers

from accounts.serializers import UserLightSerializer
from blog.models import Category, Post, Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('title',)


class ReplyCommentSerializer(serializers.ModelSerializer):
    user = UserLightSerializer()
    class Meta:
        model = Comment
        fields = ('user', 'title', 'caption')


class CommentListSerializer(serializers.ModelSerializer):
    user = UserLightSerializer()
    class Meta:
        model = Comment
        fields = ('id', 'user', 'title', 'caption', 'replies_count')


class CommentDetailSerializer(serializers.ModelSerializer):
    user = UserLightSerializer()
    replies = ReplyCommentSerializer(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = ('user', 'title', 'caption', 'replies')
        extra_kwargs = {
            'user': {'read_only': True}
        }


class CommentWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('user', 'post', 'title', 'caption', 'reply_to')


class PostListSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True)
    status = serializers.CharField(source='get_status_display')
    author = UserLightSerializer()

    class Meta:
        model = Post
        fields = ('id', 'title', 'status', 'author', 'description', 'categories', 'like_count', 'image', 'created_at')


class PostDetailSerializer(PostListSerializer):
    comments = serializers.SerializerMethodField()
    likes = UserLightSerializer(many=True, read_only=True)

    def get_comments(self, post):
        comments = post.comments.root()
        return CommentListSerializer(comments, many=True).data

    class Meta:
        model = Post
        fields = PostListSerializer.Meta.fields + ('comments', 'likes')


class PostWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('title', 'status', 'description', 'categories', 'image')
