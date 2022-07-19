from rest_framework import serializers
from .models import Question,Forms,Choice,Grids,Response,Formresponses

class Choice_Serializer(serializers.ModelSerializer):
    class Meta:
        model=Choice
        fields="__all__"
        fields=["choices"]

class Grids_Serializer(serializers.ModelSerializer):
    class Meta:
        model=Grids
        fields=["row","column"]
        

class Question_Serializer(serializers.ModelSerializer):
    choices=Choice_Serializer(many=True,read_only=True)
    grids=Grids_Serializer(many=True,read_only=True)
    class Meta:
        model=Question
        fields=["question_id","question","questionType","required","is_deleted","choices","grids"]

class Form_Serializer(serializers.ModelSerializer):
    questions=Question_Serializer(many=True,read_only=True)
    class Meta:
        model=Forms
        fields=["form_id","title","description","questions"]

class Form_Responses_Serializer(serializers.ModelSerializer):
    class Meta:
        model=Formresponses
        fields=["question_id","response"]

class Response_Serializer(serializers.ModelSerializer):
    form_responses=Form_Responses_Serializer(many=True)
    class Meta:
        model=Response
        fields=["form_responses"]
class ResponseForm_Serializer(serializers.ModelSerializer):
    responses=Response_Serializer(many=True)
    class Meta:
        model=Forms
        fields=["responses"]
