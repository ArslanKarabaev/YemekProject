from django.contrib import admin

from .models import Place, Yemek
from .models import Comment
from .models import Vote
from .models import Meal

admin.site.register(Place)
admin.site.register(Comment)
admin.site.register(Vote)
admin.site.register(Meal)
admin.site.register(Yemek)
