from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class AiClass(models.Model):
    class_num = models.IntegerField()
    teacher = models.CharField(max_length=30)
    class_room = models.CharField(max_length=30)

class AiStudents(models.Model):
    participate_class = models.ForeignKey(
        AiClass, on_delete=models.CASCADE, related_name='student_object')
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='student_object')
    name = models.CharField(max_length=30)
    phone_num = models.CharField(max_length=30)

class StudentPost(models.Model):
    intro = models.TextField()
    writer = models.ForeignKey(
        AiStudents, related_name='post', on_delete=models.SET_NULL, null=True)


