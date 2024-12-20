import os
import re
from typing import cast

import pandas as pd
from typing_extensions import Literal

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

Currency = Literal["USD", "EUR", "GBP", "JPY"]
currencies = ["USD", "EUR", "GBP", "JPY"]


def load_csv(name_file: str):
    path_parts = os.path.dirname(__file__).split(os.sep)
    root_path = None

    for i in range(len(path_parts), 0, -1):
        if path_parts[i - 1] == "app":
            # Reconstruye la ruta desde la carpeta raíz del proyecto
            root_path = os.sep.join(path_parts[:i])
            break

    if root_path is None:
        raise FileNotFoundError("No se encontró la carpeta raíz del proyecto")

    path = os.path.join(root_path, "static", name_file)

    if not os.path.exists(path):
        raise FileNotFoundError(f"El archivo {name_file} no existe en la carpeta static")

    return pd.read_csv(path)


def validate_email(email: str):
    return re.fullmatch(regex, email) is not None


def simulate_transfer_currency(currency_from: Currency, currency_to: Currency, amount: float):
    if currency_from not in currencies:
        raise ValueError(f"Invalid currencies or no exchange data available.")

    if currency_to not in currencies:
        raise ValueError(f"Invalid currencies or no exchange data available.")

    if amount <= 0:
        raise ValueError("Invalid amount")

    if currency_from == currency_to:
        return amount

    rates_df = load_csv("exchange_rates.csv")
    fees_df = load_csv("exchange_fees.csv")

    rate = \
        rates_df[(rates_df["currency_from"] == currency_from) & (rates_df["currency_to"] == currency_to)][
            "rate"].values[0]
    fee = fees_df[(fees_df["currency_from"] == currency_from) & (fees_df["currency_to"] == currency_to)]["fee"].values[
        0]

    transfer = (amount * (1 - fee)) * rate

    return transfer


def get_fee_from_currencies(currency_from: Currency, currency_to: Currency) -> float:
    if currency_from not in currencies:
        raise ValueError(f"No fee information available for these currencies.")

    if currency_to not in currencies:
        raise ValueError(f"No fee information available for these currencies.")

    fees_df = load_csv("exchange_fees.csv")
    fee = fees_df[(fees_df["currency_from"] == currency_from) & (fees_df["currency_to"] == currency_to)]["fee"].values[
        0]
    return fee


def get_rate_from_currencies(currency_from: Currency, currency_to: Currency) -> float:
    if currency_from not in currencies:
        raise ValueError(f"No exchange rate available for these currencies.")

    if currency_to not in currencies:
        raise ValueError(f"No exchange rate available for these currencies.")

    rates_df = load_csv("exchange_rates.csv")

    rate = \
    rates_df[(rates_df["currency_from"] == currency_from) & (rates_df["currency_to"] == currency_to)]["rate"].values[0]

    return rate


if __name__ == "__main__":
    data = load_csv("exchange_fees.csv")
    print(data.head())

    c = cast(Currency, "USD")
    print(c)
