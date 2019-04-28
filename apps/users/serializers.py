from rest_framework.validators import UniqueValidator
from rest_framework import serializers
from django.contrib.auth import get_user_model
from apps.users.models import UserProfile
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    isSuperUser = serializers.SerializerMethodField()

    def get_isSuperUser(self, obj):
        return obj.is_superuser

    class Meta:
        model = User
        fields = ("id", "username", "email", 'isSuperUser')


class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='id', read_only=True)
    username = serializers.SerializerMethodField()

    def get_username(self, obj):
        return obj.user.username

    class Meta:
        model = UserProfile
        fields = "__all__"


class UserRegSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        label="用户名",
        help_text="用户名",
        required=True,
        allow_blank=False,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="用户已经存在")])
    email = serializers.EmailField(
        label="邮箱",
        help_text="邮箱",
        required=True,
        allow_blank=False,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="邮箱已被注册")])
    password = serializers.CharField(
        style={
            'input_type': 'password'},
        help_text="密码",
        label="密码",
        write_only=True,
    )

    class Meta:
        model = User
        fields = ("username", "email", "password")
