from re import I
from unicodedata import name
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import ToDoList
from .forms import CreateNewList

# Create your views here.
def home(response):
    userStatus = response.user.is_authenticated
    return render(response, 'main/home.html', {"user": response.user, "userStatus": userStatus})

def toDoList(response,id):
    ls  = ToDoList.objects.get(id=id)
    
    if ls in response.user.todolist.all():
        if response.method == "POST":
            print(response.POST)
            if response.POST.get("save"):
                for item in ls.item_set.all():
                    if response.POST.get("c" + str(item.id)) == "clicked":
                        item.complete = True
                    else:
                        item.complete = False
                    item.save()

            elif response.POST.get("newItem"):
                txt = response.POST.get("new")

                if len(txt)>2:
                    ls.item_set.create(text=txt, complete=False)
                else:
                    print("Invalid")

        return render(response, 'main/list.html', {"list": ls})
    return render(response, "main/home.html", {})

def create(response):
    if response.method == 'POST':
        form = CreateNewList(response.POST)

        if form.is_valid():
            n =  form.cleaned_data['name']
            t = ToDoList(name=n)
            t.save()
            response.user.todolist.add(t)

        return HttpResponseRedirect('/{}'.format(int(t.id)))
    else:
        form = CreateNewList()
    return render(response, 'main/create.html', {'form':form})

def view(response):
    return render(response, "main/view.html", {"user":response.user})
