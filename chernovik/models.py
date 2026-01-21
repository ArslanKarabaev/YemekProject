from django.contrib.auth.models import User
from django.db import models


class Place(models.Model):
    place_id = models.CharField(max_length=300, unique=True)
    name = models.CharField(max_length=250)
    rating = models.FloatField(null=True, blank=True)
    price_level = models.IntegerField(null=True, blank=True)
    types = models.JSONField(null=True, blank=True)
    lat = models.FloatField(null=True, blank=True)
    lng = models.FloatField(null=True, blank=True)

    # Новые поля:
    phone_number = models.CharField(max_length=100, null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    opening_hours = models.JSONField(null=True, blank=True)
    google_reviews = models.JSONField(null=True, blank=True)
    details_last_updated = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        managed = True
        db_table = 'chernovik-place'


class Comment(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chernovik_comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def likes(self):
        return self.votes.filter(is_like=True).count()

    def dislikes(self):
        return self.votes.filter(is_like=False).count()

    class Meta:
        managed = True
        db_table = 'chernovik-comment'


class Vote(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='votes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chernovik_votes')
    is_like = models.BooleanField()

    class Meta:
        unique_together = ('comment', 'user')
        managed = True
        db_table = 'chernovik-vote'
