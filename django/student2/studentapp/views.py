from django.shortcuts import render, redirect
from.models import AiStudents, AiClass, StudentPost
from django.contrib.auth.models import User
from django.contrib import auth


# Create your views here.
def home(request):
    class_object = AiClass.objects.all()

    context = {
        'class_object' : class_object
    }

    return render(request, 'home.html', context)

def detail(request, class_pk):
    class_object = AiClass.objects.get(pk=class_pk)

    context = {
        'class_object' : class_object,
    }

    return render(request, 'detail.html', context)

def add(request, student_pk):
    student_object = AiStudents.objects.get(pk=student_pk)

    if request.method == 'POST':
        StudentPost.objects.create(
            intro_text = request.POST['intro_text'],
            writer = student_object
        )

        return redirect('detail', student_pk)

    return render(request, 'add.html')


def student(request, student_pk):
    student_object = AiStudents.objects.get(pk=student_pk)

    if request.method == 'POST':
        AiStudents.objects.get(pk=student_pk).delete()
        return redirect('detail', student_object.class_num)

    context = {
        'student_object' : student_object
    }

    return render(request, 'student.html', context)


def edit(request, student_pk):
    student_object = AiStudents.objects.get(pk=student_pk)

    if request.method == 'POST':
        AiStudents.objects.filter(pk=student_pk).update(
            name = request.POST['name'],
            phone_num = request.POST['phone_num'],
            # intro_text = request.POST['intro_text'],
        )
        return redirect('student', student_pk)
    
    context = {
        'student_object' : student_object
    }

    return render(request, 'edit.html', context)

# <-----------------------------------------------------------> 

ERROR_MSG = {
    'NOT_ID' : "아이디가 없습니다.",
    'NOT_PW' : "비밀번호가 틀렸습니다.",
    'DOUBLE_ID' : "중복된 아이디가 있습니다.",
    'NO INFO' : "빈칸을 채우세요"
}


def login(request):
    
    context = {
        'error' : {
            'state' : False,
            'msg' : ""
        }
    }
    if request.method == 'POST':
        user_id = request.POST['user_id']
        user_pw = request.POST['user_pw']

        if user_id or user_pw is not "": 
            user = User.objects.filter(username=user_id)

            if len(user) != 0:
                
                old_user = auth.authenticate(
                    username = user_id,
                    password = user_pw
                )
                    
                if old_user != None:
                    auth.login(request, old_user)

                    return redirect('home')
                else:
                    context['error']['state'] = True
                    context['error']['msg'] = ERROR_MSG['NOT_PW']
            else:
                context['error']['state'] = True
                context['error']['msg'] = ERROR_MSG['NOT_ID']
        else:
            context['error']['state'] = True
            context['error']['msg'] = ERROR_MSG['NO INFO']

    return render(request, 'login.html', context['error'])


def logout(request):
    if request.method == 'POST':
        auth.logout(request)

    return redirect('home')


def signin(request):

    context = {
        'error' : {
            'state' : False,
            'msg' : ""
        }
    }

    if request.method == 'POST':
        user_id = request.POST['user_id']
        user_pw = request.POST['user_pw']
        user_pw_check = request.POST['user_pw_check']

        class_num = int(request.POST['class_num'])
        name = request.POST['name']
        phone_num = request.POST['phone_num']

        if user_id or user_pw or user_pw_check is not "": 

            user = User.objects.filter(username=user_id)

            if len(user) != 0:
                context['error']['state'] = True
                context['error']['msg'] = ERROR_MSG['DOUBLE_ID']

            else:
                if user_pw == user_pw_check:
                    participate_class = AiClass.objects.get(
                        class_num = class_num
                    )
                    created_user = User.objects.create_user(
                        username=user_id,
                        password=user_pw
                    )

                    AiStudents.objects.create(
                        participate_class = participate_class,
                        user = created_user,
                        name = name,
                        phone_num = phone_num
                    )

                    auth.login(request, created_user)
                    return redirect('login')
                else:
                    context['error']['state'] = True
                    context['error']['msg'] = ERROR_MSG['NOT_PW']

        else:
            context['error']['state'] = True
            context['error']['msg'] = ERROR_MSG['NO INFO']       

    return render(request, 'signin.html' , context['error'])



