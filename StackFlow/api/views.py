from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets
from .serializers import *
from rest_framework import permissions
from rest_framework import authentication
from .models import *
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework_simplejwt.authentication import JWTAuthentication
# Create your views here.


class UserView(viewsets.ViewSet):
    
    def create(self,request):
        ser=UserSer(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(data=ser.data)
        return Response(data=ser.errors)
    

class QuestionView(viewsets.ModelViewSet):
    serializer_class=QuestionSer
    queryset=Question.objects.all()
    # authentication_classes=[authentication.TokenAuthentication]
    authentication_classes=[JWTAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        ser=QuestionSer(data=request.data)
        if ser.is_valid():
            ser.save(user=request.user)
            return Response(data=ser.data)
        return Response(data=ser.errors)
    
    # def get_queryset(self):
   #     return Question.objects.all().exclude(user=self.request.user)

    @action(methods=['POST'],detail=True)
    def add_answer(self,request,*args,**kwargs):
        qid=kwargs.get('pk')
        ques=Question.objects.get(id=qid)
        user=request.user
        ser=AnswerSer(data=request.data)
        if ser.is_valid():
            ser.save(question=ques,user=user)
            return Response(data=ser.data)
        return Response(data=ser.errors)


class AnswerView(viewsets.ModelViewSet):
    serializer_class=AnswerSer
    queryset=Answer.objects.all()
    # authentication_classes=[authentication.TokenAuthentication]
    authentication_classes=[JWTAuthentication]
    permission_classes=[permissions.IsAuthenticated]


    def create(self, request, *args, **kwargs):
        raise serializers.ValidationError("invalid request")
    def list(self, request, *args, **kwargs):
        raise serializers.ValidationError('Invalid Error')
    def destroy(self, request, *args, **kwargs):
        aid=kwargs.get('pk')
        ans=Answer.objects.get(id=aid)
        if ans.user==request.user:
            ans.delete()
            return Response({'msg':'OK'})
        else:
            return Response({'msg':'Request not acceptable'})
    @action(methods=["POST"],detail=True) 
    def add_upvote(self,request,*args,**kwargs):
        aid=kwargs.get('pk')
        ans=Answer.objects.get(id=aid)
        user=request.user
        ans.upvote.add(user)
        return Response({'msg':'Upvotted'})