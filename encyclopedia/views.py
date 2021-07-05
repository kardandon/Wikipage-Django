from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.utils.regex_helper import Choice

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "Status": "index"
    })

def title(request, TITLE):
    status = "title"
    entry = util.get_entry(TITLE)
    if entry  == None:
        entry = "Entry not found!"
        status = "error"
    import markdown2
    entry = markdown2.markdown(entry)
    return render(request, "encyclopedia/index.html",{
        "Title": TITLE,
        "Entry": entry,
        "Status": status
    })

def search(request):
    form = request.GET
    title = form["q"]
    if title != "":
        ls = util.list_entries()  
        array = []
        for name in ls:
            if title.lower() in name.lower():
                array.append(name)
            if title.lower() == name.lower():
                return HttpResponseRedirect(reverse("title",kwargs={'TITLE': title}))
        if len(array) == 0:
            return HttpResponseRedirect(reverse("title",kwargs={'TITLE': title}))
        return render(request, "encyclopedia/index.html",{
            "Title": "Search Results",
            "entries": array,
            "Status": "search"
        })

    else:
        return HttpResponseRedirect(reverse("index"))

class NewEntryForm(forms.Form):
    Title = forms.CharField(label="Title ")
    Entry = forms.CharField(label="Entry", widget=forms.Textarea)

class EditEntryForm(forms.Form):
    Entry = forms.CharField(label="Entry", widget=forms.Textarea)

def new(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new.html",{
        "form": NewEntryForm()
        })
    elif request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            Title = form.cleaned_data["Title"]
            Entry = form.cleaned_data["Entry"]
            ls = util.list_entries() 
            for name in ls:
                if name.lower() == Title.lower():
                    return render(request, "encyclopedia/index.html",{
                        "Title": "Already Exists",
                        "Entry": Title + " already exists!",
                        "Status": "error"
                    })
            util.save_entry(title=Title, content=Entry)
            return HttpResponseRedirect(reverse("title",kwargs={'TITLE': Title}))
        else:
            return render(request, "encyclopedia/new.html",{
                "form": NewEntryForm()
                })

def edit(request, TITLE):
    if request.method == "GET":
        initial={"Entry":util.get_entry(TITLE)}
        form = EditEntryForm(initial=initial)
        if initial["Entry"] == None:
            return render(request, "encyclopedia/index.html",{
                        "Title": "Does not Exist",
                        "Entry": TITLE + " does not exist!",
                        "Status": "error"
                    })
        return render(request, "encyclopedia/edit.html",{
            "Title": TITLE,
            "form": form
        })
    elif request.method == "POST":
        form = EditEntryForm(request.POST)
        if form.is_valid():
            Entry = form.cleaned_data["Entry"]
            ls = util.list_entries() 
            for name in ls:
                if name.lower() == TITLE.lower():
                    util.save_entry(title=TITLE, content=Entry)
                    return HttpResponseRedirect(reverse("title",kwargs={'TITLE': TITLE}))
            return render(request, "encyclopedia/index.html",{
                        "Title": "Does not Exist",
                        "Entry": TITLE + " does not exist!",
                        "Status": "error"
                    })
        else:
            return HttpResponseRedirect(reverse("edit",kwargs={'TITLE': TITLE}))

def random(request):
    ls = util.list_entries() 
    import random
    return HttpResponseRedirect(reverse("title",kwargs={'TITLE': random.choice(ls)}))
    