from django.shortcuts import render, redirect
from django.http import HttpRequest


async def index(req):
    cookies = req.COOKIES.keys()
    if 'schoolKind' in cookies and 'eduGovernCode' in cookies and 'schoolCode' in cookies:
        return redirect("front:time")
    return render(req, "index.html")


async def search_school(req: HttpRequest):
    return render(req, "search.html")


async def time_page(req):
    return render(req, "time.html")
