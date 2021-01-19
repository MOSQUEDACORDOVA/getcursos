from django.shortcuts import render, redirect, reverse
from django.views import View
from django.views.generic import ListView
from .models import Category, Course, Opinion, Tag, UserExtended
from django.contrib.auth.models import User
from .forms import SignUpForm, LoginForm
from django.contrib.auth import authenticate, login

# Create your views here.
class Loged(View):
    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            user = UserExtended.objects.get(user=self.request.user)
            self.context["user_data"] = user
            print(user.profile_pic)
        
           
class Base(Loged):
    template_dir = "core/"
    range_score = 5
    context = {}

    def __init__(self, *args, **kwargs):
        self.template_name = self.template_dir + self.template_name
        self.context["range_score"] = range(self.range_score)

    def get(self, request, *args, **kwargs):
        super().get(request,*args, **kwargs)

class CategoryPage(ListView, Base):
    template_name= "category.html"
    paginate_by = 3
    model = Category
    #def get(self, request, *args, **kwargs):


class Login(Base):
    template_name="login.html"
    def get(self, request, *args, **kwargs):
        super().get(request,*args, **kwargs)
        login = LoginForm()

        self.context.update({"login_form":login})
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        print(self.request.user.is_authenticated)
        if self.request.user.is_authenticated:
            return redirect(reverse("index"))
        else:
            print("EL PEPEPEPPE")
            user = User.objects.filter(email=self.request.POST["email"])
            if user.exists():
                username = user.first().username
                password = self.request.POST["password"]
                result = authenticate(request, username=username, password=password)
                if result is not None:
                    login(request, result)
                    return redirect(reverse("index"))
                else:
                    return redirect(reverse("login")+"?error")
            else:
                return redirect(reverse("login")+"?not_registered")





class SignUpUser(Base):
    template_name = "sign-up-first.html"
    def get(self, request, *args, **kwargs):
        super().get(request,*args, **kwargs)
        user_form = UserForm()
        self.context.update({
            "form": register_form,
        })
        return render(request, self.template_name, self.context)


class SignUp(Base):
    template_name="sign-up.html"
    def get(self, request, *args, **kwargs):
        super().get(request,*args, **kwargs)
        register_form = SignUpForm()
        self.context.update({
            "form": register_form,
        })
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        #super().post(*args, *kwargs)
        register_form = SignUpForm(request)
        print(self.request.POST)
        user = User.objects.filter(email=self.request.POST["email"]).exists()
        print(user)
        if user:
            self.context.update({
                "errors":"el usuario ingresado ya existe, ingrese un nuevo usuario"
            })
            return redirect(reverse("register")+"?email=-1")

        user = User(first_name=self.request.POST["first_name"], last_name=self.request.POST["last_name"], email=self.request.POST["email"], password=self.request.POST["password"])
        user.save()
        if register_form.is_valid():
            register_form.save()



class Index(Base):
    template_name = "index.html"
    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
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
        super().get(request,*args, **kwargs)
        print(request, self.template_name)
        # todos los cursos
        course = Course.objects.get(pk=pk)

        return render(request, self.template_name, {"course":course})