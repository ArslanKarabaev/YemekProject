# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.contrib.auth.models import User
from django.db import models


# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.contrib.auth.models import User
from django.db import models


class Place(models.Model):
    name = models.CharField(max_length=250)
    image = models.ImageField(upload_to='canteens/', blank=True, null=True)
    def _str_(self):
        return self.name


    @property
    def average_rating(self):
        ratings = self.ratings.all()
        if ratings.exists():
            return round(sum(r.value for r in ratings) / ratings.count(), 1)
        return None


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='ratings')
    value = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])  # от 1 до 5

    class Meta:
        unique_together = ('user', 'place')

    def __str__(self):
        return f"{self.user.username} rated {self.place.name}: {self.value} stars"


class Comment(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def likes(self):
        return self.votes.filter(is_like=True).count()
    def dislikes(self):
        return self.votes.filter(is_like=False).count()

class Vote(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='votes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_like = models.BooleanField()

    class Meta:
        unique_together = ('comment','user')


class Meal(models.Model):
    name = models.CharField(max_length=255)
    image_url = models.URLField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = True
        db_table = 'meal'

class Yemek(models.Model):
    name = models.CharField(max_length=255)
    image_url = models.URLField()

    class Meta:
        managed = True
        db_table = 'yemek'

class Feedback(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)