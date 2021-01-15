from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=150)
    father = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=150)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class UserExtended(models.Model):
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_instructor = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Course(models.Model):
    title = models.CharField(max_length=150)
    instructor = models.ForeignKey(UserExtended, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    tags = models.ManyToManyField(Tag)
    img_main = models.ImageField(upload_to="courses")
    score = models.PositiveSmallIntegerField()
    price = models.FloatField(null=True)
    description = models.TextField(max_length=450, null=True)
    uploaded_date = models.DateTimeField(null=True, default=datetime.now())
    students = models.ManyToManyField(UserExtended, related_name="students")


    def __str__(self):
        return self.title


class Video(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    duration = models.TimeField(default=timedelta(seconds=0), null=True, blank=True)


class Opinion(models.Model):
    user = models.ForeignKey(UserExtended, on_delete=models.CASCADE)
    message = models.TextField(max_length=800)
    uploaded_date = models.DateTimeField(null=True, default=datetime.now())
    