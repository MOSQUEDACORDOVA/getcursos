from django.shortcuts import render
from django.views import View
from .models import Category, Course, Opinion, Tag

# Create your views here.

class Base(View):
    template_dir = "core/"
    def __init__(self, *args, **kwargs):
        self.template_name = self.template_dir + self.template_name
    def get(self):
        pass 


class Index(Base):
    template_name = "index.html"
    def get(self, request, *args, **kwargs):
        super().get(*args, **kwargs)
        print(request, self.template_name)
        # todos los cursos
        courses = Course.objects.all()
        latest_courses = Course.objects.order_by("-uploaded_date")
        opinions = Opinion.objects.all()
        popular_tags = Tag.objects.all()
        return render(request, self.template_name, {"courses":courses, "latest_courses":latest_courses, "opinions":opinions, "popular_tags":popular_tags})


class CourseView(Base):
    template_name = "course-lesson.html"
    def get(self, request, pk, *args, **kwargs):
        super().get(*args, **kwargs)
        print(request, self.template_name)
        # todos los cursos
        course = Course.objects.get(pk=pk)

        return render(request, self.template_name, {"course":course})