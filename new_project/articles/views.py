from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpRequest
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify

from articles.models import Article
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
        context['created']=True
        context['object']=article_obj

        slug_create(article_obj)

        # data = article_obj.__dict__
        # title = data["title"] 
        # slug_create(title)
        # print (title)
        # slug = slugify(title.lower())
        # print (slug)

        # a = Article(slug = slug)
        # a.save()

        return render(request, "articles/create.html" , context=context)
    else:
        return render(request, "articles/create.html" , context=context)
    

def slug_create(request):
    article = Article.objects.all()
    print ("request",request)
    print("article",article)
    # slug = slugify(title.lower())
    # print (slug)

    # a = Article(slug = slug)
    # a.save()

# def article_create(request):

#     form = ArticleForm(request.POST or None)
#     context = {
#         "form":form
#     }
#     if form.is_valid():
#         article_obj = form.save()
#         context ['form'] = ArticleForm()
#         context['created']=True
#         context['object']=article_obj


       
#         # context = {
#         #     "object": article_obj,
#         #     "created": True
#         # }
#         return render(request, "articles/create.html" , context=context)
#     else:
#         return render(request, "articles/create.html" , context=context)
                      

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

# def slug_create(request):   
#     query_dict = request.GET #This is a dict
#     obj = query_dict.get("title") #<input type="text" name="id"/>
#     article_object = None

#     try:
#         obj = int(query_dict.get("title"))

#     except:
#         id = None
#         return HttpResponse ("""<h1> Invalid search params </h1>""")

#     if obj is not None:
#         article_object = Article.objects.get(id=obj)

#     context = {
#         "search": article_object
#     }

#     return render(request, "articles/search.html", context=context)

# def slug_create(request):
#     article = Article.objects.all()
#     print (article)
#     article1 = request.GET
#     print ("article1", article1)
#     pass

# slug_create()
# id = 1


