from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpRequest
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from .models import Article
from .forms import ArticleForm

# Create your views here.

# create the form and submit the new article
@csrf_exempt
@login_required
def article_create(request):

    form = ArticleForm(request.POST or None)
    context = {
        "form":form
    }
    if form.is_valid():
        article_obj = form.save()
        context ['form'] = ArticleForm()
       
        # context = {
        #     "object": article_obj,
        #     "created": True
        # }
        return render(request, "articles/create.html" , context=context)
    else:
        return render(request, "articles/create.html" , context=context)


# def article_create(request):

#     form = ArticleForm(request.POST or None)
#     context = {
#         "form":form
#     }
#     if form.is_valid():
#         title=form.cleaned_data.get('title')
#         content=form.cleaned_data.get('content')

#         article_object = Article.objects.create(title=title,content=content)
#         context = {
#             "object": article_object,
#             "created": True
#         }
#         return render(request, "articles/create.html" , context=context)
#     else:
#         return render(request, "articles/create.html" , context=context)




# @csrf_exempt
# @login_required
# def article_create(request):

#     form = ArticleForm()
#     context = {
#         "form":form
#     }

#     # This is article create
#     if request.method == "POST":
#         form = ArticleForm(request.POST)
#         context["form"]=form
#         if form.is_valid():
#             title=form.cleaned_data.get('title')
#             content=form.cleaned_data.get('content')

#             article_object = Article.objects.create(title=title,content=content)
#             context = {
#                 "object": article_object,
#                 "created": True
#             }
#             return render(request, "articles/create.html" , context=context)
#         else:
#             return render(request, "articles/create.html" , context=context)

#     return render(request, "articles/create.html" , context=context)
                              

# View the detail of the article
def article_detail_view(request, id=None, *args, **kwargs):   
    detail = Article.objects.all()
    article_object = None
    context = {}
    if id is not None:
        article_object = Article.objects.get(id=id)
        context = {
            "id": id,
            "title": article_object.title,
            "content": article_object.content
        }

    return render (request, "articles/detail.html", context = context)


#search the article with id
def article_search_view(request):   
    query_dict = request.GET #This is a dict
    obj = query_dict.get("id") #<input type="text" name="id"/>
    article_object = None

    try:
        obj = int(query_dict.get("id"))

    except:
        id = None
        return HttpResponse ("""<h1> Invalid search params </h1>""")

    if obj is not None:
        article_object = Article.objects.get(id=obj)

    context = {
        "search": article_object
    }

    return render(request, "articles/search.html", context=context)





