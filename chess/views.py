from django.http import Http404, HttpResponseServerError, HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import *
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login, logout
from .forms import *
from django.db.models import Q
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
import re
import random

# Create your views here.
def index(request):
    return render(request, 'index.html')

class UserSignup(CreateView):
    model = APIUser
    form_class = UserSignupForm
    template_name = 'signup.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/')

class UserLogin(LoginView):
    template_name='login.html'

def logout_user(request):
    logout(request)
    return redirect("/")

@login_required
def account(request):
    games_as_white = Game.objects.filter(white=request.user.id)
    games_as_black = Game.objects.filter(black=request.user.id)

    currently_playing = set()

    for game in games_as_white:
        currently_playing.add(game.black.id)

    for game in games_as_black:
        currently_playing.add(game.white.id)

    other_users = APIUser.objects.exclude(id__in=currently_playing).exclude(id=request.user.id)

    return render(request, 'account.html', {'other_users': other_users, 'games': games_as_white | games_as_black})

@login_required
def game(request, game_id):
    game = Game.objects.filter(id=game_id).first()

    if not game:
        raise Http404("Game does not exist!")

    if request.user.id != game.white.id and request.user.id != game.black.id:
        raise Http401("You do not have permission to view this game")

    if request.user.id == game.white.id:
        user_color = 'white'
    elif request.user.id == game.black.id:
        user_color = 'black'
    else:
        user_color = 'none'

    return render(request, 'game.html', {'game': game, 'user_color': user_color})

@login_required
def start_game(request, opponent_id):
    opponent = APIUser.objects.filter(id=opponent_id).first()
    if not opponent:
        raise Http404("User does not exist!")

    w, b = random.sample([request.user, opponent], k=2)
    game = Game.objects.create(white=w, black=b, challenge_accepted=True)
    if not game:
        return HttpResponseServerError("Our bad!")

    return redirect("/game/{}".format(game.id))
