import requests
from .models import Place
from datetime import timedelta
from django.utils import timezone

def fetch_and_save_places(location, radius, api_key):
    lat, lng = location
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

    params = {
        "location": f"{lat},{lng}",
        "radius": radius,
        "key": api_key,
        "type": "restaurant",  # Основной тип
    }

    response = requests.get(url, params=params)
    data = response.json()

    for result in data.get("results", []):
        place_id = result.get("place_id")
        name = result.get("name")
        rating = result.get("rating")
        price_level = result.get("price_level")
        types = result.get("types", [])
        geometry = result.get("geometry", {}).get("location", {})
        opening_hours = result.get("opening_hours", {}).get("weekday_text")
        #address = result.get("vicinity")

        if place_id and name and geometry:
            Place.objects.update_or_create(
                place_id=place_id,
                defaults={
                    "name": name,
                    "rating": rating,
                    "price_level": price_level,
                    "types": types,
                    "lat": geometry.get("lat"),
                    "lng": geometry.get("lng"),
                    "opening_hours": opening_hours,
                  #  "address": address
                }
            )
def fetch_place_details(place_id, api_key):
    url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        "place_id": place_id,
        "key": api_key,
        "fields": ",".join([
            "name",
            "rating",
            "formatted_phone_number",
            "international_phone_number",
            "website",
            "opening_hours",
            "reviews",
        ]),
        "language": "ru"  # или "en" если нужно
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data.get("result")
    else:
        return None


def update_place_details_if_needed(place: Place, api_key: str, max_age_days: int = 7):
    # Если данные были обновлены недавно, не делаем запрос
    if place.details_last_updated and timezone.now() - place.details_last_updated < timedelta(days=max_age_days):
        return

    data = fetch_place_details(place.place_id, api_key)

    if data:
        place.phone_number = data.get("international_phone_number") or data.get("formatted_phone_number")
        place.website = data.get("website")
        place.opening_hours = data.get("opening_hours", {}).get("weekday_text", [])
        place.google_reviews = data.get("reviews", [])[:5]  # ограничим 5 отзывами
        place.details_last_updated = timezone.now()
        place.save()