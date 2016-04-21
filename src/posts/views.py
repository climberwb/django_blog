from urllib import quote_plus

from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from .forms import PostForm
from .models import Post #,Admin

# for generic key Comments recieved
# code for imports from https://docs.djangoproject.com/en/1.9/ref/contrib/contenttypes/
from comments.models import Comment

from comments.forms import CommentForm

from django.utils import timezone
# from settings import AUTH_USER_MODEL
from django.db.models import Q



# pagination
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render

# Create your views here.

def post_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
        
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
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

def post_detail(request,slug=None):
    
    instance = get_object_or_404(Post,slug=slug)
    
   
    #comments = Comment.objects.filter_by_instance(instance)
    
    comments = instance.comments
    
    if(instance.draft or instance.publish > timezone.now().date()) and(not request.user.is_staff or not request.user.is_superuser):
        raise Http404
    user = instance.user
    
    share_string = quote_plus(instance.content)
    
    initial_data = {
        "content_type": instance.get_content_type,
        "object_id": instance.id
    }
    form = CommentForm(request.POST or None, initial=initial_data)
    
    if form.is_valid():
        c_type = form.cleaned_data.get("content_type")
        content_type = ContentType.objects.get(model=c_type)
        obj_id = form.cleaned_data.get('object_id')
        content_data = form.cleaned_data.get('content')
        parent_obj = None
        try:
            parent_id = int(request.POST.get("parent_id"))
        except:
            parent_id = None
        
        if parent_id:
            parent_qs = Comment.objects.filter(id=parent_id)
            if parent_qs.exists() and parent_qs.count()==1:
                parent_obj = parent_qs.first()
            
    
        new_comment, created = Comment.objects.get_or_create(
                                                        user = request.user,
                                                        content_type = content_type,
                                                        object_id = obj_id,
                                                        content = content_data,
                                                        parent = parent_obj
                                                    )
        return HttpResponseRedirect(new_comment.content_object.get_absolute_url())
        if created:
            print("Yeah it worked!") 
        
        
    
    detail = {
        "title":"Detail",
        "post":instance,
        "user":user,
        "share_string": share_string,
        "comments":comments,
        "comment_form":form,
    }
    return render(request,"post_detail.html",detail)


    


def post_list(request):
    if request.user.is_staff or request.user.is_superuser:
        queryset_list = Post.objects.all().order_by("-timestamp")
    else:
        queryset_list = Post.objects.active().order_by("-timestamp")
    
    query = request.GET.get("q")   
    if query:
        queryset_list = queryset_list.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)|
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) 
            ).distinct()
        
    paginator = Paginator(queryset_list, 3) # Show 2 contacts per page
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
        "title":"List",
        "page_request_var":page_request_var
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
    
def post_update(request,slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
        
    post_instance = get_object_or_404(Post,slug=slug)

    form = PostForm( request.POST or None, request.FILES or None, instance=post_instance)
    
    # form = IntentionForm(instance=intention)
    print( form)
    if form.is_valid() and  request.method =="POST":
        print("inside if")
        post_instance = form.save(commit=False)
        post_instance.save()
        messages.success(request,"made successful post")
        return HttpResponseRedirect(post_instance.get_absolute_url())
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

def post_delete(request,slug=None):
    
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
        
    instance = get_object_or_404(Post,slug=slug)
    
    messages.success(request, "Successfully Updated")
    instance.delete()
    return redirect("posts:list")
    
    