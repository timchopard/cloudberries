import os

from django.shortcuts import render
from cloudberries.models import Category, Post, Project, Tutorial, Upload

from django.conf import settings
from django.views.generic import FormView, TemplateView
from django.core.mail import send_mail
from django.shortcuts import reverse
from django.contrib.auth.decorators import login_required

from .forms import ContactForm, PostForm

def cloudberries_index(request):
    posts = Post.objects.filter(
        publish=True
    ).order_by("-created_on")[:5]
    tutorials = Tutorial.objects.filter(
        publish=True
    ).order_by("-created_on")[:3]
    projects = Project.objects.filter(
        publish=True
    ).order_by("-created_on")[:3]
    context = {
        "posts": posts,
        "post_header": "Latest Blog Posts",
        "post_footer": "more posts",
        "footer_link": "cloudberries_posts",
        "projects": projects,
        "project_header": "Latest Projects",
        "project_footer": "more projects",
        "project_link": "cloudberries_projects",
        "tutorials": tutorials, 
        "tutorial_header": "Latest Tutorials",
        "tutorial_footer": "more tutorials",
        "tutorial_link": "cloudberries_tutorials",
    }
    return render(request, "cloudberries/index.html", context)

def cloudberries_posts(request):
    posts = Post.objects.filter(publish=True).order_by("-created_on")
    context = {
        "title": "Blog",
        "posts": posts,
        "post_header": "Posts",
        "post_type": "cloudberries_detail",
    }
    return render(request, "cloudberries/listpage.html", context)

def cloudberries_projects(request):
    projects = Project.objects.filter(publish=True).order_by("-created_on")
    context = {
        "title": "Projects",
        "posts": projects,
        "post_header": "Projects",
        "post_type": "cloudberries_project_detail",
    }
    return render(request, "cloudberries/listpage.html", context)

def cloudberries_category(request, category):
    posts = Post.objects.filter(
        categories__name__contains=category
    ).order_by("-created_on")
    categories = Category.objects.all()
    context = {
        "categories": categories,
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

def cloudberries_tutorial_detail(request, pk):
    post = Tutorial.objects.get(pk=pk)
    context = {
        "post": post,
    }
    return render(request, "cloudberries/detail.html", context)

def cloudberries_project_detail(request, pk):
    post = Project.objects.get(pk=pk)
    context = {
        "post": post,
    }
    return render(request, "cloudberries/detail.html", context)

class SuccessView(TemplateView):
    template_name = "cloudberries/success.html"

class ContactView(FormView):
    form_class = ContactForm
    template_name = "cloudberries/contact.html"

    def get_success_url(self):
        return reverse("cloudberries_success")
    
    def form_valid(self, form):
        sender = form.cleaned_data.get("email")
        subject = form.cleaned_data.get("subject")
        message = form.cleaned_data.get("message")
        cc_myself = form.cleaned_data.get("cc_myself")

        full_message =  f"Received message from < {sender} > "
        full_message += f"with subject [ {subject} ]"
        full_message += '\n' + 20 * '-' + '\n\n'
        full_message += f"{message}"

        send_vars = {
            "subject" : "Message from cloudberries Contact Form",
            "message" : full_message,
            "fail_silently" : False,
            "from_email" : settings.DEFAULT_FROM_EMAIL,
        }

        send_mail(recipient_list=[settings.NOTIFY_EMAIL], **send_vars)

        if cc_myself:
            send_vars["subject"] = "Do Not Reply: Cloudberries Contact Form"
            send_mail(recipient_list=[sender], **send_vars)

        return super(ContactView, self).form_valid(form)

def cloudberries_tutorials(request):
    tutorials = Tutorial.objects.filter(publish=True)
    context = {
        "title": "Tutorials",
        "posts": tutorials,
        "post_header": "Tutorials",
        "post_type": "cloudberries_tutorial_detail",
    }
    return render(request, "cloudberries/listpage.html", context)

@login_required
def upload_file_view(request):
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        form = PostForm
        obj = Upload.objects.get(activated=False)
        info_dict = {"TYPE": obj.post_type}
        with open(obj.meta_file.path, 'r') as f:
            for line in f.readlines():
                if '=' not in line:
                    continue
                info_dict[line.split("=")[0]] = line.split("=")[1]
        with open(obj.body_file.path, 'r') as f:
            info_dict["BODY"] = f.read()

        os.remove(obj.meta_file.path)
        os.remove(obj.body_file.path)
        
        obj.activated = True  
        obj.save()
        
        for key in ["TITLE", "SUMMARY", "BODY"]:
            if key not in info_dict.keys():
                return render(
                    request, 
                    "cloudberries/upload.html", 
                    {"form": form}
                )

        categories = []
        categories_raw = info_dict["CATEGORIES"].split('[')[1].split(']')[0]
        categories_raw = categories_raw.split(' ')
        for category in categories_raw:
            if len(Category.objects.filter(name=category)) < 1:
                Category.objects.create(
                    name = category
                )
            categories.append(Category.objects.filter(name=category))

        if info_dict["TYPE"] == "post":
            Post.objects.create(
                title = info_dict["TITLE"],
                body = info_dict["BODY"],
                summary = info_dict["SUMMARY"],
                publish=False
            )
        elif info_dict["TYPE"] == "tutorial":
            Tutorial.objects.create(
                title = info_dict["TITLE"],
                body = info_dict["BODY"],
                summary = info_dict["SUMMARY"],
                publish=False
            )
        elif info_dict["TYPE"] == "project":
            Project.objects.create(
                title = info_dict["TITLE"],
                body = info_dict["BODY"],
                summary = info_dict["SUMMARY"],
                publish=False
            )
            

    
    return render(request, "cloudberries/upload.html", {"form": form})