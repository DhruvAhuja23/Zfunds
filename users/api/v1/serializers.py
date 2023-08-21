from rest_framework import serializers
from users.models import User, Client
from home.utils import RolesEnum


class AdvisorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'name', 'mobile', 'role']
        read_only_fields = ('role',)

    def create(self, validated_data):
        username = self.generate_unique_username(validated_data['name'])
        user = User.objects.create(username=username, **validated_data)
        return user

    @staticmethod
    def generate_unique_username(name):
        base_username = name.lower().replace(' ', '_')
        username = base_username
        number = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{number}"
            number += 1
        return username


class SignupSerializer(UserSerializer):
    otp = serializers.CharField(max_length=6, write_only=True)

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ['otp']

    def create(self, validated_data):
        otp = validated_data.pop('otp')
        # TODO: Here we can check and validate the OTP
        # we can user 3rd party API integration or redis/db for otp verification flow
        advisor = super().create(validated_data)
        return advisor


class ClientSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=50, required=True)
    mobile = serializers.CharField(max_length=15, required=True)

    class Meta:
        model = Client
        fields = '__all__'
        read_only_fields = ('advisor', 'client')

    def create(self, validated_data):
        advisor = self.context['request'].user
        validated_data['role'] = RolesEnum.USER.value
        validated_data['otp'] = RolesEnum.USER.value
        client_user_serializer = UserSerializer(data=validated_data)
        client_user_serializer.is_valid(raise_exception=True)
        client_user = client_user_serializer.save(role=RolesEnum.USER.value)
        client = Client.objects.create(advisor=advisor, client=client_user)

        return client
