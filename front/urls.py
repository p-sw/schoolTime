from django.urls import path
from front.views import index, search_school, time_page

app_name = "front"

urlpatterns = [
    path("", index),
    path("search", search_school),
    path("time", time_page, name="time")
]
