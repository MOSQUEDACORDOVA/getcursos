from django.contrib import admin
from .models import *
# Register your models here.


admin.site.register(UserExtended)
admin.site.register(Course)
admin.site.register(Category)
admin.site.register(Opinion)
admin.site.register(Video)
admin.site.register(Tag)