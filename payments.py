from telegram import LabeledPrice
from config import STARS_PRICE


def stars_invoice():
    return {
        "title": "Unlimited access",
        "description": "Unlimited video downloads forever",
        "payload": "unlimited_access",
        "currency": "XTR",
        "prices": [LabeledPrice("Unlimited", STARS_PRICE)],
    }
