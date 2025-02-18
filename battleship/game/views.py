from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import SignUpForm
from django.contrib.auth.decorators import login_required
from .models import GameSession

# Create your views here.
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
        return redirect('game_room', game_id=open_game.id)
    else:
        new_game = GameSession.objects.create(player1=request.user)
        return render(request, 'game/matchmaking.html', {'waiting': True, 'game_id': new_game.id})