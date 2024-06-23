from django.shortcuts import render
from cloudberries.models import Category, Post, Project, Tutorial
from cloudberries.markdownparser import MarkDownToHtml

from django.conf import settings
from django.views.generic import FormView, TemplateView
from django.core.mail import send_mail
from django.shortcuts import reverse
from django.contrib.auth.decorators import login_required
from .forms import ContactForm

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
        "title": "Blog",
        "posts": posts,
        "post_header": "Posts",
    }
    return render(request, "cloudberries/listpage.html", context)

def cloudberries_projects(request):
    projects = Project.objects.all()
    context = {
        "title": "Projects",
        "posts": projects,
        "post_header": "Projects",
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
    mdhtml = MarkDownToHtml(post)
    body = mdhtml.iterate(post.body)
    context = {
        "post": post,
        "body": body,
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
    tutorials = Tutorial.objects.all()
    context = {
        "title": "Tutorials",
        "posts": tutorials,
        "post_header": "Tutorials",
    }
    return render(request, "cloudberries/listpage.html", context)