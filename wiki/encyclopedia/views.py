from django.shortcuts import render
from . import util
from markdown2 import Markdown
import random as rand
from django import forms

markdowner = Markdown()


class Search(forms.Form):
    title = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'search', 'placeholder': 'Search'}))


def index(request):
    query = list()
    queries = util.list_entries()
    if request.method == 'POST':
        form = Search(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            for q in queries:
                if title in queries:
                    re = markdowner.convert(util.get_entry(title))
                    return render(request, "encyclopedia/entry.html", {
                        "entry": re,
                        "title": title,
                        "form": form
                    })
                if title.lower() in q.lower():
                    query.append(q)
                    return render(request, "encyclopedia/search.html", {
                        "query": query,
                        "title": title,
                        "form": Search()
                    })
                else:
                    return render(request, 'encyclopedia/404.html', {
                        "form": Search()
                    })
        else:
            return render(request, "encyclopedia/index.html", {
                "form": form
            })
    else:
        return render(request, "encyclopedia/index.html", {
            "queries": util.list_entries(),
            "form": Search()
        })


def query(request, title):
    if title in util.list_entries():
        re = markdowner.convert(util.get_entry(title))
        return render(request, "encyclopedia/entry.html", {
            "entry": re,
            "title": title,
            "form": Search()
        })
    else:
        return render(request, "encyclopedia/404.html")


def random(request):
    entries = util.list_entries()
    title = rand.choice(entries)
    re = markdowner.convert(util.get_entry(title))
    return render(request, "encyclopedia/random.html", {
        "entry": re,
        "title": title
    })
