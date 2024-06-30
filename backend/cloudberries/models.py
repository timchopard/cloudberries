from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=64)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=256)
    body = models.TextField()
    summary = models.CharField(max_length=200)
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField("Category", related_name="posts")
    publish = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title


class Project(models.Model):
    title = models.CharField(max_length=256)
    body = models.TextField()
    summary = models.CharField(max_length=200)
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    publish = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.title


class Tutorial(models.Model):
    title = models.CharField(max_length=256)
    body = models.TextField()
    summary = models.CharField(max_length=200)
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    publish = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.title