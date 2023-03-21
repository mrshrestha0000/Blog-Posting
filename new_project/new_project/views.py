""" views render the pages """

from django.http import HttpResponse
import random 
from articles.models import Article
from django.template.loader import render_to_string

def article_home_view(request):
    return HttpResponse()



def home_view(request , id=None):

    # from database
    number = random.randint(1,4)
    article_obj = Article.objects.get(id=number)
    article_qs = Article.objects.all()

    my_list = [100, 200, 300, 400, 500, 600]        

    context = {
        "object_list" : article_qs, 
        "id" : id,
        "title" : article_obj.title,
        "content" : article_obj.content
    }
 
    # from template

    # template_home_page = get_template("home_page.html")
    # template_string = template_home_page.render(context = data )

    html_string = render_to_string("home_page.html", context=context)
    # html_string = f"""
    # {context}
    # """
    
    return HttpResponse(html_string)




