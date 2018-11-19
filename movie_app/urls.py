from django.urls import path
from .views import Movies

urlpatterns = [
	path('', Movies.as_view()),
	path('<int:pk>/', Movie_Detail.as_view()),
]