from django.contrib import admin
from django_micro import configure
from django.db import models
from django_micro import get_app_label
from django_micro import route
from django_micro import configure, route, run
from django.shortcuts import render, redirect
from django.contrib import messages
import os
from django import forms

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




@route('', name='homepage')
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
        if id:
            post_form = PostForm(request.POST, instance=post)
        else:
            post_form = PostForm(request.POST)

        if post_form.is_valid():
            post = post_form.save()
            messages.success(request, f"post {post.id} created")
            return redirect(f"/?id={post.id}")
        else:
            messages.error(request, f"error in form")
     
    context = {
        'form': post_form,
        'request':request,
    }
    #messages.info(request, "aaaa")
    return render(request, "index.html", context)

admin.site.register(Post)

route('admin/', admin.site.urls)
application = run()