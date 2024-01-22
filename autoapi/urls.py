from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.documentation import include_docs_urls
from django.views.static import serve
from django.conf import settings

urlpatterns = [
    # Django Admin -> not important
    path('admin/', admin.site.urls),
    # API URLs
    path('', include('App.urls')),
    # API DOCS
    path('', include_docs_urls(title="AUTO API")),
    # serves static files for api docs
    # re_path -> regular exp. path
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
]