from django.contrib import admin
from django_micro import configure
from django.db import models
from django_micro import get_app_label
from django_micro import route
from django_micro import configure, route, run
from django.shortcuts import render, redirect
from django.views.generic import *
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

#### MODELS

class Post(models.Model):
    title = models.CharField(max_length=255, unique =True)
    content = models.TextField(blank=True)
    create_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = get_app_label()
        ordering = ('-create_date',)

admin.site.register(Post)
route('admin/', admin.site.urls)

#### VIEWS

class Messages(TemplateView):
    template_name="messages.html"
route("messages/", Messages.as_view(), name="messages")


class ListPost(ListView):
    template_name = "list.html"
    model = Post
route("list/", ListPost.as_view(), name="list")

class Index(ListView):
    template_name="base.html"
    model = Post
route("", Index.as_view(), name="index")


@route("update/<int:id>/", name="update")
def update(request, id):
    PostForm = forms.modelform_factory(Post, fields="__all__")
    post = Post.objects.get(id=id)
    context={'post':post,'form' :PostForm(instance=post) }
    if request.POST:
        f = PostForm(request.POST, instance=post)
        if f.is_valid():
            post = f.save()
            messages.info(request,"data updated")
            resp = HttpResponse("")
            resp["X-IC-Redirect"]= "/"
            return resp

        context.update({'form': f})
    return render(request, "form.html", context)



@route("create",name="create")
def create(request):
    PostForm = forms.modelform_factory(Post, fields="__all__")
    context = {'form': PostForm()}
    if request.POST:
        f = PostForm(request.POST)
        if f.is_valid():
            post = f.save()
            messages.success(request, f"post {post.id} create")
            resp = HttpResponse("")
            resp["X-IC-Redirect"]= "/"
            return resp
        else:
            messages.error(request, f"Error in form")
        context = {'form':f}
    return render(request, "form.html", context)
    
            



application = run()