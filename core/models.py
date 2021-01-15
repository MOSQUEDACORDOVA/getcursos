from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.db.models.signals import post_save
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

        
class Social(models.Model):
    url = models.URLField()
    platform = models.CharField(max_length=50)


class UserExtended(models.Model):
    profile_pic = models.ImageField(upload_to="profiles", null=True)
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about = models.TextField(max_length=450, default="")
    is_instructor = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    social = models.ForeignKey(Social, on_delete=models.CASCADE, null=True)
    
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
    students = models.ManyToManyField(UserExtended, related_name="students", blank=True)

    def __str__(self):
        return self.title


class Review(models.Model):
    user = models.ForeignKey(UserExtended, on_delete=models.CASCADE)
    score = models.PositiveSmallIntegerField()
    opinion = models.TextField()
    likes = models.PositiveIntegerField(null=True, blank=True)
    dislikes = models.PositiveIntegerField(null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        # si el score no está en ese rango
        if not 0 < self.score < 5:
            raise ValueError("score must be less than 5 and greater than 0")
        super().save(*args, **kwargs)
    class Meta:
        unique_together = ["user", "course"]

class Video(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    duration = models.TimeField(default=timedelta(seconds=0), null=True, blank=True)


class Opinion(models.Model):
    # opiniones de usuarios con respecto a la plataforma
    user = models.OneToOneField(UserExtended, on_delete=models.CASCADE)
    message = models.TextField(max_length=800)
    uploaded_date = models.DateTimeField(null=True, default=datetime.now())
    def __str__(self):
        return self.user.user.username

# signals
def promedio_score_course(sender, instance, **kwargs):
    course_to_rate = instance.course
    related_reviews = Review.objects.filter(course=course_to_rate)
    sigma = 0
    for i in related_reviews:
        sigma += i.score

    middle = sigma / len(related_reviews)
    print(f"PROMEDIO: {middle}")
    course_to_rate.score = round(middle)
    course_to_rate.save()
    print(related_reviews)

post_save.connect(promedio_score_course, sender=Review)