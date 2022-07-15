from django.urls import path

from .views import *
urlpatterns = [
    path("",Home.as_view(),name="home"),
    path("home",Home.as_view(),name="home"),
    path("preform",Pre_Form.as_view(),name="preform"),
    path("Myforms",Myforms.as_view(),name="Myforms"),
    path("Createform/<str:form_id>",Createform.as_view(),name="createform"),
    path("Response/<str:form_id>",Respond.as_view(),name="respond"),
    path("Download/<str:form_id>",Download.as_view(),name="download"),
    path("edit/<str:form_id>",Edit.as_view(),name="edit"),
    path("editquestions/<str:form_id>/",Edit_Questions.as_view(),name="editquestions"),
]
