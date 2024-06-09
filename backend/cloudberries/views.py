from django.shortcuts import render
from cloudberries.models import Post

def cloudberries_index(request):
    posts = Post.objects.all().order_by("-created_on")[:3]
    context = {
        "posts": posts,
        "post_header": "Latest Blog Posts",
        "post_footer": "more posts",
        "footer_link": "cloudberries_posts",
    }
    return render(request, "cloudberries/index.html", context)

def cloudberries_posts(request):
    posts = Post.objects.all().order_by("-created_on")
    context = {
        "posts": posts,
        "post_header": "Posts",
    }
    return render(request, "cloudberries/posts.html", context)

def cloudberries_category(request, category):
    posts = Post.objects.filter(
        categories__name__contains=category
    ).order_by("-created_on")
    context = {
        "category": category,
        "posts": posts,
        "post_header": f"Posts Tagged: {category}"
    }
    return render(request, "cloudberries/category.html", context)

def cloudberries_detail(request, pk):
    post = Post.objects.get(pk=pk)
    context = {
        "post": post,
    }
    return render(request, "cloudberries/detail.html", context)