from django.shortcuts import render
from django.views import View
from django.views.generic import ListView
from .models import Category, Course, Opinion, Tag, UserExtended

# Create your views here.

class Base(View):
    template_dir = "core/"
    range_score = 5
    context = {}

    def __init__(self, *args, **kwargs):
        self.template_name = self.template_dir + self.template_name
        self.context["range_score"] = range(self.range_score)

    def get(self):
        pass 

class CategoryPage(ListView, Base):
    template_name= "category.html"
    paginate_by = 3
    model = Category
    #def get(self, request, *args, **kwargs):
        
class Index(Base):
    template_name = "index.html"
    def get(self, request, *args, **kwargs):
        super().get(*args, **kwargs)
        print(request, self.template_name)
        # todos los cursos
        courses = Course.objects.order_by("-score")
        latest_courses = Course.objects.order_by("-uploaded_date")
        opinions = Opinion.objects.all()
        popular_tags = Tag.objects.all()
        instructors = UserExtended.objects.filter(is_instructor=True)
        optimus_instructors = instructors.order_by("-popular_index")
        categories = Category.objects.order_by("-course")
        print(f"optimus {optimus_instructors}")
        self.context.update(
            {
                "courses":courses, 
                "latest_courses":latest_courses, 
                "opinions":opinions, 
                "popular_tags":popular_tags, 
                "instructors":instructors, 
                "optimus_instructors":optimus_instructors,
                "top_categories": categories
                }
                
            )
        
        return render(request, self.template_name,self.context)


class CourseView(Base):
    template_name = "course-lesson.html"
    def get(self, request, pk, *args, **kwargs):
        super().get(*args, **kwargs)
        print(request, self.template_name)
        # todos los cursos
        course = Course.objects.get(pk=pk)

        return render(request, self.template_name, {"course":course})