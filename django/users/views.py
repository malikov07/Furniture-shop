from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login,logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegisterForm
from django.contrib.auth.models import User
# Create your views here.


class LoginView(View):
    def get(self,request):
        return render(request, "users/login.html")
    
    def post(self,request):
        user = User.objects.get(username = request.POST["username"])
        login_form = AuthenticationForm(data = request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            return redirect("home")
        context = {
                "data":request.POST,
                "msg":"Username yoki parol xato!!!!",
        }
        return render(request,"users/login.html",context)
            
    

class RegisterView(View):
    def get(self,request):
        return render(request, "users/register.html")
    
    def post(self,request):
        password1 = request.POST["password"]
        password2 = request.POST["re_pass"]
        data = {
            "first_name": request.POST["first_name"],
            "last_name": request.POST["last_name"],
            "email": request.POST["email"],
            "username": request.POST["username"],
            "password": request.POST["password"],
        }
        user_form = UserRegisterForm(data)
        if user_form.is_valid() and password1 == password2:
            user_form.save()
            return redirect("login")
        else:
            context = {
                "data":data,
                "msg":"Polyalar noto'gri kiritildi!!!!!",
            }
            return render(request,"users/register.html",context)
        


class LogOutView(View):
    def get(self,request):
        logout(request)
        return redirect("home")
    

