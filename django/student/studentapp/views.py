from django.shortcuts import render, redirect
from.models import AiClass, AiStudents

ERROR


# Create your views here.
def home(request):
    class_object = AiClass.objects.all()
   
    context = {
        'class_object' : class_object
        }

    return render(request, 'home.html', context)

def detail(request, class_pk):
    print(class_pk)

    class_obj = AiClass.objects.get(pk=class_pk)
    student_obj = AiStudents.objects.filter(class_num=class_pk)

    context = {
        'class_pk': class_pk,
        'class_obj': class_obj,
        'student_obj': student_obj
    }

    return render(request, 'detail.html', context)

def add(request, class_pk):

    class_obj = AiClass.objects.get(pk=class_pk)

    if request.method == 'POST':
        AiStudents.objects.create(
            class_num = class_pk,
            name = request.POST['name'],
            phone_num = request.POST['phone_num'],
            intro_text = request.POST['intro_text']
        )
        return redirect('datail', class_pk)
    
    context = {
        'class_obj' : class_obj
    }

    return render(request, 'add.html', context)

def edit(request, student_pk):
    if request.method == 'POST':

        AiStudents.object.filter(pk=student_pk).update(
            name = request.POST['name'],
            class_num = request.POST['class_num'],
            phone_num = request.POST['phone_num'],
            intro = request.POST['intro_text']
        )

        return redirect('student', student_pk)
    
    student = AiStudents.object.get(pk=student_pk)

    context = {
        'student' : student
    }

    return render(request, 'edit.html', context)

def student(request):
    return render(request, 'render.html')

def delete(request, class_num, student_pk):
    target_student = AiStudents.object.get(pk=student_pk)
    target_student.delete()

    class_pk = class_num

    return redirect('detail', class_pk)

