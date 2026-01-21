from django.urls import path
from . import views

urlpatterns = [
       path('', views.index, name='index'),
       path('menu', views.menu, name='menu'),
       path('kirat', views.kirat, name='kirat'),
       path('chay bahche', views.chay_bahche, name='chay_bahche'),

       path('canteen/<int:pk>/', views.canteen_detail, name='canteen_detail'),
       path('vote/<int:comment_id>/<str:vote_type>/', views.vote_comment, name='vote_comment'),
       path('rate/<int:pk>/', views.rate_place, name='rate_place'),


       path('register/', views.register_view, name='register'),
       path('login/', views.login_view, name='login'),
       path('logout/', views.logout_view, name='logout'),
]