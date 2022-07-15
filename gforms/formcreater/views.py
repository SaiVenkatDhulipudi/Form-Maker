from tkinter.tix import Form
from urllib import response
from django.http import FileResponse, HttpResponse, JsonResponse,HttpResponseRedirect

from django.shortcuts import render,redirect
from xlwt import Workbook
from .models import *
import random, string
from django.views.generic import TemplateView,CreateView,ListView


#for Home page
class Home(TemplateView):
    template_name= "index.html"

#Rendering Forms for the user  
class Myforms(ListView):
    template_name= "forms.html"
    model=Forms
    
class Respond(CreateView):
    template_name="formrespond.html"

    def get_context_data(self, **kwargs):
        self.form_id=self.kwargs["form_id"]
        instance=Forms.objects.filter(form_id=self.form_id).exists()
        if not instance:
            return {"message" :"Invalid Form"}

        #getting Form Data
        form_data=Forms.objects.filter(form_id=self.form_id).values()[0]
        questions=list(Question.objects.filter(form_id=self.form_id).values())
        for i in range(len(questions)):
            del questions[i]["form_id_id"]
            qid=questions[i]["question_id"]

            #for choice type questions
            if questions[i]["questionType"] in ["Multiple Choice","Checkbox","Linear scale","Drop-down"]:
                """
                Choices are stored in {"options": []} format
                """
                questions[i]['options']=list(Choice.objects.filter(question_id=qid).values()[0]["choices"]["options"])

            #for grid type questions
            elif questions[i]["questionType"] in ["Tick box grid","Mutiple-choice grid"]:
                """
                Grids have two feilds #rows and #columns
                {"rows": []}
                {"column": []}
                """
                questions[i]['row']=Grids.objects.filter(question_id=qid).values()[0]['row']['rows']
                questions[i]['column']=Grids.objects.filter(question_id=qid).values()[0]['column']['column']

        form_data["questions"]=questions
        return form_data
        
    def post(self,request,*args,**kwargs):
        x=Forms.objects.get(form_id=self.kwargs["form_id"])
        resp_id=''.join(random.choices(string.ascii_letters + string.digits, k=8))
        Response.objects.create(form_id=x,responseid=resp_id)
        inst=Response.objects.get(responseid=resp_id)
        for i in list(request.POST.keys())[1:]:
            inst2=Question.objects.get(question_id=i)
            answer=request.POST[i]
            Formresponses.objects.create(question_id=inst2,response_id=inst,response={"answer":answer})
        return HttpResponse("<h1>Thanks for responding</h1>")

    

class Createform(CreateView):
    template_name="CreateForm.html"

    model=Question
    fields="__all__"

    def post(self,request,*args,**kwargs):
        form_id=self.kwargs["form_id"]

        #adding for Linear Scale
        if "low" in request.POST:
            options=[i for i in range(int(request.POST["low"]),int(request.POST["high"])+1)]
            inst=Question.objects.get(question_id=request.session["qid"])
            Choice.objects.create(question_id=inst,choices={"options":options})
            del request.session["qid"]
            return render(request,"CreateForm.html")

        #adding options
        if "value1" in request.POST:
            options=[]
            for i in list(request.POST.values())[1:]:
                options.append(i)
            inst=Question.objects.get(question_id=request.session["qid"])
            Choice.objects.create(question_id=inst,choices={"options":options})
            del request.session["qid"]
            return render(request,"CreateForm.html")

        #for options
        if "optionno" in request.POST:
            return render(request,"addoptions.html",{"nos":[str(i) for i in range(1,int(request.POST["optionno"])+1)],"id":form_id}) 

        if "Typeofque" in request.POST:
            #generating unique 6 charactered Qid for the question
            qid=''.join(random.choices(string.ascii_letters + string.digits, k=6))
            question_title=request.POST['question']
            required=request.POST['required'] 
            QuestionType=request.POST["Typeofque"]
            inst=Forms.objects.get(form_id=form_id)
            Question.objects.create(form_id=inst,question_id=qid,question=question_title,questionType=QuestionType,required=required)

            #for text based questions
            if QuestionType in ["Short answer","Paragraph","date","time"]:
                return render(request,"CreateForm.html")
            
            if  QuestionType in ["Tick box grid","Mutiple-choice grid"]:
                inst=Question.objects.get(question_id=qid)
                """
                Grids have two feilds #rows and #columns
                {"rows": []}
                {"column": []}
                """
                Grids.objects.create(question_id=inst,row={"rows":[]},column={"column":[]})
                return render(request,"CreateForm.html")

            #for options input
            elif QuestionType in ["Multiple Choice","Checkbox","Linear scale","Drop-down"]:
                request.session["qid"]=qid
                if request.POST["Typeofque"]=="Linear scale":
                    #using status variable for rendering form for linear scale
                    return render(request,"addoptions.html",{"status":1})
                else:
                    return render(request,"options.html") 
        

#form for title and description
class Pre_Form(CreateView):
    template_name="preform.html"
    model=Forms
    fields="__all__"
    def post(self,request,*args,**kwargs):
        title=request.POST["ftitle"]
        description=request.POST["fdesc"]
        #generating unique 16 charactered Formid for the Form
        form_id = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        #saving the form
        Forms.objects.create(form_id=form_id,title=title,description=description)
        return redirect("Createform/{}".format(form_id))
  

    
#for downloading responses
class Download(ListView):
    def get(self,request,**kwargs):
        form_id=self.kwargs["form_id"]
        inst=Forms.objects.filter(form_id=form_id)

        #checking for if forms exists or not
        if not inst:
            return HttpResponse("no form exists")

        #creating a sheet to store responses
        wb = Workbook()
        sheet1 = wb.add_sheet('Sheet1')
        questions=Question.objects.filter(form_id=form_id)
        if not questions:
            return HttpResponse("no questions exists") 
        
        #checking for if the forms have responses
        resps=Response.objects.filter(form_id=form_id)
        if not resps:
            return HttpResponse("no responses found")
        resps=[response["responseid"] for response in resps.values("responseid")]
        
        #getting questions
        questions=list(questions.values())
        ques_data=dict()
        column=0

        #writing questions on top of the sheet
        for ques in questions:
            ques_data[ques["question_id"]]=[column,ques["question"]]
            sheet1.write(0,column,ques['question'])
            column+=1
        row=1
        #writing answers to the sheet
        """
        answers are stored in this json format
        {"answer": "3"}
        """
        for resp_id in resps:
            answers=list(Formresponses.objects.filter(response_id=resp_id).values())
            for answer in answers:
                column=ques_data[answer["question_id_id"]][0]
                sheet1.write(row,column,answer["response"]["answer"])
            row+=1
        
        #saving sheet with form_id as name
        path='static/files/{}.xls'.format(form_id)
        wb.save(path)
        x=open(path, 'rb')
        return FileResponse(x)





#edit option page with add questions and delete questions
class Edit(TemplateView):
    template_name="edit.html"
    def get_context_data(self, *args, **kwargs):
        return self.kwargs

#delete questions
class Edit_Questions(TemplateView):
    template_name="editquestions.html"
    model=Question
    def get_context_data(self, *args, **kwargs):
        context=dict()
        form_id=(self.kwargs["form_id"])
        context['response']=Question.objects.filter(form_id=form_id)
        if  len(context["response"])==0:
            return ({'message':"no questions added"})
        return context

    #deleting questions
    """
    using form for deleting questions
    """
    def post(self,request,*args, **kwargs):
        ques=Question.objects.get(question_id=request.POST["qno"])
        ques.delete()
        return  HttpResponseRedirect(self.request.path_info)
        
        
    

