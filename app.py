import requests
from datetime import datetime, timedelta

BASE_URL = "https://sef.podkolzin.consulting/api/users/lastSeen"

localizations = {
    "en": {
        "just_now": "just now",
        "less_than_a_minute_ago": "less than a minute ago",
        "couple_of_minutes_ago": "couple of minutes ago",
        "hour_ago": "hour ago",
        "today": "today",
        "yesterday": "yesterday",
        "this_week": "this week",
        "long_time_ago": "long time ago",
        "is_online": "is online",
        "was_online": "was"
    },
    "fr": {
        "just_now": "à l'instant",
        "less_than_a_minute_ago": "il y a moins d'une minute",
        "couple_of_minutes_ago": "il y a quelques minutes",
        "hour_ago": "il y a une heure",
        "today": "aujourd'hui",
        "yesterday": "hier",
        "this_week": "cette semaine",
        "long_time_ago": "il y a longtemps",
        "is_online": "est en ligne",
        "was_online": "était en ligne"
    },
    "es": {
        "just_now": "justo ahora",
        "less_than_a_minute_ago": "hace menos de un minuto",
        "couple_of_minutes_ago": "hace unos minutos",
        "hour_ago": "hace una hora",
        "today": "hoy",
        "yesterday": "ayer",
        "this_week": "esta semana",
        "long_time_ago": "hace mucho tiempo",
        "is_online": "está en línea",
        "was_online": "estuvo en línea"
    }
}

def fetch_users_last_seen(offset=0):
    params = {"offset": offset}
    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()
    return response.json()

def human_readable_last_seen(last_seen_date, current_time=None):
    if not last_seen_date:
        return "Unknown"

    now = current_time or datetime.utcnow()

    # Truncate the fractional second part to 6 digits
    if "." in last_seen_date:
        date_parts = last_seen_date.split(".")
        last_seen_date = f"{date_parts[0]}.{date_parts[1][:6]}Z"

    last_seen = datetime.fromisoformat(last_seen_date.replace('Z', '+00:00'))
    last_seen = last_seen.replace(tzinfo=None)

    difference = now - last_seen

    if difference < timedelta(seconds=30):
        return "just now"
    elif timedelta(seconds=30) <= difference < timedelta(minutes=1):
        return "less than a minute ago"
    elif timedelta(minutes=1) <= difference < timedelta(minutes=59):
        return "couple of minutes ago"
    elif timedelta(minutes=60) <= difference < timedelta(minutes=119):
        return "hour ago"
    elif timedelta(minutes=120) <= difference < timedelta(days=1):
        return "today"
    elif timedelta(days=1) <= difference < timedelta(days=2):
        return "yesterday"
    elif timedelta(days=2) <= difference < timedelta(days=7):
        return "this week"
    else:
        return "long time ago"

def display_users(offset=0):
    response = fetch_users_last_seen(offset)
    users = response["data"]

    now = datetime.utcnow()

    for user in users:
        if user["isOnline"]:
            print(f"{user['nickname']} is online")
        else:
            last_seen_status = human_readable_last_seen(user["lastSeenDate"], now)
            print(f"{user['nickname']} was {last_seen_status}")

if __name__ == "__main__":
    display_users()
