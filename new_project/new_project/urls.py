"""new_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from .views import home_view
from .settings import STATIC_ROOT, STATIC_URL
from articles.views import (
    article_create,
    article_detail_view,
    article_search_view,
    article_update,
    article_detail_update
)
from accounts.views import (
    login_view,
    logout_view,
    register_view
)
from khalti.views import (
    movies_views,
    new_khanepani,
    counter_update,
    migrate_sage_movies,
    uranus
)
from khalti.encode import (
    encode,
    decode
)
from khalti.kalimati import(
    sign_kalimati
)
from khalti.regex import(
    recharge
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', home_view),

    path('login/', login_view),
    path('logout/', logout_view),
    path('register/', register_view),

    path('articles/', article_search_view),
    path('articles/create/', article_create),
    path('articles/<int:id>/<title>', article_detail_view),
    path('articles/details/<int:id>/', article_detail_view),
    path('articles/update/<int:id>/',article_update),
    path('articles/update/',article_detail_update),


    path("khalti/movies/", movies_views),
    path("khalti/new_khanepani/", new_khanepani),
    path("khalti/counter_update/", counter_update),
    path("khalti/migrate_sage_movies/",migrate_sage_movies),
    path("khalti/encode/",encode),
    path("khalti/decode/",decode),
    path("khalti/kalimati",sign_kalimati),
    path("khalti/recharge",recharge),
    path("khalti/uranus", uranus)
] 
