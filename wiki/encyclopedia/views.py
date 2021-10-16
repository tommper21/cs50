from django.shortcuts import render, redirect
from . import util
from django import forms
import random


class NewTaskForm(forms.Form):
    search = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),label="Search")

class CreatePageForm(forms.Form):
    title = forms.CharField()
    content = forms.CharField()




def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": NewTaskForm()
    })


def page(request,name):
    if util.get_entry(name) != None:
        return render(request, "encyclopedia/page.html", {
        "entries": util.get_entry(name),
        "form": NewTaskForm(),
        "name":name
        })
    else:
        return render(request, "encyclopedia/notfound.html",{
        "form": NewTaskForm()
        })


def edit(request,name):
    #display page editor
    if request.method == "GET":
        return render(request, "encyclopedia/edit.html", {
        "entries": util.get_entry_md(name),
        "name":name,
        "form":NewTaskForm()
        })
    else:
        content = request.POST["content"]
        #wir wollen die file verändern
        util.save_entry(name, content)

    return redirect('page', name=name)

def search(request):
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid():
            search = form.cleaned_data["search"]
            list = util.list_entries()
            if search in list:
                return redirect('page', name=search)
            else:
                sublist = []
                for item in list:
                    if search in item:
                        sublist.append(item)
                return render(request, "encyclopedia/index.html", {
                "entries": sublist,
                "form": NewTaskForm()
                })
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(),
            "form": NewTaskForm()
        })

def create(request):
    if request.method == "GET":
        return render(request, "encyclopedia/create.html", {
        "form": NewTaskForm()
        })
    form = CreatePageForm(request.POST)
    if form.is_valid():
        title = form.cleaned_data["title"]
        content = form.cleaned_data["content"]
        list = util.list_entries()
        if title in list:
            return render(request, "encyclopedia/error.html", {
            "entries": util.get_entry(search), "title":search,
            "form": NewTaskForm()
            })
        util.save_entry(title,content)
        return redirect('page',name=title)
    return render(request, "encyclopedia/notfound.html")

def rand(request):
    list = util.list_entries()
    random_page = random.choice(list)
    return redirect('page',name=random_page)
