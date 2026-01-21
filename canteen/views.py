from datetime import time, datetime

from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect

from canteen.models import Meal, Place, Rating, Yemek, Feedback
from .forms import CommentForm
from .forms import RegisterForm, LoginForm
from .models import Comment, Vote


def index(request):
    dishes = Yemek.objects.all()
    now = datetime.now().time()
    can_leave_feedback = time(11, 0) <= now <= time(13, 0)

    if request.method == "POST" and can_leave_feedback:
        feedback_text = request.POST.get("feedback")
        if feedback_text:
            Feedback.objects.create(
                text=feedback_text,
                created_at=datetime.now()
            )
            return redirect('index')  # чтобы избежать повторной отправки формы

    feedbacks = Feedback.objects.order_by('-created_at')  # последние вверху

    return render(request, 'canteens/index.html', {
        'dishes': dishes,
        'can_leave_feedback': can_leave_feedback,
        'feedbacks': feedbacks
    })

def menu(request):
    meals = Meal.objects.all()
    canteens = Place.objects.all()
    return render(request, 'canteens/menu.html', {
        'meals': meals,
        'canteens': canteens,
        'active_section': 'menu',
    })


def kirat(request):
    return render(request, 'canteens/kirat.html')


def chay_bahche(request):
    return render(request, 'canteens/chay_bahche.html')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = RegisterForm()
    return render(request, 'user/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = LoginForm()
    return render(request, 'user/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


def canteen_detail(request, pk):
    place = get_object_or_404(Place, pk=pk)
    canteens = Place.objects.all()
    comments = place.comments.all().order_by('-created_at')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.place = place
            new_comment.user = request.user
            new_comment.save()
            return redirect('canteen_detail', pk=pk)
    else:
        form = CommentForm()

    return render(request, 'canteens/canteen_detail.html', {
        'canteens': canteens,
        'place': place,
        'comments': comments,
        'form': form,
    })


@login_required
def vote_comment(request, comment_id, vote_type):
    comment = get_object_or_404(Comment, id=comment_id)

    # if comment.user == request.user:
    #     return JsonResponse({'error': 'You cannot vote on your own comment.'}, status=400)

    is_like = True if vote_type == 'like' else False

    # Попытаться найти существующий голос пользователя для этого комментария
    try:
        vote = Vote.objects.get(comment=comment, user=request.user)
        # Если голос уже был сделан, то его нужно обновить
        if vote.is_like != is_like:
            vote.is_like = is_like
            vote.save()
    except Vote.DoesNotExist:
        # Если голосования не существует, создаем новый
        vote = Vote.objects.create(comment=comment, user=request.user, is_like=is_like)

    # Возвращаем актуальные значения лайков и дизлайков
    return JsonResponse({'likes': comment.likes(), 'dislikes': comment.dislikes()})


@login_required
def rate_place(request, pk):
    place = get_object_or_404(Place, pk=pk)
    if request.method == 'POST':
        value = int(request.POST.get('rating'))
        if 1 <= value <= 5:
            Rating.objects.update_or_create(user=request.user, place=place, defaults={'value': value})
        average = place.average_rating or 0
        return JsonResponse({'average_rating': average})
    return JsonResponse({'error': 'Invalid request'}, status=400)
