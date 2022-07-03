

from django.shortcuts import render,redirect
import datetime
from . models import Category, Course, Subject
from public.models import Expert,ExpertDocument, LoginT, StudentRequest,Classroom
from django.db.models import Count

# Create your views here.


def admin_home(request):

    experts=Classroom.objects.values_list('expert').annotate(exp_count=Count('expert')).order_by('-exp_count')
    print(experts)
    for exp in experts:
        pass
    
    

    return render(request,'adminhome.html')


def add_category(request):

    if request.method=='POST':
        category=Category()
        category.name = request.POST.get('catname')
        category.description = request.POST.get('catdesc')
        category.save()
        return redirect('admin-home')





    return render(request,'addcategory.html')


def view_category(request):
    data = Category.objects.all()
    context = {
        'data': data
    }

    return render(request,'categorylist.html',context)

def remove_category(request,pk):
    cat=Category.objects.get(id=pk)
    cat.delete()
    return redirect('admin-home')


def add_course(request):
    data = Category.objects.all()

    context={
        'data':data
    }

    if request.method=='POST':
        course=Course()
        course.name = request.POST.get('name')
        course.description = request.POST.get('desc')

        cat=request.POST.get('category')
        course.category=Category.objects.get(name=cat)
        course.save()
        return redirect('admin-home')

    return render(request,'addcourse.html',context)


def view_course(request):
    data = Course.objects.all()
    context = {
        'data': data
    }

    return render(request,'courselist.html',context)



def remove_course(request,pk):
    cat=Course.objects.get(id=pk)
    cat.delete()
    return redirect('admin-home')


def add_subject(request):
    data = Course.objects.all()

    context={
        'data':data
    }


    if request.method=='POST':
        subject=Subject()
        subject.name = request.POST.get('name')
        

        co=request.POST.get('course')
        subject.course=Course.objects.get(name=co)
        subject.save()
        return redirect('admin-home')

    return render(request,'addsubject.html',context)


def view_subjects(request):
    data = Subject.objects.all()
    context = {
        'data': data
    }

    return render(request,'subjectlist.html',context)



def remove_subject(request,pk):
    sub=Subject.objects.get(id=pk)
    sub.delete()
    return redirect('admin-home')


def expert_requests(request):
    exps = Expert.objects.all()
    docs = ExpertDocument.objects.all()
    
  
    context = {
        'exps':exps,
        'docs':docs
    }
    return render(request,'expertrequests.html',context)

def approve_expert(request,pk):
    exp=Expert.objects.get(id=pk)
    exp.status='A'
    log= LoginT()
    log.username=exp.email
    log.password=exp.phone
    log.type='E'
    log.save()
    exp.save()
    return redirect('expert-requests')

def reject_expert(request,pk):
    exp=Expert.objects.get(id=pk)
    exp.status='B'
    exp.save()
    return redirect('expert-requests')

def block_expert(request,pk):
    exp=Expert.objects.get(id=pk)
    exp.status= 'B'
    exp.save()
    return redirect('expert-requests')

def unblock_expert(request,pk):
    exp=Expert.objects.get(id=pk)
    exp.status= 'A'
    exp.save()
    return redirect('expert-requests')


def student_requests(request):
    sreq= StudentRequest.objects.all().filter(status='w')
    context = {
        'sreq' :sreq
    }
    return render(request,'studentrequests.html',context)

def approve_sreq(request,pk):
    sreq = StudentRequest.objects.get(id=pk)
    sreq.status='A'
    sreq.allot_date=datetime.datetime.now()
    sreq.save()
    return redirect('student-requests')
def reject_sreq(request,pk):
    sreq = StudentRequest.objects.get(id=pk)
    sreq.status='R'
    sreq.save()
    return redirect('student-requests')
