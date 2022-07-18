from collections import defaultdict
from django.http import FileResponse, HttpResponse, JsonResponse,HttpResponseRedirect
from django.shortcuts import render,redirect
from xlwt import Workbook
from .models import *
import random, string
from django.views.generic import TemplateView,CreateView,ListView,UpdateView
from django.views import View

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
        instance=Forms.objects.filter(form_id=self.form_id)
        if not instance:
            return {"message" :"Invalid Form"}
        
        #getting Form Data
        form_data=instance.values()[0]
        questions=list(Question.objects.filter(form_id=self.form_id,is_deleted=False).values("question_id","question","questionType","required"))
        for question in questions:
            qid=question["question_id"]

            #for choice type questions
            if question["questionType"] in ["Multiple Choice","Checkbox","Linear scale","Drop-down"]:
                """
                Choices are stored in {"options": []} format
                """
                question['options']=[options["choices"] for options in Choice.objects.filter(question_id=qid).values("choices")]

            #for grid type questions
            elif question["questionType"] in ["Tick box grid","Mutiple-choice grid"]:
                """
                Grids have two feilds #rows and #columns
                {"rows": []}
                {"column": []}
                """
                question['row']=[options["row"] for options in Grids.objects.filter(question_id=qid).values("row")]
                question['column']=[options["column"] for options in Grids.objects.filter(question_id=qid).values("column")]

        form_data["questions"]=questions
        print(form_data)
        return form_data
        
    def post(self,request,*args,**kwargs):
        form_instance=Forms.objects.get(form_id=self.kwargs["form_id"])
        resp_id=''.join(random.choices(string.ascii_letters + string.digits, k=8))
        Response.objects.create(form_id=form_instance,responseid=resp_id)
        inst=Response.objects.get(responseid=resp_id)
        for ques_id,answer in list(request.POST.items())[1:]:
            inst2=Question.objects.get(question_id=ques_id)
            if type(answer) is list:
                for value in answer:
                    Formresponses.objects.create(question_id=inst2,response_id=inst,response=value)
            else:
                Formresponses.objects.create(question_id=inst2,response_id=inst,response=answer)

        return HttpResponse("<h1>Thanks for responding</h1>")

    

class Createform(CreateView):
    template_name="CreateForm.html"

    model=Question
    fields="__all__"

    def post(self,request,*args,**kwargs):
        form_id=self.kwargs["form_id"]

        #adding for Linear Scale
        if "low" in request.POST:
            
            inst=Question.objects.get(question_id=request.session["qid"])

            for value in range(int(request.POST["low"]),int(request.POST["high"])+1):
                Choice.objects.create(question_id=inst,choices=value)
            del request.session["qid"]
            return render(request,"CreateForm.html")

        #adding options
        if "value1" in request.POST:
            inst=Question.objects.get(question_id=request.session["qid"])
            for option in list(request.POST.values())[1:]:
                Choice.objects.create(question_id=inst,choices=option)
                
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
                
                """
                Grids.objects.create(question_id=inst,row=" ",column=" ")
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
class Download(View):
    def get(self,request,**kwargs):
        form_id=self.kwargs["form_id"]
        inst=Forms.objects.filter(form_id=form_id)

        #checking for if the forms have responses
        resps=Response.objects.filter(form_id=form_id)
        if not resps:
            return HttpResponse("no responses found")
        resps=[response["responseid"] for response in resps.values("responseid")]
        
        #getting questions
        questions=Question.objects.filter(form_id=form_id)
        questions=list(questions.values())
        ques_data=dict()
        column=0

        #creating a sheet to store responses
        wb = Workbook()
        sheet1 = wb.add_sheet('responses')
        #writing questions on top of the sheet
        for ques in questions:
            ques_data[ques["question_id"]]=[column,ques["question"]]
            sheet1.write(0,column,ques['question'])
            column+=1
        row=1
        #writing answers to the sheet
        
        for resp_id in resps:
            answers=list(Formresponses.objects.filter(response_id=resp_id).values("question_id","response"))
            responses=defaultdict(lambda:[])
            for answer in answers:
                responses[answer["question_id"]].append(answer["response"])
            for question,answer in responses.items():
                column=ques_data[question][0]
                sheet1.write(row,column,','.join(answer))
                
            row+=1
        
        #saving sheet with form_id as name
        path='static/files/{}.xls'.format(form_id)
        wb.save(path)
        x=open(path, 'rb')
        return FileResponse(x)





#edit option page with add questions and delete questions
class Edit_Page(TemplateView):
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
        context['response']=Question.objects.filter(form_id=form_id,is_deleted=False)
        if  len(context["response"])==0:
            return ({'message':"no questions exists in this form"})
        return context

    #deleting questions
    """
    using form for deleting questions
    """
   
    def post(self,request,*args, **kwargs):
        ques=Question.objects.filter(question_id=request.POST["ques_id"]).update(is_deleted=True)
        return  HttpResponseRedirect(self.request.path_info)
