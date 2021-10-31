from django.shortcuts import render, redirect
from .models import User, Movie
from django.contrib import messages
import bcrypt

def index(request):
    return render(request, 'index.html')

def process_reg(request):
    errors = User.objects.reg_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        this_user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = pw_hash)
        request.session['first_name'] = this_user.first_name
        request.session['id'] = this_user.id
        return redirect('/movies')

def process_login(request):
    if request.method == "POST":
        errors = User.objects.login_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        one_user = User.objects.filter(email = request.POST['email'])
        request.session['id'] = one_user[0].id
        request.session['first_name'] = one_user[0].first_name
        return redirect('/movies')
    return redirect('/')

def display_home(request):
    conext = {
        'user': User.objects.get(id=request.session['id']),
        'users': User.objects.all(),
        'movies': Movie.objects.all()
    }
    return render(request, 'movies.html', conext)


def upload_movie(request):
    errors = Movie.objects.movie_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/movies')
    else:
        this_movie = Movie.objects.create(
            title = request.POST['title'],
            year_released = request.POST['year_released'],
            desc = request.POST['desc'],
            uploaded_by = User.objects.get(id=request.session['id']
            )
        )
        user = User.objects.get(id = request.session['id'])
        user.liked_movies.add(this_movie)
        request.session['movie_id'] = this_movie.id
        return redirect('/movies')

def logout(request):
    request.session.flush()
    return redirect('/')

def render_display_movie(request, this_movie_id):
    context = {
        'movie': Movie.objects.get(id=this_movie_id),
        'user': User.objects.get(id=request.session['id'])
    }
    return render(request, 'display_movie.html', context)

def add_to_likes(request, this_movie_id):
    movie = Movie.objects.get(id=this_movie_id)
    user = User.objects.get(id=request.session['id'])
    movie.liked_by.add(user)
    return redirect('/movies')

def remove_from_likes(request, this_movie_id):
    movie = Movie.objects.get(id=this_movie_id)
    user = User.objects.get(id=request.session['id'])
    movie.liked_by.remove(user)
    return redirect('/movies')


def update_movie(request, this_movie_id):
    movie = Movie.objects.get(id=this_movie_id)
    movie.title = request.POST['title']
    movie.year_released = request.POST['year_released']
    movie.desc = request.POST['desc']
    movie.save()
    return redirect(f'/display_movie/{this_movie_id}')

def delete_movie(request, this_movie_id):
    Movie.objects.get(id=this_movie_id).delete()
    return redirect('/movies')
