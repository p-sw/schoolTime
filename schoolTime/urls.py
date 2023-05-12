from django.urls import path, include, re_path
from django.conf import settings
from django.http.response import FileResponse, HttpResponseNotFound
from os.path import exists

# dev only view


def static(_, path):
    if not exists(settings.BASE_DIR / 'static' / path):
        return HttpResponseNotFound()
    return FileResponse(open(settings.BASE_DIR / 'static' / path, 'rb'))


urlpatterns = [
    path("", include("front.urls", namespace="front")),
    path("api/", include("api.urls", namespace="api"))
] + ([
    re_path(r"^static/(?P<path>.*)$", static)
] if settings.DEBUG else [])
