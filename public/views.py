

from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from main.models import Subject, Course, Category
from public.forms import NotesForm, QueryForm, TaskUploadForm, VideoForm
from public.models import Classroom, Expert, ExpertDocument, Queries, Student, LoginT, StudentRequest ,Notes, Task, Video
from django.db.models import Q
import datetime



def index(request):
    return render(request,'index.html')

def expert_register(request):
    sub= Subject.objects.all()
    
    context = {
        'sub' : sub
    }
    if request.method=='POST':
        expert= Expert()
        doc = ExpertDocument()
        expert.name = request.POST.get('expname')
        expert.gender = request.POST.get('gender')
        expert.dob = request.POST.get('dob')
        expert.qualification = request.POST.get('qual')
        expert.experience = request.POST.get('exp')
        subject = request.POST.get('sub')
        expert.subject = Subject.objects.get(id=subject)
        expert.phone = request.POST.get('phone')
        expert.email = request.POST.get('email')
        expert.details= request.POST.get('desc')
        expert.status='W'
        expert.save()
        doc.document_name = request.POST.get('docname')
        doc.file = request.FILES.get('docfile')
        doc.expert=expert
        doc.details = request.POST.get('docdesc')
        doc.save()
        return redirect('index')
    return render(request,'expertregister.html',context)

def student_register(request):
    cat = Category.objects.all()
    cou = Course.objects.all()
    context ={
        'cat' : cat,
        'cou' : cou
    }
    if request.method == 'POST':
        student = Student()
        log= LoginT()
        student.name= request.POST.get('name')
        student.phone = request.POST.get('phone')
        email = request.POST.get('email')
        student.email=email
        category =  request.POST.get('cat')
        print(category)
        student.category = Category.objects.get(name=category)
        course = request.POST.get('cou')
        student.course = Course.objects.get(id=course)
        print(course)

        qs = LoginT.objects.filter(username__iexact=email)
        if qs.exists():
            messages.error(request, 'email already exists try another email')
            return redirect('student-register')
        student.save()
        log.username = request.POST.get('email')
        password1 = request.POST.get('password')
        password2 = request.POST.get('password1')
        if password1 == password2 :
            log.password= password1
            log.type = 'S'
            log.save()
            return redirect('index')
        else:
            messages.error(request, 'Passwords does not match')
            return redirect('student-register')

    return render(request,'studentregister.html',context)

def login_page(request):  

    if request.method=='POST':
        uname=request.POST.get('username')
        paword=request.POST.get('password')
        print(uname)
        print(paword)
        data=LoginT.objects.all()
        flag=0

        for da in data:
            if uname==da.username and paword==da.password:
                type=da.type
                flag=1
                if type=="A":
                    request.session['adm']=uname
                    return redirect("admin-home")
                elif type=="E":
                    request.session['exp']=uname
                    return redirect("expert-home")
                elif type=="S":
                    request.session['std']=uname
                    return redirect("student-home")
                else:
                    return HttpResponse("Invalid Category")
        if flag==0:
            return HttpResponse("Invalid User")
    return render(request,'login.html')


def logout_admin(request):
    del request.session['adm']
    return redirect('index')

def logout_expert(request):
    del request.session['exp']
    return redirect('index')

def logout_student(request):
    del request.session['std']
    return redirect('index')




def student_home(request):
    if 'std' not in request.session:
        return redirect('login')
    student_email =request.session['std']
    print(student_email)
    student = Student.objects.get(email=student_email)
    print(student)
    subjects = Subject.objects.filter(course=student.course)
    print(subjects)
    context = {
        'subjects':subjects
    }
    return render (request, 'studenthome.html',context)

def subject_experts(request,pk):
    if 'std' not in request.session:
        return redirect('login')
    student_email =request.session['std']
    student = Student.objects.get(email=student_email)
    c1 = Q(subject=pk)
    c2 = Q(status='A')
    experts = Expert.objects.filter(c1 & c2)
    sreq= StudentRequest.objects.filter(student=student)
    print(experts)
    context ={
        'experts' : experts,
        'sreq' : sreq
    }

    return render(request,'subjectexperts.html',context)

def student_expert_request(request,pk):
    if 'std' not in request.session:
        return redirect('login')
    student_email =request.session['std']
    student = Student.objects.get(email=student_email)
    expert = Expert.objects.get(id=pk)
    student_request = StudentRequest()
    qs = StudentRequest.objects.filter(expert=expert,student=student)
    if qs.exists():
        return HttpResponse("Request Already Exists")
    student_request.student = student
    student_request.expert = expert
    student_request.req_date = datetime.datetime.now()
    student_request.status = 'W'
    student_request.save()
    return redirect('student-home')


def expert_home(request):
    if 'exp' not in request.session:
        return redirect('login')
    expert_email = request.session['exp']
    expert = Expert.objects.get(email=expert_email)
    qs=Classroom.objects.filter(expert=expert)

    sreq = StudentRequest.objects.filter(expert=expert)
    print(sreq)
    for s in sreq:
        for q in qs:
            if s.student == q.student:
               sreq = sreq.exclude(id=s.id)
    context = {
        'sreq' : sreq
    }
    return render(request, 'experthome.html',context)

def create_classroom(request,pk):
    if 'exp' not in request.session:
        return redirect('login')
    expert_email = request.session['exp']
    expert = Expert.objects.get(email=expert_email)
    student=Student.objects.get(id=pk)
    qs=Classroom.objects.filter(expert=expert,student=student)
    if qs.exists():
        return HttpResponse("Classroom Already exists")
    classroom = Classroom()
    classroom.student=student
    classroom.expert=expert
    classroom.save()
    return redirect('expert-home')

def expert_classrooms(request):
    if 'exp' not in request.session:
        return redirect('login')
    expert_email = request.session['exp']
    expert = Expert.objects.get(email=expert_email)
    classroom= Classroom.objects.filter(expert=expert)
    context = {
        'classroom': classroom
    }
    return render(request,'expertclassrooms.html',context)

def expert_classroom(request,pk):
    if 'exp' not in request.session:
        return redirect('login')
    expert_email = request.session['exp']
    expert = Expert.objects.get(email=expert_email)
    classroom = Classroom.objects.get(id=pk)
    context = {
        'classroom' : classroom
    }
    return render(request,'expertclassroom.html',context)


def upload_notes(request,pk):
    if 'exp' not in request.session:
        return redirect('login')
    classroom = Classroom.objects.get(id=pk)
    form = NotesForm
    if request.method=='POST':
        form = NotesForm(request.POST ,request.FILES)
        if form.is_valid():
            note=form.save(commit=False)
            note.classroom=classroom
            note.save()
            return redirect('expert-classroom' , pk=classroom.id)
        else:
            return HttpResponse(form.errors.values())

    context={
        'form': form
    }
    return render(request,'notesuploadform.html',context)

def upload_videos(request,pk):
    if 'exp' not in request.session:
        return redirect('login')
    classroom = Classroom.objects.get(id=pk)
    form = VideoForm
    if request.method=='POST':
        form = VideoForm(request.POST ,request.FILES)
        if form.is_valid():
            video=form.save(commit=False)
            video.classroom=classroom
            video.save()
            return redirect('expert-classroom' , pk=classroom.id)
        else:
            return HttpResponse(form.errors.values())

    context={
        'form': form
    }
    return render(request,'videouploadform.html',context)


def upload_tasks(request,pk):
    if 'exp' not in request.session:
        return redirect('login')
    classroom = Classroom.objects.get(id=pk)
    form = TaskUploadForm
    if request.method=='POST':
        form = TaskUploadForm(request.POST ,request.FILES)
        if form.is_valid():
            task=form.save(commit=False)
            task.classroom=classroom
            task.save()
            return redirect('expert-classroom' , pk=classroom.id)
        else:
            return HttpResponse(form.errors.values())

    context={
        'form': form
    }
    return render(request,'taskuploadform.html',context)



def view_queries(request,pk):
    if 'exp' not in request.session:
        return redirect('login')
    clas = Classroom.objects.get(id=pk)
    queries = Queries.objects.filter(classroom=clas).filter(status='W')
    context ={
        'queries' : queries
    }
    return render(request,'viewqueries.html',context)

def student_classrooms(request):
    if 'std' not in request.session:
        return redirect('login')
    student_email =request.session['std']
    student = Student.objects.get(email=student_email)
    classroom= Classroom.objects.filter(student=student)
    context = {
        'classroom': classroom
    }
    return render(request,'studentclassrooms.html',context)


def student_classroom(request,pk):
    if 'std' not in request.session:
        return redirect('login')
    student_email = request.session['std']
    student = Student.objects.get(email=student_email)
    classroom = Classroom.objects.get(id=pk)
    context = {
        'classroom' : classroom
    }
    return render(request,'studentclassroom.html',context)

def view_notes(request,pk):
    if 'std' not in request.session:
        return redirect('login')
    classroom = Classroom.objects.get(id=pk)
    notes =Notes.objects.filter(classroom=classroom)
    context ={
        'notes':notes
    }
    return render(request,'viewnotes.html',context)

def view_videos(request,pk):
    if 'std' not in request.session:
        return redirect('login')
    classroom = Classroom.objects.get(id=pk)
    video =Video.objects.filter(classroom=classroom)
    context ={
        'video': video
    }
    return render(request,'viewvideos.html',context)

def view_tasks(request,pk):
    if 'std' not in request.session:
        return redirect('login')
   
    classroom = Classroom.objects.get(id=pk)
    tasks =Task.objects.filter(classroom=classroom)
    print(tasks)
    context ={
        'tasks': tasks
    }
    return render(request,'viewtasks.html',context)

def upload_answer(request,pk):
    if 'std' not in request.session:
        return redirect('login')
    task = Task.objects.get(id=pk)
    if request.method=='POST':
        task.answer_file = request.FILES.get('answer')
        task.save()
        return redirect('student-classroom' , pk=task.classroom.id)
    return render(request,'uploadanswer.html')

def make_query(request,pk):
    if 'std' not in request.session:
        return redirect('login')
    classroom = Classroom.objects.get(id=pk)
    form = QueryForm
    context ={
        'form' : form
    }
    if request.method=='POST':
        form = QueryForm(request.POST)
        if form.is_valid():
            query=form.save(commit=False)
            query.classroom=classroom
            query.save()
            return redirect('student-classroom' , pk=classroom.id)
    return render (request,'makequery.html',context)