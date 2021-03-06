from django.http import JsonResponse
from django.views import View
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from movie_app.models import Movie
from django.contrib import auth
from django.shortcuts import render

import json

# Create your views here.
@ensure_csrf_cookie
def getToken(request):
	return JsonResponse({"data": "token successful"}, safe=False)

def logout(request):

	print(request.user, '<--request.user in logout')
	auth.logout(request)
	print(request.user, request.user.is_authenticated)
	return JsonResponse({"data": "logout successful"}, safe=False)

class CreateUser(View):
	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super(CreateUser, self).dispatch(request, *args, **kwargs)

	def post(self, request):

		data = request.body.decode('utf-8')
		data = json.loads(data)
		try:
			new_user = User(username=data["username"], password=data["password"])
			new_user.set_password(new_user.password)
			new_user.save()
			auth.login(request, new_user)
			print(request, '<--here is request')
			print(new_user)
			return JsonResponse({"data": "registration successful"}, safe=False)
		except:
			return JsonResponse({"error": 'unsucces'}, safe=False)

class Authentication(View):

	def post(self, request):
		data = request.body.decode('utf-8')
		data = json.loads(data)
		user = auth.authenticate(username=data["username"], password=data["password"])
		if user is not None:
			auth.login(request, user)
			return JsonResponse({"data": "login successful"}, safe=False)
		else:
			return JsonResponse({"data": "login unsuccessful"}, safe=False)

class User_Detail(View):

	def get(self, request, pk):
		user = list(User.objects.filter(pk=pk).values())
		user_movies = list(Movie.objects.filter(created_by_id=pk).values())
		return JsonResponse({"data": {"user": user, "movies": user_movies}}, safe=False)