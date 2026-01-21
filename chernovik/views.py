import googlemaps
from django.shortcuts import render
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Place, Comment, Vote
from .forms import CommentForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from .utils import fetch_and_save_places
from django import forms
from geopy.distance import distance
from .utils import update_place_details_if_needed

class PlaceFilterForm(forms.Form):
    radius = forms.IntegerField(label="Радиус (м)", min_value=100, max_value=50000, initial=2000)
    place_type = forms.ChoiceField(choices=[
        ('restaurant', 'Ресторан'),
        ('cafe', 'Кафе'),
        ('bar', 'Бар')
    ], required=False)
    min_rating = forms.FloatField(label="Мин. рейтинг", min_value=0, max_value=5, required=False)
    max_price = forms.IntegerField(label="Макс. бюджет", min_value=0, max_value=4, required=False)
# (42.833491913046586, 74.57606048753111)
@login_required()
def places_map(request):
    location = (42.833491913046586, 74.57606048753111)
    radius = int(request.GET.get('radius', 2000))

    if "refresh" in request.GET:
        fetch_and_save_places(location=location, radius=radius, api_key=settings.GOOGLE_MAPS_API_KEY)

    places = Place.objects.exclude(types__contains='lodging')

    # Фильтрация по расстоянию
    places_with_distance = []
    for place in places:
        if place.lat and place.lng:
            place_distance = distance(location, (place.lat, place.lng)).meters
            if place_distance <= radius:
                place.calculated_distance = round(place_distance)
                places_with_distance.append(place)

    # Сортируем по расстоянию
    places_with_distance.sort(key=lambda x: x.calculated_distance)

    return render(request, 'places_map.html', {
        'places': places_with_distance,
        'radius': radius
    })
@login_required()
def place_detail(request, place_id):
    place = get_object_or_404(Place, place_id=place_id)
    update_place_details_if_needed(place, settings.GOOGLE_MAPS_API_KEY)

    comments = place.comments.select_related('user').prefetch_related('votes')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.place = place
            comment.user = request.user
            comment.save()
            return redirect('chernovik:place_detail', place_id=place_id)
    else:
        form = CommentForm()

    return render(request, 'place_detail.html', {
        'place': place,
        'comments': comments,
        'form': form,
    })
@login_required
def vote_comment(request):
    if request.method == 'POST':
        comment_id = request.POST.get('comment_id')
        action = request.POST.get('action')

        comment = get_object_or_404(Comment, id=comment_id)
        is_like = True if action == 'like' else False

        vote, created = Vote.objects.get_or_create(user=request.user,
                                                   comment=comment,
                                                   defaults={'is_like': is_like})
        if not created:
            # Если голос уже был, обновим его только если отличается
            if vote.is_like != is_like:
                vote.is_like = is_like
                vote.save()
            else:
                # Если пользователь повторно нажал тот же голос — удаляем
                vote.delete()

            # Обновляем количество голосов
        likes = comment.votes.filter(is_like=True).count()
        dislikes = comment.votes.filter(is_like=False).count()

        return JsonResponse({'likes': likes, 'dislikes': dislikes})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('/')