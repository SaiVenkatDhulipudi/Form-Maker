from collections import defaultdict
from django.http import FileResponse, HttpResponse, JsonResponse,HttpResponseRedirect
from django.shortcuts import render,redirect
from xlwt import Workbook
from .models import *
import random, string
from django.views.generic import TemplateView,CreateView,ListView
from django.views import View
from .serializers import Form_Serializer,Question_Serializer,Response_Serializer
from rest_framework.renderers import JSONRenderer
from rest_framework import viewsets
from .serializers import *
from .models import *
import requests