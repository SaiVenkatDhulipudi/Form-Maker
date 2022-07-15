from django.db import models

class Forms(models.Model):
    Formid=models.CharField(primary_key=True,max_length=16)
    title=models.CharField(max_length=20,null=False,default='')
    description=models.CharField(max_length=200,default='')
    def __str__(self):
        return str(self.Formid)

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
    formid= models.ForeignKey(Forms, on_delete=models.CASCADE)
    Qid= models.CharField(primary_key=True,max_length=6)
    question=models.CharField(max_length=200,null=False)
    Type=models.CharField(max_length=20,choices=choices)
    required=models.CharField(max_length=20,choices=(("required","True"),(" ","False")))
    def __str__(self):
        return str(self.Qid)

class Choice(models.Model):
    Qid= models.ForeignKey(Question, on_delete=models.CASCADE)
    choices=models.JSONField()

class Grids(models.Model):
    Qid= models.ForeignKey(Question, on_delete=models.CASCADE)
    row=models.JSONField()
    column=models.JSONField()
    
class Response(models.Model):
    formid= models.ForeignKey(Forms, on_delete=models.CASCADE)
    responseid= models.CharField(primary_key=True,max_length=8)

class Formresponses(models.Model):
    responseid=models.ForeignKey(Response, on_delete=models.CASCADE)
    qid=models.ForeignKey(Question, on_delete=models.CASCADE)
    response=models.JSONField()

# class TextAnswer(models.Model):
#     Qid=models.ForeignKey(Question,on_delete=models.CASCADE)
#     Answer=models.CharField(max_length=200,default='')
#     def __str__(self):
#         return str(self.Qid)
# class Datequestion(models.Model):
#     Qid=models.ForeignKey(Question,on_delete=models.CASCADE)
#     answer=models.DateField()

# class ChoiceQuestion(models.Model):
#     option=models.CharField(max_length=20,default='')

