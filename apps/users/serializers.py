from rest_framework.validators import UniqueValidator
from rest_framework import serializers
from django.contrib.auth import get_user_model
from apps.users.models import UserProfile, UserWantJob
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("id", "username", "email")


class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='id', read_only=True)
    email = serializers.SerializerMethodField()
    education_name = serializers.SerializerMethodField()
    province = serializers.SerializerMethodField()
    city_name = serializers.SerializerMethodField()

    def get_email(self, obj):
        return obj.user.email

    def get_education_name(self, obj):
        return obj.education.name

    def get_city_name(self, obj):
        return obj.city.name

    def get_province(self, obj):
        return obj.city.province.id

    class Meta:
        model = UserProfile
        fields = "__all__"


class UserWantJobSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='id', read_only=True)
    industry_parent = serializers.SerializerMethodField()
    jobfunction_parent = serializers.SerializerMethodField()
    province = serializers.SerializerMethodField()
    industry_name = serializers.SerializerMethodField()
    jobfunction_name = serializers.SerializerMethodField()
    city_name = serializers.SerializerMethodField()

    def get_industry_parent(self, obj):
        return obj.want_industry.category.id

    def get_jobfunction_parent(self, obj):
        return obj.want_jobfunction.category.id

    def get_province(self, obj):
        return obj.want_city.province.id

    def get_industry_name(self, obj):
        return obj.want_industry.name

    def get_jobfunction_name(self, obj):
        return obj.want_jobfunction.name

    def get_city_name(self, obj):
        return obj.want_city.name

    class Meta:
        model = UserWantJob
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
