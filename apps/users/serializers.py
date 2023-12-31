from django.contrib.auth import get_user_model
from django_countries.serializer_fields import CountryField
from djoser.serializers import UserCreateSerializer
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    gender = serializers.CharField(source='profile.gender') # достаем gender из модели profile.gender
    phone_number = PhoneNumberField(source="profile.phone_number")
    profile_photo = serializers.ImageField(source="profile.profile_photo")
    country = CountryField(source="profile.country")
    top_seller = serializers.BooleanField(source="profile.top_seller")
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField(source='get_full_name')

    class Meta:
        model = User #  указывает, что эта форма связана с моделью User.
        fields=['id','username','email','first_name',"last_name",'full_name','gender','phone_number','profile_photo','country','city','top_seller'] # определяет, какие поля будут отображаться в ответе.

    def get_first_name(self, obj):
        return obj.first_name.title() # title() используются для преобразования имени и фамилии в формат с заглавной буквы.
    
    def get_last_name(self, obj):
        return obj.last_name.title()
    

    '''
    Этот метод переопределяет стандартный метод to_representation и добавляет дополнительное
    поле "admin" в сериализованные данные, если пользователь является суперпользователем.
    '''
    def to_representation(self, instance):
        representation = super(UserSerializer, self).to_representation(instance)
        if instance.is_superuser:
            representation["admin"] = True
        return representation
    
class CreateUserSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ['id','username','email','first_name','last_name','password'] # поля которые возвращаются в ответе

    