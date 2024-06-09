from django.contrib import admin
from cloudberries.models import Category, Post 

class CategoryAdmin(admin.ModelAdmin):
    pass 

class PostAdmin(admin.ModelAdmin):
    pass 

admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
