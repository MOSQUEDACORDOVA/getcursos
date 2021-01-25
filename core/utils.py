from .models import Course, UserExtended, Category



def get_top_categories(self):
    courses = Course.objects.all()
    categories = Category.objects.order_by("-course")

def slice_by_two(lista):
    middle_index = len(lista)//2
    first_part = lista[:middle_index]
    second_part = lista[middle_index:]
    return first_part, second_part
    