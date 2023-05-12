from django.shortcuts import render
from django.http import HttpRequest


async def index(req):
    return render(req, "index.html")


async def search_school(req: HttpRequest):
    return render(req, "search.html")


async def time_page(req):
    return render(req, "time.html")
