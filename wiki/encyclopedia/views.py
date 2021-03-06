from django.shortcuts import render
from . import util
from markdown2 import Markdown
import random as rand
from django import forms

markdowner = Markdown()


class Search(forms.Form):
    title = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'search', 'placeholder': 'Search'}))


class Form2(forms.Form):
    title = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'title', 'placeholder': 'Article Title'}), label='')
    content = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'content', 'placeholder': 'Article Content'}), label='')


class Form3(forms.Form):
    textarea = forms.CharField(widget=forms.Textarea(), label='')


def index(request):
    query = []
    queries = util.list_entries()
    if request.method == 'POST':
        form = Search(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            if util.get_entry(title) is not None:
                re = markdowner.convert(util.get_entry(title))
                return render(request, "encyclopedia/entry.html", {
                    "entry": re,
                    "title": title,
                    "form": form
                })
            else:
                for q in queries:
                    if title.lower() in q.lower():
                        query.append(q)
                return render(request, "encyclopedia/search.html", {
                    "query": query,
                    "title": title,
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


def newpage(request):
    if request.method == 'POST':
        form = Form2(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            entries = util.list_entries()
            if title in entries:
                err = "Article already exists."
                title = "Something went wrong..."
                return render(request, "encyclopedia/formerror.html", {
                    "error": err,
                    "title": title,
                    "form": Search()
                })
            else:
                util.save_entry(title, content)
                re = markdowner.convert(util.get_entry(title))
                return render(request, "encyclopedia/entry.html", {
                    "entry": re,
                    "title": title,
                    "form": Search()
                })
        pass
    else:
        return render(request, 'encyclopedia/newpage.html', {
            "form": Search(),
            "form2": Form2()
        })


def editpage(request, title):
    if request.method == 'GET':
        article = util.get_entry(title)

        return render(request, 'encyclopedia/editpage.html',
                      {'form': Search(),
                       'form3': Form3(initial={'textarea': article}),
                       'title': title})
    else:
        form = Form3(request.POST)
        if form.is_valid():
            content = form.cleaned_data['textarea']
            util.save_entry(title, content)
            re = markdowner.convert(util.get_entry(title))
            return render(request, "encyclopedia/entry.html", {
                "entry": re,
                "title": title,
                "form": Search()
            })
