from django.shortcuts import render, redirect
from .models import AiClass, AiStudent, StudentPost
from django.contrib.auth.models import User
from django.contrib import auth

ERROR_MSG = {
    'ID_EXIST': '이미 사용 중인 아이디 입니다.',
    'ID_NOT_EXIST': '존재하지 않는 아이디 입니다.',
    'ID_PW_MISSING': '아이디와 비밀번호를 확인해주세요.',
    'PW_CHECK': '비밀번호가 일치하지 않습니다.'
}

# Create your views here.


def home(request):
    class_obj_list = AiClass.objects.all()

    context = {
        'class_obj_list': class_obj_list
    }
    return render(request, 'home.html', context)


def detail(request, class_num):
    # class_num에 해당하는 반을 가져온다
    # ( 그 반에 속해있는 학생은 foreign key로 연결되어있다 )
    class_obj = AiClass.objects.get(class_num=class_num)

    context = {
        'class_obj': class_obj
    }
    return render(request, 'detail.html', context)


def add(request, student_pk):

    student = AiStudent.objects.get(pk=student_pk)

    if request.method == 'POST':
        # StudentPost를 생성하는걸로 변경
        StudentPost.objects.create(
            intro=request.POST['intro'],
            writer=student
        )

        return redirect('student', student_pk)

    return render(request, 'add.html')


def student(request, student_pk):

    student = AiStudent.objects.get(pk=student_pk)

    context = {
        'student': student
    }

    return render(request, 'student.html', context)


def edit(request, student_pk):

    if request.method == "POST":
        # 업데이트 해주기
        target_student = AiStudent.objects.filter(pk=student_pk)

        target_student.update(
            name=request.POST['name'],
            phone_num=request.POST['phone_num'],
        )

        return redirect('student', student_pk)

    student = AiStudent.objects.get(pk=student_pk)

    context = {
        'student': student
    }

    return render(request, 'edit.html', context)


def delete(request, student_pk, class_num):

    student = AiStudent.objects.get(pk=student_pk)
    student.delete()

    return redirect('detail', class_num)


def signup(request):

    context = {
        'error': {
            'state': False,
            'msg': ''
        }
    }

    if request.method == "POST":

        user_id = request.POST['user_id']
        user_pw = request.POST['user_pw']
        user_pw_check = request.POST['user_pw_check']

        # 추가
        class_num = int(request.POST['class_num'])
        name = request.POST['name']
        phone_num = request.POST['phone_num']

        if (user_id and user_pw):

            user = User.objects.filter(username=user_id)

            if len(user) == 0:

                if user_pw == user_pw_check:

                    participate_class = AiClass.objects.get(
                        class_num=class_num)

                    created_user = User.objects.create_user(
                        username=user_id,
                        password=user_pw
                    )

                    # 추가
                    AiStudent.objects.create(
                        participate_class=participate_class,
                        user=created_user,
                        name=name,
                        phone_num=phone_num
                    )

                    auth.login(request, created_user)

                    return redirect('home')

                else:
                    context['error']['state'] = True
                    context['error']['msg'] = ERROR_MSG['PW_CHECK']
            else:
                context['error']['state'] = True
                context['error']['msg'] = ERROR_MSG['ID_EXIST']

        else:
            context['error']['state'] = True
            context['error']['msg'] = ERROR_MSG['ID_PW_MISSING']

    return render(request, 'signup.html', context)


def login(request):

    context = {
        'error': {
            'state': False,
            'msg': ''
        },
    }

    if request.method == 'POST':
        user_id = request.POST['user_id']
        user_pw = request.POST['user_pw']

        user = User.objects.filter(username=user_id)

        if (user_id and user_pw):
            if len(user) != 0:

                user = auth.authenticate(
                    username=user_id,
                    password=user_pw
                )

                if user != None:
                    auth.login(request, user)

                    return redirect('home')
                else:
                    context['error']['state'] = True
                    context['error']['msg'] = ERROR_MSG['PW_CHECK']
            else:
                context['error']['state'] = True
                context['error']['msg'] = ERROR_MSG['ID_NOT_EXIST']

        else:
            context['error']['state'] = True
            context['error']['msg'] = ERROR_MSG['ID_PW_MISSING']

    return render(request, 'login.html', context)


def logout(request):

    auth.logout(request)

    return redirect('home')
