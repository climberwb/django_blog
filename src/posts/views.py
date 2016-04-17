from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

from .forms import PostForm
from .models import Post

# pagination
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render

# Create your views here.

def post_create(request):
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request,"made successful post")
        return HttpResponseRedirect(instance.get_absolute_url())
    elif form.errors:
        messages.error(request, "Not Successfully Created")
    else:
        pass
        
        
    context = {
        "form":form
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
    queryset_list = Post.objects.all().order_by("-timestamp")
    
    paginator = Paginator(queryset_list, 15) # Show 15 contacts per page
    page_request_var ='page'
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.# If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)
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
    post_instance = get_object_or_404(Post,id=id)
    
    form = PostForm( instance=post_instance)
    
    # form = IntentionForm(instance=intention)
    if form.is_valid() and  request.method =="POST":
        instance = form.save(commit=False)
        instance.save()
        messages.success(request,"made successful post")
        return HttpResponseRedirect(instance.get_absolute_url())
    elif form.errors and request.method =="POST":
        messages.error(request, "Not Successfully Created")
    else:
        pass
       
    context = {
        "title":post_instance.title,
        "content":post_instance.content,
        "form":form
    }
    
    return render(request,"post_form.html",context)

def post_delete(request,id=None):
    instance = get_object_or_404(Post,id=id)
    
    messages.success(request, "Successfully Updated")
    instance.delete()
    return redirect("posts:list")
    
    