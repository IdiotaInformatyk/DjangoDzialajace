from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import ToDoList, Item
from .forms import CreateNewList
from .forms import RegisterForm

# przekazujy dane do templatów

#metoda POST łączy dane z forms, koduje i przesyła na serwer
# po czym dostaje odpowiedź zwrotną


def index(response, id):
    ls = ToDoList.objects.get(id=id)

    if response.method == "POST":
        if response.POST.get("save"):
            for item in ls.item_set.all():
                if response.POST.get("c" + str(item.id)) == "clicked":
                    item.complete = True
                else:
                    item.complete = False

                item.save()

        elif response.POST.get("newItem"):
            txt = response.POST.get("new")

        if len(txt) > 2:
            ls.item_set.create(text=txt, complete=False)
        else:
            print("invalid")

    return render(response, "home/list.html", {"ls": ls})


# sprawdzenie, czy otrzymujemy żądanie POST, co oznaczałoby, że formularz został przesłany
def create(response):
    if response.method == "POST":
        # utwórz nowy formularz i wypełnij go danymi, które otrzymaliśmy z zapytania
        form = CreateNewList(response.POST)
        # sprawdź, czy formularz jest poprawny, jeśli tak, utworzymy i zapiszemy nowy obiekt listy zadań
        if form.is_valid():
            n = form.cleaned_data["name"]
            t = ToDoList(name=n)
            t.save()

        return HttpResponseRedirect("/%i" % t.id)
    else:
        form = CreateNewList()

    return render(response, "home/create.html", {"form": form})


def home(response):
    return render(response, "home/home.html", {})


def Registration(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():

            form.save()

        return redirect("/login")
    form = RegisterForm()
    return render(request, "home/Registration.html", {"form":form})

def login(request):
    return render(request, "home/login.html", {})