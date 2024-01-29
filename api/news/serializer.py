from rest_framework.serializers import ModelSerializer
from .models import News
from api.accounts.models import User
from rest_framework import serializers


class NewsCreateSerializer(ModelSerializer):
    
    class Meta:
        model = News
        fields = ('title','author')
        
        
# User = get_user_model()

# class UserProfileChangeSerializer(ModelSerializer):
#     username = serializers.CharField(required=False, allow_blank=True, initial="current username")
#     class Meta:
#         model = User
#         fields = [
#             'username',
#             'password',
#         ]

#     def update(self, instance, validated_data):
#         instance.username = validated_data.get('username',instance.username)
#         print('instance of username',instance.username)
#         return instance 
        