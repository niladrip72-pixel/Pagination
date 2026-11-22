from django.shortcuts import render,redirect
from django.core.paginator import Paginator
from django.contrib import messages

from .models import Post
from .tasks import fetch_posts

def home(request):
    return render(request,'home.html')

def retrieve_posts(request):
    if request.method == 'POST':
        fetch_posts.delay()
        messages.success(request,"The API fetch task has been started. Please wait for it to finish.")
    return redirect("home")
def all_posts(request):
    post_list = Post.objects.all().order_by("api_id")

    paginator:Paginator = Paginator(post_list,10)
    page_number = request.GET.get("page")   # Here 'page' is a query-string parameter. For example : http://127.0.0.1:8000/posts/?page=2
    page_obj = paginator.get_page(page_number)

    return render(request,"home.html",{
        "page_obj":page_obj,
        "show_posts" : True,
    })

def search_post(request):
    if request.method == "POST":
        entered_id = request.POST.get("post_id", "").strip()
        try:
            post_id:int = int(entered_id)
        except ValueError:
            return render(request, "home.html", {
                "error": "Please enter a valid post ID."
            })
        if post_id < 0:
            return render(request, "home.html", {
                "error": "Negative IDs are not allowed."
            })

        post = Post.objects.filter(api_id=post_id).first()

        if post is None:
            return render(request, "home.html", {
                "searched_post": {},
                "error": "No post found for this ID. Fetch the API data first if needed."
            })

        return render(request, "home.html", {
            "searched_post": post
        })

    return redirect("home")
