from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

# @csrf_exempt
# def login_view(request):

#     # if request.user.is_authenticated:
#     #     return render(request, "accounts/already-logged-in.html", {})
    
#     context = {}
#     if request.method == "POST":
#         username = request.POST.get("username")
#         password = request.POST.get("password")

#         user = authenticate(request, username=username, password=password)

#         if user is not None:
#             login(request, user)
#             return redirect('/admin')
       
#         if user is None:
#             context = {"error":"Username or password invalid."}
#             return render(request, "accounts/login.html", context = context)
#         print(user)
     
#     return render(request, "accounts/login.html", context = context)


def logout_view(request):
    context = {}
    if request.method == "POST":
        logout(request)
        return redirect('/login')

    return render(request, "accounts/logout.html", context = context)


def register_view(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        user_obj = form.save()
        return redirect('/login')
    context = {
        "form":form
    }
    return render(request, "accounts/register.html", context = context)


def login_view(request):       
   
    if request.method == "POST":
        form = AuthenticationForm(request, data = request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/admin')
    else:
        form = AuthenticationForm(request)
    context = {
        "form":form
    }    
    return render(request, "accounts/login.html", context = context)