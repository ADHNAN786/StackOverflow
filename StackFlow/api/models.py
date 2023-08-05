from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class  Question(models.Model):
    title=models.CharField(max_length=100)
    description=models.CharField(max_length=100)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    image=models.ImageField(upload_to='question_image',null=True)
    date=models.DateField(auto_now_add=True)


    @property
    def question_answer(self):
        return self.answer_set.all()

class Answer(models.Model):
    answer=models.CharField(max_length=100)
    question=models.ForeignKey(Question,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    date=models.DateField(auto_now_add=True)
    upvote=models.ManyToManyField(User,related_name='upuser')



    @property
    def upvote_count(self):
        cnt=self.upvote.all().count()
        return cnt
    
