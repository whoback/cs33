from django.shortcuts import render
from . import util
from markdown2 import Markdown

markdowner = Markdown()
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki(request, title):
	if title in util.list_entries():
		re = markdowner.convert(util.get_entry(title))
		return render(request, "encyclopedia/entry.html", {
			"entry": re,
			"title" : title
			})
	else:
		return render(request, "encyclopedia/entry.html")
