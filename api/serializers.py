from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from .models import Comment, Follow, Group, Post, User


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    text = serializers.CharField(required=True)

    class Meta:
        model = Post
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = ('id', 'pub_date', 'author')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'author', 'post', 'text', 'created')
        read_only_fields = ('id', 'author', 'created')


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'title')
        read_only_fields = ('id',)


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)
    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    def validate(self, data):
        user = get_object_or_404(User, username=data['following'].username)
        follow = Follow.objects.filter(
            user=self.context['request'].user,
            following=user
        ).exists()

        if user == self.context['request'].user:
            raise serializers.ValidationError(
                'Попытка подписаться на самого себя.')
        if follow:
            raise serializers.ValidationError(
                'Подписка уже существует.')
        return data

    class Meta:
        fields = ('user', 'following')
        model = Follow
