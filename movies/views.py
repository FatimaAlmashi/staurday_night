from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import Http404, JsonResponse
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from .models import Genre, Movie, Favorite
from .forms import MovieForm, SignupForm, SigninForm
import requests

def tv_show_search(request):
	query = request.GET.get('search', '')
	url = "http://api.tvmaze.com/search/shows?q="+query
	response = requests.get(url)
	# return JsonResponse(response.json(), safe=False)
	context = {
		'response': response.json(),
	}
	return render(request, 'tv_shows.html', context)


def favorite(request, movie_id):
	if request.user.is_anonymous:
		return redirect('signin')

	movie_obj = Movie.objects.get(id=movie_id)
	fav, created = Favorite.objects.get_or_create(user=request.user, movie=movie_obj)
	
	if created:
		favorited = True
	else:
		favorited = False
		fav.delete()

	fav_count = movie_obj.favorites.count()
	response = {
		"favorited": favorited,
		"fav_count": fav_count,
	}
	return JsonResponse(response)


def signup(request):
	form = SignupForm()
	if request.method == "POST":
		form = SignupForm(request.POST)
		if form.is_valid():
			user_obj = form.save(commit=False)
			user_obj.set_password(user_obj.password)
			user_obj.save()
			login(request, user_obj)
			messages.success(request, 'Welcome to Saturday Night!')
			return redirect('movie-list')
		messages.warning(request, form.errors)
	context = {
		'form': form,
	}
	return render(request, 'signup.html', context)


def signin(request):
	form = SigninForm()
	if request.method == "POST":
		form = SigninForm(request.POST)
		if form.is_valid():
			my_username = form.cleaned_data['username']
			my_password = form.cleaned_data['password']
			user_obj = authenticate(username=my_username, password=my_password)
			if user_obj is not None:
				login(request, user_obj)
				messages.success(request, "Welcome %s!"%(user_obj.username))
				return redirect('movie-list')
			messages.warning(request, "Username/password combination is incorrect!")
		messages.warning(request, form.errors)
	context = {
		'form': form,
	}
	return render(request, 'signin.html', context)

def signout(request):
	logout(request)
	messages.warning(request, "Come back jack!")
	return redirect('signin')

def movie_list(request):
	movies = Movie.objects.all()
	query = request.GET.get('search')
	if query:
		movies = movies.filter(
				Q(title__icontains=query)|
				Q(description__icontains=query)|
				Q(added_by__username__icontains=query)
			).distinct()
	favorited = []
	if request.user.is_authenticated:
		favorited = request.user.favorites.all().values_list('movie', flat=True)
	context = {
		'movies': movies,
		'favorited': favorited,
	}
	return render(request, 'movie_list.html', context)


def movie_detail(request, movie_id):
	movie = Movie.objects.get(id=movie_id)
	
	favorited = movie.favorites.all().values_list('user', flat=True)
	
	fav_count = favorited.count()
	fav = False
	if request.user.is_authenticated and request.user.id in favorited:
		fav=True

	context = {
		'movie': movie,
		'fav': fav,
		'fav_count': fav_count,
	}
	return render(request, 'movie_detail.html', context)


def add_movie(request):
	if request.user.is_anonymous:
		return redirect('movie-list')
	form = MovieForm()
	if request.method == "POST":
		form = MovieForm(request.POST, request.FILES)
		if form.is_valid():
			movie = form.save(commit=False)
			movie.added_by = request.user
			movie.save()
			form.save_m2m()
			return redirect(movie)
	context = {
		'form': form,
	}
	return render(request, 'add_movie.html', context)


def update_movie(request, movie_id):
	movie = Movie.objects.get(id=movie_id)

	if request.user.is_anonymous:
		return redirect('movie-list')

	if not(request.user.is_staff or request.user == movie.added_by):
		raise Http404

	form = MovieForm(instance=movie)
	if request.method == "POST":
		form = MovieForm(request.POST, request.FILES, instance=movie)
		if form.is_valid():
			form.save()
			return redirect(movie)
	context = {
		'form': form,
		"movie": movie,
	}
	return render(request, 'update_movie.html', context)


def delete_movie(request, movie_id):
	if request.user.is_anonymous:
		return redirect('movie-list')

	if not request.user.is_staff:
		raise Http404
	
	Movie.objects.get(id=movie_id).delete()
	return redirect('movie-list')
