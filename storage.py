import json
import time
import os


def save_to_file(data: dict, path: str = "currency_rate.json") -> None:
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def read_from_file(path: str = "currency_rate.json") -> dict:
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def is_fresh(path: str = "currency_rate.json", max_age_hours: int = 24) -> bool:
    if not os.path.exists(path):
        return False
    now = time.time()
    try:
        data = read_from_file(path)
        updated = data.get("time_last_update_unix", os.path.getmtime(path))
        age_hours = (now - updated) / 3600
        return age_hours < max_age_hours
    except (OSError, ValueError):
        return False
