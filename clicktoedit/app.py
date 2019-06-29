from django.contrib import admin
from django_micro import configure
from django.db import models
from django_micro import get_app_label
from django_micro import route
from django_micro import configure, route, run
from django.shortcuts import render, redirect
from django.views.generic import ListView, TemplateView
from django.contrib import messages
from django.http import HttpResponse
import os
from django import forms

from django.contrib.messages import constants as msg

MESSAGE_TAGS = {
    msg.ERROR: 'danger',
    msg.SUCCESS: 'success',
    msg.WARNING: 'warning',
    msg.INFO: 'info'
}


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_URL = '/static/'
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
}
INSTALLED_APPS=[
        'widget_tweaks',
]
#SECRET_KEY="jyeakey"
#MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'

configure(locals(), django_admin=True)


class Post(models.Model):
    title = models.CharField(max_length=255, unique =True)
    content = models.TextField(blank=True)
    create_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = get_app_label()
        ordering = ('-create_date',)


class ListPost(ListView):
    template_name = "list.html"
    model = Post

route("list/", ListPost.as_view(), name="list")

class Index(ListView):
    template_name="base.html"
    model = Post

route("", Index.as_view(), name="index")

class Messages(TemplateView):
    template_name="messages.html"
route("messages/", Messages.as_view(), name="messages")


@route('create', name='create')
def create(request):
    context = {}
    PostForm = forms.modelform_factory(Post, fields="__all__")
    id = request.GET.get("id")
    post = None
    if id:
        post = Post.objects.get(id=id)
        post_form = PostForm(instance=post)
    else:
        post_form = PostForm()

    if request.POST:
        msg="created"
        if id:
            post_form = PostForm(request.POST, instance=post)
            msg="updated"
        else:
            post_form = PostForm(request.POST)

        if post_form.is_valid():
            post = post_form.save()
            messages.success(request, f"post {post.id} {msg}")
            url =f"/"
            r = HttpResponse("")
            r["X-IC-Redirect"]= url
            return r
        else:
            messages.error(request, f"Error in form")
     
    context = {
        'form': post_form,
        'request':request,
        'post':post,
    }
    #messages.info(request, "aaaa")
    return render(request, "form.html", context)

admin.site.register(Post)

route('admin/', admin.site.urls)
application = run()