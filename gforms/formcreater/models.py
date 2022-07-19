from django.core.exceptions import ValidationError
from django.db import models

class Forms(models.Model):
    form_id=models.CharField(primary_key=True,max_length=16)
    title=models.CharField(max_length=20,null=False)
    description=models.CharField(max_length=200,default='')
    def __str__(self):
        return str(self.form_id)
class Question(models.Model):
    choices=(
    ("Short answer","Short answer"),
    ("Paragraph","Paragraph"),
    ("Multiple Choice","Multiple Choice"),
    ("Checkbox","Checkbox"),
    ("Drop-down","Drop-down"),
    ("Linear scale","Linear scale"),
    ("Tick box grid","Tick box grid"),
    ("Mutiple-choice grid","Mutiple-choice grid"),
    ("Date","Date"),
    ("time","time")
    )
    form_id= models.ForeignKey(Forms, on_delete=models.CASCADE,related_name="questions")
    question_id= models.CharField(primary_key=True,max_length=6)
    question=models.CharField(max_length=200,null=False )
    questionType=models.CharField(max_length=20,choices=choices)
    required=models.CharField(max_length=20,choices=(("required","True"),(" ","False")))
    is_deleted=models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.question_id)

class Choice(models.Model):
    question_id=models.ForeignKey(Question, on_delete=models.CASCADE,related_name="choices")
    choices=models.CharField(max_length=30,null=True,blank=True,default=None)
    def __str__(self):
        return str(self.question_id)

class Grids(models.Model):
    question_id=models.ForeignKey(Question, on_delete=models.CASCADE,related_name="grids")
    row=models.CharField(max_length=30)
    column=models.CharField(max_length=30)
    def __str__(self):
        return str(self.question_id)

class Response(models.Model):
    form_id= models.ForeignKey(Forms, on_delete=models.CASCADE,related_name="responses")
    response_id= models.CharField(primary_key=True,max_length=8)
    def __str__(self):
        return str(self.response_id)

class Formresponses(models.Model):
    response_id=models.ForeignKey(Response, on_delete=models.CASCADE,related_name="form_responses")
    question_id=models.ForeignKey(Question, on_delete=models.CASCADE)
    response=models.CharField(max_length=30)
    def __str__(self):
        return str(self.response_id)


