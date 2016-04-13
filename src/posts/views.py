from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from .models import Post

# Create your views here.
def post_create(request):
    return HttpResponse("<h1>Create</h1>")

def post_detail(request):
    #instance = Post.objects.get(id=10)
    instance = get_object_or_404(Post,id=3)
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
    return render(request,"index.html",context)
    
def post_update(request):
    return HttpResponse("<h1>update</h1>")

def post_delete(request):
    return HttpResponse("<h1>delete</h1>")
    
    