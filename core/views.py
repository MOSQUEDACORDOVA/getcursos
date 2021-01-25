from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse
from django.views import View
from django.views.generic import ListView
from django.core.paginator import Paginator
from .models import Category, Course, Opinion, Tag, UserExtended
from django.contrib.auth.models import User
from .forms import SignUpForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from .utils import slice_by_two
RANGE_SCORE = 5
# Create your views here.
class Loged(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user = UserExtended.objects.get(user=self.request.user)
            self.context["user_data"] = user
            print(user.profile_pic)
        
           
class Base(Loged):
    template_dir = "core/akadimia/" 
    
    context = {}

    def __init__(self, *args, **kwargs):
        self.template_name = self.template_dir + self.template_name
        self.context["range_score"] = range(RANGE_SCORE)

    def get(self, request, *args, **kwargs):
        super().get(request,*args, **kwargs)
        opinions = Opinion.objects.all()
        self.context["opinions"] = opinions

        categories = Category.objects.order_by("-course__score").values()
        categories_distinct = []
        instructors = UserExtended.objects.filter(is_instructor=True)
        optimus_instructors = instructors.order_by("-popular_index") 
        popular_tags = Tag.objects.all()[:10]
        for i in categories:
            if i not in categories_distinct:
                categories_distinct.append(i)

        self.context["top_categories"] = categories_distinct
        self.context["popular_tags"] = popular_tags
        self.context["optimus_instructors"] = optimus_instructors

    def get_context_data(self, **kwargs):
        """ super(Base, self).get(**kwargs) """
        opinions = Opinion.objects.all()
        # CAMBIAR ESTO CUANDO SE PUEDA----------------------------------------------------------- ← ← ← ← ← ← ←
        context = self.context
        context["opinions"] = opinions

        categories = Category.objects.order_by("-course__score").values()
        categories_distinct = []
        instructors = UserExtended.objects.filter(is_instructor=True)
        optimus_instructors = instructors.order_by("-popular_index") 
        popular_tags = Tag.objects.all()[:12]
        for i in categories:
            if i not in categories_distinct:
                categories_distinct.append(i)

        context["top_categories"] = categories_distinct[:6]
        context["popular_tags"] = popular_tags
        context["optimus_instructors"] = optimus_instructors
        return context


# Json Responses
class CategoryAsync(Base):
    """ Peticion asíncrona para obtener los cursos en dos filas """
    template_name = ""
    def get(self, request, *args, **kwargs):
        courses = list(Course.objects.filter(category__name__iexact=self.kwargs["category"]).values(
            "category__name",
            "description",
            "id",
            "img_main",
            "instructor__user__first_name",
            "instructor__user__last_name",
            "price",
            "score",
            "title",
            "uploaded_date"
        ))
        p = Paginator(courses, 8)
        actual_page = self.kwargs["page"]

        # evita páginas que no existen o fuera del rango
        if actual_page > p.page_range[-1]:
            actual_page = 1

        # lista a rebanar
        to_slice = list(p.page(actual_page).object_list)
        

        return JsonResponse({"objects":slice_by_two(to_slice), "page":actual_page})


class CategoryPage(ListView, Base):
    template_name= "category.html"
    paginate_by = 3
    model = Category
    def get_context_data(self, **kwargs):
        context = super(CategoryPage,self).get_context_data(**kwargs)
        context.update(Base.get_context_data(self,**kwargs))
        
        
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        courses = {}

        for i in qs:
            p = Paginator(i.course_set.all(), 8)
            courses[i] = []
            for j in p.page_range:
                courses[i] += [p.page(j).object_list]
        
        
        

        return tuple(courses.items())

class Login(Base):
    template_name="login.html"
    def get(self, request, *args, **kwargs):
        super().get(request,*args, **kwargs)
        login = LoginForm()

        context={"login_form":login, "login_request":True}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        print(self.request.user.is_authenticated)
        if self.request.user.is_authenticated:
            return redirect(reverse("index"))
        else:
            
            user = User.objects.filter(email=self.request.POST["email"])
            if user.exists():
                username = user.first().username
                password = self.request.POST["password"]
                result = authenticate(request, username=username, password=password)
                if result is not None:
                    login(request, result)
                    return redirect(reverse("index"))
                else:
                    return redirect(reverse("login")+"?error=ad")
            else:
                return redirect(reverse("login")+"?not_registered")

class Logout(View):
    def get(self, request, *args, **kwargs):
        logout(self.request)
        return redirect(reverse("index"))

class SignUp(Base):
    template_name="sign-up.html"
    def get(self, request, *args, **kwargs):
        super().get(request,*args, **kwargs)
        if not self.request.user.is_authenticated:
            register_form = SignUpForm()
            self.context.update({
                "form": register_form,
            })
            return render(request, self.template_name, self.context)
        else:
            return redirect(reverse("index"))

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
        courses = Course.objects.order_by("-score")[:4]
        latest_courses = Course.objects.order_by("-uploaded_date")[:3]
        
        
        instructors = UserExtended.objects.filter(is_instructor=True)[:4]
        self.context.update(
            {
                "courses":courses, 
                "latest_courses":latest_courses, 
                "instructors":instructors, 

                }
                
            )
        
        return render(request, self.template_name, self.context)


class CourseView(Base):
    template_name = "course-detail.html"
    def get(self, request, pk, *args, **kwargs):
        super().get(request,*args, **kwargs)
        print(request, self.template_name)
        # todos los cursos
        self.context["course"] = Course.objects.get(pk=pk)

        return render(request, self.template_name, self.context)