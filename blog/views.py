from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, filters
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateAPIView, get_object_or_404, \
    RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from blog.models import Category, Post, Comment
from blog.permission import PostOwnerPermission, CommentOwnerPermission
from blog.serializers import CategorySerializer, PostListSerializer, PostDetailSerializer, CommentDetailSerializer, \
    CommentWriteSerializer, PostWriteSerializer
from utils.views import StandardResultsSetPagination


class CategoryListView(ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class PostListView(ListAPIView):
    pagination_class = StandardResultsSetPagination
    queryset = Post.objects.published()
    serializer_class = PostListSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['author', 'categories__title']
    search_fields = ['title', 'description', 'categories__title', '=author__username']


class PostDetailView(RetrieveAPIView):
    queryset = Post.objects.published()
    serializer_class = PostDetailSerializer


class UserPostViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated, PostOwnerPermission)
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status', 'categories__title']
    search_fields = ['title', 'description', 'categories__title']
    write_serializer_class = PostWriteSerializer
    read_serializer_class = PostDetailSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return PostListSerializer
        if self.action == 'retrieve':
            return self.read_serializer_class

    def get_queryset(self):
        return Post.objects.for_user(self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.write_serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(self.read_serializer_class(instance=instance).data, status=status.HTTP_201_CREATED,
                        headers=headers)

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.write_serializer_class(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(self.read_serializer_class(instance=instance).data)


class CommentCreateView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Comment.objects.all()
    serializer_class = CommentWriteSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentView(RetrieveUpdateAPIView):
    permission_classes = (CommentOwnerPermission, )
    queryset = Comment.objects.all()
    serializer_class = CommentDetailSerializer


class PostLike(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get_object(pk):
        return get_object_or_404(Post, pk=pk)

    def post(self, request, pk):
        post = self.get_object(pk)
        post.likes.add(request.user)
        return Response(status=status.HTTP_200_OK)

    def delete(self, request, pk):
        post = self.get_object(pk)
        post.likes.remove(request.user)
        return Response(status=status.HTTP_200_OK)
