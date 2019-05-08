from django.contrib.auth.models import User, Group
from rest_framework import serializers
from explomail.models import Mail, Client


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class MailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mail
        fields = ('id', 'sender', 'receiver', 'date', 'chronological_order', 'subject', 
        	'text', 'client', 'client_code', 'study', 'data_set')

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('id', 'name')
# class MailSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     sender = serializers.CharField(required=True)
#     receiver = serializers.CharField(required=True)
#     date = serializers.DateField(required=True)
#     text = serializers.CharField(required=True)

#     def create(self, validated_data):
#         """
#         Create and return a new `Snippet` instance, given the validated data.
#         """
#         return Mail.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         """
#         Update and return an existing `Snippet` instance, given the validated data.
#         """
#         instance.sender = validated_data.get('sender', instance.sender)
#         instance.receiver = validated_data.get('receiver', instance.receiver)
#         instance.date = validated_data.get('date', instance.date)
#         instance.text = validated_data.get('text', instance.text)
#         instance.save()
#         return instance