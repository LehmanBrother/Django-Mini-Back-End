from django.http import JsonResponse
from django.views import View
from .models import Movie
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render
import json

# Create your views here.
class Movies(View):
	def get(self, request):
		print(request.user)
		if(request.user.is_authenticated):
			user = User.objects.get(id=request.user.id)

			movie_list = list(user.movies.all().values())

			return JsonResponse({
				'Content-Type': 'application/json',
				'status': 200,
				'data': movie_list
				}, safe=False)
		else:
			return JsonResponse({
				'Content-Type': 'application/json',
				'status': 200,
				'message': 'Must be logged in to see the data'
				}, safe=False)

	#@method_decorator(login_required)
	def post(self, request):
		data = request.body.decode('utf-8')
		data = json.loads(data)

		try:
			new_movie = Movie(title=data["title"], description=data["description"])
			new_movie.created_by = request.user
			new_movie.save()
			data["id"] = new_movie.id
			print(data, '<--this is data', request.user)
			return JsonResponse({"data": data}, safe=False)
		except:
			return JsonResponse({"error": "Data not valid"}, safe=False)

class Movie_Detail(View):
	#@method_decorator(csrf_exempt)
	#def dispatch(self, request, *args, **kwargs):
	#	return super(Movie_Detail, self).dispatch(request, *args, **kwargs)

	def get(self, request, pk):
		movie_list = list(Movie.objects.filter(pk=pk).values())
		return JsonResponse({"data": movie_list}, safe=False)

	def put(self, request, pk):
		data = request.body.decode('utf-8')
		data = json.loads(data)

		try:
			edit_movie = Movie.objects.get(pk=pk)
			data_key = list(data.keys())

			for key in data_key:
				if key == "title":
					edit_movie.title = data[key]
				if key == "description":
					edit_movie.description = data[key]
			edit_movie.save()
			data["id"] = edit_movie.id
			return JsonResponse({"data": data}, safe=False)
		except:
			return JsonResponse({"error": "Something went wrong"}, safe=False)

	def delete(self, request, pk):
		try:
			movie_to_delete = Movie.objects.get(pk=pk)
			movie_to_delete.delete()
			return JsonResponse({"data": "deleted"}, safe=False)
		except:
			return JsonResponse({"error": "Something went wrong"}, safe=False)