from django.urls import path
from library_api.views import Library, LibraryDetail

urlpatterns = [path("", Library.as_view()), path("<str:pk>", LibraryDetail.as_view())]
