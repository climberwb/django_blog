from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

from .forms import PostForm
from .models import Post

# Create your views here.

def post_create(request):
    form = PostForm(request.POST or None)
    if form.is_valid() and request.method == 'POST':
        instance = form.save(commit=False)
        instance.save()
        # message success
        ## TODO GET MESSAGES TO NOT DISPLAY SUCCESS AND FAILURE
        messages.add_message(request,messages.SUCCESS, "Logged in Successfully")
        return HttpResponseRedirect(instance.get_absolute_url())
    elif(request.method == 'POST'):
        messages.error(request, "Not Successfully Created")
        
        
    context = {
        "form":form,
    }
    return render(request,"post_form.html",context)

def post_detail(request,id=None):
    #instance = Post.objects.get(id=10)
    instance = get_object_or_404(Post,id=id)
    detail = {
        "title":"Detail",
        "post":instance
    }
    return render(request,"post_detail.html",detail)
    
def post_list(request):
    queryset = Post.objects.all()
    context = {
        "object_list":queryset,
        "title":"List"
    }
    # if request.user.is_authenticated():
    #     context = {
    #         "title":"My User List"
    #     }
    # else:
    #     context = {
    #         "title":"List"
    #     }
    return render(request,"post_list.html",context)
    
def post_update(request,id=None):
    instance = get_object_or_404(Post,id=id)
    
    print(instance)
    form = PostForm(request.POST or None, instance=instance)
    # form = IntentionForm(instance=intention)
    if form.is_valid() and request.method == 'POST':
        instance = form.save(commit=False)
        instance.save()
        # message success
        ## TODO GET MESSAGES TO NOT DISPLAY SUCCESS AND FAILURE
        messages.success(request, "Successfully Updated")
        print(instance.get_absolute_url())
        return HttpResponseRedirect(instance.get_absolute_url())
    elif(request.method == 'POST'):
        print("hit the else")
        messages.error(request,"Failed To Update")
       
    context = {
        "title":instance.title,
        "content":instance.content,
        "form":form
    }
    
    return render(request,"post_form.html",context)

def post_delete(request,id=None):
    instance = get_object_or_404(Post,id=id)
    
    messages.success(request, "Successfully Updated")
    instance.delete()
    return redirect("posts:list")
    
    