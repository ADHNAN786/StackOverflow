from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *

class UserSer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['username','password','email']
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)





class AnswerSer(serializers.ModelSerializer):
    user=serializers.CharField(read_only=True)
    date=serializers.DateField(read_only=True)
    question=serializers.CharField(read_only=True)
    upvote=serializers.CharField(read_only=True)
    upvote_count=serializers.IntegerField(read_only=True)

    class Meta:
        model=Answer
        fields='__all__'


class QuestionSer(serializers.ModelSerializer):
    user=serializers.CharField(read_only=True)
    date=serializers.DateField(read_only=True)
    question_answer=AnswerSer(read_only=True,many=True)
    class Meta:
        model=Question
        fields='__all__'