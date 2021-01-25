from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.db.models.signals import post_save
from django.core.validators import MaxValueValidator,MinValueValidator, FileExtensionValidator
# Create your models here.
# validator function

#def min_value(number):
#    if 
#

class Category(models.Model):
    # Categoría a la que pertenece el curso
    # Nota: se puede armar un arbol con recursividad
    name = models.CharField(max_length=150)
    father = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return self.name


class Tag(models.Model):
    # Etiquetas por las cuales se filtrarán los cursos
    name = models.CharField(max_length=150)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class UserExtended(models.Model):
    # modificación extendida del modelo User de django
    profile_pic = models.ImageField(upload_to="profiles", null=True)
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about = models.TextField(max_length=450, default="")
    phone = models.CharField(max_length=30, null=True)
    is_instructor = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    popular_index = models.PositiveSmallIntegerField(validators=[MaxValueValidator(5),MinValueValidator(1)], default=1, blank=True)

    def save(self, *args, **kwargs):
        if self.popular_index > 5:
            self.popular_index = 5
        
        super().save(*args,**kwargs)
        
    def __str__(self):
        return self.user.username

    def get_full_name(self):
        return self.user.first_name +" "+self.user.last_name
    def courses_count(self):
        return len(self.course_set.all())


class Social(models.Model):
    # Redes sociales del usuario
    user = models.ForeignKey(UserExtended, on_delete=models.CASCADE, null=True)
    url = models.URLField()
    platform = models.CharField(max_length=50)


class Course(models.Model):
    # Cursos de la plataforma
    title = models.CharField(max_length=150)
    instructor = models.ForeignKey(UserExtended, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    tags = models.ManyToManyField(Tag)
    img_main = models.ImageField(upload_to="courses")
    score = models.PositiveSmallIntegerField(validators=[MaxValueValidator(5),MinValueValidator(1)], default=1)
    price = models.FloatField(null=True)
    description = models.TextField(max_length=1000, null=True)
    requirements = models.TextField(max_length=1000, null=True)
    uploaded_date = models.DateTimeField(null=True, default=datetime.now())
    students = models.ManyToManyField(UserExtended, related_name="students", blank=True)

    def save(self, *args, **kwargs):
        if self.score > 5:
            self.score = 5
        
        super().save(*args,**kwargs)

    def __str__(self):
        return self.title


class Lesson(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=500, null=True)


class Topic(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    description = models.CharField(max_length=200)


class Review(models.Model):
    # Opiniones sobre cada curso
    user = models.ForeignKey(UserExtended, on_delete=models.CASCADE)
    score = models.PositiveSmallIntegerField(validators=[MaxValueValidator(5),MinValueValidator(1)])
    opinion = models.TextField()
    likes = models.PositiveIntegerField(null=True, blank=True)
    dislikes = models.PositiveIntegerField(null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ["user", "course"]
    def save(self, *args, **kwargs):
        if self.score > 5:
            self.score = 5
        
        super().save(*args,**kwargs)


class Video(models.Model):
    # Videos de cada curso
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=150)
    duration = models.TimeField(default=timedelta(seconds=0), null=True, blank=True)
    video = models.FileField(null=True)


class Opinion(models.Model):
    # opiniones de usuarios con respecto a la plataforma
    user = models.OneToOneField(UserExtended, on_delete=models.CASCADE)
    message = models.TextField(max_length=800)
    uploaded_date = models.DateTimeField(null=True, default=datetime.now())
    def __str__(self):
        return self.user.user.username


# signals
def promedio_score_course(sender, instance, **kwargs):
    # se saca un promedio de los scores cada vez que se guardan Reviews
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


def update_popular_index(sender, instance, **kwargs):
    instructor = instance.course.instructor
    courses_to_exam = Course.objects.filter(instructor=instructor)
    sigma = 0
    for i in courses_to_exam:
        sigma += i.score
    middle = sigma / len(courses_to_exam)

    print(f"PROMEDIO: {middle}")
    instructor.popular_index = round(middle)
    instructor.save()


post_save.connect(promedio_score_course, sender=Review)
post_save.connect(update_popular_index, sender=Review)