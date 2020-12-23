from django.contrib import admin
from .models import AiClass, AiStudent, StudentPost


# Register your models here.
admin.site.register(AiClass)
admin.site.register(AiStudent)
admin.site.register(StudentPost)
