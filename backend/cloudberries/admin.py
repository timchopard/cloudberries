from django.contrib import admin
from cloudberries.models import Category, Post, Project, Tutorial

class CategoryAdmin(admin.ModelAdmin):
    pass 

class PostAdmin(admin.ModelAdmin):
    pass 

class ProjectAdmin(admin.ModelAdmin):
    pass 

class TutorialAdmin(admin.ModelAdmin):
    pass

admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Tutorial, TutorialAdmin)
admin.site.register(Project, ProjectAdmin)
