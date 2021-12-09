from django.shortcuts import render, redirect
from .forms import RegisterForm
# Create your views here.
# przekazujy dane do templatów

#metoda POST łączy dane z forms, koduje i przesyła na serwer
# po czym dostaje odpowiedź zwrotną


def Registration(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():

            form.save()

        return redirect("/login")
    form = RegisterForm()
    return render(request, "Registration/Registration.html", {"form":form})


