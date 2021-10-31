from django.urls import path, include

urlpatterns = [
    path('', include('movie_app.urls')),
]
