from django.contrib import admin
from .models import Category, User, Listing

# Register your models here.
admin.site.register(Category)
admin.site.register(User)
admin.site.register(Listing)
