from .models import Courses, UserExtended, Category



def get_top_categories(self):
    courses = Course.objects.all()
    categories = Category.objects.order_by("-course")