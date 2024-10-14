from datetime import datetime, timedelta, timezone


utc_tz = timezone.utc

def get_now():
    return datetime.now(utc_tz)


def get_delta_days(days: int) -> datetime:
    return get_now() + timedelta(days=days)


def get_now_filename():
    return get_now().strftime("%Y%m%d%H%M%S")


def get_today():
    return get_now().strftime("%Y-%m-%d")


def get_yesterday():
    return (get_now() - timedelta(days=1)).strftime("%Y-%m-%d")


def str_to_datetime(date_str):
    return datetime.strptime(date_str, "%m/%d/%Y, %I:%M %p, %z UTC")


def set_utc_tz(given_datetime: datetime) -> datetime:
    return given_datetime.replace(tzinfo=utc_tz)


def time_ago(utc_datetime):
    now = get_now()
    diff = now - set_utc_tz(utc_datetime)

    seconds = diff.total_seconds()
    minutes = seconds // 60
    hours = minutes // 60
    days = hours // 24

    if seconds < 60:
        return f"Just now"
    elif minutes < 60:
        return f"{int(minutes)} mins ago" if minutes > 1 else "1 min ago"
    elif hours < 24:
        return f"{int(hours)} hours ago" if hours > 1 else "1 hour ago"
    elif days < 7:
        return f"{int(days)} days ago" if days > 1 else "1 day ago"
    else:
        return utc_datetime.strftime("%Y-%m-%d")


def is_future(utc_datetime) -> bool:
    return get_now() < set_utc_tz(utc_datetime)
