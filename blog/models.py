from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models, IntegrityError

from utils.models import BaseModel

User = get_user_model()


class Category(BaseModel):
    title = models.CharField(max_length=32)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.title


class PostManager(models.Manager):

    def published(self):
        return self.get_queryset().filter(status=self.model.PUBLISHED)

    def for_user(self, user):
        return self.get_queryset().filter(author=user)

    def published_for_user(self, user):
        return self.get_queryset().filter(status=Post.PUBLISHED, author=user)


class Post(BaseModel):
    DRAFT = 0
    ARCHIVED = 1
    PUBLISHED = 2
    STATUS_CHOICES = (
        (DRAFT, 'draft'),
        (ARCHIVED, 'archived'),
        (PUBLISHED, 'published')
    )

    title = models.CharField(max_length=64)
    description = models.TextField()
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=DRAFT)
    author = models.ForeignKey(User, related_name='posts', on_delete=models.SET_NULL, null=True)
    categories = models.ManyToManyField(Category, blank=True)
    likes = models.ManyToManyField(User, blank=True)
    image = models.ImageField(upload_to='post/images', null=True, blank=True)

    objects = PostManager()

    class Meta:
        ordering = ['-modified_at']

    def __str__(self):
        return f'{self.title} ({self.get_status_display()})'

    @property
    def like_count(self):
        return self.likes.all().count()

    @property
    def likes_users(self):
        return self.likes.all().values_list('user', flat=True)


class CommentManager(models.Manager):

    def root(self):
        return self.get_queryset().filter(reply_to__isnull=True)


class Comment(BaseModel):
    user = models.ForeignKey(User, related_name='comments', on_delete=models.SET_NULL, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    title = models.CharField(max_length=30)
    caption = models.TextField()
    reply_to = models.ForeignKey('self', related_name='replies', on_delete=models.CASCADE, null=True, blank=True
                                 )

    objects = CommentManager()

    def __str__(self):
        return f'{self.user} -> {self.post}'

    def save(self, *args, **kwargs):
        if self.reply_to and self.reply_to.reply_to is not None:
            raise IntegrityError('Can not add a reply for a comment which is a reply itself')
        super().save(*args, **kwargs)

    def replies_count(self):
        return self.replies.all().count()


class SocialMedia(BaseModel):
    title = models.CharField(max_length=64)
    text = models.TextField(blank=True)
    link = models.URLField()
    color = models.CharField(max_length=32)
    icon_id = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])

    def __str__(self):
        return self.title
