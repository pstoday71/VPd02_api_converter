import requests

API_URL = "https://open.er-api.com/v6/latest/{base}"


def get_currency_rates(base: str) -> dict:
    url = API_URL.format(base=base)
    response = requests.get(url)
    if response.status_code != 200:
        raise RuntimeError(f"API вернул ошибку: код {response.status_code} ({response.reason})")
    data = response.json()
    if data.get("result") != "success":
        raise ValueError(f"API вернул ошибку: {data.get('error-type', 'unknown')}")
    return data
