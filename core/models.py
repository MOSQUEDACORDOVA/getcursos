from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=150)
    father = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return self.name


class UserExtended(models.Model):
    name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_instructor = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class Course(models.Model):
    title = models.CharField(max_length=150)
    instructor = models.ForeignKey(UserExtended, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    img_main = models.ImageField(upload_to="courses")
    score = models.PositiveSmallIntegerField()
    price = models.FloatField(null=True)
    description = models.TextField(max_length=450, null=True)
    def __str__(self):
        return self.title


    