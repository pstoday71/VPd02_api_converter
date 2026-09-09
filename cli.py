import requests
from api_client import get_currency_rates
from storage import save_to_file, read_from_file, is_fresh

CACHE_FILE = "currency_rate.json"
SHOW_RATES = ["RUB", "EUR", "GBP", "USD", "CNY", "JPY", "KZT", "UAH", "BYN", "KGS"]


def load_rates(base: str) -> dict:
    try:
        cached = read_from_file(CACHE_FILE)
        if cached.get("base_code") == base and is_fresh(CACHE_FILE):
            return cached["rates"]
    except (OSError, ValueError, KeyError):
        pass
    print(f"Обновляю курсы для {base}...")
    data = get_currency_rates(base)
    save_to_file(data, CACHE_FILE)
    return data["rates"]


def show_rates(rates: dict, base: str) -> None:
    print(f"\nКурсы относительно {base}:")
    for code in SHOW_RATES:
        if code in rates:
            print(f"  {code}: {rates[code]:.4f}")
        else:
            print(f"  {code}: не поддерживается")


def convert(rates: dict, base: str) -> None:
    from_code = input("Из какой валюты: ").strip().upper()
    if from_code not in rates:
        print(f"Валюта {from_code} не найдена в списке.")
        return
    to_code = input("В какую валюту: ").strip().upper()
    if to_code not in rates:
        print(f"Валюта {to_code} не найдена в списке.")
        return
    try:
        amount = float(input("Сумма: "))
    except ValueError:
        print("Некорректная сумма.")
        return
    result = amount / rates[from_code] * rates[to_code]
    print(f"{amount:.4f} {from_code} = {result:.4f} {to_code}")


def main() -> None:
    base = input("Базовая валюта (например USD): ").strip().upper()
    if not base:
        base = "USD"
    try:
        rates = load_rates(base)
    except (requests.RequestException, RuntimeError, ValueError) as exc:
        print(f"Ошибка: {exc}")
        return
    show_rates(rates, base)
    convert(rates, base)


if __name__ == "__main__":
    main()
