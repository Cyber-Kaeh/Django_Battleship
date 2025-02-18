from django.http import JsonResponse
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from .forms import SignUpForm
from django.contrib.auth.decorators import login_required
from .models import GameSession

# Create your views here.
def home_view(request):
    return render(request, 'game/home.html')


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('matchmaking')
    else:
        form = SignUpForm()
    return render(request, 'game/signup.html', {'form': form})


@login_required
def matchmaking_view(request):
    open_game = GameSession.objects.filter(player2__isnull=True).first()

    if open_game:
        open_game.player2 = request.user
        open_game.save()
        print(f"Game {open_game.id} now has player1: {open_game.player1} and player2: {open_game.player2}")
        # return redirect('game_room', game_id=open_game.id)
        game_url = reverse('game_room', kwargs={'game_id': open_game.id})
        return JsonResponse({'redirect': game_url})
    else:
        new_game = GameSession.objects.create(player1=request.user)
        print(f"New Game {new_game.id} created with player1: {new_game.player1}")
        return render(request, 'game/matchmaking.html', {'waiting': True, 'game_id': new_game.id})


@login_required
def game_room_view(request, game_id):
    game = get_object_or_404(GameSession, id=game_id)
    return render(request, 'game/game_room.html', {'game': game})
