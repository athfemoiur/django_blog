from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

User = get_user_model()


class UserLightSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True, write_only=True)
    confirm_password = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'confirm_password', 'first_name', 'last_name',)

    @staticmethod
    def clean_validated_data(validated_data):
        validated_data.pop('confirm_password')
        return validated_data

    def validate(self, attrs):
        validate_password(attrs.get('password'))

        if attrs.get('password') != attrs.get('confirm_password'):
            raise serializers.ValidationError('password and confirm password are not equal!')

        return attrs

    def create(self, validated_data):
        user = self.Meta.model.objects.create_user(**self.clean_validated_data(validated_data))
        return user

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret.update(instance.serialize_jwt_pair_tokens())
        return ret


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'avatar')


class UserInfoUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'avatar')


class UserChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)
    confirm_password = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = ('old_password', 'new_password', 'confirm_password')

    def validate(self, attrs):
        validate_password(attrs.get('new_password'))
        if attrs.get('new_password') != attrs.get('confirm_password'):
            raise serializers.ValidationError('password and confirm password are not equal!')

        return attrs

    def update(self, instance, validated_data):
        if instance.check_password(validated_data.get('old_password')):
            instance.set_password(validated_data.get('new_password'))
            instance.save()
            return instance
        else:
            raise serializers.ValidationError('old password is not correct!')
