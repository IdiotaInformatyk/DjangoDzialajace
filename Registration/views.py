from django.shortcuts import render, redirect
from .forms import RegisterForm
# Create your views here.
def Registration(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
           form.save()

        return redirect("/login")


    form = RegisterForm()
    return render(response, "Registration/Registration.html", {"form":form})