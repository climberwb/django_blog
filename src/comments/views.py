from django.contrib import messages

from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from .models import Comment
from django.contrib.contenttypes.models import ContentType
from .forms import ReplyForm
# Create your views here.

def comment_thread(request,id):
    instance = get_object_or_404(Comment,id=id)
    content_type = instance.content_object.get_content_type
    print(content_type)
    object_id = instance.id
    # content_object = instance.content_object
    # content_id = content_object.id
    
    #  initial_data = {
    #     "content_type": instance.get_content_type,
    #     "object_id": instance.id
    # }
    
    form = ReplyForm(request.POST or None)
    print(form.errors)
    print(request.method)
    
    if form.is_valid() and request.method =="POST":
        # c_type = form.cleaned_data.get("content_type")
        # content_type = ContentType.objects.get(model=c_type)
        # obj_id = form.cleaned_data.get('object_id')
        content_data = form.cleaned_data.get('content')
        
            
    
        new_comment, created = Comment.objects.get_or_create(
                                                        user = request.user,
                                                        content_type = content_type,
                                                        object_id = instance.id,
                                                        content = content_data,
                                                        parent = instance
                                                    )
        print(new_comment.parent.content_object)
        return HttpResponseRedirect(new_comment.parent.content_object.get_absolute_url())
        
    comment = {
        "comment": instance,
        "form":form
    }
    # form = CommentForm(request.POST or None, initial=initial_data)
    return render(request,"comment_thread.html",comment)