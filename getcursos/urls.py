"""getcursos URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from core import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.Index.as_view(), name="index"),
    # cursos
    path("category/<int:page>", views.CategoryPage.as_view(), name="category"),
    path("curso/<int:pk>", views.CourseView.as_view(), name="course_detail"),
    path("sign_up/", views.SignUp.as_view(), name="register"),
    path("login/", views.Login.as_view(), name="login"),
    path("logout/", views.Logout.as_view(), name="logout"),
    path("api/category_courses/<str:category>/<int:page>", views.CategoryAsync.as_view(), name="category_courses"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
