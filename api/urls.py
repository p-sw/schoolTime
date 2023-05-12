from django.urls import path
from .views import school_search, school_get_time, school_get_meal

app_name = "api"

urlpatterns = [
    path("school", school_search),
    path("timetable", school_get_time),
    path("meal", school_get_meal)
]
